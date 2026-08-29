# P3M

Interactions like WCA or Lennard-Jones have a short range, decaying with r^-12 or r^-6.

Electrostatic interactions only decay with r^-1. 

$$U_{\text{Coulomb}} = \frac{1}{2} \sum_{\mathbf{n} \in \mathbb{Z}^3}{}^{'} \sum_{i=1}^{N} \sum_{j=1}^{N} \frac{q_i q_j}{4\pi\varepsilon_0 \varepsilon_r \vert{}\mathbf{r}_{ij} + \mathbf{n}L\vert{}}$$
where:$\mathbf{n} = (n_x, n_y, n_z) \in \mathbb{Z}^3$ is the integer vector identifying each replica box.The prime ($\sum'$) indicates that when $\mathbf{n} = (0,0,0)$, the self-interaction term $i = j$ is excluded.

1. Conditional Convergence: The volume of a spherical shell at radius $r$ scales as $r^2 \, dr$, while the interaction decays as $r^{-1}$. The integral $\int (r^2 / r) \, dr = \int r \, dr$ diverges. Even in a globally neutral system ($\sum q_i = 0$), the infinite sum is only conditionally convergent—the computed energy and force depend entirely on the geometric order in which the periodic shells are summed.
2. Computational Cost: A direct pairwise calculation without cutoffs scales as $O(N^2)$ for a single box, and summing over infinitely replicated periodic images is computationally intractable.

## Solution: Ewald Summation

Ewald solved this problem in 1921 by splitting the Coulomb potential into a short and long range part.
These series converge absolutely and can be summed in any order:
A short-range, real-space sum.

A smooth, long-range reciprocal-space (Fourier) sum.

```text
Point Charge              Screening Clouds (Real Space)     Compensating Clouds (Fourier Space)
    (+)             =          (+) + (-)              +                   (+)
 [Point-like]             [Short-Range Screened]                  [Smooth & Periodic]
```

#### Step 1: Adding Screening Gaussian Clouds (Real-Space Part) RED

Surround every point charge $q_i$ at position $\mathbf{r}_i$ with a smooth screening cloud of opposite charge density:

$$\rho_{\text{screen}, i}(\mathbf{r}) = -q_i \left(\frac{\alpha}{\sqrt{\pi}}\right)^3 \exp\left(-\alpha^2 \vert{}\mathbf{r} - \mathbf{r}_i\vert{}^2\right)$$

where $\alpha$ (the splitting parameter) controls the spatial width of the Gaussian distribution.

* At distances $r > r_{\text{cut}}$, the point charge is completely screened by this neutralizing Gaussian cloud.
* The electrostatic potential of this screened charge decays exponentially:

$$\phi_{\text{real}}(r) = \frac{q_i}{4\pi\varepsilon} \frac{\text{erfc}(\alpha r)}{r}$$



where $\text{erfc}(x) = 1 - \text{erf}(x)$ is the complementary error function.
* Because $\text{erfc}(\alpha r)/r \to 0$ rapidly, this sum can be truncated using standard minimum-image conventions and spherical cutoffs with negligible truncation error.

#### Step 2: Compensating Gaussians (Reciprocal/Fourier-Space Part) BLUE

Because the screening Gaussians were artificially added, an identical set of compensating Gaussians with the **same sign** as the original point charges must be added back to maintain exact physical equivalence:


$$\rho_{\text{comp}}(\mathbf{r}) = \sum_{j=1}^N q_j \left(\frac{\alpha}{\sqrt{\pi}}\right)^3 \exp\left(-\alpha^2 \vert{}\mathbf{r} - \mathbf{r}_j\vert{}^2\right)$$

* This charge density $\rho_{\text{comp}}(\mathbf{r})$ is smooth, continuous, and periodic across the entire lattice.
* Smooth periodic functions solve Poisson's equation $\nabla^2 \phi = -\rho / \varepsilon$ efficiently in Fourier (reciprocal) space:

$$\phi_{\text{rec}}(\mathbf{k}) = \frac{1}{\varepsilon_0 \varepsilon_r k^2} \tilde{\rho}(\mathbf{k}) = \frac{1}{\varepsilon_0 \varepsilon_r k^2} \sum_{j=1}^N q_j \exp(-i \mathbf{k} \cdot \mathbf{r}_j) \exp\left(-\frac{k^2}{4\alpha^2}\right)$$


* The Gaussian factor $\exp(-k^2 / 4\alpha^2)$ ensures that the reciprocal sum converges rapidly for small wave vectors $\mathbf{k} = \frac{2\pi}{L}\mathbf{m}$ ($\mathbf{m} \in \mathbb{Z}^3 \setminus \{\mathbf{0}\}$).

#### Step 3: Self-Energy and Surface Corrections

1. **Self-Interaction Correction:** The smooth compensating Gaussian at $\mathbf{r}_i$ exerts an unphysical self-potential on particle $i$ itself. This constant self-energy must be subtracted:

$$U_{\text{self}} = \frac{\alpha}{4\pi^{3/2}\varepsilon_0 \varepsilon_r} \sum_{i=1}^N q_i^2$$


2. **Dipole / Surface Term:** If the outer boundary conditions are vacuum/conducting, an additional dipolar term $U_{\text{surface}}$ accounts for the net dipole moment of the simulation box.

---

### 3. Summary of the Ewald Decomposition

The total Coulomb energy decomposes into three distinct terms:

$$U_{\text{total}} = \underbrace{\frac{1}{2}\sum_{i \neq j}^N \frac{q_i q_j \text{erfc}(\alpha r_{ij})}{4\pi\varepsilon r_{ij}}}_{\text{Real-Space Sum (Short-range, Cutoff } r_c\text{)}} + \underbrace{\frac{1}{2V\varepsilon}\sum_{\mathbf{k} \neq \mathbf{0}} \frac{\exp(-k^2/4\alpha^2)}{k^2} \vert{}\tilde{\rho}(\mathbf{k})\vert{}^2}_{\text{Reciprocal-Space Sum (Fourier space)}} - \underbrace{\frac{\alpha}{4\pi^{3/2}\varepsilon}\sum_{i=1}^N q_i^2}_{\text{Self-Energy Correction}}$$

* **Scaling of Standard Ewald:** By tuning $\alpha$, the optimum computational complexity of standard Ewald is $O(N^{3/2})$.
* **Transition to P3M:** While $O(N^{3/2})$ is an improvement over $O(N^2)$, it remains too slow for large polyelectrolyte systems. Mesh-based algorithms like **P3M** replace the direct reciprocal-space sum with Fast Fourier Transforms on a grid, reducing the scaling to **$O(N \log N)$**.