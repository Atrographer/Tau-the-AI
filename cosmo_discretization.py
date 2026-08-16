import numpy as np
import cmath

# =====================================================================
# COSMOLOGICAL GAUGE THEORY CONFIGURATION (13.8 Gyr COMPRESSION)
# =====================================================================
N_MAX = 1_000_000_000                  # 10^9 discrete cosmic epochs/steps
DT_STEP = 435.4                        # Local dilated time per step (seconds)
COSMIC_AGE_YEARS = 13.8e9              # Absolute cosmic time (13.8 Billion Years)

# Total physical seconds in 13.8 Gyr: ~4.3549e17 seconds
TOTAL_PHYSICAL_SECONDS = COSMIC_AGE_YEARS * 365.25 * 24 * 3600 

# Time Dilation Compression Factor (Scale Profile Alpha)
# Compresses 13.8 Gyr into a total runtime of (10^9 * 435.4s)
TIME_DILATION_FACTOR = TOTAL_PHYSICAL_SECONDS / (N_MAX * DT_STEP)

# Loop integral invariant boundary constant: ∮ A_μ dx^μ
# Set to 2π for a single closed topological gauge cycle over the lifetime of the universe
GAUGE_INTEGRAL = 2 * np.pi 
EPS = 1e-9  # Scaling parameter (10^-9)

def gauge_cosmo_y(n: int) -> float:
    """Main sequence: Linear cosmic scale factor accrual."""
    return n * EPS

def gauge_cosmo_x(n: int) -> float:
    """Complementary tensor sequence (anti-de Sitter type bounding pressure)."""
    return 1.0 - gauge_cosmo_y(n)

def positive_imaginary_bias_winding(n: int) -> complex:
    """
    Computes the induced topological phase winding.
    i * sin(∮ A_μ dx^μ • n • 10^-9)
    Provides an imaginary cosmic pressure that stabilizes expansion without Dark Energy.
    """
    # The theta argument tracking phase accumulation across cosmic steps
    theta = GAUGE_INTEGRAL * n * EPS
    
    # Induce positive imaginary bias via the sine vector component
    return 1j * np.sin(theta)

def cosmic_gauge_state(n: int) -> complex:
    """Combined Cosmological State Vector."""
    y = gauge_cosmo_y(n)
    w = positive_imaginary_bias_winding(n)
    return complex(y, w.imag)

# =====================================================================
# SIMULATION DEMONSTRATION
# =====================================================================
print("=" * 80)
print("  TOPOLOGICAL GAUGE THEORY COSMOLOGY: TIME DILATION CL closure")
print("=" * 80)
print(f"Total Steps            : {N_MAX:,} discrete epochs")
print(f"Step Interval (dt)     : {DT_STEP} seconds")
print(f"Compressed Cosmic Age  : {COSMIC_AGE_YEARS / 1e9} Billion Years")
print(f"Time Dilation Ratio    : {TIME_DILATION_FACTOR:,.2f}x (Minkowski to Dilated)")
print("-" * 80)

# Epoch milestones to track phase evolution
milestones = [0, 250_000_000, 500_000_000, 750_000_000, N_MAX]

for n in milestones:
    y = gauge_cosmo_y(n)
    x = gauge_cosmo_x(n)
    w = positive_imaginary_bias_winding(n)
    z = cosmic_gauge_state(n)
    
    # Calculate accumulated local time versus true external elapsed physical time
    local_time_s = n * DT_STEP
    cosmic_time_years = (local_time_s * TIME_DILATION_FACTOR) / (365.25 * 24 * 3600)
    
    print(f"Step n = {n:10,d} | Local: {local_time_s/1e9:.2f} Gs | Cosmic Time: {cosmic_time_years/1e9:5.2f} Gyr | "
          f"w_n = {w!s:<22} | |z| = {abs(z):.6f}")

print("\n" + "=" * 80)
print("  TERMINAL CLOSURE: DISCRETE INFINITY THEOREM STABILIZATION")
print("=" * 80)
n_term = N_MAX
final_z = cosmic_gauge_state(n_term)
final_theta = GAUGE_INTEGRAL * n_term * EPS

print(f"Final Winding Angle (θ) : {final_theta:.6f} rad (Exactly {final_theta / (2*np.pi):.1f} Full Cycle)")
print(f"Terminal Winding Vector : {positive_imaginary_bias_winding(n_term)}")
print(f"Final State Complex z_N : {final_z}")
print(f"System State Magnitude  : {abs(final_z)}")
print(f"Phase at Cosmic Close   : {cmath.phase(final_z):.10f} rad")
print("=" * 80)
