import numpy as np
import matplotlib.pyplot as plt
from qutip import qeye, sigmax, sigmay, sigmaz, tensor, ptrace, entropy_vn

# 1. Quantum System Parameters
N = 6  # Number of qubits in the spin chain
PHI = (1 + 5**0.5) / 2  # The Golden Ratio (~1.618033)

def build_two_body_operator(op_i, i, op_j, j, N):
    """Constructs a two-body tensor product operator for sites i and j."""
    op_list = [qeye(2)] * N
    op_list[i] = op_i
    op_list[j] = op_j
    return tensor(op_list)

def get_hamiltonian(N, alpha, configuration="naressi"):
    """
    Constructs the system Hamiltonian to test energy propagation models.
    Compares conventional cable conduction with Naressi's Geometric Law.
    """
    H = 0
    g = 0.5  # Transverse magnetic field representing environmental quantum fluctuations
    
    for i in range(N - 1):
        if configuration == "naressi":
            # NARESSI'S LAW: Golden ratio geometric coupling combined 
            # with the space-vacuum dampening factor: e^( -i / phi^2 )
            J = alpha * (PHI ** (-i)) * np.exp(-i / (PHI ** 2))
        elif configuration == "classical_linear":
            # CLASSICAL MODEL: Linear decay proportional to internal cable resistance
            J = alpha * (1 / (i + 1))
        else:
            # UNIFORM IDEAL CONFIGURATION
            J = alpha
            
        H -= J * build_two_body_operator(sigmax(), i, sigmax(), i + 1, N)
    
    # Single-particle transverse field term
    for i in range(N):
        op_list = [qeye(2)] * N
        op_list[i] = sigmaz()
        H -= g * tensor(op_list)
        
    return H

# 2. Coupling Parameter Scan for Numerical Proof
alpha_values = np.linspace(0.0, 3.0, 50)
configurations = ["classical_linear", "naressi"]
entropies = {conf: [] for conf in configurations}
ground_energies = {conf: [] for conf in configurations}

print("Running comparative quantum simulation...")

for conf in configurations:
    for a in alpha_values:
        H = get_hamiltonian(N, a, configuration=conf)
        
        # Exact diagonalization to extract eigenvalues (energy) and eigenstates
        eigenvalues, eigenstates_list = H.eigenstates()
        
        # Store Ground State Energy
        ground_energies[conf].append(eigenvalues[0])
        
        # Compute reduced density matrix (partial trace over the first half of the chain)
        rho_subsystem = ptrace(eigenstates_list[0], list(range(N // 2)))
        
        # Compute Von Neumann Entanglement Entropy
        s_vn = entropy_vn(rho_subsystem, base=2)
        entropies[conf].append(s_vn)

# 3. Plotting the Simulation Results for Verification
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# GRAPH 1: Entanglement Entropy Profile (Non-local information capacity)
ax1.plot(alpha_values, entropies["classical_linear"], label="Classical Cable Model (Linear)", linestyle="--", color="gray")
ax1.plot(alpha_values, entropies["naressi"], label="Naressi's Geometric Law", linewidth=2.5, color="blue")
ax1.axvline(x=PHI, color="red", linestyle="-.", label=f"Critical Resonance (α = φ = {PHI:.3f})")
ax1.set_title("1. Entanglement Profile (Von Neumann Entropy)")
ax1.set_xlabel("Scaling Parameter (α)")
ax1.set_ylabel("Entanglement Entropy $S_{VN}$ (Bits)")
ax1.grid(True, alpha=0.3)
ax1.legend()

# GRAPH 2: Ground State Energy Level (System Efficiency)
ax2.plot(alpha_values, ground_energies["classical_linear"], label="Classical Cable Model (Linear)", linestyle="--", color="gray")
ax2.plot(alpha_values, ground_energies["naressi"], label="Naressi's Geometric Law", linewidth=2.5, color="green")
ax2.set_title("2. Ground State Energy Profile")
ax2.set_xlabel("Scaling Parameter (α)")
ax2.set_ylabel("Ground State Energy $E_0$ (Arbitrary Units)")
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.show()
print("Simulation finished. Displaying charts.")