# Step 2 — Đặc tả kỹ thuật (tóm tắt)

Bản đầy đủ, có sơ đồ state machine và ERD: [Five Nights at VNUK — Step 2: Đặc tả kỹ thuật](https://claude.ai/artifact/BAq292ukrqpsLT7NN282FL).

## ① PRD — Features & Acceptance Criteria

| ID | Tính năng | Acceptance Criteria |
| --- | --- | --- |
| F1 | Night Timer | 12 AM → 6 AM; 45 s thực = 1 giờ (270 s/đêm). Đồng hồ đứng khi nghe bộ đàm hoặc tạm dừng. |
| F2 | Điện năng | Pin đầu đêm 100/90/85%. Tụt 0,15%/s + 0,25%/s cho mỗi cửa, đèn, camera. Hết pin → Blackout, Phát jumpscare sau 5–10 s. |
| F3 | Phòng học | Phóng 1,35×, nhìn qua lại; DOOR + LIGHT mỗi bên; đèn soi lờ mờ. |
| F4 | Camera | 7 cam ảnh thật; nhiễu CRT khi chuyển cam hoặc khi quái di chuyển. |
| F5 | AI | Tick 5 s, 1d20 ≤ AI Level thì tiến; cửa mở 4–5 s → jumpscare; cửa đóng → rút sau 3–4 s. |
| F6 | Jumpscare | Tiếng hét riêng từng con, mắt đỏ, Game Over phóng to Hưng. |
| F7 | Cốt truyện | Màn mở đầu 5 trang; cuộc gọi bộ đàm đầu mỗi đêm. |
| F8 | Ending | Sau Đêm 5: bình minh → biên bản → twist → ★ mở Custom Night. |
| F9 | Custom Night | Khoá tới khi phá đảo; AI 0–20, hệ số hao điện 0,5–2×. |
| F10 | Cài đặt & Debug | 6 thanh âm lượng; Debug test nhanh mọi phần. |

## Cấu hình 5 đêm

| Đêm | Phát | Long | Sỹ | Phúc | Pin đầu đêm (%) |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 0 | 1 | 100 |
| 2 | 0 | 3 | 2 | 3 | 100 |
| 3 | 2 | 4 | 3 | 4 | 90 |
| 4 | 4 | 6 | 5 | 6 | 90 |
| 5 | 6 | 8 | 7 | 8 | 85 |

## ③ Architecture

Canvas 2D + Web Audio, state machine 9 trạng thái, vòng lặp `requestAnimationFrame`. Module đề xuất cho Step 3: `Game`, `NightSystem`, `AIDirector`, `OfficeView`, `CameraView`, `FX`, `AudioEngine`, `Story/Calls/Ending`, `ApiService`.

## ④ Database (ERD)

- `Players` (player_id PK, username, created_at)
- `GameProgress` (progress_id PK, player_id FK UNIQUE, current_night 1–5, stars_unlocked 0–1, best_survival_seconds, last_power_remaining)
- `NightConfigs` (night_number PK, freddy/bonny/foxy/chica_ai 0–20, start_power, power_drain_multiplier)
- `Settings` — mới (player_id PK/FK, volumes jsonb, tts_enabled, updated_at)
- `SessionLogs` — mới (session_id PK, player_id FK, night_number FK null = Custom, result, killer, survival_seconds, power_remaining, played_at)

## ⑤ API

| Method | Endpoint | Mục đích |
| --- | --- | --- |
| GET | `/api/night-config/:night` | Độ khó + pin đầu đêm |
| GET | `/api/progress` | Tiến độ + người chơi |
| POST | `/api/progress/save` | `{ night_completed, power_remaining, survival_seconds? }` → mở khoá đêm tiếp |
| GET/PUT | `/api/settings` | Âm lượng (Step 3) |
| POST | `/api/sessions` | Log phiên chơi (Step 3) |

Hiện tại `ApiService` trong `src/game.template.html` mock các endpoint trên bằng `localStorage`.
