from textblob import TextBlob
import colorama
import time
from colorama import Fore, Style
import re

colorama.init()

conversation_history = []

def show_processing_animation():
    animation = "//-\\"
    for i in range(10):
        print(f"\r{Fore.YELLOW}Processing{Style.RESET_ALL} {animation[i % len(animation)]}", end="")
        time.sleep(0.5)
    print("\r", end="", flush=True)
 
def execute_command(command):
    global red_counter, green_counter, yellow_counter
    if command == "exit":
        print(f"{Fore.CYAN}Exiting Sentiment Spy. Farewell, Agent {user_name}!{Style.RESET_ALL}")
        return True
        print(f"{Fore.BLUE}Positive: {Style.RESET_ALL}{Fore.GREEN}{green_counter}{Style.RESET_ALL} \n"
        f"{Fore.BLUE}Negative: {Style.RESET_ALL}{Fore.RED}{red_counter}{Style.RESET_ALL} \n"
        f"{Fore.BLUE}Neutral: {Style.RESET_ALL}{Fore.YELLOW}{yellow_counter}{Style.RESET_ALL}")
    elif command == "reset":
        if conversation_history == []:
            print(f"{Fore.MAGENTA}No conversation history to delete.{Style.RESET_ALL}")
        else:
            conversation_history.clear()
            show_processing_animation()
            print(f"{Fore.YELLOW}All conversation history deleted.{Style.RESET_ALL}")
    elif command == "history":
        if not conversation_history:
            print(f"{Fore.MAGENTA}No conversation history yet.{Style.RESET_ALL}")
        else:
            red_counter = 0
            green_counter = 0
            yellow_counter = 0
            print(f"{Fore.YELLOW}Conversation History: {Style.RESET_ALL}")
            for idx, (text, polarity, sentiment_type) in enumerate(conversation_history, start=1):
                if sentiment_type == 'Positive':
                    color = Fore.GREEN
                    emoji = '😊'
                    green_counter += 1
                elif sentiment_type == 'Negative':
                    color = Fore.RED
                    emoji = '😞'
                    red_counter += 1
                else:
                    color = Fore.YELLOW
                    emoji = '😐'
                    yellow_counter += 1
                    
                print(f"{idx}. {color}{emoji} {text} " f"(Polarity: {polarity:.2f}, {sentiment_type}){Style.RESET_ALL}")
    elif command == 'summary':
        # compute counts on demand so summary works even if 'history' hasn't been run
        green_counter = sum(1 for _t, _p, s in conversation_history if s == "Positive")
        red_counter   = sum(1 for _t, _p, s in conversation_history if s == "Negative")
        yellow_counter= sum(1 for _t, _p, s in conversation_history if s == "Neutral")

        print(f"{Fore.BLUE}Positive: {Style.RESET_ALL}{Fore.GREEN}{green_counter}{Style.RESET_ALL} \n"
              f"{Fore.BLUE}Negative: {Style.RESET_ALL}{Fore.RED}{red_counter}{Style.RESET_ALL} \n"
              f"{Fore.BLUE}Neutral: {Style.RESET_ALL}{Fore.YELLOW}{yellow_counter}{Style.RESET_ALL}")

    elif command == 'help':
        print(f"{Fore.BLUE}Reset: resets all stored data.\nHistory: displays all previous messages.\n Summary: displays the sentiment analysis summary.\nHelp: lists available commands.\nExit: stops the program. {Style.RESET_ALL}")

def analyze_sentiment(text):
    show_processing_animation()
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.0:
        sentiment_type, color, emoji = 'Positive', Fore.GREEN, '😊'
    elif polarity < 0.0:
        sentiment_type, color, emoji = 'Negative', Fore.RED, '😞'
    else:
        sentiment_type, color, emoji = 'Neutral', Fore.YELLOW, '😐'

    conversation_history.append((text, polarity, sentiment_type))
    # print result before returning
    print(f"{color}{emoji} {sentiment_type} sentiment detected! (Polarity: {polarity:.2f}){Style.RESET_ALL}")
    return polarity, sentiment_type, color, emoji

def get_valid_name(user_name):
    if not user_name or not user_name.strip():
        return "Mystery Agent"
    name = user_name.strip()

    parts = user_name.split(r'[ -], name')
    if all(part.isalpha() for part in parts if part):
        return name
    else:
        print(f"{Fore.MAGENTA}Numbers are not allowed in the name. Setting name to 'Mystery Agent'.{Style.RESET_ALL}")
        user_name = "Mystery Agent"

user_name = input(f"{Fore.CYAN}Welcome to Sentiment Spy! Enter your name: {Style.RESET_ALL}").strip()

get_valid_name(user_name)

print(f"{Fore.GREEN}Hello, Agent {user_name}! Type a sentence and I will analyze its sentiment polarity using TextBlob. Commands: {Fore.YELLOW}reset, history, summary, exit, help.{Style.RESET_ALL}")

while True:
    user_input = input(f"{Fore.GREEN}>> {Style.RESET_ALL}").strip()
    
    if user_input.lower() == "exit":
        execute_command("exit")
        execute_command('summary')
        break
    elif user_input.lower() == "reset":
        execute_command("reset")
        continue
    elif user_input.lower() == "history":
        execute_command("history")
        continue
    elif user_input.lower() == "summary":
        execute_command("summary")
        continue
    elif user_input.lower() == "help":
        execute_command("help")
        continue
    elif not user_input:
        print(f"{Fore.MAGENTA}Please enter a sentence or valid command.{Style.RESET_ALL}")
        continue

    analyze_sentiment(user_input)