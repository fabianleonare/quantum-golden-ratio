# Computational Analysis of Von Neumann Entropy in One-Dimensional Spin Chains with Golden Ratio Geometric Coupling

**Author:** Fabian Leo Naressi

**Affiliation:** Independent Researcher

**Date:** July 2026

---

## Abstract

This study investigates the influence of geometric coupling profiles on bipartite entanglement in one-dimensional spin chains. We analyze a transverse-field Ising model in which nearest-neighbor interactions are assigned according to three different spatial patterns: constant coupling, linear coupling, and a geometric decay governed by the Golden Ratio, φ. The ground state of the system is obtained through exact diagonalization using the QuTiP numerical framework, and the degree of entanglement is quantified by the Von Neumann entropy of a reduced density matrix corresponding to one half of the chain. The results indicate that the Golden Ratio-based coupling profile produces a distinctive entropy response near the scaling parameter α ≈ φ, yielding a broader and more pronounced entanglement profile than the constant and linear cases.

## 1. Introduction and Hamiltonian Model

We consider a transverse-field Ising chain of N spin-1/2 particles. The site-dependent coupling used in this study follows:

$$J_n = \alpha \cdot \phi^{-n} \cdot e^{-n/\phi^2}$$

where φ is the Golden Ratio and α the global scale. Substituting this into the Hamiltonian gives:

$$
H = - \sum_{n=0}^{N-2} \left(\alpha \phi^{-n} e^{-n/\phi^2}\right) \sigma_x^{(n)} \sigma_x^{(n+1)} - g \sum_{n=0}^{N-1} \sigma_z^{(n)}.
$$

## 2. Computational Methods

Ground states were obtained by exact diagonalization (QuTiP). Bipartite entanglement was quantified as the Von Neumann entropy of the reduced density matrix of the left half of the chain.

## 3. Results and Discussion

The geometric (Golden-Ratio) coupling suppresses early entropy growth and produces a stable inflection near α = φ. Energetically, the geometric chain stabilizes at a systematically higher ground-state energy (less negative) than the linear model, indicating a more optimized configuration that reduces overall binding energy required for global coherence.

## Figure

The figure compares the entanglement profile (left panel) and ground-state energy profile (right panel) for linear and Golden-Ratio coupling laws. Replace `figure.png` in this folder with the high-resolution figure to embed.

## References

Amico, L., Fazio, R., Osterloh, A., & Vedral, V. (2008). Entanglement in many-body systems. Reviews of Modern Physics, 80(2), 517–576.

Preskill, J. (2018). Quantum computing in the NISQ era and beyond. Quantum, 2, Article 79.
