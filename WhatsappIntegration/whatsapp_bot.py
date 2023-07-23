from flask import request, session
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import openai

from main import app

class WhatsAppBot:
    account_sid = 'AC6e8ed1754efe4920ee6e31b9e8f30788'
    auth_token = '8684b54fde14c2a7766f40d2e42bf888'
    client = Client(account_sid, auth_token)

    openai.api_key = "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"
    completion = openai.Completion()

    start_chat_log = '''You are an Intelligent AI assistant tasked in helping the guests that have booked their stay at the Lake Fairy lodge.
    ###KNOWLEDGE BASE###
    The Lake Fairy Chalet is a charming and secluded lodge located in the heart of the beautiful Plitvice National Park. Its central position puts it within easy reach of popular tourist hotspots: a mere 15 minutes' walk to the main attraction, Lake Kozjak, a delightful 20-minute stroll to the enchanting Big Waterfall, and approximately 45 minutes to the spring of "Plitvica" stream.
    As your helpful assistant, I'm here to answer any questions you may have about this wonderful chalet. If you're seeking a serene retreat to immerse yourself in nature's wonders, Lake Fairy is the ideal destination. The chalet's unique location off the main village road ensures privacy and tranquility, allowing you to appreciate the surrounding forest and its captivating beauty.
    At the Lake Fairy Chalet, you'll find a lovely terrace that offers breathtaking views of the forest. For cozy evenings, you can enjoy the warmth of two fireplaces, adding a touch of romance to your stay.
    The chalet's owner, Iskra, has a deep connection to this place, having spent much of her childhood here, exploring the flora and fauna and falling in love with the mesmerizing nature of Plitvice. Now, she and her sister have decided to share this hidden treasure with like-minded people like you. Although they reside in Switzerland and can only visit occasionally, their dear friends, who are rooted in Plitvice, will be your gracious hosts during your stay, ensuring you have a memorable experience.
    While the Lake Fairy Chalet is in the old village of Plitvice selo, offering easy access to the lakes and waterfalls, it's essential to note that the village's infrastructure may occasionally experience water shortages, especially during peak tourist seasons and hot summers. However, the chalet itself remains refreshingly cool, even on warmer days.
    Whether you have questions about the nearby attractions, amenities at the chalet, or anything else related to your stay, feel free to ask. I'm here to assist you and make sure you have a fantastic time at the Lake Fairy Chalet in Plitvice National Park!
    ###INSTRUCTIONS###
    Answer any questions the user will pose through the messages about the lodge and the surrounding area to the best of your ability, if you lack details, you can pose questions to the user to clarify.
    '''

    def send_whatsapp_message(self, message, phone_number):
        self.client.messages.create(
            from_='whatsapp:+14155238886',
            body=message,
            to='whatsapp:' + phone_number
        )

    def ask(self, question, chat_log=None):
        if chat_log is None:
            chat_log = self.start_chat_log
        prompt = f'{chat_log}Human: {question}\nAI:'
        response = self.completion.create(
            prompt=prompt, engine="text-davinci-003", stop=['\nHuman'], temperature=0.2,
            top_p=1, frequency_penalty=0.1, presence_penalty=0.0, best_of=1,
            max_tokens=256)
        answer = response.choices[0].text.strip()
        return answer

    def append_interaction_to_chat_log(self, question, answer, chat_log=None):
        if chat_log is None:
            chat_log = self.start_chat_log
        return f'{chat_log}Human: {question}\nAI: {answer}\n'

    @app.route('/bot', methods=['POST'])
    def bot(self):
        incoming_msg = request.values['Body']
        phone_number = (request.values['WaId'])

        if incoming_msg:
            chat_log = session.get('chat_log')
            answer = self.ask(incoming_msg, chat_log)
            session['chat_log'] = self.append_interaction_to_chat_log(incoming_msg, answer, chat_log)
            self.send_whatsapp_message(answer, phone_number)
            print(answer)
        else:
            self.send_whatsapp_message("Message Cannot Be Empty!")
            print("Message Is Empty")
        r = MessagingResponse()
        r.message("")        
        return str(r)