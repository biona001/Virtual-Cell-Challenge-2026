# Matched-context NTC bootstrap (seed 2026)

## Description

This submission is the initial null baseline. For every context–perturbation pair, it samples 400 non-targeting control cells with replacement from the matched context. Each sampled cell's raw expression counts are copied unchanged and labelled with the target perturbation.

The baseline therefore assumes that every knockdown behaves exactly like an untreated cell from the same context. It establishes a performance floor for models that attempt to predict perturbation-specific effects.

## Reproduction

- Random seed: `2026`
- Submission ID: `CGbdzCOTvHYYGIYWQQLA`
- Builder: [`scripts/build_ntc_bootstrap.py`](../scripts/build_ntc_bootstrap.py)
- Submitted: August 21, 2026

