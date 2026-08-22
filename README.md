# Virtual Cell Challenge 2026

+ Website: https://virtualcellchallenge.org/
+ Data suggested by organizers: https://virtualcellchallenge.org/app/datasets
+ Other (processed) publicly available data: https://projects.sanderlab.org/scperturb/datavzrd/scPerturb_vzrd_v1/dataset_info/index_1.html

## Repository setup

The official VCC CLI is the supported path for downloading data, validating predictions,
packaging `.vcc` files, and submitting them:

```bash
brew install uv
uv tool install vcc-cli
vcc --version
```

This repository vendors the official VCC agent skill at
`.agents/skills/vcc/`. Codex discovers repository skills from `.agents/skills`, so requests
such as “prepare a submission” automatically use the official workflow. After upgrading the
CLI, refresh the checked-in copy and review the resulting diff:

```bash
uv tool upgrade vcc-cli
vcc skill install --dir .agents/skills
```

Authenticate without putting the API key in the repository or shell history:

```bash
vcc login --token-stdin
vcc whoami
```

The downloaded control bundle belongs at `data/controls.zip`; extracted working data belongs
under `data/controls/`, and generated prediction packages belong under `submissions/`. Both
directories are ignored by Git because the artifacts are large and may contain challenge data.

