import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import speech_recognition as sr
import os
import time
import sys
from gtts import gTTS
from pygame import mixer
import re
from io import BytesIO
import warnings
import subprocess

# Try to from vaani.core import config as Config for FFmpeg path
try:
    from vaani.core import config as Config
    HAS_CONFIG = True
except ImportError:
    HAS_CONFIG = False

# Try to import pydub, but don't fail if it's not available
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    warnings.warn("pydub not installed. Voice enhancement disabled. Using original voice.")

# Check if ffmpeg is available, looking in multiple locations
def check_ffmpeg():
    """Check if ffmpeg is available in the system or in our custom path"""
    # First check if we have a custom FFmpeg path in Config
    if HAS_CONFIG and hasattr(Config, 'FFMPEG_PATH'):
        ffmpeg_path = os.path.join(Config.FFMPEG_PATH, 'ffmpeg')
        if sys.platform == 'win32':
            ffmpeg_path += '.exe'
        
        if os.path.exists(ffmpeg_path):
            # Add the directory to PATH so pydub can find it
            os.environ['PATH'] = Config.FFMPEG_PATH + os.pathsep + os.environ['PATH']
            return True
    
    # Check if it's in the PATH
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=2)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        # Check for ffmpeg in current directory/ffmpeg subdirectory as a fallback
        ffmpeg_local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg', 'ffmpeg')
        if sys.platform == 'win32':
            ffmpeg_local_path += '.exe'
        
        if os.path.exists(ffmpeg_local_path):
            ffmpeg_dir = os.path.dirname(ffmpeg_local_path)
            os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ['PATH']
            return True
        
        return False

FFMPEG_AVAILABLE = check_ffmpeg() if PYDUB_AVAILABLE else False

if not FFMPEG_AVAILABLE and PYDUB_AVAILABLE:
    warnings.warn("FFmpeg not found. Voice enhancement disabled. Using original voice.")

def bolo(text, lang='hi'):
    # Print the text to terminal before speaking
    print(f"\n🔊 Vaani: {text}\n")
    
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

def apply_voice_effects(audio_segment, voice_style='news_anchor'):
    """
    Apply voice effects to sound like a professional female news anchor.
    
    Parameters:
    - audio_segment: AudioSegment object
    - voice_style: 'news_anchor' for professional female voice, 'default' for original
    
    Returns:
    - Modified AudioSegment
    """
    if voice_style == 'news_anchor':
        # Palki Sharma style: Professional female news anchor voice
        # 1. Increase pitch for feminine voice (200-300 Hz range is typical for female voice)
        # Shift up by 3-5 semitones (300-500 cents) for female pitch
        octaves = 0.3  # Shift up by ~3.6 semitones
        new_sample_rate = int(audio_segment.frame_rate * (2.0 ** octaves))
        pitched_audio = audio_segment._spawn(audio_segment.raw_data, overrides={'frame_rate': new_sample_rate})
        pitched_audio = pitched_audio.set_frame_rate(audio_segment.frame_rate)
        
        # 2. Slightly increase speed for news anchor clarity (5% faster)
        # News anchors typically speak at 160-180 words per minute
        speed_audio = pitched_audio.speedup(playback_speed=1.05)
        
        # 3. Add slight emphasis (increase volume by 2-3 dB for authority)
        emphasized_audio = speed_audio + 2.5
        
        # 4. Improve clarity with slight compression
        # Normalize to prevent clipping
        normalized_audio = emphasized_audio.normalize()
        
        return normalized_audio
    
    return audio_segment

def bolo_stream(text, lang='hi', voice_style='news_anchor'):
    """
    ENHANCED FUNCTION: Processes and plays audio with professional news anchor voice.
    Falls back to original voice if FFmpeg is not available.
    
    Parameters:
    - text: Text to speak
    - lang: Language code (default 'hi' for Hindi)
    - voice_style: 'news_anchor' for Palki Sharma style, 'default' for original gTTS
    """
    # Clean and validate input text
    if not text or not text.strip():
        print("Error in bolo_stream function: No text to send to TTS API")
        return
    
    text = text.strip()
    
    # Print the full text to terminal before speaking
    print(f"\n🔊 Vaani: {text}\n")
    sentences = re.split(r'(?<=[.?!।])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 0]
    
    # If no sentences found, treat whole text as one sentence
    if not sentences:
        sentences = [text]

    for sentence in sentences:
        if not sentence or len(sentence) < 1:
            continue
        try:
            # Generate speech with gTTS
            tts = gTTS(text=sentence, lang=lang, slow=False)
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            
            # Check if voice enhancement is available and requested
            if voice_style == 'news_anchor' and PYDUB_AVAILABLE and FFMPEG_AVAILABLE:
                try:
                    # Apply voice effects for news anchor style
                    audio = AudioSegment.from_mp3(mp3_fp)
                    modified_audio = apply_voice_effects(audio, voice_style='news_anchor')
                    
                    # Export to BytesIO for playback
                    output = BytesIO()
                    modified_audio.export(output, format='mp3')
                    output.seek(0)
                    
                    # Play modified audio
                    mixer.init()
                    mixer.music.load(output)
                    mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(0.1)
                    time.sleep(0.15)
                    mixer.quit()
                except Exception as e:
                    # If voice effects fail, fall back to original
                    print(f"Voice enhancement failed, using original voice: {e}")
                    mp3_fp.seek(0)  # Reset to beginning
                    mixer.init()
                    mixer.music.load(mp3_fp)
                    mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(0.1)
                    time.sleep(0.2)
                    mixer.quit()
            else:
                # Original streaming without effects (fallback)
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

def listen_command(lang_code='hi-IN', prompt_text="कृपया बोलिए :"):
    """
    Listen to user command with multi-language support
    
    Parameters:
    - lang_code: Google Speech Recognition language code (e.g., 'hi-IN', 'en-IN', 'mr-IN')
    - prompt_text: Text to display when listening
    """
    r = sr.Recognizer()
    r.energy_threshold = 4000  # Adjust based on environment
    r.dynamic_energy_threshold = True
    
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source, duration=0.5)
        print(f"\n🎤 {prompt_text}")
        try:
            audio = r.listen(source, timeout=7, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("कोई आवाज़ नहीं सुनाई दी।")
            bolo_stream("कोई आवाज़ नहीं सुनाई दी।")
            return ""
    try:
        command = r.recognize_google(audio, language=lang_code)
        print(f"\n👤 आपने कहा: {command}")
        print("-" * 50)  # Visual separator
        # Don't echo back automatically - let main.py handle this
        return command.lower()
    except sr.UnknownValueError:
        print("क्षमा करें, मैं आपकी बात समझ नहीं पाया।")
        bolo("क्षमा करें, मैं आपकी बात समझ नहीं पाया।")
        return ""
    except sr.RequestError as e:
        print(f"Google Speech Recognition सेवा से कनेक्ट नहीं हो सका; {e}")
        bolo("Google Speech Recognition सेवा से कनेक्ट नहीं हो सका।")
        return ""