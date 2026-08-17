from decimal import Decimal, getcontext
import math
import cmath
import numpy as np

getcontext().prec = 28

# =====================================================================
# JCR KERNEL DIVISION BRIDGE (shared constants)
# =====================================================================
class KernelDivisionBridge:
    def __init__(self):
        self.psi        = Decimal('0.1503378808')
        self.Re_tau     = Decimal('1.4129651365')
        self.cos_psi    = Decimal('0.9887205')
        self.sin_Re_tau = Decimal('0.98768834059')

        self.numerator = self.cos_psi * self.Re_tau
        self.K         = self.numerator / self.sin_Re_tau
        self.k_norm    = Decimal(1) / self.K

        print("=== JCR KERNEL DIVISION BRIDGE ===")
        print(f"ψ          = {float(self.psi):.10f}")
        print(f"Re(τ)      = {float(self.Re_tau):.10f}")
        print(f"K          = {float(self.K):.10f}")
        print(f"k_norm     = {float(self.k_norm):.10f}\n")


# =====================================================================
# COSMOLOGICAL CLOCK  →  GEOMETRIC PRESSURE
# =====================================================================
class CosmologicalClockGeometricPressure:
    """
    Geometric pressure is produced by the Cosmological Clock e-fold
    a(N) = exp(ε · N) together with the +90° counter-clockwise imaginary bias.
    """

    def __init__(self, bridge: KernelDivisionBridge = None):
        self.bridge   = bridge or KernelDivisionBridge()
        self.epsilon  = 1e-9
        self.N_max    = 1_000_000_000          # present-day epoch

    # ----- Cosmological Clock e-fold (the definition) -----
    def scale_factor(self, N: float) -> float:
        """a(N) = exp(ε · N)  ← the e-fold that generates geometric pressure"""
        return math.exp(self.epsilon * N)

    # ----- +90° counter-clockwise imaginary bias -----
    def imaginary_bias_90deg(self, N: float) -> complex:
        """
        Positive imaginary unit rotates the real sine by +90°
        (counter-clockwise). This fixes the direction of the pressure.
        """
        theta = 2.0 * math.pi * N * self.epsilon
        return 1j * math.sin(theta)

    # ----- Geometric pressure -----
    def geometric_pressure(self, N: float) -> complex:
        """
        Geometric pressure = Cosmological Clock e-fold oriented by the
        +90° counter-clockwise bias.
        """
        a = self.scale_factor(N)                 # e-fold
        bias = self.imaginary_bias_90deg(N)     # direction

        # Pressure magnitude is the Clock scale factor;
        # direction remains pure positive-imaginary (+90°)
        pressure_magnitude = a
        return 1j * pressure_magnitude

    # ----- Combined cosmological state -----
    def cosmic_state(self, N: float) -> complex:
        """
        Full state vector:
          real part  → linear accrual (or scale-related)
          imag part  → geometric pressure from the Clock e-fold
        """
        y = N * self.epsilon
        pressure = self.geometric_pressure(N)
        return complex(y, pressure.imag)

    # ----- Convenience: present-day values -----
    def present_day(self):
        N = self.N_max
        a = self.scale_factor(N)
        P = self.geometric_pressure(N)
        z = self.cosmic_state(N)
        return {
            "N": N,
            "a(N)": a,                     # ≈ e
            "geometric_pressure": P,
            "cosmic_state": z,
            "phase_bias": 2 * math.pi * N * self.epsilon  # = 2π
        }


# =====================================================================
# DEMONSTRATION
# =====================================================================
if __name__ == "__main__":
    bridge = KernelDivisionBridge()
    clock  = CosmologicalClockGeometricPressure(bridge)

    print("=" * 78)
    print("  GEOMETRIC PRESSURE FROM THE COSMOLOGICAL CLOCK E-FOLD")
    print("  a(N) = exp(ε·N)   +   +90° counter-clockwise bias")
    print("=" * 78)
    print(f"{'N':>12}   {'a(N)':>12}   {'Pressure':>22}   {'|z|':>10}")
    print("-" * 78)

    milestones = [0, 250_000_000, 500_000_000, 750_000_000, 1_000_000_000]

    for N in milestones:
        a = clock.scale_factor(N)
        P = clock.geometric_pressure(N)
        z = clock.cosmic_state(N)
        print(f"{N:12,d}   {a:12.6f}   {str(P):>22}   {abs(z):10.6f}")

    print("\n" + "=" * 78)
    print("  PRESENT-DAY SUMMARY (N = 10⁹)")
    print("=" * 78)
    today = clock.present_day()
    for k, v in today.items():
        print(f"{k:<22}: {v}")
    print("=" * 78)
