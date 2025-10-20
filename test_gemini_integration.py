"""
Quick test for Gemini general knowledge integration
"""

from general_knowledge_service import get_gk_service, handle_general_knowledge_query
from Voice_tool import bolo_stream

# Test questions
test_questions = [
    "आसमान नीला क्यों है?",
    "बारिश कैसे होती है?",
    "पेड़ हरे क्यों होते हैं?",
    "चाँद पर क्या होता है?"
]

print("=" * 60)
print("🧪 Testing Gemini General Knowledge Integration")
print("=" * 60)

service = get_gk_service()

if not service.is_configured():
    print("\n❌ Gemini API is not configured!")
    print("Please check your GEMINI_API_KEY in .env file")
    exit(1)

print("\n✅ Gemini API is configured and ready!")
print("\n" + "=" * 60)

for i, question in enumerate(test_questions, 1):
    print(f"\n📝 Question {i}: {question}")
    print("-" * 60)
    
    # Get answer
    answer, error = service.ask_question(question)
    
    if error:
        print(f"❌ Error: {error}")
        continue
    
    if answer:
        print(f"✅ Answer:\n{answer}")
        print("\n🔊 Speaking the answer...")
        
        # Test voice output
        try:
            bolo_stream(answer, lang='hi')
            print("✅ Voice output successful!")
        except Exception as e:
            print(f"⚠️ Voice output failed: {e}")
    
    print("-" * 60)
    
    if i < len(test_questions):
        import time
        time.sleep(2)  # Pause between questions

print("\n" + "=" * 60)
print("✅ Test completed!")
print("=" * 60)
