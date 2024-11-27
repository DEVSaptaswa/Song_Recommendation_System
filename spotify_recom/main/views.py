# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests  # Import requests to make the API call
import pandas as pd
import random
import csv
import base64
import io

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
            # print(i, weather_condition)
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


import tensorflow as tf
import numpy as np
from PIL import Image

# Load the model once at server startup
model = tf.keras.models.load_model("mood_detection_model1.h5")

CSV_FILE_PATH = settings.BASE_DIR / 'main' / 'static' / 'muse_v3.csv'  # Adjust the path as needed

def load_songs_from_csv():
    songs = []
    try:
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                songs.append({
                    "track": row['track'],
                    "artist": row['artist'],
                    "seeds": row['seeds'],
                })
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return songs

def preprocess_image(image):
    """Preprocess the image to fit the model input requirements."""
    image = Image.open(image).convert("L")  # Convert to grayscale
    image = image.resize((48, 48))          # Resize to the required dimensions
    image_array = np.array(image) / 255.0   # Normalize
    image_array = np.expand_dims(image_array, axis=(0, -1))  # Add batch and channel dims
    return image_array

def analyze_emotion(image):
    """Predict emotion from the image using the loaded model."""
    processed_image = preprocess_image(image)
    predictions = model.predict(processed_image)
    emotions = ["angry", "disgusted", "sad", "fear", "neutral", "happy"]  # Adjust based on your model
    predicted_emotion = emotions[np.argmax(predictions)]
    return predicted_emotion

def analyze_facial_expression(request):
    if request.method == "POST":
        print('Yes')
        try:
            # Retrieve uploaded image
            image_url = request.POST["image"]
            print(image_url)

            format, imgstr = image_url.split(';base64,')  # Format: data:image/<format>;base64,<data>
            ext = format.split('/')[-1]  # Get file extension, e.g., png or jpg
            
            # Decode base64
            img_data = base64.b64decode(imgstr)
            
            # Save image to media folder
            file_name = f"uploaded_image.{ext}"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            
            with open(file_path, 'wb') as f:
                f.write(img_data)
            
            # Predict emotion from the uploaded image
            emotion = analyze_emotion(file_path)
            
            # Load songs from CSV
            all_songs = load_songs_from_csv()
            
            # Filter songs based on the detected emotion
            recommended_songs = [
                {"track": song["track"], "artist": song["artist"]}
                for song in all_songs if emotion.lower() in song["seeds"].lower()
            ]
            
            # Check if songs are available for the detected emotion
            if not recommended_songs:
                recommended_songs = [{"track": "No songs available", "artist": "N/A"}]
            
            # Return the emotion and recommended songs
            return JsonResponse({
                "emotion": emotion,
                "songs": [f"{song['track']} by {song['artist']}" for song in recommended_songs]
            })
        except Exception as e:
            # Handle errors during processing
            print(f"Error during analysis: {e}")
            return JsonResponse({"error": "Error processing the request."}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)

import os
import pandas as pd
from django.shortcuts import render
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from django.conf import settings

file_path = os.path.join(settings.BASE_DIR, 'main', 'muse_v3.csv')
dataset = pd.read_csv(file_path)

# Preprocess the 'seeds' column
dataset['seeds'] = dataset['seeds'].apply(lambda x: eval(x) if isinstance(x, str) else [])
dataset['seeds'] = dataset['seeds'].apply(lambda seeds: [seed.lower() for seed in seeds])


# Function to suggest songs based on a mood (seed)
def suggest_songs(seed_input):
    """
    Suggests songs based on a given mood (seed).

    Parameters:
        seed_input (str): A mood (e.g., 'happy', 'calm') to search for songs.

    Returns:
        List[Dict]: A list of dictionaries containing song and artist.
    """
    seed_input = seed_input.lower()
    suggestions = dataset[dataset['seeds'].apply(lambda seeds: seed_input in seeds)]
    return suggestions[['track', 'artist']].to_dict('records')

# Quiz Page View
def quiz_page(request):
    if request.method == 'POST':
        # Extract quiz answers
        question1 = request.POST.get('question1')
        question2 = request.POST.get('question2')
        question3 = request.POST.get('question3')
        question4 = request.POST.get('question4')
        question5 = request.POST.get('question5')

        # Determine final mood (example logic, adjust as needed)
        mood_map = {
            'A': 'Energetic',
            'B': 'Calm',
            'C': 'Thoughtful',
            'D': 'Happy'
        }
        answers = [question1, question2, question3, question4, question5]
        mood_counts = {key: answers.count(key) for key in mood_map.keys()}
        final_answer = max(mood_counts, key=mood_counts.get)
        final_mood = mood_map[final_answer]

        # Suggest songs based on mood
        suggested_songs = suggest_songs(final_mood)

        return render(request, 'main/quiz_result.html', {'final_mood': final_mood, 'suggested_songs': suggested_songs})

    return render(request, 'main/quiz_page.html')

from django.http import JsonResponse

def quiz_result(request):
    if request.method == "POST":
        # Assume request.POST contains the submitted answers
        answers = request.POST.getlist('answers')  # Fetch submitted answers
        correct_answers = ['A', 'C', 'B', 'D']  # Example: correct answers for a 4-question quiz
        score = sum(1 for user_ans, correct_ans in zip(answers, correct_answers) if user_ans == correct_ans)
        
        result = {
            'score': score,
            'total': len(correct_answers),
            'percentage': (score / len(correct_answers)) * 100
        }
        
        # Render result in a template or return as JSON
        return render(request, 'main/quiz_result.html', {'result': result})
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)