import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "text.color": "#4b756d",
    "axes.labelcolor": "#4b756d",
    "xtick.color": "#4b756d",
    "ytick.color": "#4b756d",
    "axes.edgecolor": "#25313a",
    "grid.color": "#25313a",
    "font.family": "sans-serif"
})

# -----------------------------
# Model setup (toy, symmetry-based)
# -----------------------------
t = 1.0
mu = -0.6
temperature = 0.06

# Altermagnetic splitting amplitudes (anisotropic, d-wave-like + mixed term)
delta1 = 0.35
delta2 = 0.15

n_k = 301
k = np.linspace(-np.pi, np.pi, n_k)
kx, ky = np.meshgrid(k, k, indexing='ij')

def fermi(E, mu=0.0, T=0.05):
    """Fermi-Dirac distribution."""
    return 1.0 / (1.0 + np.exp((E - mu) / T))

def eps0(kx, ky, t=1.0):
    """Spin-independent base dispersion on square lattice."""
    return -2.0 * t * (np.cos(kx) + np.cos(ky))

def delta_altermagnet(kx, ky, d1=0.3, d2=0.1):
    """Momentum-dependent spin splitting compatible with altermagnetic anisotropy."""
    return d1 * (np.cos(kx) - np.cos(ky)) + d2 * np.sin(kx) * np.sin(ky)

# Base dispersion
E0 = eps0(kx, ky, t=t)

# AFM (PT-symmetric toy): exact spin degeneracy
E_up_afm = E0
E_dn_afm = E0

# Altermagnet: opposite anisotropic splittings for the two channels
Delta = delta_altermagnet(kx, ky, d1=delta1, d2=delta2)
E_up_am = E0 + Delta
E_dn_am = E0 - Delta

# -----------------------------
# Off-diagonal proxy
# -----------------------------
# Toy weighting factor representing odd matrix-element / Berry-curvature-like structure
Wxy = np.sin(kx) * np.sin(ky)

# Minimal proxy for sigma_xy: opposite channel weights => cancellation if occupations match
integrand_afm = Wxy * (fermi(E_up_afm, mu, temperature) - fermi(E_dn_afm, mu, temperature))
integrand_am = Wxy * (fermi(E_up_am, mu, temperature) - fermi(E_dn_am, mu, temperature))

sigma_xy_proxy_afm = np.mean(integrand_afm)
sigma_xy_proxy_am = np.mean(integrand_am)

print(f"AFM off-diagonal proxy    <sigma_xy> ~ {sigma_xy_proxy_afm:.4e}")
print(f"Altermagnet off-diag proxy <sigma_xy> ~ {sigma_xy_proxy_am:.4e}")

# -----------------------------
# High-symmetry path for band plots
# -----------------------------
def segment(p0, p1, n=140):
    p0 = np.array(p0, dtype=float)
    p1 = np.array(p1, dtype=float)
    a = np.linspace(0.0, 1.0, n, endpoint=False)[:, None]
    return (1 - a) * p0 + a * p1

Gamma = (0.0, 0.0)
X = (np.pi, 0.0)
M = (np.pi, np.pi)

path = np.vstack([
    segment(Gamma, X),
    segment(X, M),
    segment(M, Gamma),
    np.array([Gamma], dtype=float),
])

kxp = path[:, 0]
kyp = path[:, 1]
xp = np.arange(len(path))

E0p = eps0(kxp, kyp, t=t)
Dp = delta_altermagnet(kxp, kyp, d1=delta1, d2=delta2)

Eup_afm_p = E0p
Edn_afm_p = E0p
Eup_am_p = E0p + Dp
Edn_am_p = E0p - Dp

ticks = [0, len(path)//3, 2*len(path)//3, len(path)-1]
ticklabels = [r"$\Gamma$", r"$X$", r"$M$", r"$\Gamma$"]

# -----------------------------
# Plot
# -----------------------------
fig, axes = plt.subplots(1, 2, figsize=(10, 5), constrained_layout=True)


# Altermagnet bands
ax = axes[0]
ax.plot(xp, Eup_afm_p, lw=2, color="#1C43D3", label='AFM up')
ax.plot(xp, Edn_afm_p, lw=2, ls='--', color='#191970', label='AFM down')
ax.plot(xp, Eup_am_p, lw=2, color='#880808', label='Altermagnet +')
ax.plot(xp, Edn_am_p, lw=2, ls='--', color='#FF2400', label='Altermagnet -')
ax.set_xticks(ticks, ticklabels)
ax.set_title('Altermagnet toy bands (anisotropic splitting)')
ax.legend(frameon=True, loc='upper left')


# Integrand Altermagnet
ax = axes[1]
im1 = ax.imshow(
    integrand_am.T, origin='lower', cmap='coolwarm',
    extent=[-np.pi, np.pi, -np.pi, np.pi], vmin=-0.2, vmax=0.2, aspect='auto'
 )
ax.set_title(r'Altermagnet integrand $W_{xy}[f(E_+)-f(E_-)]$')
ax.set_xlabel(r'$k_x$')
ax.set_ylabel(r'$k_y$')
fig.colorbar(im1, ax=ax, fraction=0.046, pad=0.02)

fig.suptitle('Why cancellation holds in AFM and can fail in altermagnets (toy model)', fontsize=13)
plt.show()