import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


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
        print(json.loads(request.body))

    # Return invalid request if neither matched
    return HttpResponse('Error, invalid token!')
