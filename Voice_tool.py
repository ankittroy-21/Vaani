import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import speech_recognition as sr
import os
import time
from gtts import gTTS
from pygame import mixer
import re
from io import BytesIO
import io
import warnings

# Try to import pydub, but don't fail if it's not available
try:
    from pydub import AudioSegment
    from pydub.playback import play
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    warnings.warn("pydub not installed. Voice enhancement disabled. Using original voice.")

# Check if ffmpeg is available
def check_ffmpeg():
    """Check if ffmpeg is available in the system"""
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=2)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

FFMPEG_AVAILABLE = check_ffmpeg() if PYDUB_AVAILABLE else False

if not FFMPEG_AVAILABLE and PYDUB_AVAILABLE:
    warnings.warn("FFmpeg not found. Voice enhancement disabled. Using original voice.")

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
    sentences = re.split(r'(?<=[.?!])\s*', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    for sentence in sentences:
        if not sentence:
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

def listen_command():
    r = sr.Recognizer()
    r.energy_threshold = 4000  # Adjust based on environment
    r.dynamic_energy_threshold = True
    
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("कृपया बोलिए :")
        try:
            audio = r.listen(source, timeout=7, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("कोई आवाज़ नहीं सुनाई दी।")
            bolo_stream("कोई आवाज़ नहीं सुनाई दी।")
            return ""
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