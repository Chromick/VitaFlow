from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'ehr.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            doctor_name TEXT NOT NULL,
            appointment_date TEXT,
            notes TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/record', methods=['POST'])
def create_record():
    data = request.json
    if not data or 'patient' not in data or 'notes' not in data:
        return jsonify({"error": "Parâmetros 'patient' e 'notes' são obrigatórios"}), 400
        
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO records (patient_name, doctor_name, appointment_date, notes, created_at) VALUES (?, ?, ?, ?, ?)",
        (data['patient'], data.get('doctor', 'N/A'), data.get('date', ''), data['notes'], datetime.now().isoformat())
    )
    conn.commit()
    record_id = c.lastrowid
    conn.close()
    
    app.logger.info(f"Prontuário salvo para: {data['patient']}")
    return jsonify({"status": "success", "record_id": record_id}), 201

@app.route('/record/<patient_name>', methods=['GET'])
def get_records(patient_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM records WHERE patient_name = ? ORDER BY created_at DESC", (patient_name,))
    rows = c.fetchall()
    conn.close()
    
    records = []
    for row in rows:
        records.append({
            "id": row[0],
            "patient": row[1],
            "doctor": row[2],
            "date": row[3],
            "notes": row[4],
            "created_at": row[5]
        })
        
    return jsonify({"patient": patient_name, "records": records}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ehr healthy"}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8003)
