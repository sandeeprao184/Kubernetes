
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# POST: Connect to mysql-0 (WRITE)
@app.route("/write", methods=["POST"])
def write_data():

    conn = mysql.connector.connect(
        host="mysql-0.mysql-headless.default.svc.cluster.local",
        user="root",
        password="root123",
        database="testdb",
        port=3306
    )

    data = request.get_json()

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (data["name"], data["email"])
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Data written successfully",
        "connected_to": "mysql-0"
    })


# GET: Connect to mysql-1 (READ)
@app.route("/read", methods=["GET"])
def read_data():

    conn = mysql.connector.connect(
        host="mysql-1.mysql-headless.default.svc.cluster.local",
        user="root",
        password="root123",
        database="testdb",
        port=3306
    )

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Data read successfully",
        "connected_to": "mysql-1",
        "data": result
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
