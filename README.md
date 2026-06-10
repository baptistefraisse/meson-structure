# meson-structure

Meson Structure Analysis  

[The full documentation](https://jeffersonlab.github.io/meson-structure/)

# Post-analysis: Λ-reconstruction and Kaon structure function studies

## Overview

The branch **`analysis/multicalo-lambda`** of the **meson-structure** repository provides a lightweight and user-friendly Python framework to:

- Read reconstructed $\Lambda^0$ candidates from EICrecon outputs  
- Compare reconstructed $\Lambda^0$ to Geant4 truth and afterburner observables  
- Estimate reconstruction efficiencies  
- Produce kinematic maps in $(x_B, Q^2)$ and $(x_K, Q^2)$  
- Propagate statistical uncertainties to the kaon structure function $F_2^K$  
- Evaluate the constraining and discriminating power of EIC data on $F_2^K$ models  

## Physics Scope

- Beam energies: 5×41, 10×100, 18×275 GeV  
- Luminosities: 5, 10, 50 $\mathrm{fb}^{-1}$  
- Reconstruction methods:
  - Truth  
  - Electron  
  - Jacquet–Blondel (JB)  
- Models:
  - Toy models $F^K_2\propto x^a(1-x)^b$
  - Global QCD fits (JAM)  
  - Dyson–Schwinger theory (CoSMAO22)  

## Uncertainty Quantification

The kaon structure function is assumed to scale with the number of reconstructed $\Lambda^0$ hyperons from the Sullivan process:

$$
F_2^K \propto N_\Lambda
$$

The expected yield is:

$$
N_\Lambda = \varepsilon \times \sigma \times L
$$

where:
- $\varepsilon$ is the reconstruction efficiency  
- $\sigma$ is the (differential) cross section  
- $L$ is the integrated luminosity  

Assuming Poisson statistics:

$$
\frac{\Delta F_2^K}{F_2^K}
= \frac{1}{\sqrt{N_\Lambda}}
= \frac{1}{\sqrt{\varepsilon \times \sigma \times L}}
$$

In practice:

$$
\frac{\Delta F_2^K}{F_2^K}
= \sqrt{\frac{N_\Lambda^{\mathrm{simu}}}{N_\Lambda^{\mathrm{reco}} \times \sigma \times L}}
$$

## Models


### Toy Models

A set of simple, physics-inspired toy models is provided to explore sensitivity to different partonic contributions:

- `toy_baseline`  
- `toy_soft_valence`  
- `toy_hard_valence`  
- `toy_sea_enhanced`  
- `toy_su3_breaking`  

These models allow controlled variations of the kaon structure function and serve as benchmarks to:

- Build intuition on the impact of different components (valence vs. sea)  
- Test the sensitivity of EIC projections to specific shape modifications  
- Provide simple reference scenarios for validation 

### Global QCD Fit (JAM)

The framework implements a $\chi^2$-based reweighting of JAM replicas:

- A prior ensemble represents current knowledge  
- Projected EIC uncertainties define a $\chi^2$ for each replica  
- Weights are assigned as $w_i \propto e^{-\chi^2_i/2}$  
- A posterior distribution is obtained  

In addition, **ratio observables** are used to assess model discrimination:

- Ratios are defined with respect to a reference replica  
- Projected EIC uncertainties are propagated to these ratios  
- Model separation is evaluated against expected experimental precision  

### Dyson–Schwinger Approach (CoSMAO22)

Model discrimination is also evaluated using **ratio observables**:

- Structure function ratios are defined with respect to a reference model (e.g. JAM)  
- Projected EIC uncertainties are propagated to these ratios  
- Model separation is assessed against expected experimental precision  

## Input Data: Λ Reconstruction with EICrecon

Input ROOT files must be produced using:

- `reco/lambda-ff-multicalo` branch of EICrecon  

This reconstruction combines multiple far-forward calorimeters:

- EndcapP ECal  
- LFHCAL  
- B0 ECal  
- ZDC HCal  

to reconstruct:

$$
\Lambda^0 \rightarrow n + \gamma_1 + \gamma_2
$$

### Available datasets

```
/work/eic3/users/fraisse/meson-structure/data/
```

### Regeneration from simulation campaigns

Example:

```
/volatile/eic/romanov/meson-structure-2026-02
```

Using:
- container: `eic_xl:25.11-stable`  
- branch: `reco/lambda-ff-multicalo`  

## Running the Analysis

### Configuration

Update paths in:

```
meson-structure/analysis/multicalo-lambda/config.py
```

(Default works on iFarm for the Summer 2025 campaign.)

### Execution

```bash
python -m run --task all --nfiles 1 --suffix test
```

## General Usage

### Command

```bash
python -m run --task <task> [options]
```

### Input files

```
k_lambda_<beam>_5000evt_<idx>_<suffix>.root
```

### Available tasks

- `all`       : full analysis  
- `angles`    : angular distributions  
- `spectra`   : energy spectra  
- `eff`       : efficiencies  
- `kin`       : kinematic maps  
- `relerr`    : statistical uncertainties  
- `replicas`  : replica comparison and reweighting  

### Options

- `--nfiles`      : number of files  
- `--suffix`      : file tag  
- `--beam`        : `5x41`, `10x100`, `18x275`  
- `--bins`        : binning  
- `--lumin-fb`    : luminosity ($\mathrm{fb}^{-1}$)  
- `--logQ2`       : log scale for $Q^2$  
- `--with-beta`   : normalize to neutral branching ratio  
- `--tmax`        : cut on $|t|$ (GeV$^2$)  

## Outputs

All figures are saved in:

```
meson-structure/analysis/multicalo-lambda/outputs/
```

### Examples

- `spectrum_<beam>_<suffix>.png`  
- `kinematics_xB_Q2_<beam>_<suffix>.png`  
- `relerr_xK_Q2_<beam>_<suffix>_L5fb.png`  
- `replica_reduction_<beam>_<suffix>.png`  
- `ratio_models_<beam>_<suffix>.png`  

## TO DO

- [physics] Include systematic uncertainties (e.g. $\Delta\sigma$)  
- [physics] Include kinematic uncertainties (e.g. $\Delta x_K$)  
- [visual] Adopt publication-quality plotting style (ESR)  