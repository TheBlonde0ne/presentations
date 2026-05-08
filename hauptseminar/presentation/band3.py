import numpy as np
import matplotlib.pyplot as plt

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
delta_am = 0.3
afm_perturbation = 0.03  # Slightly stronger breaking to visualize faded cancellation
n_k = 400
k = np.linspace(-np.pi, np.pi, n_k)
kx, ky = np.meshgrid(k, k)

# --- Base dispersion ---
E0 = -2 * t * (np.cos(kx) + np.cos(ky))

# --- AFM: nearly degenerate channels with small perturbation ---
# Represents tiny breaking (SOC, strain, disorder, etc.)
Pert = afm_perturbation * (np.cos(kx) - np.cos(ky))
E_up_afm = E0 + Pert
E_dn_afm = E0 - Pert

# --- Altermagnet: d-wave splitting ---
Delta = delta_am * (np.cos(kx) - np.cos(ky))
E_up_am = E0 + Delta
E_dn_am = E0 - Delta

# --- Kubo integrand proxy ---
# Weighting factor: odd symmetry in kx, ky (represents velocity/Berry-curvature-like matrix element)
Wxy = np.sin(kx) * np.sin(ky)

# AFM integrand: cancels because channels are identical
integrand_afm = Wxy * (np.exp(-(E_up_afm - mu)**2 / 0.05) - np.exp(-(E_dn_afm - mu)**2 / 0.05))

# Altermagnet integrand: nonzero because channels split
integrand_am = Wxy * (np.exp(-(E_up_am - mu)**2 / 0.05) - np.exp(-(E_dn_am - mu)**2 / 0.05))

sigma_xy_afm = np.mean(integrand_afm)
sigma_xy_am = np.mean(integrand_am)

print(f"AFM:        <sigma_xy> ~ {sigma_xy_afm:.4e}")
print(f"Altermagnet:<sigma_xy> ~ {sigma_xy_am:.4e}")

# --- Plotting ---
fig, axes = plt.subplots(2, 2, figsize=(13, 11), constrained_layout=True)

# --- Row 1: Fermi Surfaces ---

# AFM Fermi Surface (nearly degenerate with small perturbation)
ax = axes[0, 0]
ax.contour(kx, ky, E_up_afm, levels=[mu], colors=['#7fffe8'], linewidths=2.5)
ax.contour(kx, ky, E_dn_afm, levels=[mu], colors=['#ff8fab'], linewidths=2.5, linestyles='--')
ax.set_title("AFM: Nearly Degenerate\n(Weak Perturbation)", fontsize=13, pad=12)
ax.set_aspect('equal')
ax.set_xlabel("$k_x$", fontsize=11)
ax.set_ylabel("$k_y$", fontsize=11)
ax.set_xlim(-np.pi, np.pi)
ax.set_ylim(-np.pi, np.pi)
ax.text(0, -2.8, "Small splitting\n$\\Rightarrow$ Suppressed $\\sigma_{xy}$", 
        ha='center', fontsize=10, color='#b6fff0', style='italic')

# Altermagnet Fermi Surface (split)
ax = axes[0, 1]
ax.contour(kx, ky, E_up_am, levels=[mu], colors=['#7fffe8'], linewidths=2.5)
ax.contour(kx, ky, E_dn_am, levels=[mu], colors=['#ff8fab'], linewidths=2.5, linestyles='--')
ax.set_title("Altermagnet: Split Fermi Surfaces\n(Non-zero Response)", fontsize=13, pad=12)
ax.set_aspect('equal')
ax.set_xlabel("$k_x$", fontsize=11)
ax.set_ylabel("$k_y$", fontsize=11)
ax.set_xlim(-np.pi, np.pi)
ax.set_ylim(-np.pi, np.pi)
ax.text(0, -2.8, "Distinct contours\n$\\Rightarrow$ $\\sigma_{xy} \\neq 0$", 
        ha='center', fontsize=10, color='#b6fff0', style='italic')

# --- Row 2: Kubo Integrands ---

# AFM Integrand
ax = axes[1, 0]
im0 = ax.imshow(integrand_afm.T, origin='lower', cmap='RdBu_r',
                extent=[-np.pi, np.pi, -np.pi, np.pi], vmin=-0.6, vmax=0.6, aspect='auto')
ax.set_title(r"AFM: $\int_{\text{BZ}} W_{xy}[f(E_\uparrow) - f(E_\downarrow)] d^2k$", 
             fontsize=12, pad=12)
ax.set_xlabel("$k_x$", fontsize=11)
ax.set_ylabel("$k_y$", fontsize=11)
cbar0 = fig.colorbar(im0, ax=ax, fraction=0.046, pad=0.04)
cbar0.set_label("Contribution", fontsize=10)
ax.text(0, -3.0, f"$\\langle\\sigma_{{xy}}\\rangle \\approx {sigma_xy_afm:.1e}$ (cancels)", 
        ha='center', fontsize=10, color='#b6fff0', weight='bold')

# Altermagnet Integrand
ax = axes[1, 1]
im1 = ax.imshow(integrand_am.T, origin='lower', cmap='RdBu_r',
                extent=[-np.pi, np.pi, -np.pi, np.pi], vmin=-0.6, vmax=0.6, aspect='auto')
ax.set_title(r"Altermagnet: $\int_{\text{BZ}} W_{xy}[f(E_+) - f(E_-)] d^2k$", 
             fontsize=12, pad=12)
ax.set_xlabel("$k_x$", fontsize=11)
ax.set_ylabel("$k_y$", fontsize=11)
cbar1 = fig.colorbar(im1, ax=ax, fraction=0.046, pad=0.04)
cbar1.set_label("Contribution", fontsize=10)
ax.text(0, -3.0, f"$\\langle\\sigma_{{xy}}\\rangle \\approx {sigma_xy_am:.1e}$ (survives!)", 
        ha='center', fontsize=10, color='#b6fff0', weight='bold')

plt.savefig("band_comparison.svg")
plt.show()


##########################################################################################
##########################################################################################
##########################################################################################


fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), constrained_layout=True)
ax = axes[0]
ax.contour(kx, ky, E_up_afm, levels=[mu], colors=['#7fffe8'], linewidths=2.5)
ax.contour(kx, ky, E_dn_afm, levels=[mu], colors=['#ff8fab'], linewidths=2.5, linestyles='--')
ax.set_title("AFM: Nearly Degenerate\n(Weak Perturbation)", fontsize=13, pad=12)
ax.set_aspect('equal')
ax.set_xlabel("$k_x$", fontsize=11)
ax.set_ylabel("$k_y$", fontsize=11)
ax.set_xlim(-np.pi, np.pi)
ax.set_ylim(-np.pi, np.pi)
ax.text(0, -2.8, "Small splitting\n$\\Rightarrow$ Suppressed $\\sigma_{xy}$", 
        ha='center', fontsize=10, color='#b6fff0', style='italic')

# Altermagnet Fermi Surface (split)
ax = axes[1]
ax.contour(kx, ky, E_up_am, levels=[mu], colors=['#7fffe8'], linewidths=2.5)
ax.contour(kx, ky, E_dn_am, levels=[mu], colors=['#ff8fab'], linewidths=2.5, linestyles='--')
ax.set_title("Altermagnet: Split Fermi Surfaces\n(Non-zero Response)", fontsize=13, pad=12)
ax.set_aspect('equal')
ax.set_xlabel("$k_x$", fontsize=11)
ax.set_ylabel("$k_y$", fontsize=11)
ax.set_xlim(-np.pi, np.pi)
ax.set_ylim(-np.pi, np.pi)
ax.text(0, -2.8, "Distinct contours\n$\\Rightarrow$ $\\sigma_{xy} \\neq 0$", 
        ha='center', fontsize=10, color='#b6fff0', style='italic')

plt.savefig("bands.svg")
plt.show()

##########################################################################################
##########################################################################################
##########################################################################################

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), constrained_layout=True)

# AFM Integrand
ax = axes[0]
im0 = ax.imshow(integrand_afm.T, origin='lower', cmap='RdBu_r',
                extent=[-np.pi, np.pi, -np.pi, np.pi], vmin=-0.6, vmax=0.6, aspect='auto')
ax.set_title(r"AFM: $\int_{\text{BZ}} W_{xy}[f(E_\uparrow) - f(E_\downarrow)] d^2k$", 
             fontsize=12, pad=12)
ax.set_xlabel("$k_x$", fontsize=11)
ax.set_ylabel("$k_y$", fontsize=11)
cbar0 = fig.colorbar(im0, ax=ax, fraction=0.046, pad=0.04)
cbar0.set_label("Contribution", fontsize=10)
ax.text(0, -3.0, f"$\\langle\\sigma_{{xy}}\\rangle \\approx {sigma_xy_afm:.1e}$ (cancels)", 
        ha='center', fontsize=10, color='#b6fff0', weight='bold')

# Altermagnet Integrand
ax = axes[1]
im1 = ax.imshow(integrand_am.T, origin='lower', cmap='RdBu_r',
                extent=[-np.pi, np.pi, -np.pi, np.pi], vmin=-0.6, vmax=0.6, aspect='auto')
ax.set_title(r"Altermagnet: $\int_{\text{BZ}} W_{xy}[f(E_+) - f(E_-)] d^2k$", 
             fontsize=12, pad=12)
ax.set_xlabel("$k_x$", fontsize=11)
ax.set_ylabel("$k_y$", fontsize=11)
cbar1 = fig.colorbar(im1, ax=ax, fraction=0.046, pad=0.04)
cbar1.set_label("Contribution", fontsize=10)
ax.text(0, -3.0, f"$\\langle\\sigma_{{xy}}\\rangle \\approx {sigma_xy_am:.1e}$ (survives!)", 
        ha='center', fontsize=10, color='#b6fff0', weight='bold')


plt.savefig("kubo.svg")
plt.show()