from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card
    global flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# GUI
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer= window.after(3000, flip_card)

canvas = Canvas(window, width=800, height=526)
card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(highlightthickness=0, bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=2)

yes_img = PhotoImage(file="images/right.png")
yes_button = Button(image=yes_img, command=is_known)
yes_button.config(highlightthickness=0, borderwidth=0)
yes_button.grid(column=1, row=1)

no_img = PhotoImage(file="images/wrong.png")
no_button = Button(image=no_img, command=next_card)
no_button.config(highlightthickness=0, borderwidth=0)
no_button.grid(column=0, row=1)

next_card()
window.mainloop()