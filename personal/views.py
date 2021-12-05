from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from bs4 import BeautifulSoup
import requests

DEBUG = True


def home_screen_view(request):
    context = {}
    context['debug_mode'] = settings.DEBUG
    context['debug'] = DEBUG
    context['room_id'] = "1"
    return render(request, "personal/home.html", context)


def link(request):
    url = request.GET.get('url')
    msg_id = request.GET.get("msg_id")
    html_page = requests.get(url)
    result = {}
    if html_page.ok:
        soup = BeautifulSoup(html_page.text, 'lxml')
        # BeautifulSoup takes in str
        result = {
            'title': soup.find("meta", property="og:title")['content'],
            'image': soup.find("meta", property="og:image")['content'],
            'description': soup.find("meta", property="og:description")['content'],
            "msg_id": msg_id
        }
        print(result)
        return JsonResponse(result, safe=False)
    else:
        result['status'] = 'bad'
        return JsonResponse(result, safe=False)
