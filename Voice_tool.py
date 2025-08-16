import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import speech_recognition as sr
import os
import time
from gtts import gTTS
from pygame import mixer

def bolo(text, lang='hi'):
    audio_file = "temp_audio.mp3" 
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(audio_file)

        # Use pygame mixer to play the audio
        mixer.init()
        mixer.music.load(audio_file)
        mixer.music.play()

        # Wait for the audio to finish playing before continuing
        while mixer.music.get_busy():
            time.sleep(0.1)
        
        
        mixer.music.unload() 
        mixer.quit()         
        os.remove(audio_file)

    except Exception as e:
        print(f"Error in bolo function: {e}")
        # Fallback in case of an error
        if os.path.exists(audio_file):
            os.remove(audio_file)

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