#!/usr/bin/env python3
"""
mlcc_calculator.py

Recomputes the multilayer ceramic capacitor (MLCC) design values from the
"Multilayer Capacitor Design" presentation (Taylor, Pizzolato, Shapo — Dec 2025).

Implements:
  - Equation 1: C = eps0 * epsr * A / d              (single-layer capacitance)
  - Total stack capacitance: C_x = sum_i (n_i - 1) * eps0 * k_i * A_i / d_i
  - Parallel-plate electric field: E = V_applied / d_layer

Design parameters (from the "The capacitor design" and "Series Field Equality"
slides):

    Layer   Dielectric   k       A (mm^2)   d (um)   n (layer count)
    y       Y5V          15000   37         3        50
    x       X7R          4600    47         3        20
    c       C0G (NP0)    60      44         120      10

Note: the presentation's FEM simulation reports an equal electric field of
1.66e6 V/m across all three dielectrics at 5 V applied. That value matches
E = V/d for the two thin (3 um) active layers (y, x). The thick 120 um
"c" (C0G) layer is treated in the design as a separate structural/margin
layer, so its E = V_applied / d_layer works out differently under the simple
per-layer formula used here — both this script and the original per-layer
table are included so you can see both views.
"""

from dataclasses import dataclass

EPS0 = 8.854e-12  # vacuum permittivity, F/m


@dataclass
class Layer:
    name: str
    dielectric: str
    k: float       # relative dielectric constant
    area_mm2: float
    thickness_um: float
    n_layers: int

    @property
    def area_m2(self) -> float:
        return self.area_mm2 * 1e-6

    @property
    def thickness_m(self) -> float:
        return self.thickness_um * 1e-6

    def capacitance(self) -> float:
        """(n - 1) * eps0 * k * A / d, per the C_x formula in the slides."""
        return (self.n_layers - 1) * EPS0 * self.k * self.area_m2 / self.thickness_m

    def field(self, v_applied: float) -> float:
        """E = V_applied / d_layer."""
        return v_applied / self.thickness_m


LAYERS = [
    Layer(name="y", dielectric="Y5V", k=15000, area_mm2=37, thickness_um=3, n_layers=50),
    Layer(name="x", dielectric="X7R", k=4600, area_mm2=47, thickness_um=3, n_layers=20),
    Layer(name="c", dielectric="C0G (NP0)", k=60, area_mm2=44, thickness_um=120, n_layers=10),
]

V_APPLIED = 5.0  # volts, per the FEM simulation (+5 V signal plate, 0 V ground plate)


def total_capacitance(layers=LAYERS) -> float:
    return sum(layer.capacitance() for layer in layers)


def report(layers=LAYERS, v_applied=V_APPLIED):
    print(f"{'Layer':<6}{'Dielectric':<12}{'k':>8}{'A (mm^2)':>10}{'d (um)':>8}{'n':>5}"
          f"{'C (uF)':>12}{'E (V/m)':>14}")
    print("-" * 75)
    for layer in layers:
        c_uF = layer.capacitance() * 1e6
        e_field = layer.field(v_applied)
        print(f"{layer.name:<6}{layer.dielectric:<12}{layer.k:>8}{layer.area_mm2:>10}"
              f"{layer.thickness_um:>8}{layer.n_layers:>5}{c_uF:>12.4f}{e_field:>14.3e}")

    c_total_uF = total_capacitance(layers) * 1e6
    print("-" * 75)
    print(f"Total stack capacitance: {c_total_uF:.2f} uF")


if __name__ == "__main__":
    report()
