from django.urls import path
from .views import *

app_name = 'api_v2'

urlpatterns = [
    path('echo/', json_echo_view, name='echo'),
    path('token/', get_token_view, name='get_token'),
    path('articles/', ArticleView.as_view()),
    path('articles/<int:pk>/', ArticleDetailView.as_view()),
    path('articles/<int:pk>/update/', ArticleUpdateView.as_view()),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view()),
]

