# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests  # Import requests to make the API call
import pandas as pd

API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = settings.WEATHER_API_KEY

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

def suggest_song(weather, dataset):
    # Filter songs for the given weather condition
    filtered_songs = dataset[dataset['Weather'].str.lower() == weather.lower()]
    
    if filtered_songs.empty:
        return None
    
    # Select a random song from the filtered list
    song = filtered_songs.sample().iloc[0]
    return {
        "Track Name": song["TrackName"],
        "Artist": song["Artist"],
        "Album": song["Album"]
    }

# View function to handle song suggestion request
def suggest_weather_song_view(request):
    weather = request.POST['weather'].strip()
    
    if not weather:
        return JsonResponse({"error": "Please provide a weather condition"}, status=400)
    
    # Get song suggestion based on the weather
    suggestion = suggest_song(weather, data)
    
    if suggestion:
        return JsonResponse(suggestion)
    else:
        return JsonResponse({"error": f"No song suggestions found for '{weather}'"}, status=404)

# Unified weather_view
def weather_view(request):
    # Define city name and country
    city = "New York"
    country = "US"
    
    # Create the URL with city and country
    url = f"{API_URL}?q={city},{country}&appid={API_KEY}&units=metric"
    
    # Fetch data from the API
    response = requests.get(url)
    data = response.json()

    # Check if the API request was successful
    if data.get("cod") == 200:
        temperature = data['main']['temp']
        condition = data['weather'][0]['description']
        location = f"{data['name']}, {data['sys']['country']}"
    else:
        temperature = condition = location = "Data not available"

    # Return the data as JSON
    return JsonResponse({
        'temperature': temperature,
        'condition': condition,
        'location': location
    })
