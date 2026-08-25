# Multilayer Capacitor Design

A decoupling (MLCC) capacitor design project for filtering high-frequency noise from a power supply — sized for a small board (Raspberry Pi Pico use case).

## Overview

A Multilayer Ceramic Capacitor (MLCC) is built from alternating ceramic dielectric layers and metal electrode layers, connected at two (or three) external terminals. This project designs a three-dielectric-layer MLCC stack combining three common dielectric materials, computes each layer's contribution to total capacitance, and simulates the resulting electric field/potential distribution.

Goals for the capacitor:
- Decouple / filter high-frequency noise from the power supply
- Support a steady, reliable power supply (critical to board function)
- Be physically small while keeping capacitance low and controlled

See [`docs/presentation.md`](docs/presentation.md) for the full slide content this repo is based on, and [`src/mlcc_calculator.py`](src/mlcc_calculator.py) for the capacitance/electric-field model.

## Design Summary

**Materials**

| Layer | Dielectric | Dielectric constant (k) |
|---|---|---|
| y | Y5V | 15000 |
| x | X7R | 4600 |
| c | C0G (NP0) | 60 |

Electrodes: Copper, Silver, Nickel.

**Three-terminal electrode layout** was chosen over a standard two-terminal layout because it reduces the current loop area, which reduces acoustic/vibrational noise while maintaining ideal capacitor performance (Sun, Wu, Zhang, Hwang & Yang, 2020).

**Stack geometry**

| Layer | Area A (mm²) | Layer thickness d (µm) | # of layers n |
|---|---|---|---|
| y (Y5V) | 37 | 3 | 50 |
| x (X7R) | 47 | 3 | 20 |
| c (C0G) | 44 | 120 | 10 |

Width scaling (relative to total active width, 1.6 mm total footprint):
- w_α = 0.92 mm
- w_β = 0.477 mm
- w_γ = 0.22 mm

**Governing equations**

Capacitance of a single dielectric layer stack:

```
C = ε0 εr (A / d) = dQ / dV
```

Total capacitance across the multilayer stack:

```
C_x = Σ (n_i - 1) · ε0 · k_i · A_i / d_i     for i = y, x, c
```

Electric field within a parallel-plate layer:

```
E = V / d
```

Because the dielectric layers are stacked in the same series current path, the electric field magnitude is equal across each dielectric (~1.66×10⁶ V/m at +5 V applied, per the FEM simulation results in the slides).

## Simulation

Electric field and potential were simulated (COMSOL-style FEM) across the stack:
- Electric field vectors point from the +5 V signal plate toward the 0 V ground plate.
- Electric potential heat maps show a smooth gradient from signal to ground across each dielectric (C0G, Y5V shown in the slides).
- All three dielectrics (C0G, Y5V, X7R) showed the same field magnitude (1.66×10⁶ V/m) when stacked in series, confirming the series relationship `E = V_applied / d_layer`.

## State of the Art

Recent MLCC research (University of Sheffield, Functional Materials and Devices Group, 2025) is developing PbO-free (lead-free) MLCCs with higher operating voltage and energy density without sacrificing temperature stability — relevant for EV applications (10,000+ MLCCs per electric vehicle) and for making lead-free designs more suitable for consumer electronics.

## Conclusion

- **Orientation matters:** mounting the capacitor vertically has been shown to reduce parallel resonances, improving performance.
- **Room for growth:** a follow-up could evaluate the cost-effectiveness of the design (material and manufacturing cost vs. performance).

## Repo Structure

```
mlcc-design/
├── README.md              # this file
├── docs/
│   └── presentation.md    # full slide-by-slide content
├── src/
│   └── mlcc_calculator.py # capacitance / electric field calculator (from slide equations)
└── sources.md              # full reference list
```

## Usage

```bash
python3 src/mlcc_calculator.py
```

This recomputes total stack capacitance and per-layer electric field from the design parameters in the tables above.

## Sources

See [`sources.md`](sources.md) for the full reference list (11 sources, IEEE style).
