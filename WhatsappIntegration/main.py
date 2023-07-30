from flask import Flask, request
from gmail_api import GmailAPI
from whatsapp_bot import WhatsAppBot
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

gmail_api = GmailAPI()
whatsapp_bot = WhatsAppBot()

@app.route('/notifications', methods=['POST'])
def notifications():
    # Gmail sends a POST request with a JSON body
    data = request.get_json()

    # Check if it's a new email notification
    if data['message']['data']:
        # Get the email ID from the notification
        email_id = data['message']['data']['emailId']

        # Fetch the email using the Gmail API
        email = gmail_api.get_email(email_id)

        # Check if it's a booking confirmation email
        if gmail_api.is_booking_email(email['subject']):
            # Extract the booking data from the email
            booking_data = gmail_api.extract_booking_data(email['body'])

            # Trigger the WhatsApp bot to send the first message
            whatsapp_bot.send_whatsapp_message(
                f"Hello {booking_data['Guest Name']}, I'm Astraea, the AI avatar of the Lake Fairy lodge :) ill be assisting you during your stay, feel free to ask me any questions regarding the lodge and the surrounding area before or during your stay. Here's a little video about the lodge: [video_link]",
                booking_data['Contact Phone']
            )

    return '', 204

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    phone_number = request.values.get('WaId', '')

    if incoming_msg:
        # Get the chat log for this user, or start a new one
        chat_log = whatsapp_bot.chat_logs.get(phone_number, whatsapp_bot.start_chat_log)
        answer = whatsapp_bot.ask(incoming_msg, chat_log)
        whatsapp_bot.chat_logs[phone_number] = whatsapp_bot.append_interaction_to_chat_log(incoming_msg, answer, chat_log)
        whatsapp_bot.send_whatsapp_message(answer, phone_number)
        print(answer)
    else:
        whatsapp_bot.send_whatsapp_message("Message Cannot Be Empty!")
        print("Message Is Empty")
    r = MessagingResponse()
    r.message("")        
    return str(r)

if __name__ == '__main__':
    # Authenticate with the Gmail API
    gmail_api.authenticate()

    # Set up Gmail push notifications
    gmail_api.watch('https://your-pythonanywhere-username.pythonanywhere.com/notifications')

    # Start the Flask app
    app.run()