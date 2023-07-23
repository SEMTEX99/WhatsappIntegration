from flask import Flask, request
from gmail_api import GmailAPI
from whatsapp_bot import WhatsAppBot

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

if __name__ == '__main__':
    # Authenticate with the Gmail API
    gmail_api.authenticate()

    # Set up Gmail push notifications
    gmail_api.watch('https://your-pythonanywhere-username.pythonanywhere.com/notifications')

    # Start the Flask app
    app.run()