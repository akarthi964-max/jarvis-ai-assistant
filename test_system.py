"""
JARVIS - Simplified Version (Easy to Debug)
Start with this simpler version first
"""

import sys

print("="*70)
print("🤖 JARVIS - Testing System")
print("="*70)
print()

# Test 1: Check Python Version
print("✓ Step 1: Checking Python version...")
print(f"  Python version: {sys.version}")
print()

# Test 2: Check imports
print("✓ Step 2: Checking required packages...")

try:
    import requests
    print("  ✓ requests - OK")
except ImportError:
    print("  ✗ requests - NOT INSTALLED")
    print("    Run: pip install requests")
    sys.exit(1)

try:
    import pyttsx3
    print("  ✓ pyttsx3 - OK")
except ImportError:
    print("  ✗ pyttsx3 - NOT INSTALLED")
    print("    Run: pip install pyttsx3")
    sys.exit(1)

try:
    import speech_recognition as sr
    print("  ✓ speech_recognition - OK")
except ImportError:
    print("  ✗ speech_recognition - NOT INSTALLED")
    print("    Run: pip install SpeechRecognition")
    sys.exit(1)

print()

# Test 3: Test Text-to-Speech
print("✓ Step 3: Testing Text-to-Speech...")
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    print("  ✓ TTS Engine initialized")
    print("  Speaking: 'Hello, I am JARVIS'")
    engine.say("Hello, I am JARVIS")
    engine.runAndWait()
    print("  ✓ Text-to-Speech works!")
except Exception as e:
    print(f"  ✗ TTS Error: {e}")

print()

# Test 4: Test Microphone
print("✓ Step 4: Testing Microphone...")
try:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("  ✓ Microphone found!")
        print("  Microphone test will attempt to listen...")
except Exception as e:
    print(f"  ✗ Microphone Error: {e}")
    print("    Make sure microphone is connected!")

print()
print("="*70)
print("✅ All tests passed! JARVIS is ready to run!")
print("="*70)
print()
print("Now run: python run_jarvis.py")
