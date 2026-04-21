import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)  

# Mematikan caching template agar saat file HTML diedit langsung berubah
app.config['TEMPLATES_AUTO_RELOAD'] = True

# URL API Edurobo Anda (Bisa diatur melalui Environment Variable, jika tidak default ke localhost)
API_URL = os.environ.get("API_URL", "http://localhost:7861/edurobo/chat")

@app.route('/')
def home():
    return render_template('index.html')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/edurobo/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    data = request.get_json()
    user_message = data.get('message')
    
    payload = {
        "message": user_message,
        "history": [],
        "conversation_id": ""
    }

    # Cek apakah aplikasi diakses secara lokal (localhost/127.0.0.1)
    if request.host.startswith('localhost') or request.host.startswith('127.0.0.1'):
        api_url = "http://edurobo-api:7860/edurobo/chat"
    else:
        api_url = "https://arnhuggingface-my-ai-agent.hf.space/edurobo/chat"

    try:
        api_response = requests.post(api_url, json=payload, timeout=60)
        response_data = api_response.json()
        if response_data.get('status_code') == 200:
            bot_reply = response_data.get('response')
        else:
            bot_reply = "Maaf, terjadi kesalahan dari server AI (Status bukan 200)."

    except requests.exceptions.RequestException as e:
        print(f"Error API: {e}")
        bot_reply = "Maaf, server AI sedang tidak dapat dihubungi saat ini. Silakan coba beberapa saat lagi."
    
    return jsonify({'response': bot_reply})

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=7860, debug=True)