import streamlit as st
import re
import numpy as np
import matplotlib.pyplot as plt
import math
import time

st.set_page_config(page_title="AI Physics Visualizer", layout="centered")

st.title("AI Physics Word Problem Visualizer")
st.write("Enter any Physics word problem:")

problem = st.text_input(
    "Example: A car moves with a speed of 20 m/s for 10 seconds",
    "A ball is projected at 20 m/s at an angle of 45 degrees"
)

problem_lower = problem.lower()

# -------- Detect object --------
if "car" in problem_lower:
    obj = "car"
    symbol = "🚗"
elif "train" in problem_lower:
    obj = "train"
    symbol = "🚆"
elif "person" in problem_lower or "man" in problem_lower:
    obj = "person"
    symbol = "🧍"
else:
    obj = "ball"
    symbol = "⚽"

# -------- Extract numbers --------
numbers = list(map(float, re.findall(r"\d+", problem)))
velocity = numbers[0] if len(numbers) > 0 else 10
angle = numbers[1] if len(numbers) > 1 else 90
time_given = numbers[2] if len(numbers) > 2 else 5

g = st.slider("Gravity (m/s²)", 1.0, 20.0, 9.8)
speed = st.slider("Animation Speed", 0.01, 0.2, 0.05)

# -------- Detect motion type --------
if "projected" in problem_lower or "angle" in problem_lower:
    motion_type = "projectile"
elif "thrown" in problem_lower or "upward" in problem_lower:
    motion_type = "vertical"
elif "car" in problem_lower or "train" in problem_lower or "moves" in problem_lower:
    motion_type = "linear"
else:
    motion_type = "unknown"

# -------- AI Interpretation --------
st.subheader("AI Interpretation")
st.write(f"Detected object: **{obj}**")
st.write(f"Detected motion type: **{motion_type}**")
st.write(f"Velocity: **{velocity} m/s**")
st.write(f"Angle: **{angle} degrees**")

# -------- Create motion --------
if motion_type == "vertical":
    t = np.linspace(0, 2*velocity/g, 120)
    x = np.zeros_like(t)
    y = velocity*t - 0.5*g*t*t

elif motion_type == "projectile":
    theta = math.radians(angle)
    vx = velocity * math.cos(theta)
    vy = velocity * math.sin(theta)
    t = np.linspace(0, 2*vy/g, 120)
    x = vx * t
    y = vy*t - 0.5*g*t*t

elif motion_type == "linear":
    t = np.linspace(0, time_given, 120)
    x = velocity * t
    y = np.zeros_like(x)

else:
    st.warning("Unsupported problem type. Showing generic motion.")
    t = np.linspace(0, 5, 120)
    x = velocity * t
    y = np.zeros_like(x)

# -------- Scene Animation --------
fig, ax = plt.subplots()
placeholder = st.empty()

xmax = max(x) * 1.2 if max(x) > 0 else 5
ymax = max(y) * 1.2 if max(y) > 0 else 5

for i in range(len(t)):
    ax.clear()

    # Sky background
    ax.set_facecolor("#e6f2ff")

    # Ground
    ax.plot([0, xmax], [0, 0], linewidth=3)

    # Trail
    ax.plot(x[:i+1], y[:i+1], linewidth=2)

    # Emoji object
    ax.text(x[i], y[i], symbol, fontsize=25, ha='center', va='center')

    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("AI Generated Motion Scene")

    placeholder.pyplot(fig)
    time.sleep(speed)


