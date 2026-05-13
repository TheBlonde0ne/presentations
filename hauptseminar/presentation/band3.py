import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

# --- Seminar Palette ---
plt.rcParams.update({
    "text.color": "#b6fff0",
    "axes.labelcolor": "#b6fff0",
    "xtick.color": "#4b756d",
    "ytick.color": "#4b756d",
    "axes.edgecolor": "#25313a",
    "grid.color": "#1a2329",
    "font.family": "sans-serif",
    "figure.facecolor": "#05080b",
    "axes.facecolor": "#000000"
})

# --- Parameters ---
t = 1.0
mu = -0.5
delta_am_min = 0.0
delta_am_max = 0.6  # Stronger splitting
n_k = 400
k = np.linspace(-np.pi, np.pi, n_k)
kx, ky = np.meshgrid(k, k)
n_frames = 120  # Frames for animation (30 forward, 30 backward)

# --- Base dispersion ---
E0 = -2 * t * (np.cos(kx) + np.cos(ky))

# --- Weighting factor: odd symmetry in kx, ky ---
Wxy = np.sin(kx) * np.sin(ky)

# --- Create figure for animation ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

def update_frame(frame_idx):
    """Update animation frame"""
    # Create smooth loop: 0->1->0
    if frame_idx < n_frames // 2:
        progress = frame_idx / (n_frames // 2)
    else:
        progress = (n_frames - frame_idx) / (n_frames // 2)
    
    # Interpolate splitting strength
    delta_am = delta_am_min + (delta_am_max - delta_am_min) * progress
    
    # Calculate dispersions
    Delta = delta_am * (np.cos(kx) - np.cos(ky))
    E_up = E0 + Delta
    E_dn = E0 - Delta
    
    # Calculate integrand
    integrand = Wxy * (np.exp(-(E_up - mu)**2 / 0.05) - np.exp(-(E_dn - mu)**2 / 0.05))
    sigma_xy = np.mean(integrand)
    
    # Clear axes
    for ax in axes:
        ax.clear()
    
    # Left panel: Fermi surfaces
    ax = axes[0]
    ax.contour(kx, ky, E_up, levels=[mu], colors=['#7fffe8'], linewidths=2.5, label='Spin ↑')
    ax.contour(kx, ky, E_dn, levels=[mu], colors=['#ff8fab'], linewidths=2.5, linestyles='--', label='Spin ↓')
    ax.set_title(f"Altermagnet Fermi Surfaces\n(Splitting Parameter: {delta_am:.3f})", 
                 fontsize=13, pad=12)
    ax.set_aspect('equal')
    ax.set_xlabel("$k_x$", fontsize=11)
    ax.set_ylabel("$k_y$", fontsize=11)
    ax.set_xlim(-np.pi, np.pi)
    ax.set_ylim(-np.pi, np.pi)
    ax.legend(loc='upper right', fontsize=10)
    ax.text(0, -2.9, f"Progress: {progress*100:.0f}%", 
            ha='center', fontsize=10, color='#b6fff0', style='italic')
    
    # Right panel: Kubo integrand heatmap
    ax = axes[1]
    im = ax.imshow(integrand.T, origin='lower', cmap='RdBu_r',
                   extent=[-np.pi, np.pi, -np.pi, np.pi], vmin=-0.8, vmax=0.8, aspect='auto')
    ax.set_title(r"Kubo Integrand: $\int_{\text{BZ}} W_{xy}[f(E_+) - f(E_-)] d^2k$", 
                 fontsize=12, pad=12)
    ax.set_xlabel("$k_x$", fontsize=11)
    ax.set_ylabel("$k_y$", fontsize=11)
    
    if not hasattr(update_frame, 'cbar') or update_frame.cbar is None:
        update_frame.cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        update_frame.cbar.set_label("Contribution", fontsize=10)
    else:
        update_frame.cbar.update_normal(im)
    
    ax.text(0, -3.0, f"$\\langle\\sigma_{{xy}}\\rangle = {sigma_xy:.3e}$", 
            ha='center', fontsize=11, color='#b6fff0', weight='bold')

update_frame.cbar = None

# Create animation
ani = animation.FuncAnimation(fig, update_frame, frames=n_frames, 
                             interval=80, repeat=True, blit=False)

# Save as GIF
print("Creating animation... this may take a moment")
writer = PillowWriter(fps=10)
ani.save('altermagnet_animation.gif', writer=writer)
print("Animation saved as 'altermagnet_animation.gif'")

plt.show()