"""
JARVIS Main Controller - Always Listening
Continuously listens for wake word and processes commands
Run this file to start the complete JARVIS system
"""

import speech_recognition as sr
import pyttsx3
import threading
import time
from jarvis.voice_assistant import VoiceAssistant

class JARVISController:
    """Main controller for JARVIS - handles wake word detection and continuous listening"""
    
    def __init__(self):
        """Initialize the controller"""
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        self.is_active = False
        self.assistant = VoiceAssistant()
        self.wake_words = ['jarvis', 'hey jarvis', 'okay jarvis', 'jarvis listen']
    
    def speak(self, text: str):
        """Speak text"""
        print(f"\n🤖 JARVIS: {text}\n")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen_for_audio(self, timeout=10):
        """
        Listen for audio from microphone
        Returns: recognized text or None
        """
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("🎤 Listening...", end=" ", flush=True)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio)
            print(f"\n✓ Heard: '{text}'")
            return text.lower()
        
        except sr.UnknownValueError:
            print("\n✗ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"\n✗ API Error: {e}")
            return None
        except sr.Timeout:
            return None
    
    def is_wake_word(self, text: str) -> bool:
        """Check if text contains wake word"""
        if not text:
            return False
        return any(wake_word in text for wake_word in self.wake_words)
    
    def continuous_listen(self):
        """Continuously listen for wake word"""
        print("\n" + "="*70)
        print("🚀 JARVIS is now ACTIVE and LISTENING for wake words...")
        print("="*70)
        print("💡 TIP: Say 'Hey Jarvis' to wake me up!")
        print("   Then ask me anything!\n")
        
        attempt = 0
        while True:
            try:
                attempt += 1
                audio = self.listen_for_audio(timeout=5)
                
                if audio:
                    # Check for wake word
                    if self.is_wake_word(audio):
                        print("\n✅ JARVIS ACTIVATED!\n")
                        self.speak("Yes sir, I'm listening. What would you like?")
                        self.process_user_input()
                    else:
                        print(f"   (Waiting for wake word...)\n")
                
            except KeyboardInterrupt:
                print("\n\n🛑 JARVIS shutting down...")
                self.speak("Goodbye sir!")
                break
            except Exception as e:
                print(f"\n⚠️  Error: {e}")
                time.sleep(1)
                continue
    
    def process_user_input(self):
        """Process continuous user input until 'exit' command"""
        while True:
            try:
                command = self.listen_for_audio(timeout=8)
                
                if not command:
                    continue
                
                # Check for exit commands
                if any(word in command for word in ['exit', 'quit', 'bye', 'goodbye', 'stop', 'sleep']):
                    self.speak("Going back to sleep sir. Say hello when you need me again!")
                    break
                
                # Process the command
                print(f"\n⚙️  Processing: {command}")
                should_continue = self.assistant.process_command(command)
                
                if not should_continue:
                    break
                
                # Ask for next command
                self.speak("Anything else sir?")
                
            except KeyboardInterrupt:
                print("\n\n🛑 JARVIS shutting down...")
                self.speak("Goodbye sir!")
                break
            except Exception as e:
                print(f"\n⚠️  Error processing command: {e}")
                self.speak("Sorry sir, I encountered an error. Please try again.")
                continue


class SimpleJARVIS:
    """Simplified version - Direct interaction mode"""
    
    def __init__(self):
        self.assistant = VoiceAssistant()
    
    def run(self):
        """Run in interactive mode"""
        self.assistant.run()


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("🤖 JARVIS - Voice-Enabled AI Assistant Controller")
    print("="*70)
    print("\nSelect mode:")
    print("1. 🔊 Continuous Listening Mode (Wake word detection)")
    print("2. 🎤 Direct Interactive Mode (Start listening immediately)")
    print("3. ❌ Exit")
    print()
    
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice == "1":
        print("\n🔊 Starting Continuous Listening Mode...\n")
        controller = JARVISController()
        controller.continuous_listen()
    
    elif choice == "2":
        print("\n🎤 Starting Direct Interactive Mode...\n")
        simple = SimpleJARVIS()
        simple.run()
    
    elif choice == "3":
        print("\n👋 Goodbye!\n")
        return
    
    else:
        print("\n❌ Invalid choice. Please run again.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 JARVIS terminated.\n")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        print("Make sure you have:")
        print("  ✓ Microphone connected")
        print("  ✓ Internet connection")
        print("  ✓ All packages installed (pip install -r requirements.txt)")
