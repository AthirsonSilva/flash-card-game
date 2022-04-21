import tkinter as tk
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"

# Reading the database
try:
    database = pd.read_csv(
        filepath_or_buffer='projects/flash-card-game/data/words_to_learn.csv')

except FileNotFoundError:
    original_data = pd.read_csv(
        'projects/flash-card-game/data/english_words.csv')
    records = original_data.to_dict(orient='records')

else:
    records = database.to_dict(orient='records')

records = database.to_dict(orient='records')
words_to_learn = dict()
current_card = dict()


def next_card():
    '''
    Swap card

    Swap the card after a set period of time
    '''
    global records, word, current_card, flip_timer

    window.after_cancel(flip_timer)

    current_card = choice(records)

    canvas.itemconfig(title, text='English', fill='black')
    canvas.itemconfig(word, text=current_card['English'], fill='black')
    canvas.itemconfig(card_background, image=card_front_img)

    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    '''
    Flip card

    Flips the card after a set period of time
    '''
    from time import sleep
    global current_card

    sleep(1)

    canvas.itemconfig(title, text='Portuguese', fill='white')
    canvas.itemconfig(word, text=current_card['Portuguese'], fill='white')
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    '''
    Word checking

    Checks if the user already knows certain word and
    deletes it from the list of words to learn
    '''

    records.remove(current_card)
    data = pd.DataFrame(records)
    data.to_csv('projects/flash-card-game/data/words_to_learn.csv', index=False)

    next_card()


# UI setup
# Window
window = tk.Tk()
window.title('Flash card')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Getting the images
image_right = tk.PhotoImage(file='projects/flash-card-game/images/right.png')
image_left = tk.PhotoImage(file='projects/flash-card-game/images/wrong.png')
card_front_img = tk.PhotoImage(
    file='projects/flash-card-game/images/card_front.png')
card_back_img = tk.PhotoImage(
    file='projects/flash-card-game/images/card_back.png')

# Canvas
canvas = tk.Canvas(width=800, height=526,
                   bg=BACKGROUND_COLOR, highlightthickness=0)
card_background = canvas_image = canvas.create_image(
    400, 263, image=card_front_img)
canvas.grid(columnspan=2, column=0, row=0)

title = canvas.create_text(400, 150, text='Title',
                           font=('Arial', 40, 'italic'))
word = canvas.create_text(400, 263, text='Word', font=('Arial', 60, 'bold'))


# Buttons
right_btn = tk.Button(
    image=image_right, highlightthickness=0, command=is_known)
right_btn.grid(column=1, row=1, columnspan=1)

left_btn = tk.Button(image=image_left, highlightthickness=0, command=next_card)
left_btn.grid(columns=2, row=1, columnspan=1)

next_card()

window.mainloop()
