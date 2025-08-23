user_name = input("Hello! What's your name? ")
print(f"Nice to meet you {user_name}!")

user_feeling = input("How are you feeling today? ").lower()

if user_feeling == 'good':
    print("I'm glad to hear that!")
elif user_feeling == 'bad':
    print("That's sad. Hope you feel better soon!")
else:
    print("I see. Sometimes we can't express our emotions using words.")

user_option = input('Do you wish to continue or exit?')

if user_option == 'continue':
    user_hobbies = input('What are your hobbies? ')
    print("That's very interesting.")
else:
    print(f"It was nice to chat with you {user_name}. Goodbye!")
