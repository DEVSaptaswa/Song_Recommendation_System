# Song Recommendation System

A Django web application that recommends Spotify songs through three distinct AI-powered modes — **weather-based mood detection**, **facial emotion recognition**, and a **mood quiz** — each mapping to a curated song dataset.

---

## Features

| Mode | How it works |
|------|-------------|
| 🌦️ Weather Mood Music | Fetches live weather via WeatherAPI and recommends songs that match the current condition |
| 😐 Facial Mood Detection | Captures a photo via webcam, runs it through a trained Keras CNN, and recommends songs for the detected emotion |
| 📝 Mood Quiz | A 5-question quiz that determines your mood (Energetic / Calm / Thoughtful / Happy) and returns matching tracks |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Web Framework | Django 5.1.3 |
| Deep Learning | TensorFlow / Keras |
| Data Processing | pandas |
| Image Processing | Pillow (PIL) |
| Weather API | WeatherAPI (`weatherapi.com`) |
| Database | SQLite |
| Frontend | HTML, CSS, JS (Django templates) |

---

## Project Structure

```
spotify_recom/
│
├── manage.py
├── db.sqlite3
├── mood_detection_model1.h5       ← Pre-trained Keras emotion detection model
├── spotify_weather_data.csv       ← Weather → song mapping dataset
│
├── spotify_recom/                 ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                      ← Authentication app
│   ├── views.py                   ← signup_view, login_view, logout_view
│   ├── forms.py                   ← SignUpForm, LoginForm
│   └── urls.py
│
├── main/                          ← Core recommendation app
│   ├── views.py                   ← All recommendation logic
│   ├── urls.py
│   ├── muse_v3.csv                ← Mood → song mapping dataset (track, artist, seeds)
│   └── static/
│       └── muse_v3.csv
│
└── recom_eng/                     ← Recommendation engine app
    └── apps.py
```

---

## Datasets

### `spotify_weather_data.csv`
Used for weather-based recommendations.

| Column | Description |
|--------|-------------|
| `Weather` | Weather condition (e.g. Clear, Rain, Cloudy) |
| `TrackName` | Spotify track name matching that condition |

### `main/muse_v3.csv`
Used for facial mood detection and quiz recommendations.

| Column | Description |
|--------|-------------|
| `track` | Song title |
| `artist` | Artist name |
| `seeds` | List of mood tags (e.g. `['happy', 'energetic']`) |

---

## URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | `index` | Landing page |
| `/dashboard/` | `dashboard` | User dashboard |
| `/accounts/signup/` | `signup_view` | User registration |
| `/accounts/login/` | `login_view` | User login |
| `/accounts/logout/` | `logout_view` | User logout |
| `/weather-mood-music/` | `weather_mood_music` | Weather recommendation page |
| `/suggest-weather-song/` | `suggest_weather_song_view` | POST API — returns tracks for a weather condition |
| `/facial-mood-detection/` | `facial_mood_detection` | Facial detection page |
| `/analyze-facial-expression/` | `analyze_facial_expression` | POST API — returns emotion + song list |
| `/quiz/` | `quiz_page` | Mood quiz |
| `/quiz/result/` | `quiz_result` | Quiz results |

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/DEVSaptaswa/Song_Recommendation_System.git
cd Song_Recommendation_System
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install django tensorflow pandas pillow requests
```

### 4. Add your WeatherAPI key

Open `spotify_recom/settings.py` and replace the placeholder:

```python
WEATHER_API_KEY = 'your_api_key_here'
```

Get a free key at [weatherapi.com](https://www.weatherapi.com/).

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## How Each Mode Works

### 🌦️ Weather Mood Music
1. The frontend sends a `POST` request to `/suggest-weather-song/` with a `weather` field.
2. `suggest_songs_for_weather()` normalises the condition (e.g. "sunny" → "Clear") and filters `spotify_weather_data.csv`.
3. Matching `TrackName` values are returned as a JSON list.

### 😐 Facial Mood Detection
1. The user captures or uploads a photo on the `/facial-mood-detection/` page.
2. The image is sent as a base64 string via `POST` to `/analyze-facial-expression/`.
3. `analyze_emotion()` converts the image to 48×48 grayscale and runs it through `mood_detection_model1.h5`.
4. The model predicts one of six emotions: `angry`, `disgusted`, `sad`, `fear`, `neutral`, `happy`.
5. `muse_v3.csv` is filtered by the detected emotion's seed tag and matching songs are returned.

### 📝 Mood Quiz
1. The user answers 5 multiple-choice questions (A / B / C / D) on `/quiz/`.
2. The most frequent answer determines the final mood:

| Answer | Mood |
|--------|------|
| A | Energetic |
| B | Calm |
| C | Thoughtful |
| D | Happy |

3. `suggest_songs()` filters `muse_v3.csv` by that mood seed and renders results on `/quiz/result/`.

---

## Notes

- `mood_detection_model1.h5` must be present at the project root for the facial detection feature to work.
- `spotify_weather_data.csv` must be present at the project root.
- `main/muse_v3.csv` must be present inside the `main/` app directory.
- The app uses Django's built-in `User` model for authentication — no additional auth packages required.

---

## References

- [WeatherAPI Documentation](https://www.weatherapi.com/docs/)
- [TensorFlow Keras](https://www.tensorflow.org/api_docs/python/tf/keras)
