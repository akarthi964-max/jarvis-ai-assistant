"""
JARVIS - STEP 3: Voice Input + Voice Output
Now YOU speak to JARVIS and JARVIS responds with voice!
"""

import requests
import pyttsx3
import speech_recognition as sr

print("="*60)
print("🤖 JARVIS - Voice Input & Output")
print("="*60)
print()

# Initialize text-to-speech engine
print("🔊 Initializing voice engine...")
engine = pyttsx3.init()
engine.setProperty('rate', 150)      # Speed of speech
engine.setProperty('volume', 0.9)    # Loudness
print("✓ Voice engine ready!\n")

# Initialize speech recognition
print("🎤 Initializing microphone...")
recognizer = sr.Recognizer()
print("✓ Microphone ready!\n")

# Function to make JARVIS speak
def speak(text):
    """Make JARVIS say something"""
    print(f"🤖 JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to listen to user
def listen():
    """Listen to the user and convert speech to text"""
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...\n")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        # Convert audio to text
        text = recognizer.recognize_google(audio)
        print(f"👤 You said: {text}\n")
        return text.lower()
    
    except sr.UnknownValueError:
        print("❌ Could not understand. Please speak clearly.\n")
        return None
    except sr.RequestError as e:
        print(f"❌ Error: {e}\n")
        return None
    except Exception as e:
        print(f"❌ Listening error: {e}\n")
        return None

# Function to get a joke
def get_joke():
    try:
        response = requests.get('https://official-joke-api.appspot.com/random_joke')
        if response.status_code == 200:
            data = response.json()
            return data['setup'], data['punchline']
        else:
            return None, None
    except:
        return None, None

# Function to get current time
def get_time():
    from datetime import datetime
    return datetime.now().strftime("%I:%M %p")

# Main conversation loop
speak("Hello sir. I am JARVIS. I can tell you jokes, the time, or chat with you.")

while True:
    # Listen to user
    command = listen()
    
    if not command:
        continue
    
    # Check if user wants to exit
    if any(word in command for word in ['exit', 'quit', 'bye', 'goodbye', 'stop']):
        speak("Goodbye sir. Have a great day!")
        print("\n✓ JARVIS shutting down...\n")
        break
    
    # Check if user wants a joke
    elif any(word in command for word in ['joke', 'funny', 'laugh', 'humor']):
        speak("Let me fetch a joke for you.")
        setup, punchline = get_joke()
        
        if setup and punchline:
            print(f"📖 Setup: {setup}\n")
            speak(setup)
            print("⏸️  (pause for effect)\n")
            print(f"😂 Punchline: {punchline}\n")
            speak(punchline)
        else:
            speak("Sorry, I could not fetch a joke.")
    
    # Check if user wants to know the time
    elif any(word in command for word in ['time', 'what time', 'current time']):
        current_time = get_time()
        speak(f"The current time is {current_time}")
    
    # Check if user is greeting
    elif any(word in command for word in ['hello', 'hi', 'hey']):
        speak("Hello sir. How can I help you?")
    
    # Check if user wants help
    elif any(word in command for word in ['help', 'what can you do']):
        help_text = "I can tell you jokes, the time, and chat with you. Just speak naturally."
        speak(help_text)
    
    # For other commands
    else:
        speak(f"You said: {command}. I'm still learning. Try asking for a joke or the time.")

print("="*60)
