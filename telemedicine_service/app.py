from flask import Flask, request, jsonify
import uuid
import re

app = Flask(__name__)

def generate_room_name(doctor, patient):
    # Remove caracteres especiais e espaços
    doc_clean = re.sub(r'[^a-zA-Z0-9]', '', doctor)
    pat_clean = re.sub(r'[^a-zA-Z0-9]', '', patient)
    # Gera um hash curto de 6 caracteres para garantir que a sala seja única
    short_hash = str(uuid.uuid4())[:6]
    return f"VitaFlow-{doc_clean}-{pat_clean}-{short_hash}"

@app.route('/generate-link', methods=['POST'])
def generate_link():
    data = request.json
    
    if not data or 'patient' not in data or 'doctor' not in data:
        return jsonify({"error": "Parâmetros 'patient' e 'doctor' são obrigatórios"}), 400
        
    room_name = generate_room_name(data['doctor'], data['patient'])
    jitsi_url = f"https://meet.jit.si/{room_name}"
    
    app.logger.info(f"Link gerado: {jitsi_url}")
    
    return jsonify({
        "status": "success",
        "room_name": room_name,
        "url": jitsi_url
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "telemedicine healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
