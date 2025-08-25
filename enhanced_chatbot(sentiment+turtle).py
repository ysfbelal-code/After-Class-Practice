import turtle
from textblob import TextBlob

window=turtle.Screen()
window.setup(width=1200,height=600)
window.title("Chatbot")

t1=turtle.Turtle()
t1.hideturtle()
t1.speed('fastest')
t1.pensize(5)
t1.pencolor('black')

t2=turtle.Turtle()
t2.hideturtle()
t2.speed('fastest')
t2.pensize(5)
t2.pencolor('grey')

t1.penup()
t1.goto(-50,200)
t2.penup()
t2.goto(50,200)
t1.right(90)
t2.right(90)

t1.align='right'
t2.align='left'

font = ("Arial",'15',"bold")

def write_up(message, turtle):
    turtle.write(message, align = turtle.align, font = font)
    turtle.forward(75)

def write(message):
    t1.write(message, align = t1.align, font = font)
    t1.forward(75)

def return_textinput(var):
    var = var.lower()
    return var

write_up("Hello! What's your name?", t1)
user_name = window.textinput('Chatbot', "Hello! What's your name?")
write_up(user_name, t2)

write_up(f"Nice to meet you, {user_name}!\nHow are you feeling today?", t1)
user_feeling = window.textinput('Chatbot', "How are you feeling today?")

if not user_feeling:  # user cancelled or empty
    write_up("No worries—tell me later.", t1)
else:
    # optional normalization
    user_feeling = user_feeling.strip()
    write_up(user_feeling, t2)
    polarity = TextBlob(user_feeling).sentiment.polarity

    if polarity >= 0.1:
        write_up("I'm glad to hear that!", t1)
    elif polarity <= -0.1:
        write_up("That's sad. Hope you feel better soon!", t1)
    else:
        write_up("I see. Sometimes we can't express our emotions using words.", t1)

user_option = window.textinput('Chatbot', 'Do you wish to continue or exit?').lower()
write_up(user_option, t2)

if user_option == 'continue':
    write_up('What are your hobbies?', t1)
    user_hobbies = window.textinput('Chatbot', 'What are your hobbies?')
    write_up(user_hobbies, t2)
    write_up("That's very interesting.\nWhat are your favourite music genres?", t1)
    user_musicGenres = window.textinput('Chatbot', 'What are your favourite music genres?')
    write_up(user_musicGenres, t2)
    write_up(f'Really? I love those genres!\nIt was nice to chat with you {user_name}. Goodbye!', t1)

elif user_option == 'exit':
    write(f"It was nice to chat with you {user_name}. Goodbye!")

else:
    user_option = window.textinput('Chatbot', "You didn't enter either option. Do you wish to continue or exit? ").lower()

window.mainloop()