from flask import Flask, render_template, jsonify, request, redirect, url_for, session, g
import threading
import socket
import time
import json
import os
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATABASE = 'logs.db'
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'

# Load targets from config.json
with open("config.json") as f:
    TARGETS = json.load(f)

STATUS = {}  # Global dictionary to hold IP/port status

# DB helpers
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def log_status(ip, port, status):
    db = get_db()
    db.execute("INSERT INTO logs (ip, port, status, timestamp) VALUES (?, ?, ?, ?)",
               (ip, port, status, datetime.now()))
    db.commit()

def send_telegram_alert(ip, port):
    message = f"⚠️ Port kapalı: {ip}:{port}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    try:
        requests.post(url, data=payload)
    except:
        pass

def check_ports():
    while True:
        for target in TARGETS:
            ip = target["ip"]
            for port in target["ports"]:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                try:
                    s.connect((ip, port))
                    STATUS[(ip, port)] = "🟢 OPEN"
                    log_status(ip, port, "OPEN")
                except Exception:
                    STATUS[(ip, port)] = "🔴 CLOSED"
                    log_status(ip, port, "CLOSED")
                    send_telegram_alert(ip, port)
                s.close()
        time.sleep(10)

@app.before_request
def before_request():
    g.user = session.get('user')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route('/status')
def status():
    readable_status = [
        {"ip": ip, "port": port, "status": status}
        for (ip, port), status in STATUS.items()
    ]
    return jsonify(readable_status)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['user'] = 'admin'
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Hatalı giriş')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/uptime')
def uptime():
    db = get_db()
    cursor = db.execute("SELECT ip, port, status FROM logs")
    results = cursor.fetchall()
    stats = {}
    for ip, port, status in results:
        key = f"{ip}:{port}"
        if key not in stats:
            stats[key] = {'OPEN': 0, 'CLOSED': 0}
        stats[key][status] += 1

    chart_data = [
        {"target": key, "uptime": round((value['OPEN'] / (value['OPEN'] + value['CLOSED'])) * 100, 2)}
        for key, value in stats.items()
    ]
    return jsonify(chart_data)

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''CREATE TABLE logs (id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, port INTEGER, status TEXT, timestamp TEXT)''')
        conn.commit()
        conn.close()

if __name__ == "__main__":
    init_db()
    thread = threading.Thread(target=check_ports)
    thread.daemon = True
    thread.start()
    app.run(debug=True)