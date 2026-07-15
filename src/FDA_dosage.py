import numpy as np
import matplotlib.pyplot as plt

def run_pk_simulation():
    # 1. Timeline configuration (24-hour window)
    t = np.linspace(0, 24, 1000)
    
    # 2. Physiological & Kinetic Assumptions 
    V_d = 50.0   # Apparent Volume of Distribution (L)
    k_a = 1.2    # First-order absorption coefficient (hr^-1)
    k_e = 0.3    # First-order elimination coefficient (hr^-1)
    MTC = 10.0   # Toxicity threshold line (mg/L)
    
    # 3. Bioavailability weights
    F_standard = 0.01  # Raw botanical control line
    F_haldex = 0.20    # Piperine-assisted absorption factor
    
    # 4. Bateman Pharmacokinetic Equation
    def bateman(F, D):
        return ((F * D * k_a) / (V_d * (k_a - k_e))) * (np.exp(-k_e * t) - np.exp(-k_a * t))
    
    # 5. Execute calculations across test ranges
    c_std_7800 = bateman(F_standard, 7800)
    c_hal_1950 = bateman(F_haldex, 1950)
    c_hal_3900 = bateman(F_haldex, 3900)
    c_hal_7800 = bateman(F_haldex, 7800)
    
    # 6. Build the visual output
    plt.figure(figsize=(10, 6))
    plt.axhline(y=MTC, color='red', linestyle='--', linewidth=2, label='Minimum Toxic Concentration (MTC)')
    
    plt.plot(t, c_hal_1950, color='green', label='HaldEX 1950mg (1 Cap - Safe Margin)')
    plt.plot(t, c_hal_3900, color='orange', label='HaldEX 3900mg (2 Caps - Borderline Threshold)')
    plt.plot(t, c_hal_7800, color='darkred', label='HaldEX 7800mg (4 Caps - Severe Overdose)')
    plt.plot(t, c_std_7800, color='blue', linestyle=':', label='Raw Unenhanced Turmeric (7800mg)')
    
    plt.title('HaldEX 1950mg 24-Hour Plasma Accumulation Simulation', fontsize=12, fontweight='bold')
    plt.xlabel('Hours Since Intake')
    plt.ylabel('Plasma Level (mg/L)')
    plt.xlim(0, 24)
    plt.grid(True, alpha=0.4)
    plt.legend()
    
    # Save directly to workspace directory
    plt.savefig('haldex_pk_simulation.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    run_pk_simulation()
