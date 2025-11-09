# 🐛 Vaani Debugging Guide & Learning Reference

**Troubleshooting, Error Tracking & Useful Commands | College Project**

---

## 📋 Table of Contents
1. [Common Errors & Solutions](#common-errors--solutions)
2. [Debugging Techniques](#debugging-techniques)
3. [Useful Commands Learned](#useful-commands-learned)
4. [Testing Procedures](#testing-procedures)
5. [Error Tracking System](#error-tracking-system)
6. [Performance Monitoring](#performance-monitoring)

---

## 🚨 Common Errors & Solutions

### 1️⃣ Audio/Voice Errors

#### Error: "No module named 'pyaudio'"
```
ModuleNotFoundError: No module named 'pyaudio'
```

**Solution:**
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# Alternative
pip install PyAudio-0.2.11-cp38-cp38-win_amd64.whl
```

**Root Cause:** PyAudio has binary dependencies that need special installation on Windows

---

#### Error: "Could not understand audio"
```
sr.UnknownValueError: Could not understand audio
```

**Solution:**
1. Check microphone permissions
2. Reduce background noise
3. Speak clearly and closer to mic
4. Check `listen_command()` timeout settings

**Code Fix:**
```python
# In voice_tool.py - Increase timeout
recognizer.listen(source, timeout=10, phrase_time_limit=8)
```

---

#### Error: "pygame.error: No available audio device"
```
pygame.error: No available audio device
```

**Solution:**
```bash
# Restart audio service (Windows)
net stop audiosrv
net start audiosrv

# Check audio devices
python -c "import pygame; pygame.mixer.init(); print('Audio OK')"
```

**Prevention:**
```python
# Add error handling in voice_tool.py
try:
    pygame.mixer.init()
except pygame.error:
    print("Audio device not available, retrying...")
    time.sleep(1)
    pygame.mixer.init()
```

---

#### Error: "gTTS connection timeout"
```
requests.exceptions.ConnectTimeout: HTTPSConnectionPool(host='translate.google.com', port=443)
```

**Solution:**
1. Check internet connection
2. Use offline mode fallback
3. Increase timeout in gTTS

**Code Fix:**
```python
# In voice_tool.py
tts = gTTS(text=text, lang=lang, slow=False, timeout=10)
```

---

### 2️⃣ API Errors

#### Error: "API key not found"
```
KeyError: 'OPENWEATHER_API_KEY'
```

**Solution:**
```bash
# Create .env file in project root
OPENWEATHER_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

**Verification:**
```python
# Check if .env is loaded
from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv('OPENWEATHER_API_KEY'))  # Should print key
```

---

#### Error: "Rate limit exceeded"
```
HTTP 429: Too Many Requests
```

**Solution:**
1. Implement caching
2. Use offline fallback
3. Upgrade API plan

**Code Fix:**
```python
# In weather_service.py - Add caching
cache = {}
if location in cache:
    return cache[location]
# ... fetch from API ...
cache[location] = result
return result
```

---

#### Error: "JSON decode error"
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Solution:**
```python
# Add error handling
try:
    data = response.json()
except json.JSONDecodeError:
    print(f"Invalid JSON response: {response.text}")
    return None
```

---

### 3️⃣ Import Errors

#### Error: "No module named 'vaani'"
```
ModuleNotFoundError: No module named 'vaani'
```

**Solution:**
```bash
# Run from project root (Vaani-2/)
cd c:\Users\Admin\Downloads\Vaani-2
python -m vaani.core.main

# Not from inside vaani/ folder!
```

**Explanation:** Python needs to see `vaani` as a package from parent directory

---

#### Error: "Circular import"
```
ImportError: cannot import name 'bolo' from partially initialized module 'vaani.core.voice_tool'
```

**Solution:**
1. Move import inside function
2. Restructure modules
3. Use dependency injection

**Code Fix:**
```python
# Instead of:
from vaani.core.voice_tool import bolo

# Do:
def my_function():
    from vaani.core.voice_tool import bolo
    bolo("Hello")
```

---

### 4️⃣ File & Path Errors

#### Error: "FileNotFoundError"
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/crop_data/आलू.json'
```

**Solution:**
```python
# Use absolute paths
import os
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
CROP_DATA_PATH = PROJECT_ROOT / "data" / "crop_data"

# Load file
crop_file = CROP_DATA_PATH / "आलू.json"
with open(crop_file, 'r', encoding='utf-8') as f:
    data = json.load(f)
```

---

#### Error: "UnicodeDecodeError"
```
UnicodeDecodeError: 'charmap' codec can't decode byte 0x81
```

**Solution:**
```python
# Always use UTF-8 encoding for Hindi files
with open(file_path, 'r', encoding='utf-8') as f:
    data = f.read()

# For writing
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(hindi_text)
```

---

### 5️⃣ Runtime Errors

#### Error: "AttributeError: 'NoneType' object has no attribute"
```
AttributeError: 'NoneType' object has no attribute 'lower'
```

**Solution:**
```python
# Check for None before using
command = listen_command()
if command is None:
    continue  # Skip this iteration
    
# Or use default value
command = listen_command() or ""
```

---

#### Error: "KeyError in config"
```
KeyError: 'news_trigger'
```

**Solution:**
```python
# In config.py, ensure all triggers are defined
news_trigger = ["समाचार", "न्यूज", "news"]

# In code, use safe access
triggers = getattr(Config, 'news_trigger', [])
```

---

## 🔍 Debugging Techniques

### 1️⃣ Print Debugging

**Basic Print:**
```python
# In main.py
command = listen_command()
print(f"[DEBUG] Received command: {command}")
print(f"[DEBUG] Command type: {type(command)}")
```

**Structured Debug:**
```python
def debug_log(message, data=None):
    """Helper function for debugging"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")
    if data:
        print(f"  Data: {data}")

# Usage
debug_log("Listening for command...")
debug_log("Command received", command)
```

---

### 2️⃣ Logging System

**Setup Logging:**
```python
import logging

# Configure logging
logging.basicConfig(
    filename='logs/vaani.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Usage
logger.debug("Starting voice recognition")
logger.info("User said: " + command)
logger.warning("API rate limit approaching")
logger.error("Failed to fetch weather data", exc_info=True)
```

**Log Levels:**
- `DEBUG`: Detailed info for debugging
- `INFO`: General information
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

---

### 3️⃣ Exception Handling

**Comprehensive Try-Except:**
```python
try:
    # Risky operation
    response = requests.get(url, timeout=5)
    data = response.json()
    return data
except requests.exceptions.Timeout:
    print("Request timed out")
    return None
except requests.exceptions.ConnectionError:
    print("No internet connection")
    return None
except json.JSONDecodeError:
    print("Invalid JSON response")
    return None
except Exception as e:
    print(f"Unexpected error: {e}")
    import traceback
    traceback.print_exc()  # Print full error trace
    return None
```

---

### 4️⃣ Breakpoint Debugging

**Using Python Debugger (pdb):**
```python
import pdb

# Set breakpoint
pdb.set_trace()  # Execution pauses here

# Or use built-in breakpoint() in Python 3.7+
breakpoint()  # Pauses here
```

**Debugger Commands:**
```
n - Next line
s - Step into function
c - Continue execution
p variable - Print variable value
l - List code around current line
q - Quit debugger
```

---

### 5️⃣ Testing Individual Functions

**Create Test Script:**
```python
# test_voice.py
from vaani.core.voice_tool import bolo, listen_command

# Test TTS
print("Testing TTS...")
bolo("नमस्ते", lang='hi')
print("TTS OK")

# Test STT
print("Testing STT... Speak now!")
command = listen_command()
print(f"You said: {command}")
```

**Run Test:**
```bash
python test_voice.py
```

---

## 💻 Useful Commands Learned

### Git Commands

```bash
# Check status
git status
git status --short  # Compact view

# View changes
git diff
git diff main.py  # Changes in specific file

# Commit changes
git add .
git commit -m "Descriptive message"

# View commit history
git log
git log --oneline  # Compact view
git log --graph --all  # Visual tree

# Undo changes
git restore main.py  # Discard changes
git restore --staged main.py  # Unstage file

# Create branch
git checkout -b feature/new-feature
git branch  # List branches
git checkout main  # Switch branch

# View remote
git remote -v
git remote add origin https://github.com/user/repo.git

# Push/Pull
git push origin main
git pull origin main
```

---

### Python Commands

```bash
# Run module
python -m vaani.core.main

# Install packages
pip install -r requirements.txt
pip install package_name
pip install --upgrade package_name

# List installed packages
pip list
pip freeze > requirements.txt

# Check Python version
python --version

# Run Python script
python script.py

# Python interactive shell
python
>>> import vaani.core.config as Config
>>> print(Config.news_trigger)
>>> exit()

# Check syntax without running
python -m py_compile main.py

# Profile code performance
python -m cProfile main.py

# Run tests
python -m pytest tests/
python -m unittest test_module.py
```

---

### PowerShell Commands

```powershell
# Navigation
cd path\to\folder
cd ..  # Go up one level
pwd  # Print current directory

# List files
ls
ls -Name  # Names only
Get-ChildItem -Recurse -Filter "*.py"  # Find all .py files

# File operations
New-Item -ItemType File -Name "file.py"  # Create file
New-Item -ItemType Directory -Name "folder"  # Create folder
Remove-Item file.py  # Delete file
Copy-Item source.py destination.py  # Copy
Move-Item old.py new.py  # Rename/move

# Read file
Get-Content file.txt
Get-Content file.txt | Select-Object -First 10  # First 10 lines
Get-Content file.txt | Select-Object -Last 10  # Last 10 lines

# Search in files
Select-String -Path "*.py" -Pattern "def main"
Select-String -Path "main.py" -Pattern "bolo" -CaseSensitive

# Count lines
(Get-Content main.py).Count
Select-String -Path "main.py" -Pattern "^" | Measure-Object -Line

# Environment variables
$env:PYTHONPATH = "C:\path\to\project"
$env:PATH += ";C:\new\path"

# Process management
Get-Process python
Stop-Process -Name python

# Network
Test-Connection google.com
Invoke-WebRequest https://api.example.com
```

---

### VS Code / Editor Commands

```bash
# Search in files
Ctrl + Shift + F

# Find and replace
Ctrl + H

# Go to line
Ctrl + G

# Command palette
Ctrl + Shift + P

# Open terminal
Ctrl + `

# Split editor
Ctrl + \

# Comment/uncomment
Ctrl + /

# Format code
Shift + Alt + F

# Rename symbol
F2

# Go to definition
F12

# Find all references
Shift + F12
```

---

### FFmpeg Commands

```bash
# Convert audio format
ffmpeg -i input.mp3 output.wav

# Change speed (1.15x)
ffmpeg -i input.mp3 -filter:a "atempo=1.15" output.mp3

# Adjust volume
ffmpeg -i input.mp3 -filter:a "volume=1.5" output.mp3

# Combine audio effects
ffmpeg -i input.mp3 -filter:a "atempo=1.15,volume=1.2" output.mp3

# Check audio info
ffmpeg -i audio.mp3
```

---

### JSON Validation

```bash
# Python
python -m json.tool data.json  # Pretty print & validate

# Check JSON in PowerShell
Get-Content data.json | ConvertFrom-Json
```

---

### API Testing (curl)

```bash
# GET request
curl https://api.example.com/data

# With API key
curl -H "Authorization: Bearer YOUR_KEY" https://api.example.com/data

# POST request
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' https://api.example.com

# Save response
curl https://api.example.com/data > response.json
```

---

## ✅ Testing Procedures

### 1️⃣ Voice Input Testing

**Test Script:**
```python
# tests/test_voice_input.py
from vaani.core.voice_tool import listen_command

test_phrases = [
    "समाचार सुनाओ",
    "मौसम बताओ",
    "आलू की खेती",
    "नमस्ते",
    "बंद करो"
]

print("Voice Input Testing")
print("Say each phrase when prompted:")

for phrase in test_phrases:
    print(f"\n📢 Say: '{phrase}'")
    input("Press Enter when ready...")
    
    result = listen_command()
    print(f"✓ Captured: {result}")
    
    if result and phrase.lower() in result.lower():
        print("✅ PASS")
    else:
        print("❌ FAIL")
```

---

### 2️⃣ Voice Output Testing

**Test Script:**
```python
# tests/test_voice_output.py
from vaani.core.voice_tool import bolo

test_phrases = [
    ("नमस्ते", 'hi'),
    ("Hello", 'en'),
    ("मौसम अच्छा है", 'hi'),
    ("How are you?", 'en'),
]

print("Voice Output Testing")

for text, lang in test_phrases:
    print(f"\n🔊 Speaking: '{text}' ({lang})")
    try:
        bolo(text, lang=lang)
        print("✅ PASS")
    except Exception as e:
        print(f"❌ FAIL: {e}")
```

---

### 3️⃣ Service Testing

**Test Weather Service:**
```python
# tests/test_weather.py
from vaani.services.weather.weather_service import get_weather
from vaani.core.voice_tool import bolo

commands = [
    "दिल्ली का मौसम बताओ",
    "मुंबई में बारिश होगी क्या",
    "जयपुर का तापमान बताओ"
]

for cmd in commands:
    print(f"\nTesting: {cmd}")
    get_weather(cmd, bolo)
```

**Test News Service:**
```python
# tests/test_news.py
from vaani.services.news.news_service import get_news
from vaani.core.voice_tool import bolo
from vaani.core.context_manager import NewsContext

context = NewsContext()
commands = [
    "समाचार सुनाओ",
    "खेल समाचार",
    "व्यापार न्यूज"
]

for cmd in commands:
    print(f"\nTesting: {cmd}")
    get_news(cmd, bolo, context)
```

---

### 4️⃣ API Testing

**Test All APIs:**
```python
# tests/test_apis.py
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def test_openweather():
    api_key = os.getenv('OPENWEATHER_API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Delhi&appid={api_key}"
    try:
        response = requests.get(url, timeout=5)
        assert response.status_code == 200
        print("✅ OpenWeatherMap API OK")
    except Exception as e:
        print(f"❌ OpenWeatherMap API FAIL: {e}")

def test_newsapi():
    api_key = os.getenv('NEWS_API_KEY')
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    try:
        response = requests.get(url, timeout=5)
        assert response.status_code == 200
        print("✅ NewsAPI OK")
    except Exception as e:
        print(f"❌ NewsAPI FAIL: {e}")

def test_gemini():
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Test")
        print("✅ Gemini API OK")
    except Exception as e:
        print(f"❌ Gemini API FAIL: {e}")

if __name__ == "__main__":
    test_openweather()
    test_newsapi()
    test_gemini()
```

---

## 📊 Error Tracking System

### Log File Structure

```
logs/
├── vaani.log              # Main application log
├── errors.log             # Error-only log
├── api_calls.log          # API request/response log
└── voice_commands.log     # User commands log
```

### Logging Implementation

```python
# vaani/core/logger.py
import logging
import os
from datetime import datetime

class VaaniLogger:
    def __init__(self):
        self.setup_loggers()
    
    def setup_loggers(self):
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # Main logger
        self.main_logger = logging.getLogger('vaani')
        self.main_logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler('logs/vaani.log', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.main_logger.addHandler(fh)
        self.main_logger.addHandler(ch)
        
        # Error logger (separate file)
        self.error_logger = logging.getLogger('vaani.errors')
        error_fh = logging.FileHandler('logs/errors.log', encoding='utf-8')
        error_fh.setLevel(logging.ERROR)
        error_fh.setFormatter(formatter)
        self.error_logger.addHandler(error_fh)
    
    def log_command(self, command):
        """Log user command"""
        with open('logs/voice_commands.log', 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {command}\n")
    
    def log_api_call(self, service, url, status):
        """Log API calls"""
        with open('logs/api_calls.log', 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {service} - {url} - Status: {status}\n")

# Usage
logger = VaaniLogger()
logger.main_logger.info("Vaani started")
logger.log_command("समाचार सुनाओ")
logger.log_api_call("NewsAPI", "https://newsapi.org/...", 200)
```

---

## 📈 Performance Monitoring

### Response Time Tracking

```python
# vaani/utils/performance.py
import time
from functools import wraps

def measure_time(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️ {func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

# Usage
@measure_time
def get_weather(command, bolo):
    # ... implementation ...
    pass
```

### Memory Usage Tracking

```python
import psutil
import os

def check_memory():
    """Check current memory usage"""
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"💾 Memory usage: {memory_mb:.2f} MB")

# Usage
check_memory()  # Call periodically
```

---

## 🛠️ Troubleshooting Checklist

When Vaani doesn't work:

```
□ Check internet connection
□ Check microphone permissions
□ Check speaker/audio output
□ Verify .env file exists with API keys
□ Check Python version (3.8+)
□ Verify all packages installed (pip list)
□ Check logs/vaani.log for errors
□ Test individual components
□ Restart audio services
□ Clear cache folder
□ Check file paths are correct
□ Verify JSON files are valid
```

---

**Last Updated:** November 7, 2025
