import json
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pymessenger import Bot

TOKEN = 'EAAEwTcxx0TwBAGhnmXknbjJ68xop9hOeRd1ZAhmjUuN3NR7bqZBhsV7Nm6kteZBmou6l7ZCRQTBscL0EgDQ9HyE8k7FUZCKrOZC1mm04rxVhbZCLr4XBGsMqEDbJiZAZA3MrjBy4S3uZB6JSbf6OCUqhDmyMWgZChmZAA6nOdFWnOruf8cfjPyVG53dY'

bot = Bot(TOKEN)


@csrf_exempt
def index(request):

    # Validate token if get request
    if request.method == 'GET':
        is_subscribe_request = request.GET.get('hub.mode') == 'subscribe'
        is_valid_token = request.GET.get('hub.verify_token') == 'fuck'

        if is_subscribe_request and is_valid_token:
            return HttpResponse(request.GET['hub.challenge'])

    # Echo message if post request
    if request.method == 'POST':

        data = json.loads(request.body)
        logger.info(str(data))

        logger.info('Sending back echo!')
        if data['object'] == 'page':
            for entry in data['entry']:
                for messaging_event in entry['messaging']:

                    sender_id = messaging_event['sender']['id']
                    # recipient_id = messaging_event['recipient']['id']

                    if messaging_event.get('message'):
                        if 'text' in messaging_event['message']:
                            messaging_text = messaging_event['message']['text']
                        else:
                            messaging_text = 'fuck you'

                        response = messaging_text

                        bot.send_text_message(sender_id, response)

        return HttpResponse('OK')


    # Return invalid request if neither matched
    return HttpResponse('Error, invalid token!')
