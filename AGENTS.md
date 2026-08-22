# Virtual Cell Challenge repository guidance

- For any request involving VCC datasets, prediction files, packaging, validation, submission, or submission status, use the repository skill at `.agents/skills/vcc/SKILL.md` and the official `vcc` CLI.
- Treat `data/controls.zip` as the immutable source bundle. Extract working files under `data/controls/`; do not modify or delete the archive.
- Build prediction artifacts under `submissions/`. Before reporting a submission as ready, run `vcc prep` with the bundle's `gene_names.csv` and `pert_counts.csv`, using `--dry-run` first, then create the `.vcc` package only after validation succeeds.
- "Prepare a submission" means produce and locally validate the prediction artifact; it does not authorize uploading it. Run `vcc submit` only when the user explicitly asks to submit/upload.
- Never place a VCC API token, credential, or key in this repository, command arguments, logs, or chat. Use `vcc login --token-stdin`, the OS keychain, or the `VCC_TOKEN` environment variable as described by the VCC skill.
- Preserve the official context labels and gene ordering from the active challenge bundle. Never infer, rename, reorder, or swap contexts.

