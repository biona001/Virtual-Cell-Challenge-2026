# Virtual Cell Challenge 2026

+ Website: https://virtualcellchallenge.org/
+ Data suggested by organizers: https://virtualcellchallenge.org/app/datasets
+ Other (processed) publicly available data: https://projects.sanderlab.org/scperturb/datavzrd/scPerturb_vzrd_v1/dataset_info/index_1.html

## Our model ranking

Metric cells show `raw / scaled` values, matching the [live validation leaderboard](https://virtualcellchallenge.org/leaderboard). Ranks are dated snapshots and will change as new submissions arrive.

| Date | Model | Rank | Overall | PDS | MSE | JAC | NMAE | FID | Reach | Description |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| August 21, 2026 | Matched-context NTC bootstrap (seed 2026) | 76 / 104 | −0.2987 | 0.508 / 0.018 | 1.039 / 0.000 | 0.000 / −0.083 | 1.002 / −0.001 | 0.003 / −1.716 | 0.070 / −0.010 | [Details](models/ntc-bootstrap-seed-2026.md) |

## Plan

+ Model 1: Assume perturbation has no effect at all, so each perturbation is a random NTC cell
+ Model 2: Search existing CRISPRi data for the best matched NTC, and hope that data have the 300 targets perturbed
+ Model 3: Public method (Concept bottleneck models, SquiDiff, models from last year, etc)
+ Model 4: Our own thing

+ Find other existing single-cell single-gene perturbation datasets, the public ones listed on the VCC website cover only 272 targeting-genes.
  
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

## Existing methods we can try for sampling expression level X1~P(x1 | x2) for given expression levels X2=x2
| Method | Maturity of software | Software | Pretrained model available? | Normally need to train yourself? | Directly models/samples \(P(X_1 \mid X_2)\)? |
|---|---|---|---|---|---|
| **VAEAC** | Established research implementation | [tigvarts/vaeac](https://github.com/tigvarts/vaeac) | No general pretrained model | Yes | **Yes.** Designed for arbitrary conditioning: observe any subset of variables and sample the remaining variables |
| **ACFlow** | Established research implementation | [lupalab/ACFlow](https://github.com/lupalab/ACFlow) | Some pretrained models for benchmark datasets, but not gene expression | Yes | **Yes.** Explicitly models arbitrary conditional distributions \(p(x_u \mid x_o)\) |
| **MIWAE** | Established research implementation | [pamattei/miwae](https://github.com/pamattei/miwae) | No general pretrained model | Yes | **Approximately.** Designed for probabilistic imputation of missing variables using a latent-variable model |
| **TabDiff** | Modern research implementation | [MinkaiXu/TabDiff](https://github.com/MinkaiXu/TabDiff) | No general pretrained gene-expression model | Yes | **Yes/approximately.** Diffusion-based conditional generation can generate missing variables conditional on observed variables |
| **scGPT** | Mature single-cell foundation-model implementation | [bowang-lab/scGPT](https://github.com/bowang-lab/scGPT) | **Yes**, pretrained checkpoints are available | Usually fine-tune/adapt rather than train from scratch | **Partially.** Supports masked gene-expression prediction, but is not primarily an arbitrary conditional sampler |
| **scFoundation** | Mature single-cell foundation-model implementation | [biomap-research/scFoundation](https://github.com/biomap-research/scFoundation) | **Yes**, pretrained models are available | Usually fine-tune/adapt rather than train from scratch | **Partially.** Supports gene-expression reconstruction/prediction, but is not a direct arbitrary conditional sampler |
