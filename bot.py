import os
from flask import Flask, request
import requests

app = Flask(__name__)
TOKEN = os.environ.get('TELEGRAM_TOKEN')

@app.route('/')
def home():
    current_url = request.host_url.rstrip('/')
    return f"""
    <h1>Telegram Bot</h1>
    <p>Server: {current_url}</p>
    <p><a href="/set_webhook">SET WEBHOOK (Click This First!)</a></p>
    <p><a href="/webhook-info">Check Status</a></p>
    """

@app.route('/set_webhook')
def set_webhook():
    current_url = request.host_url.rstrip('/')
    webhook_url = f"{current_url}/webhook"
    
    # Set webhook via Telegram API
    response = requests.get(
        f"https://api.telegram.org/bot{TOKEN}/setWebhook",
        params={'url': webhook_url}
    )
    
    return f"""
    <h2>Webhook Set!</h2>
    <p>URL: {webhook_url}</p>
    <p>Response: {response.json()}</p>
    <p><strong>Now send /start to your bot on Telegram!</strong></p>
    """

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text', '')
        
        if text == '/start':
            # Reply to the message
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={
                    'chat_id': chat_id,
                    'text': 'Hello! I am working! ✅'
                }
            )
    
    return 'OK', 200

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)