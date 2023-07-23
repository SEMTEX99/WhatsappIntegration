# Lodge Booking Assistant Chatbot

This is a WhatsApp chatbot that enhances the booking experience for lodge accommodations. It uses the OpenAI API to answer questions about the accommodations and is integrated into WhatsApp through Twilio. The chatbot is triggered when a booking confirmation email arrives at a specified Gmail address.
NOTE: This assumes that the email recieved into the gmail adress follows the following format:

From: <no-reply@booking.com> Subject: New Booking for Your Accommodation

Dear [Your Name],

Congratulations! You have a new booking for your accommodation listed on Booking.com. Here are the details of the reservation:

Booking ID: 123456789
Guest Name: John Doe
Check-in Date: 2023-08-15
Check-out Date: 2023-08-20
Number of Guests: 2 adults
Contact Email: <johndoe@example.com>
Contact Phone: +1 (123) 456-7890

Please ensure that you are prepared to welcome the guest on their check-in date. It's essential to provide a comfortable and pleasant stay for the duration of their reservation.

If you have any questions or need further assistance, feel free to reach out to our support team.

Thank you for choosing Booking.com!

Best regards,
The Booking.com Team

## NOTE

integrating customized visual presentations requires additional APIs and runtime for StableDiffusion, probably will run using AWS sagemaker, we will have to consult eachotehr about this since such runtime is not free

## Setup

1. Clone this repository.
2. Install the required packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Twilio and OpenAI credentials in the environment variables or directly in the code.
4. Set up Gmail API Authentication by following the instructions [here](https://developers.google.com/gmail/api/quickstart/python).

## Hosting on PythonAnywhere

PythonAnywhere is a great platform for hosting Python web apps. Here are the steps to host this app on PythonAnywhere:

1. Create a PythonAnywhere account and go to the dashboard.
2. Click on the "Web" tab and then "Add a new web app".
3. Select the free tier and click "Next".
4. Choose "Flask" as the framework and Python 3.8 as the version.
5. In the "Source code" section, enter the path to the directory where you'll upload your code.
6. In the "Working Directory" section, enter the same directory path.
7. Click on the "Go to Directory" button in the "Source code" section and upload your code files (`main.py`, `gmail_api.py`, `whatsapp_bot.py`).
8. In the "Web app setup" page, replace the content of the "WSGI configuration file" with the following:

    ```python
    import sys
    path = '/home/yourusername/yourappdirectory'
    if path not in sys.path:
        sys.path.append(path)
    from main import app as application
    ```

    Replace `yourusername` and `yourappdirectory` with your PythonAnywhere username and the directory where you uploaded your code, respectively.

9. Click "Save" and then "Reload" your web app.

## Setting Up Twilio WhatsApp Sandbox

1. Go to the [Twilio Console](https://www.twilio.com/console).
2. Click on "Programmable Messaging", then on "Try it Out" and then on "Try WhatsApp".
3. Send a WhatsApp message to the number provided by Twilio to join your sandbox.
4. In the "WHEN A MESSAGE COMES IN" field, enter the URL of your PythonAnywhere web app followed by the `/bot` endpoint, like this: `https://yourusername.pythonanywhere.com/bot`. note to replace yourusername with your actual username
5. Click "Save".

## Usage

Once a new booking email is received, the chatbot will send a WhatsApp message to the guest, introducing itself as an AI assistant and offering to answer any questions about the lodge and the surrounding area.

Guests can then ask the bot any questions they have directly through WhatsApp
