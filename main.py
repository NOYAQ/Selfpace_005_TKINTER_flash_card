"""
Flash Card Game gets the most frequently used words in French from 'data/french_words.csv'
shows the first language(French) word on the screen and waits until the user presses
'x' or '✔' in 'card_flip_timer' for the first time then waits for any buttons to be pressed. 
If the user selects 'x', the code selects another word from the CSV file and 
keeps the word and asks later again. 
If the user selects '✔', the code selects another word from the CSV file and 
removes the word.
If the ''card_flip_timer' is elapsed before any user selection, the card flips and shows
English meaning of the French word.
"""
from tkinter import *
import pandas
import random

BG_COLOR = "#B1DDC6" # The main window background color code
current_card = {}
data_dict = {}  # stores the words that need to be learned. After the user knows the French word,
                # removes the word from the dictionary, otherwise keeps the word.
                
""" When the first start-up, there isn't any temporary CSV file, so using the initial 
CSV file to read and write back to the temporary CSV file. """
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    initial_data = pandas.read_csv("data/french_words.csv")
    data_dict = initial_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")

def keep_card():
    """
    The first cancels the 'card_flip_timer'.
    If the user selects 'x', keeps the word in the list but shows a different word.
    then starts 'card_flip_timer'.
    To avoid time losing a couple of milliseconds between the functions,
    the timer stops at the beginning of the function and then restarts end of the function.
    """
    global current_card
    global card_flip_timer
    main_window.after_cancel(card_flip_timer)
    current_card = random.choice(data_dict)
    main_canvas.itemconfig(card_background, image=card_front_image)
    main_canvas.itemconfig(card_language, text="French", fill="black")
    main_canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    card_flip_timer = main_window.after(2500, func=flip_to_english)
    
def flip_to_english():
    """
    Flips the card, shows the English meaning of the word and changes the background 
    and text colors
    """
    global current_card
    main_canvas.itemconfig(card_background, image=card_back_image)
    main_canvas.itemconfig(card_language, text="English", fill="white")
    main_canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    
def next_card():
    """
    If the user selects '✔', removes the word from the list and calls the 'keep_card' functions
    """
    global current_card
    data_dict.remove(current_card)
    data = pandas.DataFrame(data_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    keep_card()
       
main_window = Tk()
main_window.title("Flash Card Game")
main_window.config(padx=50, pady=50, bg=BG_COLOR)

card_flip_timer = main_window.after(2500, func=flip_to_english) # using for flipping card,
#if the user is not selected

main_canvas = Canvas(width=800, height=580)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_background = main_canvas.create_image(400, 270, image = card_front_image)
card_language = main_canvas.create_text(400, 200, text="Language", font=("Ariel", 40, "bold",))
card_word = main_canvas.create_text(400, 290, text="Word", font=("Ariel", 50, "italic"))
main_canvas.config(bg=BG_COLOR, highlightthickness=0)
main_canvas.grid(row=0, column=0, columnspan=2)

# 'x' button configuration and calls 'keep_card' function when it is pressed.
image_wrong = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=image_wrong, highlightbackground=BG_COLOR, command=keep_card)
button_wrong.grid(row=1, column=0)

# '✔' button configuration and calls 'next_card' function when it is pressed.
image_right = PhotoImage(file="images/right.png")
button_right =Button(image=image_right, highlightbackground=BG_COLOR, command=next_card)
button_right.grid(row=1, column=1)

keep_card() # gets a card for the initial start-up. 

main_window.mainloop()