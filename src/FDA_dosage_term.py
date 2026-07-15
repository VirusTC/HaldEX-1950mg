import numpy as np
import matplotlib.pyplot as plt

def run_washout_simulation():
    # 1. Timeline configuration (72h dosing + 48h elimination loop = 120h)
    t_max = 120.0
    dt = 0.01
    t = np.arange(0, t_max + dt, dt)
    n_steps = len(t)
    
    # 2. Kinetic Assumptions
    V_d = 50.0       # Apparent volume of distribution (L)
    k_a = 1.2        # First-order absorption coefficient (hr^-1)
    k_e = 0.3        # First-order elimination coefficient (hr^-1)
    F_haldex = 0.20  # High bioavailability factor
    
    tau = 8.0          # Time between doses (Hours)
    dose_mass = 1950.0 # Single capsule mass (mg)
    
    X_gi = np.zeros(n_steps)
    X_p = np.zeros(n_steps)
    
    # 3. Execution loop
    for i in range(1, n_steps):
        current_time = t[i-1]
        
        # Administer doses strictly up to day 3 (72 hours max)
        if current_time <= 72.0:
            if i == 1 or (current_time > 0 and np.isclose(current_time % tau, 0, atol=dt/2)):
                X_gi[i-1] += F_haldex * dose_mass
                
        dX_gi = -k_a * X_gi[i-1] * dt
        dX_p = (k_a * X_gi[i-1] - k_e * X_p[i-1]) * dt
        
        X_gi[i] = max(0, X_gi[i-1] + dX_gi)
        X_p[i] = max(0, X_p[i-1] + dX_p)
        
    C_t = X_p / V_d
    
    # 4. Filter output for visual focus
    plt.figure(figsize=(10, 6))
    plt.plot(t, C_t, color='darkgreen', label='Plasma Level (mg/L)')
    plt.axvline(x=72.0, color='darkred', linestyle=':', label='Cessation of Treatment (72h)')
    
    plt.title('HaldEX 1950mg Complete 48-Hour Washout Tracking', fontsize=12, fontweight='bold')
    plt.xlabel('Hours Elapsed')
    plt.ylabel('Plasma Level (mg/L)')
    plt.xlim(60, 120)  # Focus visualization zoom on washout area
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('haldex_washout_simulation.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    run_washout_simulation()
