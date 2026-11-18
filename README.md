# Five Nights at VNUK

Game kinh dị sinh tồn kiểu *Five Nights at Freddy's*, chạy ngay trên trình duyệt. Bối cảnh là Trường VNUK (Viện Nghiên cứu và Đào tạo Việt - Anh, Đại học Đà Nẵng) vào ban đêm.

Bạn vào vai **Nguyễn Tuấn Hưng**, bị phạt trực đêm 5 đêm liên tiếp (12:00 AM → 6:00 AM) trong phòng học. Hưng phải quản lý điện dự phòng, xem camera và đóng cửa để chặn 4 thực thể:

| Nhân vật | Tên | Lộ trình |
| --- | --- | --- |
| Freddy | Nguyễn Bá Phát | Sảnh → Thư viện → Cầu thang → Hành lang → Cửa Sau |
| Bonny | Nguyễn Thành Long | Sảnh → Thư viện → Hành lang trái → Cửa Trước |
| Foxy | Huỳnh Tấn Sỹ | Nấp ở Phòng Lab (CAM 3) → lao vào Cửa Trước |
| Chica | Minh Phúc | Sảnh → Căng-tin → Cầu thang → Hành lang → Cửa Sau |

## Chơi ngay

- Mở `index.html` bằng Chrome, Edge hoặc Firefox. File này chứa sẵn toàn bộ ảnh, không cần server.
- Hoặc bật GitHub Pages (xem bên dưới) để có link chơi online.

## Điều khiển

| Phím / chuột | Tác dụng |
| --- | --- |
| Rê chuột, `←` `→` | Nhìn qua lại trong phòng học |
| `Q` / `E` | Đóng/mở Cửa Trước / Cửa Sau |
| `A` / `D` | Đèn hành lang trái / phải |
| `Space` | Mở/đóng camera; `1`–`7` chọn cam |
| `M` | Bỏ qua cuộc gọi bộ đàm |
| `Esc` | Tạm dừng và cài đặt âm thanh |

Mỗi giờ trong game kéo dài 45 giây thực, nên một đêm là 4 phút 30 giây. Pin tụt 0,15%/giây ở mức cơ bản, cộng thêm 0,25%/giây cho mỗi cửa đóng, đèn bật hoặc camera mở. Khi quái đứng ngoài cửa đang mở, bạn có 4–5 giây để đóng cửa.

Phá đảo Đêm 5 để xem ending và mở khoá **Custom Night** (AI 0–20). Nút **DEBUG** ở góc dưới trái dùng để test nhanh: chọn thẳng đêm, thắng ngay, xem jumpscare, xem ending.

## Cấu trúc repo

```
.
├── index.html               # bản build, chơi được ngay (tự sinh, đừng sửa tay)
├── src/
│   └── game.template.html   # mã nguồn game (HTML + CSS + JS), có chỗ /*SPRITES*/
├── assets/
│   ├── sprites/             # khung hình nhân vật đã cắt + tách nền
│   └── maps/                # ảnh phòng học, 7 camera, cửa sắt
├── tools/
│   ├── build.py             # nhúng assets vào template → index.html
│   └── slice_sprites.py     # cắt sprite sheet mới thành khung hình
├── docs/
│   └── STEP2.md             # tóm tắt đặc tả PRD / Architecture / ERD / API
└── .github/workflows/
    └── pages.yml            # tự build và đăng lên GitHub Pages
```

## Sửa game

1. Sửa code trong `src/game.template.html`, hoặc thay ảnh trong `assets/`.
2. Chạy `python3 tools/build.py` (chỉ cần Python 3, không cần thư viện ngoài).
3. Mở lại `index.html` để chơi thử.

Muốn thay sprite sheet nhân vật: `pip install pillow numpy scipy`, rồi chạy `python3 tools/slice_sprites.py <thư mục chứa freddy.png, bonny.png, foxy.png, chica.png>`, sau đó build lại.

## Đẩy lên GitHub

```bash
git init
git add .
git commit -m "Five Nights at VNUK - prototype"
git branch -M main
git remote add origin https://github.com/<tên-bạn>/five-nights-at-vnuk.git
git push -u origin main
```

**Bật GitHub Pages:** vào repo → **Settings** → **Pages** → mục *Source* chọn **GitHub Actions**. Mỗi lần push lên `main`, workflow sẽ tự build và đăng game tại `https://<tên-bạn>.github.io/five-nights-at-vnuk/`.

## Công nghệ

- HTML5 Canvas 960×540 với `image-rendering: pixelated` cho hình, Web Audio API tự tổng hợp toàn bộ âm thanh (không có file `.mp3`).
- Game chạy theo state machine (`STORY → MENU → INTRO → PLAYING → BLACKOUT / JUMPSCARE → GAMEOVER / WIN → ENDING`) trong vòng lặp `requestAnimationFrame` 60 FPS.
- `ApiService` mock lưu tiến độ và cài đặt bằng `localStorage`, sẵn sàng chuyển sang REST API thật.

Đặc tả đầy đủ (Step 2): xem `docs/STEP2.md`.
