"""
JARVIS - STEP 1: Simple Joke Teller (No Voice Yet)
This is the easiest starting point
"""

import requests

print("="*60)
print("🤖 JARVIS - Simple Joke Teller")
print("="*60)
print()

# This function gets a joke from the internet
def get_joke():
    try:
        # We ask the joke website for a joke
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
print("Fetching a joke for you...\n")

setup, punchline = get_joke()

if setup and punchline:
    print(f"Setup: {setup}")
    print()
    print(f"Punchline: {punchline}")
    print()
    print("😂 Hope you laughed!")
else:
    print("Sorry, couldn't fetch a joke. Check your internet connection.")

print()
