"""
Test script to demonstrate terminal output feature
Shows how text is displayed before voice output
"""

from vaani.core.voice_tool import bolo_stream

print("=" * 60)
print("TERMINAL OUTPUT DEMONSTRATION")
print("=" * 60)
print()
print("This demonstrates how Vaani now shows all responses in the")
print("terminal BEFORE speaking them out loud.")
print()
print("=" * 60)
print()

# Test 1: Simple greeting
print("TEST 1: Simple Greeting")
print("-" * 60)
bolo_stream("नमस्ते! मैं वाणी हूँ। आपकी कैसे मदद कर सकती हूँ?", voice_style='default')
print()

# Test 2: Time response
print("TEST 2: Time Response")
print("-" * 60)
bolo_stream("अभी समय शाम के 5 बजकर 30 मिनट हैं।", voice_style='default')
print()

# Test 3: Weather response
print("TEST 3: Weather Response")
print("-" * 60)
bolo_stream("लखनऊ का मौसम: तापमान 28 डिग्री सेल्सियस है।", voice_style='default')
print()

# Test 4: News headline
print("TEST 4: News Headline")
print("-" * 60)
bolo_stream("आज की ताज़ा खबरें: प्रधानमंत्री ने नई योजना की घोषणा की।", voice_style='default')
print()

print("=" * 60)
print("DEMONSTRATION COMPLETE")
print("=" * 60)
print()
print("As you can see, each response is printed with:")
print("🔊 Vaani: [Response text]")
print()
print("This appears BEFORE the voice speaks, giving you:")
print("✓ Visual confirmation")
print("✓ Ability to read along")
print("✓ Easy debugging")
print("✓ Conversation logging")
print()
