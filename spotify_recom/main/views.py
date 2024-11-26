from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd

def index(request):
    return render(request, 'main/index.html')

# Load the dataset (Make sure the file path is correct)
file_path = 'spotify_weather_data.csv'  # Update this path
data = pd.read_csv(file_path)

def weather_view(request):
    return render(request, 'accounts/weather.html')

# Function to suggest a song based on the weather
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