import mpmath
import tkinter as tk
from tkinter import scrolledtext

# Set precision for pi
mpmath.mp.dps = 1000
pi_val = str(mpmath.mp.pi)

# Define special colors for each digit 0-9
digit_colors = {
    '0': '#FF0000',  # Red
    '1': '#FF7F00',  # Orange
    '2': '#FFFF00',  # Yellow
    '3': '#7FFF00',  # Chartreuse
    '4': '#00FF00',  # Green
    '5': '#00FF7F',  # Spring Green
    '6': '#00FFFF',  # Cyan
    '7': '#007FFF',  # Azure
    '8': '#0000FF',  # Blue
    '9': '#7F00FF',  # Violet
    '.': '#000000',  # Black for decimal point
}

# Create Tkinter window
root = tk.Tk()
root.title("Pi to 1000 Digits with Colors")

# Create a scrolled text widget
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20)
text_area.pack(padx=10, pady=10)

# Add color tags for each digit
for digit, color in digit_colors.items():
    text_area.tag_configure(digit, foreground=color)

# Insert pi and apply color tags
for char in pi_val:
    if char in digit_colors:
        text_area.insert(tk.END, char, char)
    else:
        text_area.insert(tk.END, char)

# Disable editing
text_area.config(state=tk.DISABLED)

# Run the GUI application
root.mainloop()
