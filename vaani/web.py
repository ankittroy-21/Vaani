"""
Vaani Web Interface - Flask Application
Provides a web UI for the Vaani voice assistant
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import io
import json
import tempfile
from datetime import datetime
import hashlib
import time
import glob
import threading
import requests
from urllib.parse import urlparse

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Import Vaani core modules
from vaani.core import config as Config
from vaani.core.voice_tool import bolo_stream as bolo, text_to_speech_file
from vaani.core.language_manager import get_language_manager
from vaani.core.context_manager import NewsContext, AgriculturalContext, SchemeContext
from vaani.core.offline_mode import OfflineMode
from vaani.core import api_key_manager

# Import services
from vaani.services.time.time_service import current_time, get_date_of_day_in_week
from vaani.services.weather.weather_service import get_weather
from vaani.services.news.news_service import get_news, process_news_selection
from vaani.services.knowledge.wikipedia_service import search_wikipedia
from vaani.services.agriculture.agri_command_processor import process_agriculture_command
from vaani.services.social.social_scheme_service import handle_social_schemes_query
from vaani.services.knowledge.general_knowledge_service import handle_general_knowledge_query
from vaani.services.finance.financial_literacy_service import handle_financial_query
from vaani.services.finance.simple_calculator_service import handle_calculation_query
from vaani.services.social.emergency_assistance_service import handle_emergency_query
from vaani.services.finance.expense_tracker_service import process_expense_command

# Initialize Flask app
app = Flask(__name__, 
            template_folder='../web/templates',
            static_folder='../web/static')
CORS(app)

# Initialize components
api_key_manager.setup_api_keys()
lang_manager = get_language_manager()
offline_mgr = OfflineMode()

# Session storage (in production, use Redis or database)
user_sessions = {}

# Keep-alive configuration for Render free tier
KEEP_ALIVE_INTERVAL = 14 * 60  # 14 minutes (just under 15 min timeout)
KEEP_ALIVE_ENABLED = os.getenv('KEEP_ALIVE_ENABLED', 'true').lower() == 'true'
RENDER_EXTERNAL_URL = os.getenv('RENDER_EXTERNAL_URL', '')  # Set by Render automatically

def cleanup_old_audio_files(max_age_minutes=30, max_files=50):
    """
    Clean up old audio files from cache directory to prevent disk space issues
    
    Args:
        max_age_minutes: Delete files older than this many minutes (default: 30)
        max_files: Maximum number of files to keep (default: 50)
    """
    try:
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache')
        
        if not os.path.exists(cache_dir):
            return
        
        # Get all audio files with their timestamps
        audio_files = []
        for filename in os.listdir(cache_dir):
            if filename.endswith('.mp3'):
                filepath = os.path.join(cache_dir, filename)
                try:
                    mtime = os.path.getmtime(filepath)
                    size = os.path.getsize(filepath)
                    audio_files.append({
                        'path': filepath,
                        'name': filename,
                        'mtime': mtime,
                        'age_minutes': (time.time() - mtime) / 60,
                        'size': size
                    })
                except Exception as e:
                    print(f"[Cleanup Warning]: Could not stat {filename}: {e}")
        
        if not audio_files:
            return
        
        deleted_count = 0
        deleted_size = 0
        
        # Sort by modification time (oldest first)
        audio_files.sort(key=lambda x: x['mtime'])
        
        print(f"\n[Audio Cleanup]: Found {len(audio_files)} audio files in cache")
        
        # Delete files older than max_age_minutes
        current_time = time.time()
        for file_info in audio_files[:]:
            age_minutes = file_info['age_minutes']
            if age_minutes > max_age_minutes:
                try:
                    os.remove(file_info['path'])
                    deleted_count += 1
                    deleted_size += file_info['size']
                    audio_files.remove(file_info)
                    print(f"  ✅ Deleted old file: {file_info['name']} (age: {age_minutes:.1f} min)")
                except Exception as e:
                    print(f"  ❌ Failed to delete {file_info['name']}: {e}")
        
        # If still too many files, delete oldest ones
        if len(audio_files) > max_files:
            files_to_delete = len(audio_files) - max_files
            print(f"[Audio Cleanup]: Too many files ({len(audio_files)}), deleting {files_to_delete} oldest")
            
            for file_info in audio_files[:files_to_delete]:
                try:
                    os.remove(file_info['path'])
                    deleted_count += 1
                    deleted_size += file_info['size']
                    print(f"  ✅ Deleted excess file: {file_info['name']}")
                except Exception as e:
                    print(f"  ❌ Failed to delete {file_info['name']}: {e}")
        
        if deleted_count > 0:
            print(f"[Audio Cleanup]: ✅ Deleted {deleted_count} files, freed {deleted_size / 1024:.1f} KB")
            print(f"[Audio Cleanup]: {len(audio_files) - deleted_count} files remaining\n")
        else:
            print(f"[Audio Cleanup]: No cleanup needed, {len(audio_files)} files within limits\n")
            
    except Exception as e:
        print(f"[Audio Cleanup Error]: {e}")
        import traceback
        traceback.print_exc()

def keep_alive_ping():
    """
    Keep-alive function to prevent Render free tier from spinning down.
    Pings the service every 14 minutes to keep it active.
    """
    while True:
        try:
            time.sleep(KEEP_ALIVE_INTERVAL)
            
            # Determine the URL to ping
            if RENDER_EXTERNAL_URL:
                url = f"{RENDER_EXTERNAL_URL}/api/health"
            else:
                url = "http://localhost:5000/api/health"
            
            print(f"\n[Keep-Alive] Pinging service at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"[Keep-Alive] ✅ Ping successful - Service is alive")
            else:
                print(f"[Keep-Alive] ⚠️ Ping returned status {response.status_code}")
                
        except Exception as e:
            print(f"[Keep-Alive] ❌ Ping failed: {e}")

def start_keep_alive():
    """Start the keep-alive background thread"""
    if KEEP_ALIVE_ENABLED and (RENDER_EXTERNAL_URL or os.getenv('RENDER')):
        print("\n" + "="*60)
        print("🔄 Keep-Alive Service Starting...")
        print(f"   Interval: {KEEP_ALIVE_INTERVAL // 60} minutes")
        print(f"   Target URL: {RENDER_EXTERNAL_URL or 'http://localhost:5000'}")
        print("="*60 + "\n")
        
        keep_alive_thread = threading.Thread(target=keep_alive_ping, daemon=True)
        keep_alive_thread.start()
    else:
        print("\n[Keep-Alive] Disabled (not running on Render or manually disabled)")


def get_user_id():
    """Generate a simple user ID based on session"""
    return hashlib.md5(("web_user" + str(datetime.now().date())).encode()).hexdigest()[:8]

def capture_output(func, *args, **kwargs):
    """Capture print output from bolo function"""
    captured_output = []
    
    def mock_bolo(text, lang='hi', **kw):
        captured_output.append(text)
    
    # Replace bolo temporarily
    original_bolo = kwargs.get('bolo_func', mock_bolo)
    
    try:
        result = func(*args, bolo=original_bolo, **kwargs)
        return result, captured_output
    except Exception as e:
        return None, [str(e)]

def process_command(command, session_id=None):
    """
    Process a text command and return response
    Returns: dict with 'text', 'success', 'audio_file' (optional)
    """
    print(f"\n{'='*60}")
    print(f"Processing command: '{command}'")
    print(f"Session ID: {session_id}")
    print(f"{'='*60}\n")
    
    if not command or not command.strip():
        return {
            'success': False,
            'text': lang_manager.get_phrase('error'),
            'message': 'Empty command'
        }
    
    response_text = []
    audio_file = None
    
    def web_bolo(text, lang='hi', **kwargs):
        """Custom bolo function that collects text"""
        if text and text.strip():
            print(f"[web_bolo] Captured: {text}")
            response_text.append(text)
        return text  # Return text for compatibility
    
    command_lower = command.lower()
    print(f"Command (lowercase): {command_lower}")
    
    try:
        # Get or create session
        if session_id not in user_sessions:
            user_sessions[session_id] = {
                'articles': [],
                'waiting_for_news': False,
                'language': 'hi',
                'context': None
            }
        
        session = user_sessions[session_id]
        print(f"Session state: {session}")
        
        # PRIORITY 1: Emergency - Handle FIRST and FAST
        print("Checking emergency...")
        if handle_emergency_query(command, web_bolo):
            print("Emergency query handled")
        
        # PRIORITY 2: Language switching
        elif any(word in command_lower for word in ['english', 'hindi', 'hinglish', 'हिंदी', 'अंग्रेजी']):
            print("Language switch detected")
            if 'english' in command_lower or 'अंग्रेजी' in command_lower:
                lang_manager.set_language('en')
                session['language'] = 'en'
                response_text.append("Switched to English. How can I help you?")
            elif 'hindi' in command_lower or 'हिंदी' in command_lower:
                lang_manager.set_language('hi')
                session['language'] = 'hi'
                response_text.append("हिंदी में बदल गया। मैं आपकी कैसे मदद कर सकता हूं?")
        
        # Handle news selection if waiting
        elif session.get('waiting_for_news', False):
            print("Processing news selection...")
            context = NewsContext(session.get('articles', []))
            if process_news_selection(command, web_bolo, context):
                session['waiting_for_news'] = False
                session['articles'] = []
        
        # Time requests
        elif any(phrase in command for phrase in Config.timedekh):
            print("Time query detected")
            current_time(web_bolo)
        
        # Date requests
        elif any(phrase in command for phrase in Config.date_trigger):
            print("Date query detected")
            get_date_of_day_in_week(command, web_bolo)
        
        # Weather
        elif any(word in command for word in Config.weather_trigger + Config.rain_trigger):
            print("Weather query detected")
            get_weather(command, web_bolo)
        
        # News
        elif any(phrase in command for phrase in Config.news_trigger):
            print("News query detected")
            articles = get_news(command, web_bolo)
            if articles:
                session['articles'] = articles
                session['waiting_for_news'] = True
        
        # Wikipedia
        elif any(phrase in command for phrase in Config.wikipedia_trigger):
            print("Wikipedia query detected")
            search_wikipedia(command, web_bolo)
        
        # Financial Literacy
        elif handle_financial_query(command, web_bolo):
            print("Financial query handled")
        
        # Calculator
        elif handle_calculation_query(command, web_bolo):
            print("Calculator query handled")
        
        # Expense Tracker
        elif any(word in command_lower for word in ["खर्च", "खर्चा", "expense", "पैसा", "रुपये", "हिसाब"]):
            print("Expense tracker query detected")
            result = process_expense_command(command, get_user_id())
            if result:
                response_text.append(result)
        
        # Agriculture
        elif (any(word in command_lower for word in Config.agri_trigger) or 
              any(crop in command_lower for crop in Config.agri_commodities)):
            print("Agriculture query detected")
            context = AgriculturalContext()
            process_agriculture_command(command, web_bolo, {}, context)
        
        # Social schemes
        elif any(phrase in command_lower for phrase in Config.social_scheme_trigger):
            print("Social scheme query detected")
            context = SchemeContext()
            handle_social_schemes_query(command, web_bolo, context)
        
        # General Knowledge
        elif (any(trigger in command_lower for trigger in Config.general_knowledge_triggers) or 
              '?' in command):
            print("General knowledge query detected")
            if not handle_general_knowledge_query(command, web_bolo):
                response_text.append(lang_manager.get_phrase('error'))
        
        # Greeting
        elif any(phrase in command for phrase in Config.greeting_triggers):
            print("Greeting detected")
            import random
            response_text.append(random.choice(Config.greeting_responses))
        
        # Fallback for unrecognized queries - Try Gemini AI
        else:
            print("Unrecognized query - trying Gemini AI for general question")
            
            # Try to answer using Gemini AI
            if handle_general_knowledge_query(command, web_bolo):
                print("✅ Gemini AI handled the query")
            else:
                # If Gemini also fails, show error
                print("❌ Gemini AI could not handle query - showing error")
                response_text.append("मुझे आपका सवाल समझ नहीं आया। कृपया दोबारा कोशिश करें।")

        # Generate audio file for response
        full_response = ' '.join(response_text) if response_text else lang_manager.get_phrase('error')
        print(f"\n[Response Generated]: {full_response[:200]}...")
        print(f"[Response Length]: {len(full_response)} characters")

        # Create audio file
        audio_file = None
        try:
            # Limit audio generation to reasonable length (max 1000 characters)
            # Long text takes too long and may fail
            audio_text = full_response
            if len(full_response) > 1000:
                print(f"[Audio Warning]: Text too long ({len(full_response)} chars), truncating for audio...")
                # Take first 900 characters and add "..." 
                audio_text = full_response[:900] + "... अधिक जानकारी के लिए कृपया पढ़ें।"
            
            print(f"[Audio Generation]: Starting for {len(audio_text)} characters...")
            audio_path = text_to_speech_file(audio_text, lang=lang_manager.get_tts_code())
            
            if audio_path and os.path.exists(audio_path):
                # Store relative path for serving
                audio_file = os.path.basename(audio_path)
                print(f"[Audio Generated]: {audio_file}")
                
                # Clean up old audio files periodically
                cleanup_old_audio_files(max_age_minutes=30, max_files=50)
            else:
                print(f"[Audio Warning]: No audio file generated")
        except Exception as e:
            print(f"[Audio Error]: {e}")
            import traceback
            traceback.print_exc()
            audio_file = None

        result = {
            'success': True,
            'text': full_response,
            'audio_file': f'/api/audio/{audio_file}' if audio_file else None,
            'language': session.get('language', 'hi'),
            'waiting_for_news': session.get('waiting_for_news', False)
        }
        
        print(f"\n[Final Result]: {result}\n")
        print(f"{'='*60}\n")
        
        return result
    
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        
        return {
            'success': False,
            'text': f"Error: {str(e)}",
            'message': str(e)
        }

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    """Handle text query from user"""
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debug log
        
        command = data.get('query', '').strip()
        session_id = data.get('session_id', 'default')
        
        print(f"Processing command: '{command}' for session: {session_id}")  # Debug log
        
        if not command:
            return jsonify({
                'success': False,
                'message': 'No query provided'
            }), 400
        
        result = process_command(command, session_id)
        print(f"Result: {result}")  # Debug log
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in query endpoint: {e}")  # Debug log
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/audio/<path:filename>')
def serve_audio(filename):
    """Serve generated audio files"""
    try:
        # Get absolute path to cache directory
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache')
        audio_path = os.path.join(cache_dir, filename)
        
        print(f"\n[Audio Request]")
        print(f"  Filename: {filename}")
        print(f"  Cache dir: {cache_dir}")
        print(f"  Full path: {audio_path}")
        print(f"  Exists: {os.path.exists(audio_path)}")
        
        if os.path.exists(audio_path):
            file_size = os.path.getsize(audio_path)
            print(f"  Size: {file_size} bytes")
            print(f"  Serving audio file: {audio_path}")
            
            # Send file with proper headers
            response = send_file(
                audio_path, 
                mimetype='audio/mpeg',
                as_attachment=False,
                download_name=filename
            )
            
            # Add CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            
            print(f"  ✅ Audio served successfully")
            return response
        else:
            print(f"  ❌ Audio file not found: {audio_path}")
            
            # List files in cache to help debug
            if os.path.exists(cache_dir):
                cache_files = os.listdir(cache_dir)
                print(f"  Files in cache: {cache_files[:5]}")
            
            return jsonify({'error': 'Audio file not found', 'path': audio_path}), 404
            
    except Exception as e:
        print(f"  ❌ Error serving audio: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """Get system status"""
    return jsonify({
        'online': offline_mgr.is_online(),
        'language': lang_manager.current_language,
        'languages_available': ['hi', 'en', 'hi-en']
    })

@app.route('/api/cleanup-audio', methods=['POST'])
def cleanup_audio():
    """Manual cleanup endpoint for audio files"""
    try:
        max_age = request.json.get('max_age_minutes', 30) if request.json else 30
        max_files = request.json.get('max_files', 50) if request.json else 50
        
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache')
        
        # Get count before cleanup
        before_count = len([f for f in os.listdir(cache_dir) if f.endswith('.mp3')]) if os.path.exists(cache_dir) else 0
        
        # Run cleanup
        cleanup_old_audio_files(max_age_minutes=max_age, max_files=max_files)
        
        # Get count after cleanup
        after_count = len([f for f in os.listdir(cache_dir) if f.endswith('.mp3')]) if os.path.exists(cache_dir) else 0
        
        return jsonify({
            'success': True,
            'message': 'Cleanup completed',
            'files_before': before_count,
            'files_after': after_count,
            'deleted': before_count - after_count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/test')
def test():
    """Simple test endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'API is working!',
        'timestamp': str(datetime.now())
    })

@app.route('/api/test-audio')
def test_audio():
    """Test if audio serving works"""
    try:
        # Find first audio file in cache
        import glob
        audio_files = glob.glob('cache/*.mp3')
        
        if audio_files:
            test_file = os.path.basename(audio_files[0])
            return jsonify({
                'status': 'ok',
                'test_audio': f'/api/audio/{test_file}',
                'files_in_cache': len(audio_files),
                'test_file_path': audio_files[0],
                'exists': os.path.exists(audio_files[0])
            })
        else:
            return jsonify({
                'status': 'no_files',
                'message': 'No audio files in cache'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'Vaani Web UI'})

@app.route('/api/greeting')
def greeting():
    """Generate greeting audio for first mic click"""
    try:
        greeting_text = "नमस्ते! मैं वाणी हूं, आपकी आवाज सहायक। आप मुझसे मौसम, समाचार, सरकारी योजनाएं और बहुत कुछ पूछ सकते हैं।"
        
        print(f"\n[Greeting Request]")
        print(f"  Generating audio for greeting...")
        
        # Generate audio
        audio_path = text_to_speech_file(greeting_text, lang='hi')
        
        if audio_path and os.path.exists(audio_path):
            audio_file = os.path.basename(audio_path)
            print(f"  ✅ Greeting audio generated: {audio_file}")
            
            return jsonify({
                'success': True,
                'text': greeting_text,
                'audio_file': f'/api/audio/{audio_file}'
            })
        else:
            print(f"  ❌ Failed to generate greeting audio")
            return jsonify({
                'success': False,
                'text': greeting_text,
                'message': 'Audio generation failed'
            })
            
    except Exception as e:
        print(f"  ❌ Error generating greeting: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Create required directories
    for directory in ["data/expense_data", "data/offline_cache", "cache", "logs"]:
        os.makedirs(directory, exist_ok=True)
    
    print("=" * 60)
    print("🌾 Vaani Web Interface Starting...")
    print("=" * 60)
    print(f"Language: {lang_manager.get_language_name()}")
    
    # Clean up old audio files on startup
    print("\n🧹 Running startup cleanup...")
    cleanup_old_audio_files(max_age_minutes=30, max_files=50)
    print(f"Online: {'Yes' if offline_mgr.is_online() else 'No (Offline Mode)'}")
    
    # Start keep-alive service for Render
    start_keep_alive()
    
    print("=" * 60)
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"\n🌐 Starting server on {host}:{port}")
    if not os.getenv('RENDER'):
        print(f"🌐 Open your browser and go to: http://localhost:{port}")
    print("=" * 60)
    
    app.run(host=host, port=port, debug=debug)
