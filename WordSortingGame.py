import tkinter as tk
from tkinter import messagebox
import random

# Load words from the file
with open('rarest_words.txt', 'r') as f:
    words = f.read().splitlines()

# Load known and unknown words
try:
    with open('known_words.txt', 'r') as f:
        known_words = f.read().splitlines()
except FileNotFoundError:
    known_words = []

try:
    with open('unknown_words.txt', 'r') as f:
        unknown_words = f.read().splitlines()
except FileNotFoundError:
    unknown_words = []

# Remove known and unknown words from the list of rarest words
words = [word for word in words if word not in known_words and word not in unknown_words]

def display_word():
    if words:
        global current_word
        current_word = random.choice(words)
        word_label.config(text=current_word)
    else:
        messagebox.showinfo("Game Over", "No more words left!")

def know_word():
    words.remove(current_word)
    if current_word not in known_words:
        known_words.append(current_word)
        with open('known_words.txt', 'a') as f:
            f.write(current_word + '\n')
    display_word()

def dont_know_word():
    words.remove(current_word)
    if current_word not in unknown_words:
        unknown_words.append(current_word)
        with open('unknown_words.txt', 'a') as f:
            f.write(current_word + '\n')
    display_word()

# Create the main window
root = tk.Tk()
root.title("Word Knowledge Game")

# Create and place widgets
word_label = tk.Label(root, text="", font=('Helvetica', 18))
word_label.pack(pady=20)

know_button = tk.Button(root, text="I know this word", command=know_word, font=('Helvetica', 14))
know_button.pack(pady=10)

dont_know_button = tk.Button(root, text="I don't know this word", command=dont_know_word, font=('Helvetica', 14))
dont_know_button.pack(pady=10)

# Display the first word
display_word()

# Run the application
root.mainloop()
