#!/usr/bin/env python3
"""Colourise a Realsee3D ``segment.png`` using the official class palette.

``segment.png`` stores raw integer class IDs, so it looks almost black when
opened directly. This tool maps every ID to the official RGB colour from the
``metadata/class_mapping_*.json`` tables and, optionally, blends the result over
the RGB panorama. Real-world scenes use ``class_mapping_real.json``; synthetic
scenes use ``class_mapping_synthetic.json``. Label ID 0 (background) is black.

Examples:
    python scripts/visualize_segmentation.py \
        --segment <viewpoint>/segment.png \
        --mapping metadata/class_mapping_real.json \
        --output seg_vis.png

    python scripts/visualize_segmentation.py \
        --segment <viewpoint>/segment.png --mapping metadata/class_mapping_synthetic.json \
        --panorama <viewpoint>/panoImage_1600.jpg --alpha 0.6 --output seg_overlay.png --legend
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def load_palette(mapping_path: Path) -> tuple[dict[int, tuple], dict[int, str]]:
    """Load ``id -> (R, G, B)`` and ``id -> name`` from a class-mapping JSON."""
    doc = json.loads(mapping_path.read_text(encoding="utf-8"))
    id2color = {int(c["id"]): tuple(int(v) for v in c["color"]) for c in doc["classes"]}
    id2name = {int(c["id"]): c["name"] for c in doc["classes"]}
    return id2color, id2name


def build_lut(id2color: dict[int, tuple]) -> np.ndarray:
    """Build a 256x3 RGB lookup table; unmapped IDs (including 0) stay black."""
    lut = np.zeros((256, 3), dtype=np.uint8)
    for cid, rgb in id2color.items():
        if 0 <= cid < 256:
            lut[cid] = rgb
    return lut


def colourise(segment: np.ndarray, lut: np.ndarray) -> np.ndarray:
    """Map a single-channel ID image to an RGB colour image."""
    if segment.ndim != 2:
        raise ValueError(f"segment.png must be single-channel, got shape {segment.shape}")
    return lut[segment]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--segment", required=True, type=Path, help="Path to segment.png")
    ap.add_argument("--mapping", required=True, type=Path,
                    help="metadata/class_mapping_real.json (real) or class_mapping_synthetic.json (synthetic)")
    ap.add_argument("--output", required=True, type=Path, help="Output PNG path")
    ap.add_argument("--panorama", type=Path, default=None,
                    help="Optional panoImage_1600.jpg to blend the segmentation over")
    ap.add_argument("--alpha", type=float, default=0.6,
                    help="Segmentation opacity for overlay (0-1, default 0.6)")
    ap.add_argument("--legend", action="store_true", help="Print the classes present in the image")
    args = ap.parse_args()

    segment = cv2.imread(str(args.segment), cv2.IMREAD_UNCHANGED)
    if segment is None:
        raise SystemExit(f"Could not read segment image: {args.segment}")
    if segment.ndim == 3:
        segment = segment[:, :, 0]

    id2color, id2name = load_palette(args.mapping)
    lut = build_lut(id2color)
    vis_bgr = cv2.cvtColor(colourise(segment, lut), cv2.COLOR_RGB2BGR)

    if args.panorama is not None:
        pano = cv2.imread(str(args.panorama), cv2.IMREAD_COLOR)
        if pano is None:
            raise SystemExit(f"Could not read panorama: {args.panorama}")
        if pano.shape[:2] != vis_bgr.shape[:2]:
            pano = cv2.resize(pano, (vis_bgr.shape[1], vis_bgr.shape[0]), interpolation=cv2.INTER_NEAREST)
        a = float(np.clip(args.alpha, 0.0, 1.0))
        blended = cv2.addWeighted(vis_bgr, a, pano, 1.0 - a, 0.0)
        # Blend only labelled pixels; keep the raw panorama in background regions.
        vis_bgr = np.where((segment != 0)[:, :, None], blended, pano)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.output), vis_bgr)
    print(f"Saved visualization to {args.output}")

    if args.legend:
        present = sorted(int(v) for v in np.unique(segment))
        print(f"{len(present)} labels present:")
        for cid in present:
            label = "background" if cid == 0 else id2name.get(cid, f"<unmapped id {cid}>")
            print(f"  {cid:>4}  {label}")


if __name__ == "__main__":
    main()
