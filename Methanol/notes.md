workflow simulating methanol:
With a foundation mace model, md steps are sampled. for one frame, an mgrid optimization is performed, the optimal parameter is used to relabel the frames with dft, corrected with d3. Then, different hyperparameters are trained for MLIPs, the best is used to run production MDs, evaluation RDF and Diffusion

## Task 1
Why would you use a workflow manager instead of a plain Python or Bash script? What specific benefits does this setup provide?

Combining the engines for DFT and MD simulations as well as the MLIP training simplifies the workflow and allows for better organization and automation. A generalized obejct-oriented workflow manager can help to manage dependencies, and allows an easy way to evaluate data from different steps of the workflow. It also allows for better reproducibility and scalability.
---

## Task 2
- How does MACE differ from the model you will train yourself?
- Why train your own model at all, given that foundation models already exist?

The MACE model is a specific type of MLIP that has been pre-trained on a large dataset and is designed to be transferable across different systems (key note "foundation model"). The own trained model will be specifically tailored to the methanol system and may perform better on this specific task. Additionally, training your own model allows for more control over the architecture and training process, which can lead to better performance on the specific task at hand. Especially if it needs to perform well e.g. in diffusion behavior.
---

## Task 3
- Adapt and execute the main.py script to generate initial configurations with Packmol. 
- What are SMILES strings? 
- Which temperatures would you simulate at, and why? 
- Run a 1ns MD simulation using the MACE foundation model. 
- Load the resulting MACE trajectory with zntrack.from_rev() and inspect the node. frames list. Familiarise yourself with the ASE Atoms object.


SMILES (or Simplified Molecular Input Line Entry System) strings are a way to represent chemical structures using a line notation. They encode the structure of a molecule in a compact format.
Wiki: https://de.wikipedia.org/wiki/Simplified_Molecular_Input_Line_Entry_System

The temperatures to simulate at would depend on the interest of the study. Important is to change the density of the system depending on the temperature. Generally, room temperature (around 300K) is a common choice for simulations of liquids.
---

## Task 4
- What does the MGRID parameter control in CP2K? 
- Perform aconvergence test: run multiple DFT calculations with varying MGRID cutoff on a small number of configurations from the MACE trajectory, until the change in forces and energies is below 0.002 (in the respective units). 
- Modify CompareDFT in src/compare.py to analyse and plot the convergence.

The MGRID parameter in CP2K controls the cutoff for the real-space grid used in the calculation of the Hartree potential and the exchange-correlation potential. It determines the accuracy of the calculation, with higher values leading to more accurate results but also increased computational cost. The ideal value of the mgrid parameter is important to find a balance between accuracy and computational cost.
---

## Task 5
- Use your optimised DFT settings to generate the training and test datasets. 
- What are the core differences between LDA and GGA exchange–correlation functionals? 
- Which of the two would you pick for methanol, and why? 
- What is the role of dispersion corrections in DFT? 
- Why can it be useful to evaluate the D3 correction outside of CP2K?

LDA (Local Density Approximation) and GGA (Generalized Gradient Approximation) are two types of exchange-correlation functionals used in DFT calculations. The core difference between them is that LDA only considers the local electron density, while GGA also takes into account the gradient of the electron density. GGA is generally more accurate than LDA for systems with varying electron densities, such as molecules and surfaces. LDA works great for systems with uniform electron density, such as bulk metals. For methanol, GGA would be a better choice due to the presence of varying electron densities in the molecule. (high near the atoms, low in the space between them)

Because DFT simulations base on locality, dispersion interactions are not captured. Dispersion corrections, such as D3, are added to account for these interactions and improve the accuracy of the calculations.

Standalone d3 works faster and only depends on the atoms, not the electronic structure, so it can be evaluated outside of CP2K and added to the DFT energies and forces afterwards. This can save computational time and resources, especially for large systems.
Outside calculation of D3 can also allow analysis and decomposition of the dispersion contribution to the total energy. Also with precalculated data, you can add d3 corrections to "improve" the unknown data.
---

## Task 6
- Try different hyperparameters and explain their impact:
    – the number of training configurations,
    – the radial cutoff r_max,
    – the number of basis functions,
    – the network architecture,
    – or any other setting from the documentation that you find worth exploring. 
- Train ensemble models and compare the resulting uncertainties. 
- Evaluate the MLIPs on the fixed test set. 
- Select your best set of parameters and train two models: one on the raw DFT data, and one on the D3-corrected data. 
- What are the benefits of model ensembles over single models?

Number of training configurations:
More training configurations generally lead to better model performance, as the model has more data to learn from. However, it also increases the computational cost and training time.
Radial cutoff r_max:
The radial cutoff determines the range of interactions considered in the model. A larger cutoff can capture more long-range interactions, but it also increases the computational cost. A smaller cutoff may miss important interactions in big molecules
Number of basis functions:
More basis functions can allow the model to capture more complex relationships in the data, but it also increases the computational cost and the risk of overfitting. (see DFT basics, infinite basis set is the exact solution, but we need to truncate it for practical calculations)
Network architecture:
The architecture of the neural network can impact the model's ability to learn complex relationships in the data. A deeper or wider network may be able to capture more complex patterns, but it also increases the risk of overfitting and the computational cost.

Model ensembles can provide better performance and uncertainty estimates compared to single models. By training multiple models with different initializations or subsets of the data, we can average their predictions to reduce variance and improve generalization.
Additionally, the spread of predictions from the ensemble can be used to estimate the uncertainty of the model's predictions, which can be valuable for decision-making and identifying areas where the model may be less reliable.
---