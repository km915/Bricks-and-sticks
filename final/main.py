import tkinter as tk
import subprocess
import sys

# Function to start the game at a specific difficulty
def start_game(difficulty):
    if difficulty == "easy":
        subprocess.Popen([sys.executable, "normal mode.py"])
    elif difficulty == "hard":
        subprocess.Popen([sys.executable, "hard mode.py"])
    root.destroy()  # Closes the menu window after launching the game

# Function to quit the game
def quit_game():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Game Menu")
root.geometry("600x380")

# Create the buttons
easy_button = tk.Button(root, text="Easy", command=lambda: start_game("easy"), width=50, height=4)
easy_button.pack(pady=20)

hard_button = tk.Button(root, text="Hard", command=lambda: start_game("hard"), width=50, height=4)
hard_button.pack(pady=20)

quit_button = tk.Button(root, text="Quit", command=quit_game, width=50, height=4)
quit_button.pack(pady=20)


# Run the tkinter loop
root.mainloop()
