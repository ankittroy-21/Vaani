import speech_recognition as sr
from gtts import gTTS
import os
import time
import datetime
from playsound import playsound
import requests

def bolo(text,lang='hi'):
    try:
      tts= gTTS(text=text,lang=lang) 
      audio_file="temp_audio.mp3" 
      tts.save(audio_file)
      playsound(audio_file)
      os.remove(audio_file)

    except ImportError:
       print("The 'playsound' Library is not installed. Please run: pip install playsound ")
       print("As a fallback, using os.system. This might not work on all systems.")  
       tts= gTTS(text=text,lang=lang) 
       audio_file="temp_audio.mp3" 
       tts.save(audio_file) 
       
       if os.name == 'nt':
          os.system(f"start {audio_file}")
       else:
          os.system(f"afplay {audio_file}")
       time.sleep(max(2,len(text) /15))
    except Exception as e:
       print(f"Error in speak function: {e}")

def listen_command():
   r=sr.Recognizer()
   with sr.Microphone() as source:
      print("नमस्ते! कृपया बोलिए...")
      r.pause_threshold = 1
      r.adjust_for_ambient_noise(source,duration=1)
      audio = r.listen(source)
   try:
      command = r.recognize_google(audio,language='hi-IN')
      print(f"आपने कहा: {command}")
      return command.lower()
   except sr.UnknownValueError:
      print("क्षमा करें, मैं आपकी बात समझ नहीं पाया।")
      bolo("क्षमा करें, मैं आपकी बात समझ नहीं पाया।")
      return ""
   except sr.RequestError as e:
      print(f"Google Speech Recognition सेवा से कनेक्ट नहीं हो सका; {e}")
      bolo("Google Speech Recognition सेवा से कनेक्ट नहीं हो सका।")
      return ""
   
def current_time():
   now=datetime.datetime.now()
   bolo(
        f"अभी {now.strftime('%I:%M')} {'सुबह' if now.hour < 12 else 'शाम'} के हैं।"
    )
   
def main():
   bolo("नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ?", lang='hi')

   while True:
      command = listen_command()
      if "समय" in command or "टाइम" in command:
        current_time()
      
      elif "नमस्ते" in command or "हेलो" in command:
        bolo("नमस्ते! क्या हाल है?")
      elif "बंद करो" in command or "अलविदा" in command:
        bolo("फिर मिलेंगे! अपना ध्यान रखना।")
        break
        # You can add more elif conditions here for other commands
      elif command:
        bolo("मैं यह समझ नहीं पाया, कृपया फिर से कहें।")

      time.sleep(1)

if __name__ == "__main__":
    main()
      
   