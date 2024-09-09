from django.urls import path
from . import views
from .views import extract_lyrics


urlpatterns = [
    path('', views.speech_to_text, name='speech_to_text'),
]
