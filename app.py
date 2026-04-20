import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Mematikan caching template agar saat file HTML diedit langsung berubah
app.config['TEMPLATES_AUTO_RELOAD'] = True

# URL API Edurobo Anda
API_URL = "https://arnhuggingface-my-ai-agent.hf.space/edurobo/chat"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    
    payload = {
        "message": user_message,
        "history": [],
        "conversation_id": ""
    }

    try:
        api_response = requests.post(API_URL, json=payload, timeout=30)
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