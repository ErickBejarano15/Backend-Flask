# backend/app.py

import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

# ——— Diagnóstico: carga el mismo .env que email_sender ——————————
env_path = find_dotenv()
print(f"[app.py]    find_dotenv → {env_path!r}")
load_dotenv(env_path)

print(f"[app.py]    MAIL_SENDER   = {os.getenv('MAIL_SENDER')!r}")
print(f"[app.py]    MAIL_RECEIVER = {os.getenv('MAIL_RECEIVER')!r}")
# ————————————————————————————————————————————————————————————

from email_sender import send_email

app = Flask(__name__)
CORS(app)

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json() or {}
    nombre  = data.get('nombre', '').strip()
    correo  = data.get('correo', '').strip()
    asunto  = data.get('asunto', '').strip()
    mensaje = data.get('mensaje', '').strip()

    if not all([nombre, correo, asunto, mensaje]):
        return jsonify({'status':'error','error':'Faltan campos obligatorios'}), 400

    try:
        send_email(nombre, correo, asunto, mensaje)
        return jsonify({'status':'ok'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'status':'error','error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
