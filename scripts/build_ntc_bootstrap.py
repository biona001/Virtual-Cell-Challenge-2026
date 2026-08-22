#!/usr/bin/env python3
"""Build the VCC 2026 matched-context NTC bootstrap baseline.

For every official (context, target_gene) pair, this script samples the
required number of control cells with replacement from that context.  The
sampled expression profiles are copied unchanged; only ``target_gene`` is
relabelled to the perturbation being predicted.

Run with the Python environment installed for the official VCC CLI, e.g.:

    /path/to/vcc-cli/bin/python scripts/build_ntc_bootstrap.py

The writer streams the large sparse prediction matrix into HDF5 so it does not
need to hold all 360,000 predicted cells in memory at once.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import anndata as ad
import h5py
import numpy as np
import pandas as pd
from scipy import sparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--controls-dir",
        type=Path,
        default=Path("data/controls"),
        help="Extracted official controls bundle (default: data/controls).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("submissions/ntc_bootstrap_seed2026.h5ad"),
        help="Output prediction .h5ad.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=2026,
        help="NumPy random seed (default: 2026).",
    )
    parser.add_argument(
        "--write-chunk-rows",
        type=int,
        default=800,
        help="Rows copied per in-memory sparse block (default: 800).",
    )
    parser.add_argument(
        "--compression-level",
        type=int,
        default=4,
        choices=range(0, 10),
        metavar="0..9",
        help="HDF5 gzip level; 0 disables compression (default: 4).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing output file.",
    )
    return parser.parse_args()


def read_one_column_csv(path: Path, expected_column: str) -> list[str]:
    frame = pd.read_csv(path)
    if frame.columns.tolist() != [expected_column]:
        raise ValueError(
            f"{path} must contain exactly one column named {expected_column!r}; "
            f"found {frame.columns.tolist()}"
        )
    values = frame[expected_column].astype(str).tolist()
    if not values or len(values) != len(set(values)):
        raise ValueError(f"{path} must contain a nonempty, duplicate-free list")
    return values


def sha256(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(block_size):
            digest.update(block)
    return digest.hexdigest()


def load_bundle_contract(controls_dir: Path) -> tuple[dict, list[str], list[str]]:
    manifest_path = controls_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    contexts = [str(value) for value in manifest["contexts"]]
    genes = read_one_column_csv(controls_dir / "gene_names.csv", "gene_name")
    targets = read_one_column_csv(controls_dir / "pert_counts.csv", "target_gene")

    if len(genes) != int(manifest["n_genes"]):
        raise ValueError("gene_names.csv disagrees with manifest.json")
    if len(targets) != int(manifest["n_constructs"]):
        raise ValueError("pert_counts.csv disagrees with manifest.json")
    if contexts != ["A", "B", "C"]:
        raise ValueError(f"Expected official contexts A/B/C, found {contexts}")
    return manifest, genes, targets


def validate_control(
    source: ad.AnnData,
    path: Path,
    context: str,
    genes: list[str],
    control_label: str,
    expected_cells: int,
) -> None:
    if source.shape != (expected_cells, len(genes)):
        raise ValueError(
            f"{path} has shape {source.shape}; expected {(expected_cells, len(genes))}"
        )
    if source.var_names.astype(str).tolist() != genes:
        raise ValueError(f"{path} does not use the official gene order")
    for column in ("target_gene", "context", "ntc_id"):
        if column not in source.obs:
            raise ValueError(f"{path} is missing obs[{column!r}]")
    if set(source.obs["target_gene"].astype(str)) != {control_label}:
        raise ValueError(f"{path} contains non-control target_gene labels")
    if set(source.obs["context"].astype(str)) != {context}:
        raise ValueError(f"{path} does not contain only context {context!r}")
    if not sparse.isspmatrix_csr(source.X):
        raise ValueError(f"{path} X must be a CSR sparse matrix")
    if source.X.data.size and (
        not np.isfinite(source.X.data).all()
        or (source.X.data < 0).any()
        or not np.equal(source.X.data, np.floor(source.X.data)).all()
    ):
        raise ValueError(f"{path} X must contain finite, nonnegative integer counts")


def prepare_sampling_plan(
    controls_dir: Path,
    manifest: dict,
    genes: list[str],
    targets: list[str],
    seed: int,
) -> tuple[pd.DataFrame, dict[str, np.ndarray], np.ndarray]:
    rng = np.random.default_rng(seed)
    contexts = [str(value) for value in manifest["contexts"]]
    cells_per_target = int(manifest["cells_per_pert"])
    rows_per_context = len(targets) * cells_per_target
    total_rows = len(contexts) * rows_per_context

    target_column = np.tile(np.repeat(np.asarray(targets, dtype=object), cells_per_target), len(contexts))
    context_column = np.repeat(np.asarray(contexts, dtype=object), rows_per_context)
    source_row_column = np.empty(total_rows, dtype=np.int32)
    source_ntc_column = np.empty(total_rows, dtype=object)
    sampled_rows: dict[str, np.ndarray] = {}
    row_nnz = np.empty(total_rows, dtype=np.int64)

    offset = 0
    for context in contexts:
        path = controls_dir / f"context_{context}.h5ad"
        source = ad.read_h5ad(path)
        expected_cells = int(manifest["per_context"][context]["control_cells"])
        validate_control(
            source,
            path,
            context,
            genes,
            str(manifest["control_label"]),
            expected_cells,
        )

        sampled = rng.integers(0, source.n_obs, size=rows_per_context, dtype=np.int32)
        sampled_rows[context] = sampled
        end = offset + rows_per_context
        source_row_column[offset:end] = sampled
        ntc_ids = source.obs["ntc_id"].astype(str).to_numpy()
        source_ntc_column[offset:end] = ntc_ids[sampled]
        source_indptr = source.X.indptr
        row_nnz[offset:end] = source_indptr[sampled + 1] - source_indptr[sampled]
        print(
            f"planned context {context}: {rows_per_context:,} rows, "
            f"{int(row_nnz[offset:end].sum()):,} stored entries",
            flush=True,
        )
        del source
        offset = end

    obs = pd.DataFrame(
        {
            "target_gene": pd.Categorical(target_column, categories=targets),
            "context": pd.Categorical(context_column, categories=contexts),
            "source_row": source_row_column,
            "source_ntc_id": pd.Categorical(source_ntc_column),
        },
        index=pd.Index(np.arange(total_rows).astype(str), name=None),
    )
    return obs, sampled_rows, row_nnz


def initialize_h5ad(
    temp_path: Path,
    obs: pd.DataFrame,
    genes: list[str],
    manifest: dict,
    seed: int,
) -> None:
    empty_x = sparse.csr_matrix((len(obs), len(genes)), dtype=np.float32)
    var = pd.DataFrame(index=pd.Index(genes, dtype=str))
    output = ad.AnnData(X=empty_x, obs=obs, var=var)
    output.uns["baseline"] = {
        "model": "matched-context NTC bootstrap with replacement",
        "seed": int(seed),
        "cells_per_context_target": int(manifest["cells_per_pert"]),
        "control_label": str(manifest["control_label"]),
    }
    output.write_h5ad(temp_path, compression="gzip", compression_opts=4)


def create_matrix_datasets(
    h5ad_path: Path,
    n_rows: int,
    n_genes: int,
    row_nnz: np.ndarray,
    compression_level: int,
) -> np.ndarray:
    output_indptr = np.empty(n_rows + 1, dtype=np.int64)
    output_indptr[0] = 0
    np.cumsum(row_nnz, out=output_indptr[1:])
    total_nnz = int(output_indptr[-1])
    compression = "gzip" if compression_level else None
    compression_opts = compression_level if compression_level else None
    element_chunk = min(1_000_000, max(1, total_nnz))

    with h5py.File(h5ad_path, "r+") as handle:
        del handle["X"]
        group = handle.create_group("X")
        group.attrs["encoding-type"] = "csr_matrix"
        group.attrs["encoding-version"] = "0.1.0"
        group.attrs["shape"] = np.asarray([n_rows, n_genes], dtype=np.int64)
        group.create_dataset(
            "data",
            shape=(total_nnz,),
            dtype=np.float32,
            chunks=(element_chunk,),
            compression=compression,
            compression_opts=compression_opts,
            shuffle=True if compression else False,
        )
        group.create_dataset(
            "indices",
            shape=(total_nnz,),
            dtype=np.int32,
            chunks=(element_chunk,),
            compression=compression,
            compression_opts=compression_opts,
            shuffle=True if compression else False,
        )
        group.create_dataset(
            "indptr",
            data=output_indptr,
            dtype=np.int64,
            chunks=(min(65_536, n_rows + 1),),
            compression=compression,
            compression_opts=compression_opts,
            shuffle=True if compression else False,
        )
    return output_indptr


def stream_sampled_matrix(
    h5ad_path: Path,
    controls_dir: Path,
    contexts: list[str],
    sampled_rows: dict[str, np.ndarray],
    output_indptr: np.ndarray,
    rows_per_context: int,
    chunk_rows: int,
) -> None:
    written_rows = 0
    started = time.monotonic()
    with h5py.File(h5ad_path, "r+") as destination:
        out_data = destination["X/data"]
        out_indices = destination["X/indices"]

        for context in contexts:
            path = controls_dir / f"context_{context}.h5ad"
            source = ad.read_h5ad(path)
            source_x = source.X
            context_samples = sampled_rows[context]
            context_output_start = written_rows

            for local_start in range(0, rows_per_context, chunk_rows):
                local_end = min(local_start + chunk_rows, rows_per_context)
                global_start = context_output_start + local_start
                global_end = context_output_start + local_end
                block = source_x[context_samples[local_start:local_end]].tocsr()
                data_start = int(output_indptr[global_start])
                data_end = int(output_indptr[global_end])
                if block.nnz != data_end - data_start:
                    raise RuntimeError("Sampled block nnz disagrees with the sampling plan")
                out_data[data_start:data_end] = block.data.astype(np.float32, copy=False)
                out_indices[data_start:data_end] = block.indices.astype(np.int32, copy=False)

                if global_end % 10_000 < chunk_rows or global_end == len(output_indptr) - 1:
                    elapsed = time.monotonic() - started
                    rate = global_end / elapsed if elapsed else 0.0
                    print(
                        f"wrote {global_end:,}/{len(output_indptr) - 1:,} rows "
                        f"({rate:,.0f} rows/s)",
                        flush=True,
                    )

            written_rows += rows_per_context
            del source, source_x
            destination.flush()


def verify_output(
    output_path: Path,
    manifest: dict,
    genes: list[str],
    targets: list[str],
    row_nnz: np.ndarray,
) -> None:
    prediction = ad.read_h5ad(output_path, backed="r")
    expected_rows = len(manifest["contexts"]) * len(targets) * int(manifest["cells_per_pert"])
    if prediction.shape != (expected_rows, len(genes)):
        raise RuntimeError(f"Output has unexpected shape {prediction.shape}")
    if prediction.var_names.astype(str).tolist() != genes:
        raise RuntimeError("Output gene order changed")
    if int(prediction.X._indptr[-1]) != int(row_nnz.sum()):
        raise RuntimeError("Output stored-entry count changed")

    expected_per_pair = int(manifest["cells_per_pert"])
    counts = prediction.obs.groupby(
        ["context", "target_gene"], observed=True
    ).size()
    if len(counts) != len(manifest["contexts"]) * len(targets):
        raise RuntimeError("Output is missing context-target pairs")
    if not (counts.to_numpy() == expected_per_pair).all():
        raise RuntimeError("Output does not have the expected cells per pair")
    if str(manifest["control_label"]) in set(prediction.obs["target_gene"].astype(str)):
        raise RuntimeError("Output contains forbidden control-labelled cells")
    prediction.file.close()


def main() -> int:
    args = parse_args()
    if args.write_chunk_rows < 1:
        raise ValueError("--write-chunk-rows must be positive")

    controls_dir = args.controls_dir.resolve()
    output_path = args.output.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_name(f".{output_path.name}.building")
    if output_path.exists() and not args.force:
        raise FileExistsError(f"Output already exists: {output_path}; pass --force to replace it")
    if temp_path.exists():
        raise FileExistsError(f"Incomplete build file already exists: {temp_path}")

    manifest, genes, targets = load_bundle_contract(controls_dir)
    obs, sampled_rows, row_nnz = prepare_sampling_plan(
        controls_dir, manifest, genes, targets, args.seed
    )
    total_nnz = int(row_nnz.sum())
    print(
        f"output plan: {len(obs):,} cells x {len(genes):,} genes; "
        f"{total_nnz:,} stored entries; seed={args.seed}",
        flush=True,
    )

    try:
        initialize_h5ad(temp_path, obs, genes, manifest, args.seed)
        output_indptr = create_matrix_datasets(
            temp_path,
            len(obs),
            len(genes),
            row_nnz,
            args.compression_level,
        )
        rows_per_context = len(targets) * int(manifest["cells_per_pert"])
        stream_sampled_matrix(
            temp_path,
            controls_dir,
            [str(value) for value in manifest["contexts"]],
            sampled_rows,
            output_indptr,
            rows_per_context,
            args.write_chunk_rows,
        )
        os.replace(temp_path, output_path)
        verify_output(output_path, manifest, genes, targets, row_nnz)
    except BaseException:
        print(f"build interrupted; partial file retained at {temp_path}", file=sys.stderr)
        raise

    print(f"created: {output_path}", flush=True)
    print(f"size: {output_path.stat().st_size:,} bytes", flush=True)
    print(f"sha256: {sha256(output_path)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
