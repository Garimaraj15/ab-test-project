from flask import Flask, render_template, request
import mysql.connector
import os
import random

app = Flask(__name__)

# Railway MySQL PUBLIC connection (use proxy URL)
db_config = {
    "host": os.getenv("MYSQLHOST", "trolley.proxy.rlwy.net"),
    "user": os.getenv("MYSQLUSER", "root"),
    "password": os.getenv("MYSQLPASSWORD", "DTKsaZtDcENPGOcvTDLisOFpwnKKFltg"),
    "database": os.getenv("MYSQLDATABASE", "railway"),
    "port": int(os.getenv("MYSQLPORT", 10071)),
}

# ✅ DB Init
def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            variant VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template("index.html")

# ✅ Auto Signup on Click
@app.route('/signup', methods=['POST'])
def signup():
    # Random user ID (you can replace with actual input if needed)
    user_id = f"user_{random.randint(1000,9999)}"

    # Randomly assign variant A or B
    variant = random.choice(["A", "B"])

    # Insert into MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (user_id, variant) VALUES (%s, %s)", (user_id, variant))
    conn.commit()
    conn.close()

    return f"🎉 Congrats {user_id}! You have been assigned to Variant {variant}"

# ✅ Debug: Show all logs
@app.route('/show')
def show_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    rows = cursor.fetchall()
    conn.close()

    html = "<h2>All Logged Data</h2><table border='1'><tr><th>ID</th><th>User</th><th>Variant</th><th>Created At</th></tr>"
    for row in rows:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
    html += "</table>"
    return html

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
