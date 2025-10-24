"""
Test script to list available Gemini models and test connection
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    exit(1)

print(f"✅ API Key found: {api_key[:10]}...")

try:
    genai.configure(api_key=api_key)
    print("✅ API configured successfully")
    
    print("\n📋 Available Models:")
    print("-" * 50)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
    
    print("\n" + "=" * 50)
    print("🧪 Testing model with a simple question...")
    print("=" * 50)
    
    # Try to use the model
    test_models = [
        'gemini-2.5-flash',
        'gemini-flash-latest',
        'gemini-pro-latest',
        'gemini-2.5-pro',
        'gemini-2.0-flash'
    ]
    
    working_model = None
    for model_name in test_models:
        try:
            print(f"\nTrying: {model_name}...", end=" ")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say hello in Hindi")
            if response and response.text:
                print(f"✅ SUCCESS!")
                print(f"Response: {response.text[:100]}...")
                working_model = model_name
                break
        except Exception as e:
            print(f"❌ Failed: {str(e)[:50]}")
    
    if working_model:
        print(f"\n✅ Working model found: {working_model}")
        print(f"\nUpdate general_knowledge_service.py to use: '{working_model}'")
    else:
        print("\n❌ No working model found!")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPossible issues:")
    print("1. Invalid API key - Get a new one from https://aistudio.google.com/app/apikey")
    print("2. API not enabled - Make sure Generative Language API is enabled")
    print("3. Network issue - Check your internet connection")
