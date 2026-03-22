import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.execute("CREATE TABLE users (username TEXT, password TEXT)")
cur.execute("INSERT INTO users VALUES ('sam', 'geheim123')")
conn.commit()

username = input("Gebruikersnaam: ")
password = input("Wachtwoord: ")

query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
print("Uitgevoerde query:", query)

cur.execute(query)
result = cur.fetchone()

if result:
    print("Login gelukt")
else:
    print("Login mislukt")


    #veilige versie
    
    #cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))