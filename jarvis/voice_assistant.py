"""
JARVIS AI Assistant with Voice Input/Output
Random Joke Generator with Voice Interaction
Uses Google Speech Recognition and Text-to-Speech (no PyAudio required)
"""

import requests
import json
from typing import Dict, Optional
import pyttsx3
import speech_recognition as sr
from datetime import datetime

class JokeGenerator:
    """Generate random jokes from various external APIs"""
    
    # API endpoints
    APIS = {
        'jokeapi': 'https://v2.jokeapi.dev/joke/Any',
        'uselessfacts': 'https://uselessfacts.jscinc.org/random.json',
        'official_joke_api': 'https://official-joke-api.appspot.com/random_joke',
        'dad_jokes': 'https://icanhazdadjoke.com/'
    }
    
    @staticmethod
    def get_joke_from_jokeapi() -> Optional[Dict]:
        """
        Fetch a joke from JokeAPI
        Returns: Dictionary with 'setup' and 'delivery' or 'joke'
        """
        try:
            response = requests.get(JokeGenerator.APIS['jokeapi'], timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data['type'] == 'twopart':
                return {
                    'source': 'JokeAPI',
                    'type': 'twopart',
                    'setup': data['setup'],
                    'delivery': data['delivery']
                }
            else:
                return {
                    'source': 'JokeAPI',
                    'type': 'single',
                    'joke': data['joke']
                }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from JokeAPI: {e}")
            return None
    
    @staticmethod
    def get_joke_from_official_api() -> Optional[Dict]:
        """
        Fetch a joke from Official Joke API
        Returns: Dictionary with 'setup' and 'punchline'
        """
        try:
            response = requests.get(JokeGenerator.APIS['official_joke_api'], timeout=5)
            response.raise_for_status()
            data = response.json()
            
            return {
                'source': 'Official Joke API',
                'type': 'twopart',
                'setup': data['setup'],
                'punchline': data['punchline']
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from Official Joke API: {e}")
            return None
    
    @staticmethod
    def get_dad_joke() -> Optional[Dict]:
        """
        Fetch a dad joke from icanhazdadjoke
        Returns: Dictionary with 'joke'
        """
        try:
            response = requests.get(
                JokeGenerator.APIS['dad_jokes'],
                headers={'Accept': 'application/json'},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'source': 'Dad Jokes API',
                'type': 'single',
                'joke': data['joke']
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from Dad Jokes API: {e}")
            return None
    
    @staticmethod
    def get_random_joke() -> Optional[Dict]:
        """
        Fetch a random joke from any available API
        Returns: Dictionary with joke data or None if all APIs fail
        """
        apis = [
            JokeGenerator.get_joke_from_jokeapi,
            JokeGenerator.get_joke_from_official_api,
            JokeGenerator.get_dad_joke
        ]
        
        for api_func in apis:
            joke = api_func()
            if joke:
                return joke
        
        return None
    
    @staticmethod
    def format_joke(joke: Dict) -> str:
        """Format joke data into readable string"""
        if not joke:
            return "Sorry, couldn't fetch a joke at this moment. Try again later!"
        
        source = joke.get('source', 'Unknown Source')
        
        if joke.get('type') == 'twopart':
            setup = joke.get('setup') or joke.get('setup', '')
            delivery = joke.get('delivery') or joke.get('punchline', '')
            return f"[{source}]\n\n{setup}\n\n{delivery}"
        else:
            joke_text = joke.get('joke', '')
            return f"[{source}]\n\n{joke_text}"


class VoiceAssistant:
    """Voice-enabled AI Assistant"""
    
    def __init__(self):
        """Initialize text-to-speech engine"""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        self.recognizer = sr.Recognizer()
        self.joke_generator = JokeGenerator()
    
    def speak(self, text: str):
        """Convert text to speech and speak it"""
        print(f"\n🤖 JARVIS: {text}\n")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self) -> Optional[str]:
        """
        Listen to microphone input and convert to text
        Returns: Recognized text or None if failed
        """
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...\n")
                audio = self.recognizer.listen(source, timeout=5)
            
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You said: {text}\n")
            return text.lower()
        
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError as e:
            self.speak(f"Could not reach the speech recognition service: {e}")
            return None
        except sr.Timeout:
            self.speak("Listening timed out. Please try again.")
            return None
    
    def process_command(self, command: str):
        """Process user command and respond"""
        if not command:
            return False
        
        # Exit commands
        if any(word in command for word in ['exit', 'quit', 'bye', 'goodbye', 'stop']):
            self.speak("Goodbye sir. Have a great day!")
            return False
        
        # Joke commands
        elif any(word in command for word in ['joke', 'funny', 'laugh', 'humor']):
            self.speak("Let me fetch a joke for you.")
            joke = self.joke_generator.get_random_joke()
            formatted_joke = self.joke_generator.format_joke(joke)
            print(formatted_joke)
            
            # Extract and speak the joke
            if joke:
                if joke.get('type') == 'twopart':
                    setup = joke.get('setup') or joke.get('setup', '')
                    delivery = joke.get('delivery') or joke.get('punchline', '')
                    self.speak(setup)
                    self.speak(delivery)
                else:
                    joke_text = joke.get('joke', '')
                    self.speak(joke_text)
            return True
        
        # Time command
        elif any(word in command for word in ['time', 'what time', 'current time']):
            current_time = datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")
            return True
        
        # Greeting commands
        elif any(word in command for word in ['hello', 'hi', 'hey', 'greet']):
            self.speak("Hello sir. How can I assist you today?")
            return True
        
        # Help command
        elif any(word in command for word in ['help', 'what can you do', 'capabilities']):
            help_text = """I can help you with the following:
            - Tell you jokes or funny stories
            - Tell you the current time
            - Respond to greetings
            - Exit when you ask me to quit
            Just speak naturally and I'll do my best to help!"""
            self.speak(help_text)
            return True
        
        else:
            self.speak(f"I received your command: {command}. I'm still learning. Please ask me for a joke, the time, or say hello!")
            return True
    
    def run(self):
        """Main voice assistant loop"""
        self.speak("Hello sir. I am JARVIS, your voice assistant. How can I help you today?")
        
        while True:
            command = self.listen()
            if command is None:
                continue
            
            should_continue = self.process_command(command)
            if not should_continue:
                break


def main():
    """Main function to run JARVIS Voice Assistant"""
    print("\n" + "="*60)
    print("🤖 JARVIS - Voice-Enabled AI Assistant 🤖")
    print("="*60)
    print("\nInitializing JARVIS...\n")
    
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"Error initializing JARVIS: {e}")
        print("\nNote: Make sure you have:")
        print("  - Microphone connected to your system")
        print("  - Internet connection for speech recognition")
        print("  - Required packages installed (see requirements.txt)")


if __name__ == "__main__":
    main()
