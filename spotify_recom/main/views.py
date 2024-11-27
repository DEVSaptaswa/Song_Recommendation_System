# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests  # Import requests to make the API call
import pandas as pd

# API_URL = "https://api.openweathermap.org/data/2.5/weather"
# API_KEY = settings.WEATHER_API_KEY

# Load the dataset (Make sure the file path is correct)
# file_path = 'spotify_weather_data.csv'  # Update this path
# data = pd.read_csv(file_path)

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
# Load the dataset (Make sure the file path is correct)
# file_path = 'spotify_weather_data.csv'  # Update this path
# data = pd.read_csv(file_path)

# def weather_view(request):
#     return render(request, 'accounts/weather.html')

# Function to suggest a song based on the weather
# def suggest_song(weather, dataset, num_suggestions=5):
#     # Filter songs for the given weather condition
#     filtered_songs = dataset[dataset['Weather'].str.lower() == weather.lower()]
    
#     if filtered_songs.empty:
#         return None

#     # Select random songs and convert to a list of dictionaries
#     songs = filtered_songs.sample(min(num_suggestions, len(filtered_songs)))
#     return songs.to_dict('records')





# def suggest_weather_song_view(request):
#     if request.method == "POST":
#         weather = request.POST.get('weather', '').strip()

#         if not weather:
#             return render(request, 'main/weather.html', {"error": "Please provide a weather condition"})

#         # Get multiple song suggestions based on the weather
#         suggestions = suggest_song(weather, data)

#         if suggestions:
#             # Ensure column names match your CSV file
#             for song in suggestions:
#                 song["TrackName"] = song.pop("TrackName")  # Replace "TrackName" with the actual column name
#             return render(request, 'main/weather.html', {"songs": suggestions})
#         else:
#             return render(request, 'main/weather.html', {"error": f"No song suggestions found for '{weather}'"})

#     return render(request, 'main/weather.html')


