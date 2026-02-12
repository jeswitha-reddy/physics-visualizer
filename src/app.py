import streamlit as st
import re
import numpy as np
import matplotlib.pyplot as plt
import math
import time

st.set_page_config(page_title="AI Physics Visualizer", layout="centered")
st.title("AI Physics Problem Visualizer")

problem = st.text_input(
    "Enter a physics problem:",
    "A ball is projected at 20 m/s at an angle of 45 degrees"
)

text = problem.lower()

# ---------- Object detection ----------
if "car" in text:
    obj = "car"
elif "train" in text:
    obj = "train"
elif "person" in text:
    obj = "person"
else:
    obj = "ball"

# ---------- Extract numbers ----------
nums = list(map(float, re.findall(r"\d+", text)))
v = nums[0] if len(nums) > 0 else 10
angle = nums[1] if len(nums) > 1 else 45
t_given = nums[2] if len(nums) > 2 else 5

g = st.slider("Gravity (m/s²)", 1.0, 20.0, 9.8)
speed = st.slider("Animation speed", 0.01, 0.2, 0.05)

# ---------- Motion type ----------
if "projected" in text or "angle" in text:
    motion = "projectile"
elif "moves" in text:
    motion = "linear"
else:
    motion = "linear"

st.subheader("AI Interpretation")
st.write(f"Object: **{obj}**")
st.write(f"Velocity: **{v} m/s**")
st.write(f"Angle: **{angle}°**")
st.write(f"Motion type: **{motion}**")

# ---------- Generate motion ----------
if motion == "projectile":
    theta = math.radians(angle)
    vx = v * math.cos(theta)
    vy = v * math.sin(theta)
    t = np.linspace(0, 2*vy/g, 120)
    x = vx * t
    y = vy*t - 0.5*g*t*t
else:
    t = np.linspace(0, t_given, 120)
    x = v * t
    y = np.zeros_like(x)

# ---------- Animation ----------
fig, ax = plt.subplots()
placeholder = st.empty()

xmax = max(x) * 1.2
ymax = max(y) * 1.2 + 1

for i in range(len(t)):
    ax.clear()

    # Background
    ax.set_facecolor("#eaf6ff")

    # Ground
    ax.plot([0, xmax], [0, 0], color="brown", linewidth=3)

    # Path
    ax.plot(x[:i+1], y[:i+1], linestyle="dashed", color="blue")

    # Object drawing
    if obj == "ball":
        ax.plot(x[i], y[i], "o", markersize=12)
    elif obj == "car":
        ax.add_patch(plt.Rectangle((x[i]-0.5, y[i]), 1, 0.4))
    elif obj == "train":
        ax.add_patch(plt.Rectangle((x[i]-1, y[i]), 2, 0.5))
    else:
        ax.plot(x[i], y[i], "s", markersize=10)

    # Labels
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Motion Visualization")

    ax.text(0.02*xmax, 0.9*ymax, f"Time: {t[i]:.2f} s")
    ax.text(0.02*xmax, 0.85*ymax, f"Velocity: {v} m/s")

    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)

    placeholder.pyplot(fig)
    time.sleep(speed)


