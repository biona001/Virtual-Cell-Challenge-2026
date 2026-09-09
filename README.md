# Virtual Cell Challenge 2026

+ Website: https://virtualcellchallenge.org/
+ Data suggested by organizers: https://virtualcellchallenge.org/app/datasets
+ Other (processed) publicly available data: https://projects.sanderlab.org/scperturb/datavzrd/scPerturb_vzrd_v1/dataset_info/index_1.html

## Our model ranking

Full record of every submission (method, scores, diagnosis): [results/submissions.md](results/submissions.md). Metric cells show `scaled / raw` values, matching the [live validation leaderboard](https://virtualcellchallenge.org/leaderboard). Ranks are dated snapshots and will change as new submissions arrive. The Description column is a one-line summary; full method notes are kept off-repo.

| Date | Model | Rank | Overall | PDS | MSE | JAC | NMAE | FID | Reach | Description |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| August 21, 2026 | Matched-context NTC bootstrap (seed 2026) | 76 / 104 | −0.2987 | 0.018 / 0.508 | 0.000 / 1.039 | −0.083 / 0.000 | −0.001 / 1.002 | −1.716 / 0.003 | −0.010 / 0.070 | [Details](models/ntc-bootstrap-seed-2026.md) |
| August 30, 2026 | b01A | 213 / 473 | 0.0184 | 0.182 / 0.583 | 0.000 / 1.591 | −0.022 / 0.022 | 0.031 / 0.981 | −0.170 / 0.463 | 0.089 / 0.158 | NB control model + Replogle K562 DE gene sets (~5 genes/target) — [details](results/submissions.md#b01a--august-30-2026) |
| August 31, 2026 | b02 | 168 / 511 | 0.0766 | 0.517 / 0.733 | 0.000 / 3.717 | −0.031 / 0.019 | 0.014 / 0.991 | −0.133 / 0.472 | 0.092 / 0.160 | calibrated NB + full shrunken K562 fold changes (\|z\| > 1) — [details](results/submissions.md#b02--august-31-2026) |
| September 3, 2026 | b03 | 236 | 0.0649 | 0.424 / 0.691 | 0.000 / >1 | −0.029 / 0.020 | 0.044 / 0.973 | −0.138 / 0.471 | 0.088 / 0.157 | b02 + simplex generation; source X-Atlas HEK293T — [details](results/submissions.md#b03--september-3-2026) |
| September 4, 2026 | b04 | 176 | 0.0953 | 0.515 / 0.732 | 0.000 / >1 | −0.024 / 0.021 | 0.042 / 0.975 | −0.085 / 0.484 | 0.123 / 0.181 | same; source X-Atlas HCT116 (best single source) — [details](results/submissions.md#b04--september-4-2026) |
| September 5, 2026 | b05 | 148 | 0.1113 | 0.559 / 0.753 | 0.000 / 4.426 | −0.021 / 0.023 | 0.070 / 0.959 | −0.074 / 0.490 | 0.134 / 0.198 | K562 + HEK293T + HCT116 weighted by control-baseline similarity (τ = 0.01); best so far — [details](results/submissions.md#b05--september-5-2026) |
| September 5, 2026 | b06 | 314 | 0.0357 | 0.487 / 0.721 | 0.000 / 1.695 | −0.035 / 0.018 | 0.050 / 0.971 | −0.377 / 0.400 | 0.089 / 0.158 | b05 × 0.4 amplitude; worse on every metric — [details](results/submissions.md#b06--september-5-2026) |
| September 5, 2026 | b07 | 250 | 0.0772 | 0.432 / 0.696 | 0.000 / 3.789 | −0.013 / 0.026 | 0.018 / 0.989 | −0.063 / 0.494 | 0.088 / 0.158 | single source: resting CD4⁺ T-cell CRISPRi screen — [details](results/submissions.md#b07--september-5-2026) |
| September 7, 2026 | b08 | 197 | 0.1005 | 0.498 / 0.725 | 0.000 / 4.191 | −0.007 / 0.028 | 0.035 / 0.978 | −0.037 / 0.501 | 0.114 / 0.180 | b05's three sources + CD4-T + vcc2025 H1 in one pool; best fid/jac — [details](results/submissions.md#b08--september-7-2026) |
| September 7, 2026 | b09 | 382 | 0.0173 | 0.463 / 0.711 | 0.000 / 1.237 | −0.023 / 0.022 | 0.046 / 0.973 | −0.454 / 0.376 | 0.072 / 0.143 | b05 with injection threshold \|z\| > 3; fid coverage collapsed — [details](results/submissions.md#b09--september-7-2026) |
| September 8, 2026 | b10 | 234 | 0.0914 | 0.560 / 0.753 | 0.000 / 2.433 | −0.029 / 0.020 | 0.067 / 0.960 | −0.155 / 0.466 | 0.106 / 0.172 | b05 with injection threshold \|z\| > 2; pds identical to b05, fid/reach down via coverage — [details](results/submissions.md#b10--september-8-2026) |
| September 8, 2026 | b11 | 116 | 0.1318 | 0.630 / 0.785 | 0.000 / 4.690 | −0.013 / 0.026 | 0.062 / 0.961 | −0.047 / 0.498 | 0.159 / 0.220 | b05 + vcc2025 H1 on its 25 targets + a boosted cross-source consensus head; best so far — [details](results/submissions.md#b11--september-8-2026) |
| September 9, 2026 | p01 (probe) | 350 | 0.0604 | 0.531 / 0.741 | 0.000 / 1.191 | −0.012 / 0.026 | 0.078 / 0.954 | −0.333 / 0.413 | 0.098 / 0.165 | diagnostic, not a candidate: the cross-source consensus head alone (~124 genes per target) with no tail — reads the head's raw mse and precision — [details](results/submissions.md#p01-probe--september-9-2026) |

## Plan

+ Try: Public method (Concept bottleneck models, SquiDiff, models from last year, etc)

+ Find other useful existing single-cell single-gene perturbation datasets.
  
## Important things to consider

+ Is the given cell line from humans?
  + If so, what tissue(s)?
+ Are the cell lines cancerous?
+ Are there DMSO controls (chemical exposure)? Probably not but good to keep in mind

## Existing methods we can try for sampling expression level X~P(x)
| Method | Maturity of software | Software | Pretrained model available? | Normally need to train yourself? |
|---|---|---|---|---|
| **scVI** | Very mature | [scverse/scvi-tools](https://github.com/scverse/scvi-tools) | Yes, some pretrained models are available | Usually yes, especially for dataset-specific applications |
| **scGen** | Mature | [theislab/scgen](https://github.com/theislab/scgen) | Limited; no universal pretrained model | Yes |
| **CPA** | Mature | [theislab/CPA](https://github.com/theislab/CPA) | Some pretrained models for specific datasets | Yes |
| **GEARS** | Mature | [snap-stanford/GEARS](https://github.com/snap-stanford/GEARS) | No universal pretrained model | Yes |
| **CellOT** | Research-quality implementation | [bunnech/cellot](https://github.com/bunnech/cellot) | No universal pretrained model | Yes |
| **scDiffusion** | Research-quality implementation | [EperLuo/scDiffusion](https://github.com/EperLuo/scDiffusion) | Partially; some pretrained components are used, but no universal diffusion model | Yes, typically substantial training |

## Existing methods we may use or adapt for sampling expression level X1~P(x1 | x2) for given expression levels X2=x2
| Method | Maturity of software | Software | Pretrained model available? | Normally need to train yourself? | Can use observed genes to predict/reconstruct other genes? | True conditional sampling \(X_1 \sim P(X_1 \mid X_2)\)? |
|---|---|---|---|---|---|---|
| **scGPT** | Mature | [bowang-lab/scGPT](https://github.com/bowang-lab/scGPT) | **Yes**, pretrained checkpoints are available | Usually fine-tune/adapt rather than train from scratch | **Yes.** Supports masked gene-expression prediction | **Not directly.** Primarily predicts/reconstructs masked expression values |
| **scFoundation** | Mature | [biomap-research/scFoundation](https://github.com/biomap-research/scFoundation) | **Yes**, pretrained weights are available | Usually fine-tune/adapt rather than train from scratch | **Yes.** Supports gene-expression enhancement/reconstruction | **Not directly.** Primarily reconstruction/prediction rather than arbitrary conditional sampling |
| **scVI** | Very mature | [scverse/scvi-tools](https://github.com/scverse/scvi-tools) | Some pretrained models are available | Usually yes for dataset-specific applications | **Indirectly.** Learns a probabilistic latent representation of the full expression profile | **Not out of the box.** Standard scVI does not directly sample an arbitrary subset of genes conditional on the remaining genes |
| **DCA** | Established | [theislab/DCA](https://github.com/theislab/DCA) | No standard universal pretrained model | Yes | **Yes.** Uses the full expression profile to denoise/reconstruct individual genes | **No.** Mainly estimates NB/ZINB distribution parameters and denoised expression |
