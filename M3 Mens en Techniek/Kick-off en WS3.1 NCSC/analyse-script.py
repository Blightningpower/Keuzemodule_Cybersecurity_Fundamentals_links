from __future__ import annotations

import argparse
import ipaddress
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd


KEYWORDS = {
    "ip": ["ip", "ip_address", "src_ip", "source_ip", "client_ip"],
    "timestamp": ["time", "timestamp", "datetime", "date", "event_time"],
    "user_agent": ["user_agent", "ua", "agent", "browser"],
    "status": ["status", "status_code", "http_status", "code"],
    "bytes": ["bytes", "size", "response_size", "content_length"],
    "url": ["url", "uri", "path", "endpoint", "request"],
    "host": ["host", "hostname", "domain", "target_host"],
    "method": ["method", "http_method", "verb"],
    "port": ["port", "dst_port", "dest_port", "target_port"],
}


def normalize_col(c: str) -> str:
    return c.strip().lower().replace(" ", "_").replace(".", "_")


def find_column(columns: List[str], kind: str) -> Optional[str]:
    cols_norm = {normalize_col(c): c for c in columns}
    for k in KEYWORDS[kind]:
        if k in cols_norm:
            return cols_norm[k]
    for n, original in cols_norm.items():
        if any(k in n for k in KEYWORDS[kind]):
            return original
    return None


def is_valid_ip(v: object) -> bool:
    if pd.isna(v):
        return False
    s = str(v).strip()
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False


def load_excel(path: Path) -> pd.DataFrame:
    xls = pd.ExcelFile(path)
    frames = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(path, sheet_name=sheet)
        if df is None or df.empty:
            continue
        df["__file"] = path.name
        df["__sheet"] = sheet
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def analyze_df(df: pd.DataFrame, source: str) -> Tuple[pd.DataFrame, Dict[str, object]]:
    findings = []
    summary: Dict[str, object] = {"source": source, "rows": len(df), "cols": len(df.columns)}

    if df.empty:
        summary["note"] = "empty"
        return pd.DataFrame(), summary

    cols = list(df.columns)
    ip_col = find_column(cols, "ip")
    ts_col = find_column(cols, "timestamp")
    ua_col = find_column(cols, "user_agent")
    host_col = find_column(cols, "host")
    method_col = find_column(cols, "method")
    port_col = find_column(cols, "port")
    path_col = find_column(cols, "url")

    # Missing values ratio per column
    miss = (df.isna().sum() / len(df)).sort_values(ascending=False)
    high_missing = miss[miss > 0.3]
    summary["high_missing_cols"] = ", ".join([f"{c}:{v:.0%}" for c, v in high_missing.items()]) or ""

    # Duplicate rows
    dup_count = int(df.duplicated().sum())
    summary["duplicates"] = dup_count

    # IP validity checks
    if ip_col:
        ip_valid = df[ip_col].apply(is_valid_ip)
        invalid_ips = df.loc[~ip_valid & df[ip_col].notna(), [ip_col]].copy()
        if not invalid_ips.empty:
            invalid_ips["finding"] = "invalid_ip_format"
            invalid_ips["source"] = source
            findings.append(invalid_ips.rename(columns={ip_col: "value"}))

        summary["invalid_ip_count"] = int((~ip_valid & df[ip_col].notna()).sum())
    else:
        summary["invalid_ip_count"] = ""
        summary["note_ip"] = "no_ip_column_found"

    # Time-based spike analysis (requests per IP per hour)
    if ip_col and ts_col:
        t = pd.to_datetime(df[ts_col], errors="coerce", utc=True)
        tmp = df.loc[t.notna(), [ip_col]].copy()
        tmp["hour"] = t[t.notna()].dt.floor("h")
        grp = tmp.groupby([ip_col, "hour"]).size().reset_index(name="requests")

        if not grp.empty:
            mean = grp["requests"].mean()
            std = grp["requests"].std(ddof=0)
            threshold = mean + (3 * std if pd.notna(std) else 0)
            spikes = grp[grp["requests"] > threshold].copy()
            if not spikes.empty:
                spikes["finding"] = "ip_hour_spike"
                spikes["source"] = source
                findings.append(spikes.rename(columns={ip_col: "value"}))
            summary["spike_threshold"] = float(threshold)
            summary["spike_count"] = int(len(spikes))
        else:
            summary["spike_count"] = 0
    else:
        summary["spike_count"] = ""
        summary["note_time"] = "ip_or_timestamp_column_missing"

    # Rare user-agent detection
    if ua_col:
        ua = df[ua_col].astype(str).str.strip()
        freq = ua.value_counts(normalize=True, dropna=True)
        rare_set = set(freq[freq < 0.01].index)
        rare_rows = df[ua.isin(rare_set) & ua.ne("")][[ua_col]].copy()
        if not rare_rows.empty:
            rare_rows["finding"] = "rare_user_agent"
            rare_rows["source"] = source
            findings.append(rare_rows.rename(columns={ua_col: "value"}))
        summary["rare_ua_rows"] = int(len(rare_rows))
    else:
        summary["rare_ua_rows"] = ""
        summary["note_ua"] = "no_user_agent_column_found"

    # Top target hosts (relevant voor organisaties/landen)
    if host_col:
        host_series = df[host_col].astype(str).str.strip()
        host_counts = host_series[host_series.ne("")].value_counts().head(10)
        summary["top_hosts"] = "; ".join([f"{h}:{c}" for h, c in host_counts.items()])
    else:
        summary["top_hosts"] = ""
        summary["note_host"] = "no_host_column_found"

    # Top paden/endpoints
    if path_col:
        path_series = df[path_col].astype(str).str.strip()
        path_counts = path_series[path_series.ne("")].value_counts().head(10)
        summary["top_paths"] = "; ".join([f"{p}:{c}" for p, c in path_counts.items()])
    else:
        summary["top_paths"] = ""

    # HTTP methods
    if method_col:
        method_series = df[method_col].astype(str).str.upper().str.strip()
        method_counts = method_series[method_series.ne("")].value_counts()
        summary["methods"] = "; ".join([f"{m}:{c}" for m, c in method_counts.items()])
    else:
        summary["methods"] = ""

    # Target ports
    if port_col:
        port_counts = df[port_col].value_counts(dropna=True).head(10)
        summary["top_ports"] = "; ".join([f"{p}:{c}" for p, c in port_counts.items()])
    else:
        summary["top_ports"] = ""

    detail = pd.concat(findings, ignore_index=True) if findings else pd.DataFrame(columns=["source", "finding", "value"])
    return detail, summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Map met Excel-bestanden")
    parser.add_argument("--output", required=True, help="Map voor rapporten")
    args = parser.parse_args()

    in_dir = Path(args.input)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = list(in_dir.rglob("*.xlsx")) + list(in_dir.rglob("*.xls"))
    all_details = []
    all_summary = []

    for f in files:
        try:
            df = load_excel(f)
            details, summary = analyze_df(df, source=f.name)
            all_details.append(details)
            all_summary.append(summary)
        except Exception as e:
            all_summary.append({"source": f.name, "error": str(e)})

    details_df = pd.concat(all_details, ignore_index=True) if all_details else pd.DataFrame()
    summary_df = pd.DataFrame(all_summary)

    details_path = out_dir / "anomalies_details.csv"
    summary_path = out_dir / "anomalies_summary.csv"

    details_df.to_csv(details_path, index=False, encoding="utf-8-sig")
    summary_df.to_csv(summary_path, index=False, encoding="utf-8-sig")

    print(f"Klaar. Bestanden:")
    print(f"- {summary_path}")
    print(f"- {details_path}")


if __name__ == "__main__":
    main()