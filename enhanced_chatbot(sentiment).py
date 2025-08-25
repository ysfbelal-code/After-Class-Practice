import textblob

user_name = input("Hello! What's your name? ")
print(f"Nice to meet you {user_name}!")

user_feeling = input("How are you feeling today? ").lower()
blob = textblob.TextBlob(user_feeling)
sentiment = blob.sentiment.polarity

if sentiment > 0:
    print("I'm glad to hear that!")
elif sentiment < 0:
    print("That's sad. Hope you feel better soon!")
else:
    print("I see. Sometimes we can't express our emotions using words.")

user_option = input('Do you wish to continue or exit? ').lower()

if user_option == 'continue':
    user_hobbies = input('What are your hobbies? ')
    print("That's very interesting.")

    user_musicGenres = input('What are your favourite music genres? ')
    print('Really? I love those genres!')

    print(f"It was nice to chat with you {user_name}. Goodbye!")

elif user_option == 'exit':
    print(f"It was nice to chat with you {user_name}. Goodbye!")

else:
    user_option = input("You didn't enter either option. Do you wish to continue or exit? ").lower()