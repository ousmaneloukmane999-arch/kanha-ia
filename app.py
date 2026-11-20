from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question', '')
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": question}]
        }]
    }
    
    try:
        r = requests.post(URL, headers=headers, json=payload)
        res = r.json()
        
        # Si Google renvoie une erreur, on l'affiche en clair
        if 'error' in res:
            return jsonify({'answer': f"Erreur Google: {res['error']['message']}"})
            
        answer = res['candidates'][0]['content']['parts'][0]['text']
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'answer': f"Erreur système: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)