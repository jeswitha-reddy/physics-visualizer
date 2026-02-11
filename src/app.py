import streamlit as st
import re
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Physics Visualizer", layout="centered")

st.title("AI Physics Problem Visualizer")
st.write("Enter a physics word problem (Vertical Motion)")

problem = st.text_input("Enter problem statement:",
                         "A ball is thrown upward with speed 10 m/s")

# Extract velocity from text using regex
velocity = re.findall(r"\d+", problem)

if velocity:
    u = float(velocity[0])
else:
    u = 10.0

g = st.slider("Gravity (m/s²)", 1.0, 20.0, 9.8)
u = st.slider("Initial Velocity (m/s)", 1.0, 50.0, u)

t = np.linspace(0, 2*u/g, 100)
h = u*t - 0.5*g*t*t

fig, ax = plt.subplots()
ax.plot(t, h)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Height (m)")
ax.set_title("Motion of Ball")

st.pyplot(fig)

