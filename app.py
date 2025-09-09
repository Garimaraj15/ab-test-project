from flask import Flask, request, render_template
import csv, os, datetime

app = Flask(__name__)
CSV_FILE = 'ab_log.csv'

# अगर file नहीं है तो header लिख दो
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id', 'variant', 'event', 'timestamp'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_event():
    data = request.get_json()
    user_id = request.remote_addr   # simple user पहचान
    variant = data.get('variant')
    event = data.get('event')       # "impression" या "conversion"
    timestamp = datetime.datetime.now().isoformat()

    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, variant, event, timestamp])

    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)
