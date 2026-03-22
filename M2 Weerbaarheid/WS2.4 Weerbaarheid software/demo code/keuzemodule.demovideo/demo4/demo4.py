from flask import Flask, request, jsonify

app = Flask(__name__)

users = {
    "1": {"id": 1, "name": "Sam", "email": "sam@test.nl", "role": "user"},
    "2": {"id": 2, "name": "Admin", "email": "admin@test.nl", "role": "admin"}
}

@app.route("/user/<user_id>")
def get_user(user_id):
    api_key = request.headers.get("X-API-Key")

    if api_key != "demo-key":
        return jsonify({"error": "unauthorized"}), 401

    # expres kwetsbaar: geen check of je deze user wel mag zien
    if user_id in users:
        return jsonify(users[user_id])

    return jsonify({"error": "not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)