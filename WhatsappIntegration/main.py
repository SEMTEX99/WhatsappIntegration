from flask import Flask
from WhatsappIntegration.gmail_api import GmailAPI
from whatsapp_bot import WhatsAppBot

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
whatsapp_bot = WhatsAppBot()

if __name__ == '__main__':
    # Instantiate Gmail API and authenticate
    gmail_api = GmailAPI()
    gmail_api.authenticate()

    # Instantiate WhatsApp Bot
    whatsapp_bot = WhatsAppBot()

    # Start the Flask app
    app.run()