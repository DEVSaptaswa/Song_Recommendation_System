from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def dashboard(request):
    return render(request, 'main/dashboard.html')

def weather_mood_music(request):
    # Logic for weather-based mood music
    return render(request, 'main/weather_mood_music.html')

def facial_mood_detection(request):
    # Logic for facial mood detection
    return render(request, 'main/facial_mood_detection.html')