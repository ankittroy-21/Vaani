"""
Test Multi-Language Support for Vaani
"""

from language_manager import get_language_manager, handle_language_command
from Voice_tool import bolo_stream

print("=" * 70)
print("🌍 Testing Multi-Language Support for Vaani")
print("=" * 70)

# Initialize language manager
lang_manager = get_language_manager()

# Test 1: Check if Gemini API is configured
print("\n📋 Test 1: Checking Gemini API Configuration")
print("-" * 70)
if lang_manager.model:
    print("✅ Gemini API is configured and ready!")
else:
    print("⚠️  Gemini API not configured - Translation features will be limited")
    print("    Add GEMINI_API_KEY to .env file to enable translation")

# Test 2: List supported languages
print("\n📋 Test 2: Supported Languages")
print("-" * 70)
print(f"Total languages supported: {len(lang_manager.languages)}")
print("\nLanguage List:")
for code, info in lang_manager.languages.items():
    print(f"  • {info['name']} ({info['name_en']}) - Code: {code}")
    print(f"    TTS: {info['tts_code']}, STT: {info['stt_code']}")

# Test 3: Common phrases in all languages
print("\n📋 Test 3: Common Phrases")
print("-" * 70)
test_langs = ['hi', 'en', 'mr', 'ta', 'te', 'gu', 'bn']

for lang_code in test_langs:
    print(f"\n{lang_manager.get_language_name(lang_code)}:")
    print(f"  Greeting: {lang_manager.get_phrase('greeting', lang_code)[0]}")
    print(f"  Goodbye: {lang_manager.get_phrase('goodbye', lang_code)[0]}")
    print(f"  Listening: {lang_manager.get_phrase('listening', lang_code)}")
    print(f"  Error: {lang_manager.get_phrase('error', lang_code)}")

# Test 4: Language detection
print("\n📋 Test 4: Language Detection")
print("-" * 70)

test_commands = [
    "हिंदी में बोलो",
    "change to english",
    "मराठी में बात करो",
    "tamil la pesungal",
    "telugu lo matladandi",
    "gujarati ma bolo",
    "bengali te bolo"
]

for command in test_commands:
    detected = lang_manager.detect_language(command)
    print(f"Command: '{command}'")
    print(f"  Detected: {lang_manager.get_language_name(detected)} ({detected})")

# Test 5: Language switching
print("\n📋 Test 5: Language Switching")
print("-" * 70)

test_switches = [
    "अंग्रेजी में बोलो",
    "मराठी में बदलो",
    "हिंदी में वापस आओ"
]

for command in test_switches:
    is_switch, new_lang = handle_language_command(command)
    if is_switch:
        print(f"✅ '{command}' → Switch to {lang_manager.get_language_name(new_lang)}")
    else:
        print(f"❌ '{command}' → Not a language switch command")

# Test 6: Translation (if Gemini API is available)
if lang_manager.model:
    print("\n📋 Test 6: Translation Test")
    print("-" * 70)
    
    test_text = "आज मौसम बहुत अच्छा है।"
    print(f"Original (Hindi): {test_text}\n")
    
    translate_to = ['en', 'mr', 'ta', 'te', 'gu']
    
    for target_lang in translate_to:
        lang_name = lang_manager.get_language_name(target_lang)
        print(f"Translating to {lang_name}...", end=" ")
        
        translated, error = lang_manager.translate_text(
            test_text, 
            target_lang=target_lang,
            source_lang='hi'
        )
        
        if error:
            print(f"❌ Error: {error}")
        else:
            print(f"✅")
            print(f"  {translated}")
    
    # Test reverse translation
    print("\n" + "-" * 70)
    print("Testing reverse translation (English to Hindi):")
    
    english_text = "The weather is very nice today."
    print(f"Original (English): {english_text}")
    
    hindi_translation, error = lang_manager.translate_text(
        english_text,
        target_lang='hi',
        source_lang='en'
    )
    
    if not error:
        print(f"Hindi: {hindi_translation}")
    
else:
    print("\n📋 Test 6: Translation Test")
    print("-" * 70)
    print("⚠️  Skipped - Gemini API not configured")

# Test 7: Voice Output (optional - comment out if you don't want audio)
print("\n📋 Test 7: Voice Output Test")
print("-" * 70)
print("Testing voice output in different languages...")
print("(You can skip this by pressing Ctrl+C)\n")

try:
    import time
    
    test_voice_langs = ['hi', 'en', 'mr']
    
    for lang_code in test_voice_langs:
        lang_name = lang_manager.get_language_name(lang_code)
        greeting = lang_manager.get_phrase('greeting', lang_code)[0]
        tts_code = lang_manager.get_tts_code(lang_code)
        
        print(f"🔊 Speaking in {lang_name}: {greeting}")
        bolo_stream(greeting, lang=tts_code)
        time.sleep(1)
    
    print("\n✅ Voice output test complete!")
    
except KeyboardInterrupt:
    print("\n⏭️  Voice test skipped by user")
except Exception as e:
    print(f"\n⚠️  Voice test error: {e}")

# Summary
print("\n" + "=" * 70)
print("✅ Multi-Language Support Test Complete!")
print("=" * 70)

print("\n📊 Summary:")
print(f"  • Total languages: {len(lang_manager.languages)}")
print(f"  • Gemini API: {'✅ Configured' if lang_manager.model else '❌ Not configured'}")
print(f"  • Translation: {'✅ Available' if lang_manager.model else '❌ Not available'}")
print(f"  • Current language: {lang_manager.get_language_name()}")

print("\n🎯 Usage in Vaani:")
print("  User can say:")
print("    • 'हिंदी में बोलो' - Switch to Hindi")
print("    • 'Change to English' - Switch to English")
print("    • 'मराठी में बात करो' - Switch to Marathi")
print("    • 'Tamil la pesungal' - Switch to Tamil")
print("    • And more...")

print("\n💡 Next Steps:")
if not lang_manager.model:
    print("  1. Add GEMINI_API_KEY to .env file for translation")
    print("  2. Restart the application")
else:
    print("  1. Run main.py to test with voice commands")
    print("  2. Try switching languages during conversation")
    print("  3. Ask questions in different languages")

print("\n" + "=" * 70)
