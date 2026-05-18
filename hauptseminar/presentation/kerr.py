import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Parameter Configuration ---
theta_K = np.radians(22.5)  # Exaggerated Kerr rotation for clarity
epsilon_K = 0.35            # Exaggerated ellipticity (minor/major axis ratio)
frames = 120

# Time array for a full optical cycle
t = np.linspace(0, 2 * np.pi, frames)

# 1. Incident Wave: Linearly polarized along X
x_inc = np.cos(t)
y_inc = np.zeros_like(t)

# 2. Reflected Wave: Elliptical polarization in its own intrinsic frame
x_prime = np.cos(t)
y_prime = epsilon_K * np.sin(t)

# Rotate intrinsic frame back to the laboratory frame by theta_K
x_ref = x_prime * np.cos(theta_K) - y_prime * np.sin(theta_K)
y_ref = x_prime * np.sin(theta_K) + y_prime * np.cos(theta_K)

# --- Figure Setup ---
fig, ax = plt.subplots(figsize=(7, 7))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_title("MOKE Polarization Transformation", fontsize=14, pad=15)
ax.set_xlabel(r"Electric Field $E_x$", fontsize=12)
ax.set_ylabel(r"Electric Field $E_y$", fontsize=12)

# Plot static full trajectories as background reference
ax.plot(x_inc, y_inc, 'b--', alpha=0.3, label="Incident (Linear)")
ax.plot(x_ref, y_ref, 'r-', alpha=0.2, label="Reflected (Full Ellipse)")

# Dynamic elements to animate
line_inc, = ax.plot([], [], 'b-', linewidth=2.5, label="Incident Vector Trace")
line_ref, = ax.plot([], [], 'r-', linewidth=2.5, label="Reflected Vector Trace")
dot_inc, = ax.plot([], [], 'bo', ms=8)
dot_ref, = ax.plot([], [], 'ro', ms=8)

ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)

# --- Animation Functions ---
def init():
    line_inc.set_data([], [])
    line_ref.set_data([], [])
    dot_inc.set_data([], [])
    dot_ref.set_data([], [])
    return line_inc, line_ref, dot_inc, dot_ref

def update(frame):
    # Progressively draw traces up to current time step
    line_inc.set_data(x_inc[:frame], y_inc[:frame])
    line_ref.set_data(x_ref[:frame], y_ref[:frame])
    
    # Current position of the E-field vector tips
    dot_inc.set_data([x_inc[frame]], [y_inc[frame]])
    dot_ref.set_data([x_ref[frame]], [y_ref[frame]])
    
    return line_inc, line_ref, dot_inc, dot_ref

ani = animation.FuncAnimation(
    fig, update, frames=frames, init_func=init, blit=True, interval=25
)

# To save this file as an MP4 for web tools/Reveal.js, uncomment below:
# ani.save('moke_polarization.mp4', writer='ffmpeg', fps=40, dpi=200)

plt.show()