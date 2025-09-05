import re, random
import requests
from datetime import datetime
import pytz
from colorama import Fore, init

init(autoreset=True)

destinations = {
    "beaches": ['Bali', 'Maldives', 'Phuket'],
    'mountains': ['Swiss Alps', 'Kilimanjaro', 'Rocky Mountains'],
    'cities': ['Doha', 'Tokyo', 'Istanbul']
}
jokes = [
    "Why don't programmers like nature? Too many bugs!",
    "Why did the computer go to the doctor? Because it had a virus!", 
    "Why do travelers always feel warm? Because of all their hot spots!"
]
facts = [
    "The world’s longest commercial flight took around 30 hours.",
    "The shortest commercial flight takes less than two minutes.",
    "Sudan has more ancient pyramids than Egypt."
]

def normalize_input(text):
    return re.sub(r'\s+', '', text.strip().lower())

def reccommend():
    print(Fore.CYAN + f"Travel GPT: Beaches, mountains, or cities?")
    preference = input(Fore.WHITE + 'You: ')
    preference = normalize_input(preference)

    if preference in destinations:
        suggestion = random.choice(destinations[preference])
        print(Fore.GREEN + f"Travel GPT: How about {suggestion}?")
        print(Fore.CYAN+ f"Travel GPT: Do you like it? (yes/no)")
        answer = input(Fore.WHITE + 'You: ').lower()

    if answer == 'yes':
        print(Fore.GREEN + f'Travel GPT: Awesome! Enjoy {suggestion}!')
    elif answer == 'no':
        print(Fore.RED + f"Travel GPT: Let's try another.")
        reccommend()
    else:
        print(Fore.RED + f"Travel GPT: Sorry, I don't have that type of destination.")

    show_help()

def packing_tips():
    print(Fore.CYAN + f"Travel GPT: Where to?")
    location = normalize_input(input(Fore.WHITE + 'You: '))
    print(Fore.CYAN + f"Travel GPT: How many days?")
    days = input(Fore.WHITE + 'You: ')

    print(Fore.GREEN + f"Travel GPT: Packing tips for {days} days in {location}")
    print(Fore.GREEN + "- Pack versatile clothes.")
    print(Fore.GREEN + "- Bring chargers/adapters.")
    print(Fore.GREEN + "- Check the weather forecast.")

def local_time():
    Doha_timezone = pytz.timezone('Asia/Qatar') #access the timezone of the entered timezone (pytz timezone list is in this link: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)
    Doha = datetime.now(Doha_timezone) #gets the time of that timezone
    Istanbul_timezone = pytz.timezone('Asia/Istanbul')
    Istanbul = datetime.now(Istanbul_timezone)
    Tokyo_timezone = pytz.timezone('Asia/Tokyo')
    Tokyo = datetime.now(Tokyo_timezone)
    
    Tokyo_formatted = Tokyo.strftime('%H:%M') #formats the time to hours & minutes. Can be adjusted.
    Doha_formatted = Doha.strftime('%H:%M')
    Istanbul_formatted = Istanbul.strftime('%H:%M')

    print(Fore.CYAN + f"Travel GPT: Which city?")
    city = input(Fore.WHITE + "You: ") #NLP can be useful here. Different names for some cities in some languages.
    
    if not city:
        print(Fore.RED + f"You haven't entered anything. Which city?")
        city = normalize_input(input(Fore.WHITE + "You: "))

    elif city == 'Doha':
        print(Fore.CYAN + f"The time in Doha is {Doha_formatted}.")
    elif city == 'Istanbul':
        print(Fore.CYAN + f"The time in Istanbul is {Istanbul_formatted}.")
    elif city == 'Tokyo':
        print(Fore.CYAN + f"The time in Tokyo is {Tokyo_formatted}.")
    else:
        print(Fore.CYAN + f"Sorry. This city isn't on my database.")

def local_weather():
    print(Fore.CYAN + "Which city? (e.g. Tokyo or Tokyo,jp)")
    city = input(">> ").strip()
    if not city:
        print(Fore.MAGENTA + "No city provided.")
        return
    elif city not in [c for cities in destinations.values() for c in cities]:
        print(Fore.MAGENTA + f"This city isn't on my database. Please enter another city.")
        city = input(">> ").strip()
    else:
        api_key = "10e5e4506d144068bd72fb9958fefca4"  # gets api key to access OpenWeatherMap
        url = "https://api.openweathermap.org/data/2.5/weather" # goes to OpenWeatherMap
        
        params = {"q": city, "appid": api_key, "units": "metric"} # can set the units
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
        except requests.RequestException as e:
            print(Fore.MAGENTA + f"Network error: {e}") # prints the error
            return

        if response.status_code != 200:
            msg = data.get("message", f"HTTP {response.status_code}")
            print(Fore.MAGENTA + f"API error: {msg}") # prints the error
            return

        temp = data["main"]["temp"] # sets the temperature variable by getting values from the url
        print(Fore.GREEN + f"The temperature in {city} is {temp}°C.")

def tell_joke():
    print(Fore.YELLOW + f"Travel GPT: {random.choice(jokes)}")

def travel_facts():
    print(Fore.YELLOW + f"Travel GPT: {random.choice(facts)}")

def show_help():
    print(Fore.MAGENTA + "\nTravel GPT can:")
    print(Fore.MAGENTA + "- Suggest travel spots (say 'reccommendation')")
    print(Fore.MAGENTA + "- Offer packing tips (say 'packing')")
    print(Fore.MAGENTA + "- Tell a joke (say 'joke')")
    print(Fore.MAGENTA + "- Tell you the local time of cities (type 'time')")
    print(Fore.MAGENTA + "Type 'exit' or 'bye' to quit.\n")
    print(Fore.MAGENTA + "Tell you the local time of cities (say 'time')")
    print(Fore.MAGENTA + "Tell you the temperature of cities (say 'weather')")
    print(Fore.MAGENTA + "Tell you travel facts (say 'facts')")

def chat():
    print(Fore.CYAN + "Hello! I'm Travel GPT.")
    name = input(Fore.WHITE + "Your name? ")
    print(Fore.CYAN + f"Nice to meet you, {name}!")

    show_help()

    while True:
        user_input = input(Fore.WHITE + f"{name}: ") 
        user_input = normalize_input(user_input) # NLP can be very useful here

        if "reccommend" in user_input or "suggest" in user_input:
            reccommend()
        elif "pack" in user_input or "packing" in user_input:
            packing_tips()
        elif "joke" in user_input or "funny" in user_input:
            tell_joke()
        elif "help" in user_input:
            show_help()
        elif "exit" in user_input or "bye" in user_input:
            print(Fore.CYAN + f"Travel GPT: Safe travels, {name}!")
            break
        elif "time" in user_input:
            local_time()
        elif "weather" in user_input or "forecast" in user_input:
            local_weather()
        elif "facts" in user_input:
            travel_facts()
        else:
            print(Fore.RED + "Travel GPT: Could you rephrase that?")

if __name__ == "__main__":
    chat()