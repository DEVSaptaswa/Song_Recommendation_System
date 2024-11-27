document.addEventListener("DOMContentLoaded", () => {
    const weatherDisplay = document.getElementById("weather-display");
    const songDisplay = document.getElementById("song-list"); // Element to display suggested songs

    const apiKey = "b2a69fdc5a1f42ec9ec05942242711"; // Replace with your API key

    document.getElementById("fetch-weather-btn").addEventListener("click", () => {
        const locationInput = document.getElementById("location-input").value.trim();
        if (locationInput) {
            fetchWeather(locationInput); // Fetch the weather data
        } else {
            alert("Please enter a location!");
        }
    });

    const fetchWeather = async (locationQuery) => {
        const url = `https://api.weatherapi.com/v1/current.json?key=${apiKey}&q=${locationQuery}&aqi=no`;

        try {
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`Error fetching weather data: ${response.statusText}`);
            }

            const data = await response.json();
            console.log("Fetched weather data:", data); // Debug the response

            // Extract data from the API response
            const temp_c = data.current.temp_c;
            const conditionText = data.current.condition.text;
            const locationName = data.location.name;
            const locationCountry = data.location.country;

            // Update the weather display
            weatherDisplay.innerHTML = `
                <p class="temperature text-white"><i class="bi bi-thermometer-half"></i> ${temp_c}°C</p>
                <p class="condition text-white"><i class="bi bi-cloud"></i> ${conditionText}</p>
                <p class="location text-white"><i class="bi bi-geo-alt-fill"></i> ${locationName}, ${locationCountry}</p>
            `;

            // Fetch songs based on the weather condition
            fetchSongsForWeather(conditionText);

        } catch (error) {
            console.error("Error:", error);
            weatherDisplay.innerHTML = `<p class="text-danger">Unable to fetch weather data. Please try again later.</p>`;
        }
    };

    const fetchSongsForWeather = async (weatherCondition) => {
        const url = "/suggest-weather-song/"; // Django endpoint URL

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"), // Add CSRF token for security
                },
                body: JSON.stringify({ weather: weatherCondition }),
            });

            const data = await response.json();

            if (data.tracks) {
            // Update the song display with the suggested tracks
            const songList = document.getElementById("song-list");
            songList.innerHTML = data.tracks
                .map((track) => `<li><i class="bi bi-music-note"></i> ${track}</li>`)
                .join("");
            } else {
                songDisplay.innerHTML = `<li>${data.error}</li>`;
            }
        } catch (error) {
            console.error("Error fetching songs:", error);
            songDisplay.innerHTML = `<li>Error fetching song suggestions.</li>`;
        }};

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
