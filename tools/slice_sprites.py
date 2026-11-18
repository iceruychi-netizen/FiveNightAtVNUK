#!/usr/bin/env python3
"""Cắt 4 sprite sheet nhân vật (3 cột x 2 hàng) thành từng khung hình và tách nền
cho các tư thế đứng. Dùng khi bạn muốn thay sprite sheet mới.

Cần:  pip install pillow numpy scipy
Chạy: python3 tools/slice_sprites.py <thư mục chứa sheet>
      (tên file: freddy.png, bonny.png, foxy.png, chica.png)
Kết quả ghi vào assets/sprites/.

Toạ độ cột/hàng dưới đây đo cho bộ sheet gốc 657x~470; sheet khác kích thước
thì chỉnh lại CUTS.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "sprites"

CUTS = {  # (cột x0,x1), (hàng y0,y1)
    "chica": ([(2, 219), (221, 439), (442, 655)], [(49, 234), (281, 456)]),
    "foxy": ([(2, 217), (220, 436), (439, 655)], [(42, 233), (276, 449)]),
    "bonny": ([(6, 175), (177, 352), (354, 521)], [(37, 193), (224, 363)]),
    "freddy": ([(2, 217), (219, 437), (439, 656)], [(47, 233), (276, 468)]),
}
NAMES = {
    "chica": ["idle", "peek", "aggr", "door", "cam", "jump"],
    "foxy": ["idle", "peek", "rush", "door", "cam", "jump"],
    "bonny": ["idle", "stare", "aggr", "door", "cam", "jump"],
    "freddy": ["idle", "stare", "aggr", "door", "cam", "jump"],
}
CUTOUT = {"idle", "stare", "aggr", "rush"}  # tư thế đứng: tách nền


def remove_bg(img: Image.Image, wide: bool) -> Image.Image:
    a = np.array(img).astype(int)
    mx, mn = a.max(2), a.min(2)
    outline = ndimage.binary_dilation(mn > 170, iterations=2)  # viền trắng của sprite chặn flood-fill
    corners = np.concatenate([a[:6, :6].reshape(-1, 3), a[:6, -6:].reshape(-1, 3)])
    tol = 22 if wide else 8
    lo, hi = corners.max(1).min() - tol, corners.max(1).max() + tol
    m = (mx - mn < (18 if wide else 14)) & (mx >= lo) & (mx <= hi) & ~outline
    m = ndimage.binary_opening(m, iterations=1)
    lab, _ = ndimage.label(m)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = ndimage.binary_dilation(np.isin(lab, list(border)), iterations=1) & ~(mn > 170)
    return Image.fromarray(np.dstack([a, np.where(bg, 0, 255)]).astype(np.uint8), "RGBA")


def main(src: Path) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for who, (cols, rows) in CUTS.items():
        sheet = Image.open(src / f"{who}.png").convert("RGB")
        i = 0
        for (y0, y1) in rows:
            for (x0, x1) in cols:
                pose = NAMES[who][i]
                frame = sheet.crop((x0, y0, x1, y1))
                if pose in CUTOUT and not (who == "foxy" and pose == "peek"):
                    remove_bg(frame, who == "chica" or (who == "bonny" and pose == "aggr")).save(OUT / f"{who}_{pose}.webp", lossless=True, method=6)
                else:
                    frame.save(OUT / f"{who}_{pose}.webp", quality=82, method=6)
                i += 1
    print("Xong:", OUT)


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "."))
