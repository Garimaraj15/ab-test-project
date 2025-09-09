from flask import Flask, request, render_template
import mysql.connector
import os

app = Flask(__name__)

# Railway MySQL connection settings
db_config = {
    "host": os.getenv("MYSQLHOST", "mysql.railway.internal"),
    "user": os.getenv("MYSQLUSER", "root"),
    "password": os.getenv("MYSQLPASSWORD", "DTKsaZtDcENPGOcvTDLisOFpwnKKFltg"),
    "database": os.getenv("MYSQLDATABASE", "railway"),
    "port": int(os.getenv("MYSQLPORT", 3306)),
}

# ✅ DB Init (1 बार table बना देगा)
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

# ✅ Insert Data
@app.route('/log', methods=['POST'])
def log_data():
    user_id = request.form.get("user_id")
    variant = request.form.get("variant")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (user_id, variant) VALUES (%s, %s)", (user_id, variant))
    conn.commit()
    conn.close()

    return "✅ Data Logged in MySQL!"

# ✅ Fetch Data (for debugging)
@app.route('/show')
def show_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    rows = cursor.fetchall()
    conn.close()
    return {"logs": rows}

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
