from PIL import Image, ImageDraw, ImageFont
import textwrap


import json
import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from pymessenger2.bot import Bot
from dateparser import parse

from fantastik.settings import TOKEN


bot = Bot(TOKEN)


# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_text_message(data):    
    for entry in data['entry']:
        for messaging_event in entry['messaging']:
            if messaging_event.get('message'):
                if 'text' in messaging_event['message']:
                    return messaging_event['message']['text']

    return 'fuck you'


def get_sender_id(data):    
    for entry in data['entry']:
        for messaging_event in entry['messaging']:
            return messaging_event['sender']['id']

def generate_meme(image_name, top_text, bottom_text='' ):
    font_path='fonts/impact/impact.ttf' 
    font_size=9

    # load image
    im = Image.open(image_name)
    #im = im.convert("JPEG")
    draw = ImageDraw.Draw(im)
    image_width, image_height = im.size
    
    # load font
    font = ImageFont.truetype(font=font_path, size=int(image_height*font_size)//100)

    # convert text to uppercase
    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    # text wrapping
    char_width, char_height = font.getsize('A')
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(top_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

    # draw top lines
    y = 10
    for line in top_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width)/2
        draw.text((x,y), line, fill='white', font=font)
        y += line_height

    # draw bottom lines
    y = image_height - char_height * len(bottom_lines) - 15
    for line in bottom_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width)/2
        draw.text((x,y), line, fill='white', font=font)
        y += line_height

    # save meme
    im.save('meme.png')


@csrf_exempt
def index(request):
    # Validate token if get request
    if request.method == 'GET':
        is_subscribe_request = request.GET.get('hub.mode') == 'subscribe'
        is_valid_token = request.GET.get('hub.verify_token') == 'fuck'

        if is_subscribe_request and is_valid_token:
            return HttpResponse(request.GET['hub.challenge'])

    logger.error(request)
    logger.error(request.body)

    # Echo message if post request
    if request.method == 'POST':
        logger.error('HERE BOY')

        data = json.loads(request.body)
        logger.error(str(data))

        # try:
        #     image_url = data['entry'][0]['messaging'][0]['message']['attachments'][0]['payload']['url'] 
        # except:
        #     try:
        #         bot.send_text_message(sender_id, )
        #     return HttpResponse('OK')

        # logger.error('HERE YYOUUUUU')
        # import requests
        # r = requests.get(image_url)
        # with open('new.jpg', 'wb') as f:
        #     f.write(r.content)


        # import random

        # list_of_texts=[]
        # list_of_texts.append(["when you want to give bonus points","but nobody volunteers as tribute"])
        # list_of_texts.append(["when they think they are overworked" ,"but you're about to give them more homework" ])
        # list_of_texts.append([ "when you think you told a good joke","but no stundent laughs" ])
        # list_of_texts.append([ "when students start learning","just after failing their midterm" ])
        # text=random.choice(list_of_texts)









        # generate_meme('new.jpg', text[0], text[1])

        # logger.error(str(data))

        sender_id = get_sender_id(data)
        message = get_text_message(data)


        # if data['object'] != 'page':
        #     bot.send_text_message(sender_id, f'Data object is {data["object"]}')
        #     return HttpResponse('OK')

        # bot.send_image(sender_id, 'meme.png')

        if 'fuck you' not in message:
            # bot.send_image(sender_id, 'new.jpg')
            bot.send_text_message(sender_id, 'De ce a trecut castravetele strada? Pentru ca era verde.')

            return HttpResponse('OK')

    # Return invalid request if neither matched
    return HttpResponse('Error, invalid request!')
