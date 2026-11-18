#!/usr/bin/env python3
"""Build index.html từ src/game.template.html.

Ảnh KHÔNG nhúng vào HTML nữa (để trang tải nhanh): template nhận một bảng
tên ảnh → đường dẫn tới assets/, kèm ?v=<hash nội dung> để trình duyệt cache lâu dài
mà vẫn lấy bản mới khi ảnh đổi.

Chạy:   python3 tools/build.py
Tuỳ chọn: python3 tools/build.py --inline   (nhúng base64 thành một file duy nhất, mở offline được)
"""
import base64
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "src" / "game.template.html"
MIME = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def main() -> None:
    inline = "--inline" in sys.argv
    sprites = {}
    for folder in ("sprites", "maps"):
        for f in sorted((ROOT / "assets" / folder).iterdir()):
            if f.suffix.lower() not in MIME:
                continue
            data = f.read_bytes()
            if inline:
                sprites[f.stem] = f"data:{MIME[f.suffix.lower()]};base64,{base64.b64encode(data).decode()}"
            else:
                sprites[f.stem] = f"assets/{folder}/{f.name}?v={hashlib.sha1(data).hexdigest()[:8]}"
    html = TEMPLATE.read_text(encoding="utf-8")
    if "/*SPRITES*/" not in html:
        raise SystemExit("Không tìm thấy /*SPRITES*/ trong template")
    out = ROOT / ("index.offline.html" if inline else "index.html")
    out.write_text(html.replace("/*SPRITES*/", json.dumps(sprites, separators=(",", ":"))), encoding="utf-8")
    print(f"Đã build {out.name}: {len(sprites)} ảnh, {out.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
