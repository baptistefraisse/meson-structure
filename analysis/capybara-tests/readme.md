# Capybara MT/ST Reproducibility Test

This script is intended to investigate potential non-deterministic behavior in EICrecon by comparing repeated multi-threaded reconstructions against a single-threaded reference reconstruction using Capybara.

## Requirements

Before running the test, make sure that:

- The EIC software environment is set up.
- The ePIC geometry is sourced.
- EICrecon is sourced and available in your `PATH`.
- Capybara is available in your `PATH`.

## Usage

```bash
python stress_st_vs_mt.py input-file.edm4hep.root [options]
```

Example:

```bash
python stress_st_vs_mt.py sim_dis_18x275_minQ2=1000_craterlake_18x275.edm4hep.root -n 100 -j 4
```

The script first reconstructs the input file once in single-thread mode. It then repeatedly reconstructs the same file in multi-thread mode and compares the resulting collections against the single-thread reference using Capybara.

The test stops immediately if a difference is found.

## Options

| Option | Description | Default |
|----------|-------------|----------|
| `-n`, `--runs` | Number of multi-thread reconstruction runs to perform | `20` |
| `-j`, `--threads` | Number of threads used for multi-thread reconstruction | `4` |
| `-o`, `--outdir` | Output directory for reconstructed files, logs, and reports | `stress_st_vs_mt` |
| `--tmpdir` | Optional temporary directory used during reconstruction | System default |
| `-m`, `--collection` | Collection to compare with Capybara. Can be specified multiple times | Default collections |

## Default Collections

If no collection is specified, the following collections are compared:

- `ReconstructedHcalFarForwardZDCNeutrals`
- `ReconstructedLFHCALNeutrals`

Custom collections can be selected, for example:

```bash
python stress_st_vs_mt.py input.edm4hep.root \
    -m ReconstructedHcalFarForwardZDCNeutrals \
    -m ReconstructedLFHCALNeutrals
```

## Output

The script creates:

- A single-thread reference reconstruction.
- One multi-thread reconstruction per iteration.
- Reconstruction logs.
- Capybara comparison reports.
- A `first_failure.txt` file if a discrepancy is detected.

When a difference is found, the script prints the Capybara output and exits immediately.

## Input Files

The input files used during the original investigation, in particular

```text
sim_dis_18x275_minQ2=1000_craterlake_18x275.edm4hep.root
```

are available as workflow artifacts from the following GitHub Actions run:

https://github.com/eic/EICrecon/actions/runs/26528753188