# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests  # Import requests to make the API call
import pandas as pd
import random

# API_URL = "https://api.openweathermap.org/data/2.5/weather"
# API_KEY = settings.WEATHER_API_KEY

# Load the dataset (Make sure the file path is correct)
file_path = 'spotify_weather_data.csv'  # Update this path
data = pd.read_csv(file_path)

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

# def suggest_song(weather, dataset):
# # Load the dataset (Make sure the file path is correct)
#     file_path = 'spotify_weather_data.csv'  # Update this path
#     data = pd.read_csv(file_path)

# def weather_view(request):
#     return render(request, 'accounts/weather.html')

# Function to suggest a song based on the weather

def suggest_songs_for_weather(weather_condition):
    """
    Filters songs based on the weather condition.
    """

    if weather_condition.lower() == "sunny":
        weather_condition = "Clear"
    
    for i in data['Weather'].tolist():
        if i.lower() in weather_condition.lower():
            print(i, weather_condition)
            weather_condition = i

    matching_songs = data[data['Weather'].str.contains(fr'\b{weather_condition}\b', case=False, na=False, regex=True)]

    if matching_songs.empty:
        return None  # Return None if no matches are found

    # sampled_songs = matching_songs.sample(n=min(20, len(matching_songs)))
    return matching_songs['TrackName'].tolist()


def suggest_weather_song_view(request):
    """
    API endpoint to suggest songs based on weather conditions.
    """
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        weather_condition = data.get('weather', '').strip()

        if not weather_condition:
            return JsonResponse({"error": "Weather condition is required."}, status=400)

        suggested_tracks = suggest_songs_for_weather(weather_condition)

        if suggested_tracks:
            return JsonResponse({"tracks": suggested_tracks})
        else:
            return JsonResponse({"error": f"No tracks found for weather: {weather_condition}"}, status=404)


