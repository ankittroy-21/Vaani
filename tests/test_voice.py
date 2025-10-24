# test_voice.py - Test the new news anchor voice

import sys
import os

print("🎤 Testing Vaani Voice Enhancement\n")
print("="*60)

# Check dependencies
print("\n1. Checking dependencies...")
try:
    from pydub import AudioSegment
    print("   ✅ pydub installed")
except ImportError:
    print("   ❌ pydub not found. Install with: pip install pydub")
    sys.exit(1)

try:
    import subprocess
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✅ ffmpeg installed")
    else:
        print("   ❌ ffmpeg not working properly")
except FileNotFoundError:
    print("   ❌ ffmpeg not found. Install with: choco install ffmpeg")
    print("   💡 Or download from: https://ffmpeg.org/download.html")
    sys.exit(1)

print("\n2. Testing Voice Module...")
try:
    from vaani.core.voice_tool import bolo_stream, apply_voice_effects
    print("   ✅ Voice module imported successfully")
except ImportError as e:
    print(f"   ❌ Import error: {e}")
    sys.exit(1)

print("\n3. Testing News Anchor Voice...")
print("   🔊 Playing sample text with news anchor voice...")
print("   (Listen for higher pitch, professional tone)")

try:
    sample_text = "नमस्ते, मैं वाणी हूँ। मैं आपकी आवाज सहायक हूँ।"
    bolo_stream(sample_text, voice_style='news_anchor')
    print("   ✅ News anchor voice test successful!")
except Exception as e:
    print(f"   ❌ Error: {e}")
    print("\n   Troubleshooting:")
    print("   - Make sure ffmpeg is in your PATH")
    print("   - Try: pip install --upgrade pydub")
    sys.exit(1)

print("\n4. Testing Original Voice (for comparison)...")
print("   🔊 Playing same text with original voice...")

try:
    bolo_stream(sample_text, voice_style='default')
    print("   ✅ Original voice test successful!")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n5. Testing News Reading Scenario...")
print("   🔊 Playing longer news text...")

news_sample = """आज की मुख्य खबरें। भारत में नई तकनीक का विकास हो रहा है। 
कृषि क्षेत्र में सुधार के लिए नई योजनाएं शुरू की गई हैं।"""

try:
    bolo_stream(news_sample, voice_style='news_anchor')
    print("   ✅ News reading test successful!")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("✅ All tests completed!")
print("\nVoice Characteristics:")
print("  • Pitch: Raised to female range (~240-280 Hz)")
print("  • Speed: 5% faster (news anchor pace)")
print("  • Volume: +2.5 dB (authoritative)")
print("  • Style: Professional news anchor")
print("\n💡 The voice now sounds like a female news anchor!")
print("\nNext steps:")
print("  1. Run: python main.py")
print("  2. Test with voice commands")
print("  3. Adjust settings in Voice_tool.py if needed")
print("  4. Read VOICE_ENHANCEMENT_GUIDE.md for customization")
print("="*60)
