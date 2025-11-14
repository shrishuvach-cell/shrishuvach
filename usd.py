import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

# Sample consistent historical data (year and exchange rate)
# For complete analysis, replace with full dataset of equal length
data = {
    'Year': [1947, 1957, 1967, 1977, 1987, 1997, 2007, 2017, 2024],
    'INR_per_USD': [3.3, 4.76, 7.5, 8.74, 13.92, 36.31, 41.35, 67.79, 84.83]
}

df = pd.DataFrame(data)

def on_move(event):
    if event.inaxes:
        x, y = event.xdata, event.ydata
        nearest_idx = ((df['Year'] - int(x)).abs()).idxmin()
        year = df.loc[nearest_idx, 'Year']
        rate = df.loc[nearest_idx, 'INR_per_USD']
        annot.set_text(f'Year: {year}\nRate: {rate:.2f}')
        annot.xy = (year, rate)
        annot.set_visible(True)
        canvas.draw_idle()
    else:
        annot.set_visible(False)
        canvas.draw_idle()

root = tk.Tk()
root.title("INR to USD Exchange Rate (Sample)")

fig, ax = plt.subplots(figsize=(8,5))
ax.plot(df['Year'], df['INR_per_USD'], marker='o', linestyle='-', color='blue')
ax.set_xlabel('Year')
ax.set_ylabel('INR per USD')
ax.set_title('INR to USD Exchange Rate (Sample Data)')
ax.grid(True)

annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

fig.canvas.mpl_connect('motion_notify_event', on_move)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root.mainloop()
