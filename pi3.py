import mpmath
import tkinter as tk
import math

# Set precision for pi
mpmath.mp.dps = 1000
pi_val = str(mpmath.mp.pi)[2:]  # remove "3."

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
}

# Tkinter setup
root = tk.Tk()
root.title("Pi Digit Clock Thread with Colors")

canvas_size = 400
center_x = center_y = canvas_size // 2
radius = 150

canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg='white')
canvas.pack()

# Positions of digits 0-9 on the circle
positions = {}
for i in range(10):
    angle = 2 * math.pi * i / 10 - math.pi / 2  # start from top
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    positions[str(i)] = (x, y)
    # Draw digit circle
    canvas.create_oval(x-20, y-20, x+20, y+20, fill='lightgrey')
    # Draw digit text
    canvas.create_text(x, y, text=str(i), font=('Helvetica', 16, 'bold'))

# Variables to track animation and lines
index = 0
lines_drawn = []

def draw_thread():
    global index
    if index >= len(pi_val) - 1:
        return
    
    current_digit = pi_val[index]
    next_digit = pi_val[index + 1]
    start_pos = positions[current_digit]
    end_pos = positions[next_digit]

    # Draw line with color based on current digit
    color = digit_colors.get(current_digit, 'black')
    line = canvas.create_line(start_pos[0], start_pos[1], end_pos[0], end_pos[1], fill=color, width=2)
    lines_drawn.append(line)

    index += 1
    # Schedule next step
    root.after(1, draw_thread)

draw_thread()
root.mainloop()
