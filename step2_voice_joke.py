"""
JARVIS - STEP 2: Joke Teller with Voice (Text-to-Speech)
Now JARVIS will SPEAK the joke out loud!
"""

import requests
import pyttsx3

print("="*60)
print("🤖 JARVIS - Joke Teller with Voice")
print("="*60)
print()

# Initialize text-to-speech engine
# This makes the computer speak
print("🔊 Initializing voice engine...")
engine = pyttsx3.init()
engine.setProperty('rate', 150)      # Speed of speech
engine.setProperty('volume', 0.9)    # Loudness (0.0 to 1.0)
print("✓ Voice engine ready!\n")

# Function to make JARVIS speak
def speak(text):
    """Make JARVIS say something"""
    print(f"🤖 JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to get a joke from internet
def get_joke():
    try:
        # Ask the joke website for a joke
        response = requests.get('https://official-joke-api.appspot.com/random_joke')
        
        # If successful, get the data
        if response.status_code == 200:
            data = response.json()
            setup = data['setup']
            punchline = data['punchline']
            return setup, punchline
        else:
            return None, None
    except:
        return None, None

# Main program
speak("Hello sir. Let me get you a funny joke.")

print("\nFetching a joke...\n")

setup, punchline = get_joke()

if setup and punchline:
    print(f"📖 Setup: {setup}\n")
    speak(setup)
    
    print("⏸️  (pause for effect)\n")
    
    print(f"😂 Punchline: {punchline}\n")
    speak(punchline)
    
    print()
    speak("I hope you enjoyed that joke!")
    
else:
    speak("Sorry, I could not fetch a joke. Please check your internet connection.")

print()
