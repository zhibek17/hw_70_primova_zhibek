from django.urls import path
from api_v1.views import json_echo_view, get_token_view, article_view

app_name = 'api_v1'

urlpatterns = [
    path('echo/', json_echo_view, name='echo'),
    path('token/', get_token_view, name='get_token'),
    path('article/', article_view, name='article')
]