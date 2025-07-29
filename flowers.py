import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import random

def draw_flower(ax):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')

    # --- Stem (behind) ---
    ax.plot([0, 0], [0, 5], color='green', linewidth=4, zorder=1)

    # --- Leaves (start from stem) ---
    num_leaves = random.randint(1, 5)
    for _ in range(num_leaves):
        base_y = random.uniform(1, 4.5)
        direction = random.choice([-1, 1])  # left or right
        angle = direction * random.uniform(np.pi / 6, np.pi / 3)
        length = random.uniform(0.8, 1.2)
        width = random.uniform(0.3, 0.5)

        t = np.linspace(0, 2 * np.pi, 100)
        x = length * (np.cos(t) - 1)  # shift so base starts at stem (x=0)
        y_leaf = width * np.sin(t)

        x_rot = x * np.cos(angle) - y_leaf * np.sin(angle)
        y_rot = x * np.sin(angle) + y_leaf * np.cos(angle)

        ax.fill(x_rot, y_rot + base_y, color='green', zorder=2)

    # --- Petals ---
    num_petals = random.randint(6, 20)
    petal_color = np.random.rand(3,)
    petal_length = random.uniform(1.5, 2.5)
    petal_width = random.uniform(0.5, 0.8)

    for i in range(num_petals):
        angle = 2 * np.pi * i / num_petals
        t = np.linspace(0, 2 * np.pi, 100)
        x = petal_length * np.cos(t)
        y = petal_width * np.sin(t)
        x_rot = x * np.cos(angle) - y * np.sin(angle)
        y_rot = x * np.sin(angle) + y * np.cos(angle)
        ax.fill(x_rot, y_rot + 5, color=petal_color, alpha=0.7, zorder=3)

    # --- Center ---
    ax.plot(0, 5, marker='o', markersize=12, color='yellow', zorder=4)

def generate_flower():
    draw_flower(ax)
    canvas.draw()

# --- GUI Setup ---
root = tk.Tk()
root.title("Random Flower Generator")
root.geometry("600x800")  # Ensure enough space

# Frame to hold everything vertically
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Canvas frame (top part)
canvas_frame = tk.Frame(main_frame)
canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Button frame (bottom part)
button_frame = tk.Frame(main_frame)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Matplotlib Figure and Canvas
fig, ax = plt.subplots(figsize=(5, 7))
canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Generate button
btn = ttk.Button(button_frame, text="Generate New Flower", command=generate_flower)
btn.pack(pady=10)

# Draw initial flower
generate_flower()

# Start GUI
root.mainloop()
