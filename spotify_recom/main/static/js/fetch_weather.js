document.addEventListener("DOMContentLoaded", () => {
    const weatherDisplay = document.getElementById("weather-display");

    const apiKey = "b2a69fdc5a1f42ec9ec05942242711 "; // Replace with your API key
    document.getElementById("fetch-weather-btn").addEventListener("click", () => {
        const locationInput = document.getElementById("location-input").value.trim();
        if (locationInput) {
            fetchWeather(locationInput); // Pass the user-specified location
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
            console.log("Fetched data:", data); // Debug the response

            // Extract data from the API response
            const temp_c = data.current.temp_c;
            const conditionText = data.current.condition.text;
            const locationName = data.location.name;
            const locationCountry = data.location.country;

            // Update the weather display
            weatherDisplay.innerHTML = `
                <p class="temperature"><i class="bi bi-thermometer-half"></i> ${temp_c}°C</p>
                <p class="condition"><i class="bi bi-cloud"></i> ${conditionText}</p>
                <p class="location"><i class="bi bi-geo-alt-fill"></i> ${locationName}, ${locationCountry}</p>
            `;
        } catch (error) {
            console.error("Error:", error);
            weatherDisplay.innerHTML = `<p class="error">Unable to fetch weather data. Please try again later.</p>`;
        }
    };

    fetchWeather();
});
