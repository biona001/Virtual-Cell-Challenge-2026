# Submission record

One section per leaderboard submission (validation leaderboard, contexts A/B/C). Scores are given as
`scaled / raw`, matching the leaderboard; scaled = (value − baseline) / (replicate − baseline) per context,
overall = mean of the six scaled metrics. Ranks are snapshots at publication time. The score table in the
[README](../README.md) is the short view of this file.

## Matched-context NTC bootstrap (seed 2026) — August 21, 2026
Rank 76 / 104 · overall **−0.2987** · entry `CGbdzCOTvHYYGIYWQQLA` · details in [models/ntc-bootstrap-seed-2026.md](../models/ntc-bootstrap-seed-2026.md)

| pds | mse | jac | nmae | fid | reach |
|---|---|---|---|---|---|
| 0.018 / 0.508 | 0.000 / 1.039 | −0.083 / 0.000 | −0.001 / 1.002 | −1.716 / 0.003 | −0.010 / 0.070 |

Null baseline: 400 control cells resampled per target, copied unchanged. Establishes the floor; note that
even this scores raw mse 1.039, above the baseline anchor (~0.99), so mse is clamped to 0 for it.

## b01A — August 30, 2026
Rank 213 / 473 · overall **0.0184** · entry id not recorded (submitted manually from the server)

| pds | mse | jac | nmae | fid | reach |
|---|---|---|---|---|---|
| 0.182 / 0.583 | 0.000 / 1.591 | −0.022 / 0.022 | 0.031 / 0.981 | −0.170 / 0.463 | 0.089 / 0.158 |

Negative-binomial control model fit on each context's controls; injected effects = Replogle K562
(genome-wide CRISPRi) DE gene sets, only a few genes per target (272/300 targets covered). Diagnosis
afterwards: the noise model double-counted the library-size variance, so ~436 spurious "down" calls per
target appeared with only ~5 genes injected.

## b02 — August 31, 2026
Rank 168 / 511 · overall **0.0766** · entry `xxOfLsSjxpyvy2pvSvNT`

| pds | mse | jac | nmae | fid | reach |
|---|---|---|---|---|---|
| 0.517 / 0.733 | 0.000 / 3.717 | −0.031 / 0.019 | 0.014 / 0.991 | −0.133 / 0.472 | 0.092 / 0.160 |

Depth-calibrated NB control model (dispersion conditional on library size; 400 null cells trigger ~1 spurious
call); full shrunken log-fold-change vectors sourced from Replogle K562, every gene with test |z| > 1
(~2,500 genes/target, 272/300 targets). Gain over b01A entirely from pds.

## b03 — September 3, 2026
Rank 236 · overall **0.0649**

| pds | mse | jac | nmae | fid | reach |
|---|---|---|---|---|---|
| 0.424 / 0.691 | 0.000 / >1 | −0.029 / 0.020 | 0.044 / 0.973 | −0.138 / 0.471 | 0.088 / 0.157 |

Same generator as b02 plus simplex-normalized generation (per-cell gene shares renormalized so the target's
knocked-down mass is redistributed); effects sourced from X-Atlas/Orion **HEK293T** (300/300 targets).
Worst single source, consistent with HEK293T ranking last in control-baseline similarity to every context.

## b04 — September 4, 2026
Rank 176 · overall **0.0953**

| pds | mse | jac | nmae | fid | reach |
|---|---|---|---|---|---|
| 0.515 / 0.732 | 0.000 / >1 | −0.024 / 0.021 | 0.042 / 0.975 | −0.085 / 0.484 | 0.123 / 0.181 |

Same generator as b03; effects sourced from X-Atlas/Orion **HCT116** (colon carcinoma, 300/300 targets).
Best single source: HCT116 > K562 > HEK293T.

## b05 — September 5, 2026
Rank 148 · overall **0.1113** · entry `Nh5Lmz1UuxKUNOzRycjI` · **best score so far**

| pds | mse | jac | nmae | fid | reach |
|---|---|---|---|---|---|
| 0.559 / 0.753 | 0.000 / 4.426 | −0.021 / 0.023 | 0.070 / 0.959 | −0.074 / 0.490 | 0.134 / 0.198 |

Same generator as b04; effects combined from three sources (Replogle K562, X-Atlas HEK293T, X-Atlas HCT116)
per target and context, weighted by the control-baseline similarity between source and context
(softmax of Pearson on log1p mean CPM, τ = 0.01 ≈ a near-hard pick: K562 leads context A, HCT116 leads B and C),
per-gene renormalization over the sources that measured each gene. About 7,100 genes injected per target;
the scorer calls ~560–900 of them.

## b06 — September 5, 2026
Rank 314 · overall **0.0357** · entry `7K4xYSRj5yAEDIGId75N`

| pds | mse | jac | nmae | fid | reach |
|---|---|---|---|---|---|
| 0.487 / 0.721 | 0.000 / 1.695 | −0.035 / 0.018 | 0.050 / 0.971 | −0.377 / 0.400 | 0.089 / 0.158 |

b05 with a global attenuation of the injected effects (×0.4). Worse on every metric: raw mse fell from 4.43
to 1.69 but stayed above the clamp, and the scorer's call sets shrank ~8× (to ~110 genes per target), which
collapsed fid through its coverage term. Global amplitude dropped as a lever.

## b07 — September 5, 2026
Rank 250 · overall **0.0772** · entry `mcpq6FqWvRp4eULwapwK`

| pds | mse | jac | nmae | fid | reach |
|---|---|---|---|---|---|
| 0.432 / 0.696 | 0.000 / 3.789 | −0.013 / 0.026 | 0.018 / 0.989 | −0.063 / 0.494 | 0.088 / 0.158 |

Same generator as b04; effects sourced from the resting CD4⁺ T-cell CRISPRi screen (Dann et al. 2026,
GSE314342, 10x Flex, 4 donors) as a single source for all contexts (297/300 targets; a 20-cell guard leaves
ABCD1, NICN1, C5orf22 uninjected). Below HCT116 despite the higher raw control-baseline similarity, which is
mostly a platform effect (Flex vs droplet); resting primary T cells lack the proliferation response modules
that dominate pds in dividing lines.

## b08 — September 7, 2026
Rank 197 · overall **0.1005**

| pds | mse | jac | nmae | fid | reach |
|---|---|---|---|---|---|
| 0.498 / 0.725 | 0.000 / 4.191 | −0.007 / 0.028 | 0.035 / 0.978 | −0.037 / 0.501 | 0.114 / 0.180 |

Same generator as b05; five sources in one pool (b05's three + the CD4⁺ T-cell screen + vcc2025 H1 hESC) with
the same similarity weights (τ = 0.01) and a 20-cell guard per source and target. Because the two Flex sources
out-rank every droplet source in raw similarity, the pool resolves to CD4-T for context A, H1 for its 25
covered targets in B and C, CD4-T for the other 269, and the droplet sources on 6 fallback targets.
Best fid and jac of all submissions (H1's 25 targets); pds, reach and nmae between b07 and b05.

## b09 — September 7, 2026
Rank 382 at publication (390 a day later) · overall **0.0173**

| pds | mse | jac | nmae | fid | reach |
|---|---|---|---|---|---|
| 0.463 / 0.711 | 0.000 / 1.237 | −0.023 / 0.022 | 0.046 / 0.973 | −0.454 / 0.376 | 0.072 / 0.143 |

b05 with a single change: only source genes with test \|z\| > 3 are injected (about 140 genes per target
instead of 7,000), motivated by the finding that 85–90 % of the \|z\| > 1 set is chance for the droplet
sources. Diagnosis: the scorer then calls only 40–84 genes per target, below the truth's typical call set
(median ~134 with a heavy tail), so fid's coverage term (fid = sign precision × min(1, calls / truth calls))
collapses; the discarded \|z\| 1–3 band also carried most of the real signal by count, so pds, reach and nmae
fell while jac did not move. mse is clamped to 0 for every member of this family, silence included, so the
mse motivation could never register. Selection by evidence is not a lever for this pipeline; a smaller
threshold (\|z\| > 2 or 2.5) sits on the same monotone curve and is not planned. The raw values confirm the
reading: fid 0.376 and pds 0.711 match the coverage arithmetic (predicted 0.37 and 0.71), and raw mse fell
from 4.43 to 1.24 with 98 % fewer injected genes yet stayed above the baseline anchor (~0.99), so the
injected effects still carry no gene-level agreement with the truth and mse remains out of reach.
