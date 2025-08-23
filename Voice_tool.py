import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import speech_recognition as sr
import os
import time
from gtts import gTTS
from pygame import mixer
import re
from io import BytesIO

def bolo(text, lang='hi'):
    audio_file = "temp_audio.mp3" 
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(audio_file)
        mixer.init()
        mixer.music.load(audio_file)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
        mixer.music.unload() 
        mixer.quit()         
        os.remove(audio_file)
    except Exception as e:
        print(f"Error in bolo function: {e}")
        if os.path.exists(audio_file):
            os.remove(audio_file)

def bolo_stream(text, lang='hi'):
    """
    NEW FUNCTION: Processes and plays audio sentence by sentence to reduce latency.
    """
    sentences = re.split(r'(?<=[.?!])\s*', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    for sentence in sentences:
        if not sentence:
            continue
        try:
            tts = gTTS(text=sentence, lang=lang)
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            mixer.init()
            mixer.music.load(mp3_fp)
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(0.1)
            time.sleep(0.2)
            
            mixer.quit()

        except Exception as e:
            print(f"Error in bolo_stream function: {e}")
            if mixer.get_init():
                mixer.quit()

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