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
        response_text.append(text)
    
    command_lower = command.lower()
    
    try:
        # Get or create session
        if session_id not in user_sessions:
            user_sessions[session_id] = {
                'articles': [],
                'waiting_for_news': False,
                'language': 'hi'
            }
        
        session = user_sessions[session_id]
        
        # PRIORITY 1: Emergency - Handle FIRST and FAST
        if handle_emergency_query(command, web_bolo):
            pass
        
        # PRIORITY 2: Language switching
        elif any(word in command_lower for word in ['english', 'hindi', 'hinglish', 'हिंदी', 'अंग्रेजी']):
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
            context = NewsContext(session.get('articles', []))
            if process_news_selection(command, web_bolo, context):
                session['waiting_for_news'] = False
                session['articles'] = []
        
        # Time requests
        elif any(phrase in command for phrase in Config.timedekh):
            current_time(web_bolo)
        
        # Date requests
        elif any(phrase in command for phrase in Config.date_trigger):
            get_date_of_day_in_week(command, web_bolo)
        
        # Weather
        elif any(word in command for word in Config.weather_trigger + Config.rain_trigger):
            get_weather(command, web_bolo)
        
        # News
        elif any(phrase in command for phrase in Config.news_trigger):
            articles = get_news(command, web_bolo)
            if articles:
                session['articles'] = articles
                session['waiting_for_news'] = True
        
        # Wikipedia
        elif any(phrase in command for phrase in Config.wikipedia_trigger):
            search_wikipedia(command, web_bolo)
        
        # Financial Literacy
        elif handle_financial_query(command, web_bolo):
            pass
        
        # Calculator
        elif handle_calculation_query(command, web_bolo):
            pass
        
        # Expense Tracker
        elif any(word in command_lower for word in ["खर्च", "खर्चा", "expense", "पैसा", "रुपये", "हिसाब"]):
            result = process_expense_command(command, get_user_id())
            response_text.append(result)
        
        # Agriculture
        elif (any(word in command_lower for word in Config.agri_trigger) or 
              any(crop in command_lower for crop in Config.agri_commodities)):
            context = AgriculturalContext()
            process_agriculture_command(command, web_bolo, {}, context)
        
        # Social schemes
        elif any(phrase in command_lower for phrase in Config.social_scheme_trigger):
            context = SchemeContext()
            handle_social_schemes_query(command, web_bolo, context)
        
        # General Knowledge
        elif (any(trigger in command_lower for trigger in Config.general_knowledge_triggers) or 
              '?' in command):
            if not handle_general_knowledge_query(command, web_bolo):
                response_text.append(lang_manager.get_phrase('error'))
        
        # Greeting
        elif any(phrase in command for phrase in Config.greeting_triggers):
            import random
            response_text.append(random.choice(Config.greeting_responses))
        
        # Unrecognized
        else:
            response_text.append(lang_manager.get_phrase('error'))
        
        # Generate audio file for response
        full_response = ' '.join(response_text) if response_text else lang_manager.get_phrase('error')
        
        # Create audio file
        try:
            audio_file = text_to_speech_file(full_response, lang=lang_manager.get_tts_code())
        except:
            audio_file = None
        
        return {
            'success': True,
            'text': full_response,
            'audio_file': audio_file,
            'language': session.get('language', 'hi')
        }
    
    except Exception as e:
        print(f"Error processing command: {e}")
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
        command = data.get('query', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not command:
            return jsonify({
                'success': False,
                'message': 'No query provided'
            }), 400
        
        result = process_command(command, session_id)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/audio/<path:filename>')
def serve_audio(filename):
    """Serve generated audio files"""
    try:
        return send_file(filename, mimetype='audio/mpeg')
    except:
        return jsonify({'error': 'Audio file not found'}), 404

@app.route('/api/status')
def status():
    """Get system status"""
    return jsonify({
        'online': offline_mgr.is_online(),
        'language': lang_manager.current_language,
        'languages_available': ['hi', 'en', 'hi-en']
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'Vaani Web UI'})

if __name__ == '__main__':
    # Create required directories
    for directory in ["data/expense_data", "data/offline_cache", "cache"]:
        os.makedirs(directory, exist_ok=True)
    
    print("=" * 60)
    print("🌾 Vaani Web Interface Starting...")
    print("=" * 60)
    print(f"Language: {lang_manager.get_language_name()}")
    print(f"Online: {'Yes' if offline_mgr.is_online() else 'No (Offline Mode)'}")
    print("=" * 60)
    print("\n🌐 Open your browser and go to: http://localhost:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
