"""
Green-screen compositor for greenscreen-rendered SplatSim frames.

Use this after rendering with `launch_nodes.py --greenscreen`, which renders
everything outside the robot's AABB (table, walls, posters) as pure green
instead of the real background. This script keys out the green and pastes
in a new background image (or solid color) behind the robot + objects.

Usage:
    python scripts/composite_background.py \
        --input_dir /path/to/images_1 \
        --output_dir /path/to/images_1_composited \
        --background_image /path/to/new_background.png

    # or a solid color instead of an image:
    python scripts/composite_background.py \
        --input_dir /path/to/images_1 \
        --output_dir /path/to/images_1_composited \
        --background_color 40 40 60
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import numpy as np
import tyro
from PIL import Image, ImageFilter


@dataclass
class Args:
    input_dir: str
    output_dir: str
    background_image: Optional[str] = None
    background_color: Optional[List[int]] = None  # e.g. [40, 40, 60], used if background_image is None
    key_color: List[int] = field(default_factory=lambda: [0, 255, 0])
    threshold: float = 60.0  # euclidean distance in RGB space to count as "green"
    feather: float = 25.0  # extra distance over which the mask fades out, for softer edges
    despill_strength: float = 0.8  # 0 = no despill, 1 = fully clamp green to max(R,B)
    add_shadow: bool = True
    shadow_opacity: float = 0.45
    shadow_blur: float = 12.0
    shadow_squash: float = 0.18  # shadow height as a fraction of the foreground silhouette height
    shadow_offset_y: int = 6  # pixels to nudge the shadow down from the silhouette's bottom edge


def make_mask(rgb: np.ndarray, key_color, threshold: float, feather: float) -> np.ndarray:
    key = np.array(key_color, dtype=np.float32)
    dist = np.linalg.norm(rgb.astype(np.float32) - key[None, None, :], axis=-1)
    # alpha = 1 (fully foreground) far from key color, 0 (fully background) at/inside threshold
    alpha = np.clip((dist - threshold) / max(feather, 1e-6), 0.0, 1.0)
    return alpha


def despill(rgb: np.ndarray, strength: float) -> np.ndarray:
    """Pull back green-channel spill on edge pixels where G exceeds max(R, B)."""
    rgb = rgb.astype(np.float32).copy()
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    excess = np.clip(g - np.maximum(r, b), 0, None)
    rgb[..., 1] = g - excess * strength
    return np.clip(rgb, 0, 255)


def make_shadow(alpha: np.ndarray, args: "Args") -> np.ndarray:
    """Fake contact shadow: squash the foreground silhouette flat, blur it, and
    return a per-pixel darkening factor in [0, 1] (0 = no shadow)."""
    h, w = alpha.shape[:2]
    alpha_img = Image.fromarray((alpha[..., 0] * 255).astype(np.uint8))
    bbox = alpha_img.getbbox()
    if bbox is None:
        return np.zeros((h, w), dtype=np.float32)

    bottom = bbox[3]
    squashed_h = max(1, int(h * args.shadow_squash))
    shadow_small = alpha_img.resize((w, squashed_h))

    shadow_canvas = Image.new("L", (w, h), 0)
    paste_y = min(max(bottom - squashed_h + args.shadow_offset_y, 0), h - squashed_h)
    shadow_canvas.paste(shadow_small, (0, paste_y))
    shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(args.shadow_blur))

    shadow = np.array(shadow_canvas).astype(np.float32) / 255.0
    # Don't let the shadow show up on top of the foreground itself.
    shadow = shadow * (1.0 - alpha[..., 0])
    return shadow * args.shadow_opacity


def main(args: Args):
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    frame_paths = sorted(input_dir.glob("*.png"))
    if not frame_paths:
        raise FileNotFoundError(f"No .png frames found in {input_dir}")

    bg_image = None
    if args.background_image is not None:
        bg_image = Image.open(args.background_image).convert("RGB")

    for i, frame_path in enumerate(frame_paths):
        fg = Image.open(frame_path).convert("RGB")
        fg_np = np.array(fg)

        if bg_image is not None:
            bg_resized = bg_image.resize(fg.size)
            bg_np = np.array(bg_resized).astype(np.float32)
        else:
            color = args.background_color if args.background_color is not None else [30, 30, 30]
            bg_np = np.tile(np.array(color, dtype=np.float32), (fg_np.shape[0], fg_np.shape[1], 1))

        alpha = make_mask(fg_np, args.key_color, args.threshold, args.feather)[..., None]
        fg_clean = despill(fg_np, args.despill_strength)

        if args.add_shadow:
            shadow = make_shadow(alpha, args)[..., None]
            bg_np = bg_np * (1.0 - shadow)

        composited = fg_clean * alpha + bg_np * (1.0 - alpha)
        composited = np.clip(composited, 0, 255).astype(np.uint8)

        out_path = output_dir / frame_path.name
        Image.fromarray(composited).save(out_path)

        if i == 0 or (i + 1) % 20 == 0 or i == len(frame_paths) - 1:
            print(f"Composited {i + 1}/{len(frame_paths)}: {out_path}")

    print(f"Done. {len(frame_paths)} frames written to {output_dir}")


if __name__ == "__main__":
    main(tyro.cli(Args))
