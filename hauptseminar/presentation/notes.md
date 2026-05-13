effect of magnetism on electronic band

kubo formula


Phys Rev X12 040501 (2022)
Nat Rev Mater 10, 473 (2025)


slides till 08.05
Meeting on 15.05
Meeting on 19.05 (final presentation)

Theory:

## Quick Recap
- What are we trying to detect
  - Symmetry breaking and no net magnetization
  - how do the bands splits
  - split bands can be examined via optical conductivity tensor

- How do optical conductivity tensor and magnetic structure link?
  - Linear Response Theory
  - Off-diagonal elements and no net magnetization -> altermagnetism
  - fitting sigma to different DFT simulations with different magnetic orders

- DFT simulations: how do we get the band structure and optical conductivity tensor?
  - DFT with different magnetic orders
  - Wannierization and Kubo formula to get optical conductivity tensor
  - show results for different grades of band splitting

- Experiment: how do we measure the optical conductivity tensor?
  - MOKE and Faraday: measure rotation and ellipticity
  - MOKKA: relate rotation and ellipticity to real and imaginary parts of optical conductivity tensor
  - Fast MOKKA: special setup for low temp measurements
  - Show animation of light wave for different cases
  - Muller Matrix: how to extract the optical conductivity tensor from the measurements
  - Jones Formalism: how to model the light-matter interaction and relate it to the optical conductivity tensor

Refined Structure & Summaries1. Quick Recap: The Altermagnetic StateSymmetry & Magnetization: Altermagnets (AM) possess zero net magnetization ($M=0$) like antiferromagnets but break time-reversal symmetry to produce non-relativistic spin-splitting like ferromagnets.Band Splitting: In $k$-space, this manifests as a $d$-wave or $g$-wave "clover" pattern where spin-up and spin-down bands are separated.The Probe: These split bands create vertical interband transitions that can be "seen" as specific peaks or humps in the optical conductivity tensor.2. Linking Conductivity to Magnetic StructureLinear Response Theory: We describe how an incident electric field $\mathbf{E}$ induces a current $\mathbf{J}$ through the tensor $\mathbf{J} = \sigma \mathbf{E}$.Tensor Signatures: In a standard AFM, symmetry forces off-diagonal elements ($\sigma_{xy}$) to zero. In AM, the $d$-wave symmetry allows these terms to survive even without a net $B$-field.The "Diagonal" Innovation: Highlight that while $\sigma_{xy}$ is the classic "MOKE" signature, altermagnetism also reconstructs the diagonal elements ($\sigma_{xx}$), providing a robust bulk fingerprint immune to domain cancellation.3. DFT: From $k$-space to $\omega$-spaceDifferent Orders: Researchers simulate Non-Magnetic (NM), AFMe (conventional), and AFMo (altermagnetic) orders to see which one matches the "real world" data.Wannierization & Kubo: DFT provides the wavefunctions; Wannier interpolation creates a dense $k$-mesh; and the Kubo Formula calculates the frequency-dependent conductivity $\sigma(\omega)$.Predictive Power: This allows us to say: "If we see a peak at $0.1\text{ eV}$, it corresponds to a specific $0.2\text{ eV}$ spin-splitting in the bands".4. Experiment: Measuring the TensorMOKE & Faraday: These effects measure how the light's polarization rotates ($\theta$) and becomes elliptical ($\eta$) upon reflection or transmission.MOKKA (Magneto-Optical Kramers-Kronig): A generalization of standard KK analysis that allows us to find the real and imaginary parts of $\sigma$ (or the dielectric function) for left- and right-handed light without using complex waveplates.Fast MOKKA (45° Protocol): A high-field/low-temp optimization where polarizers are fixed at 45°, eliminating the need to move sensitive optics inside a cryostat.Jones vs. Mueller Formalism:Jones: Used for simple, fully polarized light interactions (standard $2 \times 2$ matrix).Mueller: Used for more complex interactions (e.g., in $\kappa$-Cl) to account for arbitrary crystal symmetry and reflection using a $4 \times 4$ matrix.Suggested ImprovementsSymmetry Constraints: Add a small note on how Crystal Symmetry (like the orthorhombic $Pnnm$ structure of $FeSb_2$) dictates which terms in the $\sigma$ tensor are allowed to be non-zero.Bulk vs. Surface: Explicitly state that while ARPES is a "surface" probe for band splitting, Magneto-Optics (especially the diagonal elements) acts as a bulk probe. This is your strongest argument against the $RuO_2$ results.The "Drude" Connection: Briefly explain that the Drude part (the $0\text{ eV}$ peak) proves the material is a metal, which is necessary for "Metallic Altermagnetism" to distinguish it from the semiconductor parent $FeSb_2$.