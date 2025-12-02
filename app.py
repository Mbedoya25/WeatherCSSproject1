from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# my OpenWeatherMap API key
API_KEY = "1e95ccbddb94abee683c685339ab1905"   # ← replace this with your real key

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():
    city = request.form["city"]

    # URL for OpenWeatherMap API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"

    # Send request
    response = requests.get(url)
    data = response.json()

    # If city not found
    if data["cod"] != 200:
        return render_template("result.html", error="City not found. Try again.")

    # Extract weather info
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    description = data["weather"][0]["description"]

    # Warning messages
    warning = None
    if temp >= 100:
        warning = "🔥 Extreme heat warning!"
    elif temp <= 20:
        warning = "❄️ Extreme cold warning!"
    elif wind >= 40:
        warning = "🌬️ High wind warning!"
    elif "storm" in description.lower():
        warning = "⛈️ Storm warning!"

    return render_template(
        "result.html",
        city=city,
        temp=temp,
        feels_like=feels_like,
        humidity=humidity,
        wind=wind,
        description=description,
        warning=warning
    )

if __name__ == "__main__":
    app.run(debug=True)

