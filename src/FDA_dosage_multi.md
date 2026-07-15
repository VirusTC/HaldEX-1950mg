import numpy as np
import matplotlib.pyplot as plt

def run_multiday_simulation():
    # 1. Timeline configuration (72 hours divided by fine-grained time steps)
    t_max = 72.0
    dt = 0.01
    t = np.arange(0, t_max + dt, dt)
    n_steps = len(t)
    
    # 2. Pharmacokinetic properties
    V_d = 50.0       # Apparent volume of distribution (L)
    k_a = 1.2        # First-order absorption coefficient (hr^-1)
    k_e = 0.3        # First-order elimination coefficient (hr^-1)
    F_haldex = 0.20  # High bioavailability factor (Piperine enhanced)
    MTC = 10.0       # Minimum Toxic Concentration threshold (mg/L)
    
    # 3. Dosage schedule parameters
    tau = 8.0          # Time between doses (Hours)
    dose_mass = 1950.0 # Standard single-capsule intake mass (mg)
    
    # 4. State vector allocation
    X_gi = np.zeros(n_steps) # Mass inside the Gastrointestinal tract
    X_p = np.zeros(n_steps)  # Mass inside Blood Plasma compartment
    
    # 5. Continuous Euler simulation loop
    for i in range(1, n_steps):
        current_time = t[i-1]
        
        # Administer dose at t=0, 8, 16, 24, 32, 40, 48, 56, 64 hours
        if i == 1 or (current_time > 0 and np.isclose(current_time % tau, 0, atol=dt/2)):
            X_gi[i-1] += F_haldex * dose_mass
            
        # Determine metabolic rate shifts
        dX_gi = -k_a * X_gi[i-1] * dt
        dX_p = (k_a * X_gi[i-1] - k_e * X_p[i-1]) * dt
        
        # Commit steps
        X_gi[i] = max(0, X_gi[i-1] + dX_gi)
        X_p[i] = max(0, X_p[i-1] + dX_p)
        
    # 6. Convert tracking arrays to concentration profiles
    C_t = X_p / V_d
    
    # 7. Generate output asset
    plt.figure(figsize=(10, 6))
    plt.axhline(y=MTC, color='red', linestyle='--', label='Minimum Toxic Concentration (MTC)')
    plt.plot(t, C_t, color='darkgreen', linewidth=2, label='HaldEX 1950mg (1 Cap every 8 Hours)')
    
    plt.title('HaldEX 1950mg 72-Hour Accumulation Simulation', fontsize=12, fontweight='bold')
    plt.xlabel('Hours Elapsed')
    plt.ylabel('Plasma Level (mg/L)')
    plt.xlim(0, 72)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('haldex_72h_accumulation.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    run_multiday_simulation()
