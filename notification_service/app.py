from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/notify', methods=['POST'])
def send_notification():
    """
    Endpoint para envio de notificações (simulação).
    Recebe um payload JSON com as informações e registra um log.
    """
    data = request.json
    
    if not data or 'patient' not in data or 'doctor' not in data:
        return jsonify({"error": "Parâmetros inválidos"}), 400
        
    patient_name = data.get('patient')
    doctor_name = data.get('doctor')
    date = data.get('date', 'data não informada')
    
    app.logger.info(f"==> MICROSSERVIÇO DE NOTIFICAÇÃO <==")
    app.logger.info(f"Enviando e-mail/SMS para paciente: {patient_name}")
    app.logger.info(f"Detalhes: Consulta com Dr(a). {doctor_name} em {date}")
    app.logger.info(f"======================================")
    
    return jsonify({"status": "success", "message": "Notificação enviada com sucesso"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
