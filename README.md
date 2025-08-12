# Vaani – A Voice Assistant

Vaani is a smart, Python-based voice assistant designed for users who may face literacy challenges. It operates entirely through voice commands in Hindi, eliminating the need for reading or typing and making digital information accessible to everyone.

---
## ✨ Features

* **🗣️ Voice-Based Interaction:** Understands spoken Hindi commands and provides spoken responses.
* **⏰ Time & Date:** Get the current time with natural greetings for morning, afternoon, evening, and night.
* **🌦️ Dynamic Weather Forecasts:** Ask for the weather in any city (e.g., "Lucknow का मौसम बताओ").
* **📰 Latest News Headlines:** Listen to top news headlines from India or ask about specific topics (e.g., "क्रिकेट की खबरें सुनाओ").
* **📚 Wikipedia Search:** Get quick summaries from Wikipedia on any topic you ask about.
* **🎵 Play Songs:** Ask Vaani to play any song, and it will open it for you on YouTube.

---
## 🛠️ Built With

* **Python** 3.8+
* **Libraries**:
    * `SpeechRecognition` for voice-to-text.
    * `gTTS` for text-to-speech.
    * `playsound` for audio playback.
    * `requests` for API communication.
    * `wikipedia` for encyclopedia lookups.
    * `deep-translator` for real-time translation.
* **APIs**:
    * OpenWeatherMap API
    * GNews API

---
## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

* Python 3.8 or newer installed on your system.
* A working microphone connected to your computer.
* A stable internet connection.

### Installation

1.  **Clone the project**
    ```bash
    git clone https://github.com/groupnumber-9/Vaani
    ```

2.  **Go to the project directory**
    ```bash
    cd main
    ```

3.  **Set up your API Keys**
    * In the project folder, create a new file named `config.py`.
    * You will need to get free API keys from the services below and add them to this file.
        * **OpenWeatherMap API Key:** Get it from [OpenWeatherMap](https://openweathermap.org/appid)
        * **GNews API Key:** Get it from [GNews](https://gnews.io/)
    * Your `config.py` file should look like this:
        ```python
        # config.py
        WEATHER_API_KEY = "YOUR_SECRET_WEATHER_KEY_HERE"
        GNEWS_API_KEY = "YOUR_SECRET_GNEWS_KEY_HERE"
        ```

4.  **Install dependencies**
    * The `requirements.txt` file contains all the necessary Python libraries. Install them with one command:
        ```bash
        pip install -r requirements.txt
        ```

---
## Usage

To start the voice assistant, run the `main.py` script from your terminal:

```bash
python main.py
```

## 🚀 About Us
We are group of Devs which are focused to develop new things. Also open for new opportunities From 


![Logo](https://bbdu.ac.in/wp-content/uploads/2018/10/bbd-logo.png)
