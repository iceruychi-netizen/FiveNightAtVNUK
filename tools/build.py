#!/usr/bin/env python3
"""Build index.html: nhúng toàn bộ ảnh trong assets/ vào src/game.template.html.

Chạy:  python3 tools/build.py
Kết quả: index.html (một file duy nhất, mở trực tiếp bằng trình duyệt hoặc GitHub Pages).
"""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "src" / "game.template.html"
OUT = ROOT / "index.html"
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def main() -> None:
    sprites = {}
    for folder in ("sprites", "maps"):
        for f in sorted((ROOT / "assets" / folder).iterdir()):
            if f.suffix.lower() in MIME:
                data = base64.b64encode(f.read_bytes()).decode()
                sprites[f.stem] = f"data:{MIME[f.suffix.lower()]};base64,{data}"
    html = TEMPLATE.read_text(encoding="utf-8")
    if "/*SPRITES*/" not in html:
        raise SystemExit("Không tìm thấy /*SPRITES*/ trong template")
    OUT.write_text(html.replace("/*SPRITES*/", json.dumps(sprites)), encoding="utf-8")
    print(f"Đã build {OUT.name}: {len(sprites)} ảnh, {OUT.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
