import os
import numpy as np
import matplotlib.pyplot as plt
from qutip import jmat, sesolve, entropy_vn, ptrace, basis, tensor

def run_simulation():
    # 1. Spin Chain Parameter Configuration
    N = 6                     # Number of nodes (optimized for fast exact diagonalization)
    phi = (1 + 5**0.5) / 2    # Golden Ratio
    alpha = 1.0               # Initial scaling parameter
    beta = 0.15               # Slope for classical linear decay
    times = np.linspace(0, 10, 150) # Time horizon for the evolution
    
    print(f"Initializing quantum simulation on a spin chain with N={N} nodes...")

    # Pauli operators for spin-1/2
    sx = jmat(1/2, 'x')
    sy = jmat(1/2, 'y')
    sz = jmat(1/2, 'z')

    # Initial state: all spins aligned along Z except the first one (local excitation)
    state_list = [basis(2, 1)] + [basis(2, 0) for _ in range(N-1)]
    psi0 = tensor(state_list)

    # Building interaction operators for the chain (XX Model)
    interaction_terms = []
    for i in range(N - 1):
        # Generate coupling for node i and i+1
        op_list_x = [qutip.qeye(2)] * N
        op_list_y = [qutip.qeye(2)] * N
        op_list_x[i] = sx
        op_list_x[i+1] = sx
        op_list_y[i] = sy
        op_list_y[i+1] = sy
        interaction_terms.append((tensor(op_list_x), tensor(op_list_y)))

    # 2. Definition of Coupling Profiles (The Three Models)
    J_constant = [alpha for _ in range(N-1)]
    J_linear = [max(0.01, alpha - beta * n) for n in range(1, N)]
    J_naressi = [alpha * (phi**(-n)) * np.exp(-n / (phi**2)) for n in range(1, N)]

    models = {
        'Constant Ohmic': J_constant,
        'Classical Linear Decay': J_linear,
        'Naressi Geometric Law': J_naressi
    }

    entropy_results = {}
    fidelity_results = {}

    # 3. Solving Schrödinger Equation for each model
    for name, J_profile in models.items():
        print(f"Computing time evolution for model: {name}...")
        
        # Build specific Hamiltonian
        H = 0
        for n, (op_x, op_y) in enumerate(interaction_terms):
            H += J_profile[n] * (op_x + op_y)
            
        # Time evolution
        result = sesolve(H, psi0, times)
        
        # Calculate Von Neumann entropy and Fidelity along the evolution
        entropies = []
        fidelities = []
        for state in result.states:
            # Reduced density matrix for the first subsystem (input node)
            rho_sub = ptrace(state, [0])
            s = entropy_vn(rho_sub)
            entropies.append(s)
            
            # Calculate Fidelity with respect to the initial coherent state
            f = qutip.fidelity(state, psi0)**2
            fidelities.append(f)
            
        entropy_results[name] = entropies
        fidelity_results[name] = fidelities

    # 4. Statistical Extraction of Final Data
    print("\n--- EXTRACTED STATISTICAL-NUMERICAL RESULTS ---")
    for name in models.keys():
        s_final = entropy_results[name][-1]
        f_final = fidelity_results[name][-1]
        
        # Calculate critical decoherence time (conventional threshold at S > 0.35)
        t_crit = "> 10.0 (Stable)"
        for idx, s_val in enumerate(entropy_results[name]):
            if s_val > 0.35:
                t_crit = f"{times[idx]:.2f}"
                break
                
        print(f"[{name}] -> Final Entropy: {s_final:.4f} | Critical Time: {t_crit} | Final Fidelity: {f_final:.4f}")

    # 5. Comparative Plot Generation
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(8, 5))
    
    colors = {'Constant Ohmic': '#d9534f', 'Classical Linear Decay': '#f0ad4e', 'Naressi Geometric Law': '#5cb85c'}
    styles = {'Constant Ohmic': '--', 'Classical Linear Decay': ':', 'Naressi Geometric Law': '-'}
    
    for name in models.keys():
        ax.plot(times, entropy_results[name], label=name, color=colors[name], linestyle=styles[name], linewidth=2.5)

    ax.set_title("Time Evolution of Von Neumann Entropy\nDissipative Models vs Naressi Geometric Law", fontsize=12, fontweight='bold')
    ax.set_xlabel("Normalized Time ($t \cdot \alpha$)", fontsize=11)
    ax.set_ylabel("Von Neumann Entropy $S(t)$", fontsize=11)
    ax.set_ylim(-0.05, 0.75)
    ax.legend(frameon=True, facecolor='white', edgecolor='none', fontsize=10)
    
    plt.tight_layout()
    
    # Saving to Code Ocean mandatory results folder
    os.makedirs('/results', exist_ok=True)
    output_path = '/results/model_comparison_entropy.png'
    plt.savefig(output_path, dpi=300)
    print(f"\nComparison plot successfully saved to: {output_path}")

if __name__ == "__main__":
    # Protected local import of qutip to ensure runtime stability
    import qutip
    run_simulation()
