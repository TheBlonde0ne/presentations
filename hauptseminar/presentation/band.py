import numpy as np
import matplotlib.pyplot as plt

# --- Modern Scientific Styling ---
plt.rcParams.update({
    "text.color": "#b6fff0",
    "axes.labelcolor": "#b6fff0",
    "xtick.color": "#b6fff0",
    "ytick.color": "#b6fff0",
    "axes.edgecolor": "#25313a",
    "grid.color": "#25313a",
    "font.family": "sans-serif"
})



def plot_altermagnetic_bands():
    # 1. Create a 2D Brillouin Zone grid
    k = np.linspace(-np.pi, np.pi, 300)
    kx, ky = np.meshgrid(k, k)

    # 2. Define Physics Models
    # Base energy band (tight-binding model)
    e_base = -(np.cos(kx) + np.cos(ky))

    # d-wave altermagnetic splitting term: Delta(k) ~ sin(kx)*sin(ky)
    # This creates the alternating spin quadrants in k-space
    splitting = 0.5 * np.sin(kx) * np.sin(ky)

    # 3. Initialize Figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor='#05080b')

    # --- Plot A: Non-Splitting Band ---
    im1 = ax1.imshow(e_base, extent=[-np.pi, np.pi, -np.pi, np.pi], 
                     origin='lower', cmap='viridis', interpolation='bilinear')
    ax1.set_title("Non-Splitting Band Structure\n(Paramagnetic / AFM Case)", 
                  color='white', fontsize=15, pad=20)
    ax1.set_xlabel(r'$k_x$')
    ax1.set_ylabel(r'$k_y$')
    cbar1 = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    cbar1.set_label('Energy $E(k)$', color='#b6fff0')

    # --- Plot B: Altermagnetic Clover Splitting ---
    # We plot the energy difference between spin-up and spin-down: Delta E
    im2 = ax2.imshow(splitting, extent=[-np.pi, np.pi, -np.pi, np.pi], 
                     origin='lower', cmap='RdBu_r', interpolation='bilinear')
    ax2.set_title("d-wave Altermagnetic Splitting\n(The 'Clover' Pattern)", 
                  color='white', fontsize=15, pad=20)
    ax2.set_xlabel(r'$k_x$')
    ax2.set_ylabel(r'$k_y$')
    cbar2 = plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
    cbar2.set_label(r'Spin Splitting $\Delta E_{spin}$', color='#b6fff0')

    # Adding visual indicators for spin quadrants
    text_style = {'color': 'white', 'fontsize': 24, 'ha': 'center', 'va': 'center', 'fontweight': 'bold'}
    ax2.text(1.5, 1.5, r'$\uparrow$', **text_style)
    ax2.text(-1.5, -1.5, r'$\uparrow$', **text_style)
    ax2.text(1.5, -1.5, r'$\downarrow$', **text_style)
    ax2.text(-1.5, 1.5, r'$\downarrow$', **text_style)

    # Clean layout
    plt.tight_layout(pad=3.0)
    plt.show()

if __name__ == "__main__":
    plot_altermagnetic_bands()