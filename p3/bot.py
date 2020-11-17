from flask import Flask, request, Response

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
import logging

from viberbot.api.viber_requests import ViberMessageRequest

from p3.keyboard import keyboard_menu

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='Surgebook Viber',
    avatar='https://upload.wikimedia.org/wikipedia/commons/9/9a/Gull_portrait_ca_usa.jpg',
    auth_token='токен'
))
# аватарку можно использовать не только ту которая указана при регистрации

@app.route('/', methods=['POST'])
def incoming():
    logger.debug("received request. post data: {0}".format(request.get_data()))

    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        text = str(viber_request.sender.name + ", привет")
        message = TextMessage(text=text, keyboard=keyboard_menu)
        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])

    return Response(status=200)

if __name__ == '__main__':
    app.run(port='8090')