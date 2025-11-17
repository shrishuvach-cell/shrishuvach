import tkinter as tk
from tkinter import ttk
import time
import math
from PIL import Image, ImageDraw, ImageTk

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital / Analog Clock Toggle")

        self.mode = tk.StringVar(value="digital")

        # Toggle button to switch clock type
        toggle_frame = ttk.Frame(root)
        toggle_frame.pack(pady=10)

        ttk.Radiobutton(toggle_frame, text="Digital", variable=self.mode, value="digital", command=self.update_display).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(toggle_frame, text="Analog", variable=self.mode, value="analog", command=self.update_display).pack(side=tk.LEFT, padx=5)

        # Digital clock label
        self.digital_label = ttk.Label(root, font=("Helvetica", 40))
        self.digital_label.pack()

        # Analog clock canvas variables
        self.canvas_size = 300
        self.center = self.canvas_size // 2
        self.clock_radius = self.center - 10
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        self.clock_image = None

        # Start the clock update loop
        self.update_clock()

    def update_clock(self):
        current_time = time.localtime()
        if self.mode.get() == "digital":
            self.canvas.pack_forget()
            self.digital_label.pack()
            time_str = time.strftime("%H:%M:%S", current_time)
            self.digital_label.config(text=time_str)
        else:
            self.digital_label.pack_forget()
            self.canvas.pack()
            self.draw_analog_clock(current_time)
        self.root.after(1000, self.update_clock)

    def update_display(self):
        # Called when toggle changes - forces updating the display
        if self.mode.get() == "digital":
            self.canvas.pack_forget()
            self.digital_label.pack()
        else:
            self.digital_label.pack_forget()
            self.canvas.pack()

    def draw_analog_clock(self, current_time):
        # Create blank image with white background
        image = Image.new("RGB", (self.canvas_size, self.canvas_size), "white")
        draw = ImageDraw.Draw(image)

        # Draw clock circle
        draw.ellipse((10, 10, self.canvas_size - 10, self.canvas_size - 10), outline="black", width=4)

        # Draw hour marks
        for i in range(12):
            angle = math.pi/6 * i  # 30 degrees per hour
            x_start = self.center + (self.clock_radius - 20) * math.sin(angle)
            y_start = self.center - (self.clock_radius - 20) * math.cos(angle)
            x_end = self.center + self.clock_radius * math.sin(angle)
            y_end = self.center - self.clock_radius * math.cos(angle)
            draw.line((x_start, y_start, x_end, y_end), fill="black", width=3)

        # Calculate angles for hands
        sec = current_time.tm_sec
        min = current_time.tm_min + sec / 60.0
        hr = (current_time.tm_hour % 12) + min / 60.0

        angle_sec = math.pi/30 * sec
        angle_min = math.pi/30 * min
        angle_hr = math.pi/6 * hr

        # Hand lengths
        len_sec = self.clock_radius - 30
        len_min = self.clock_radius - 40
        len_hr = self.clock_radius - 70

        # Second hand (red)
        x_sec = self.center + len_sec * math.sin(angle_sec)
        y_sec = self.center - len_sec * math.cos(angle_sec)
        draw.line((self.center, self.center, x_sec, y_sec), fill="red", width=1)

        # Minute hand (blue)
        x_min = self.center + len_min * math.sin(angle_min)
        y_min = self.center - len_min * math.cos(angle_min)
        draw.line((self.center, self.center, x_min, y_min), fill="blue", width=4)

        # Hour hand (black)
        x_hr = self.center + len_hr * math.sin(angle_hr)
        y_hr = self.center - len_hr * math.cos(angle_hr)
        draw.line((self.center, self.center, x_hr, y_hr), fill="black", width=6)

        # Center dot
        draw.ellipse((self.center-5, self.center-5, self.center+5, self.center+5), fill="black")

        # Convert to PhotoImage and display on Tkinter canvas
        self.clock_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.clock_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()
