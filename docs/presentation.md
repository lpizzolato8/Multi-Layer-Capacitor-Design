# Multilayer Capacitor Design — Presentation Notes

Carley Taylor, Liam Pizzolato, Josh Shapo — December 8, 2025

---

## 1. What is a Multilayer Capacitor?

An MLCC is built from stacked ceramic dielectric layers, each sandwiched between internal electrode layers, terminating in external connecting terminals and a protective coating.

Capacitance of a single layer:

```
C = ε0 εr (d/A)⁻¹ = ε0 εr A/d = dQ/dV
```

(Equation 1: Capacitance of MLCC)

## 2. The Goal of Our Capacitor

- Decoupling capacitor used to filter high-frequency noise out of the power supply
- Steady power supply is vital to board function
- Needed it to be small and have low capacitance

Use case: a small board such as a Raspberry Pi Pico.

## 3. Materials

**Dielectrics**

| Material | Dielectric constant |
|---|---|
| X7R | 4600 |
| Y5V | 15000 |
| C0G (NP0) | 60 |

**Electrodes**

| Element | Symbol | Atomic # | Atomic mass |
|---|---|---|---|
| Copper | Cu | 29 | 63.546 |
| Silver | Ag | 47 | 107.868 |
| Nickel | Ni | 28 | 58.693 |

## 4. Three-Terminal Electrode Layout

With the goal of acoustic noise reduction in mind, a "three-terminal" layout (PWR / GND / PWR) was found to be best for ideal capacitor performance, minimizing the current loop area compared to a standard two-terminal layout (Y. Sun, S. Wu, J. Zhang, C. Hwang and Z. Yang).

## 5. The Capacitor Design

Width allocation across the 1.6 mm active width, split by dielectric fraction f:

```
w_α = f_α · w_act = 1.6 · 0.573 = 0.92 mm
w_β = f_β · w_act = 1.6 · 0.291 = 0.477 mm
w_γ = f_γ · w_act = 1.6 · 0.136 = 0.22 mm
```

Total capacitance:

```
C_x = Σ (n_i - 1) · ε0 · k_i · A_i / d_i     for i = y, x, c
```

| Layer | A (mm²) | d (µm) | n |
|---|---|---|---|
| y | 37 | 3 | 50 |
| x | 47 | 3 | 20 |
| c | 44 | 120 | 10 |

## 6. Field Simulation

- Electric field vectors (red) point from the signal plate (+5 V) toward the ground plate (0 V).
- Heat map gradient of electric potential across the full C0G shell shows a smooth transition from +5 V to 0 V through the thickness.
- A close-up of the Y5V dielectric shows the same style of potential gradient across its thinner layer.

## 7. Series Field Equality

When dielectrics are stacked next to each other in a multilayer capacitor, the electric field throughout each dielectric is equal:

| Dielectric | Electric Field |
|---|---|
| C0G | 1.66×10⁶ V/m |
| Y5V | 1.66×10⁶ V/m |
| X7R | 1.66×10⁶ V/m |

Derivation: `V = E·d → E(V) = V_applied / d_layer`

| Layer | d_layer (µm) | E(V_applied, d_layer) |
|---|---|---|
| y | 3 | V_applied / 3 µm |
| x | 3 | V_applied / 3 µm |
| c | 120 | V_applied / 120 µm |

## 8. State of the Art of Capacitors

University of Sheffield — *Development of High Energy Density Multilayer Ceramic Capacitors* (Jul 16, 2025), Functional Materials and Devices Group:

- Prototype testing of new PbO-free (lead-free) MLCCs with higher operating voltage and energy storage density, without compromising temperature stability.
- Applications in EVs — more than 10,000 MLCCs are used per electric car.
- Lead-free design makes them more suitable for consumer electronics.

## 9. Conclusion

**Orientation notes:** A vertical orientation of the capacitor has been found to reduce parallel resonances, assisting in performance results.

**Room for growth:** With more time, cost-effectiveness of the capacitor design could be evaluated.

---

See [`sources.md`](../sources.md) for full references.
