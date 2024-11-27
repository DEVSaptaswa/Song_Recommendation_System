from django.urls import path, include
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('weather-mood-music/', views.weather_mood_music, name='weather_mood_music'),
    path('facial-mood-detection/', views.facial_mood_detection, name='facial_mood_detection'),
    path('weather-mood-music/weatherprediction/', views.suggest_weather_song_view, name='suggest_song')

]
