"""
Random Joke Generator using external APIs
Supports multiple joke APIs for variety
"""

import requests
import json
from typing import Dict, Optional

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


def main():
    """Main function to demonstrate the joke generator"""
    print("🤖 JARVIS Random Joke Generator 🤖")
    print("=" * 50)
    
    # Generate and display jokes
    for i in range(3):
        print(f"\nJoke #{i+1}:")
        print("-" * 50)
        joke = JokeGenerator.get_random_joke()
        formatted_joke = JokeGenerator.format_joke(joke)
        print(formatted_joke)
        print()


if __name__ == "__main__":
    main()
