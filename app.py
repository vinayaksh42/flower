from flask import Flask, send_file, render_template_string, redirect, url_for
import matplotlib
matplotlib.use('Agg')  # <- add this line before importing pyplot

import matplotlib.pyplot as plt
import numpy as np
import random
from io import BytesIO


app = Flask(__name__)

def draw_flower():
    fig, ax = plt.subplots(figsize=(4, 6))
    ax.set_aspect('equal')
    ax.axis('off')

    # --- Stem (behind) ---
    ax.plot([0, 0], [0, 5], color='green', linewidth=4, zorder=1)

    # --- Leaves ---
    num_leaves = random.randint(1, 2)
    for _ in range(num_leaves):
        base_y = random.uniform(1, 4.5)
        direction = random.choice([-1, 1])
        angle = direction * random.uniform(np.pi / 6, np.pi / 3)
        length = random.uniform(0.8, 1.2)
        width = random.uniform(0.3, 0.5)

        t = np.linspace(0, 2 * np.pi, 100)
        x = length * (np.cos(t) - 1)
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

    # Save to image buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

# --- Flask Routes ---

@app.route("/")
def home():
    return render_template_string("""
        <html>
        <head><title>Random Flower Generator</title></head>
        <body style="text-align: center; font-family: Arial;">
            <h1>🌸 Random Flower Generator</h1>
            <p><a href="/flower"><button style="padding: 10px 20px;">Generate New Flower</button></a></p>
        </body>
        </html>
    """)

@app.route("/flower")
def flower():
    return render_template_string("""
        <html>
        <head><title>Your Flower</title></head>
        <body style="text-align: center; font-family: Arial;">
            <h2>Here is your random flower 🌼</h2>
            <img src="{{ url_for('flower_image') }}" alt="Random Flower" />
            <p><a href="/flower"><button>Generate Another</button></a></p>
            <p><a href="/"><button>Back to Home</button></a></p>
        </body>
        </html>
    """)

@app.route("/flower_image")
def flower_image():
    buf = draw_flower()
    return send_file(buf, mimetype='image/png')

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=8004)

