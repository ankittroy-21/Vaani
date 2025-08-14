import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound
import time

def bolo(text, lang='hi'):
    try:
        tts = gTTS(text=text, lang=lang)
        audio_file = "temp_audio.mp3"
        tts.save(audio_file)
        playsound(audio_file)
        os.remove(audio_file)
    except ImportError:
        print("The 'playsound' library is not installed. Please run: 'pip install playsound'")
        print("As a fallback, using os.system. This might not work on all systems.")
        tts = gTTS(text=text, lang=lang)
        audio_file = "temp_audio.mp3"
        tts.save(audio_file)
        if os.name == 'nt':
            os.system(f"start {audio_file}")
        else:
            os.system(f"afplay {audio_file}")
        time.sleep(max(2, len(text) / 15))
    except Exception as e:
        print(f"Error in bolo function: {e}")

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        print("कृपया बोलिए :")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language='hi-IN')
        print(f"आपने कहा: {command}")
        bolo(f"आपने कहा: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("क्षमा करें, मैं आपकी बात समझ नहीं पाया।")
        bolo("क्षमा करें, मैं आपकी बात समझ नहीं पाया।")
        return ""
    except sr.RequestError as e:
        print(f"Google Speech Recognition सेवा से कनेक्ट नहीं हो सका; {e}")
        bolo("Google Speech Recognition सेवा से कनेक्ट नहीं हो सका।")
        return ""