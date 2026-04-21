# Color Wars

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.x-2E8B57)](https://www.pygame.org/)
[![Tests](https://img.shields.io/badge/tests-54%20passed-success)](#testing)
[![License](https://img.shields.io/badge/license-MIT-green)](#license)

Color Wars là game chiến thuật theo lượt xây dựng bằng Pygame, nơi người chơi đặt chấm, kích nổ dây chuyền và chuyển quyền kiểm soát ô trên bàn cờ 5x5. Trò chơi hỗ trợ cả chế độ PvP (2 người) và PvE (đấu bot) với 3 mức độ khó.

## Mục lục

- [Tổng quan dự án](#tổng-quan-dự-án)
- [Khởi động nhanh](#khởi-động-nhanh)
- [Điều khiển](#điều-khiển)
- [Luật chơi cốt lõi](#luật-chơi-cốt-lõi)
- [Kiến trúc](#kiến-trúc)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Hành vi âm thanh và scene](#hành-vi-âm-thanh-và-scene)
- [Chuẩn hiển thị UI](#chuẩn-hiển-thị-ui)
- [Media preview](#media-preview)
- [Quy trình phát triển](#quy-trình-phát-triển)
- [Testing](#testing)
- [Xử lý sự cố](#xử-lý-sự-cố)
- [Roadmap](#roadmap)
- [Đóng góp](#đóng-góp)
- [License](#license)

## Tổng quan dự án

Mục tiêu của dự án:

- Giữ logic game tách biệt rõ giữa engine, controller, runtime và view.
- Dễ mở rộng tính năng scene, audio, settings mà không làm rối game loop.
- Dễ test bằng unit test cho AI, game logic và render contract.

## Khởi động nhanh

### Yêu cầu

- Python 3.10+
- Pygame 2.x

### Cài đặt

```bash
pip install -r requirements.txt
```

### Chạy game

```bash
python -m src.main
```

## Điều khiển

- Chuột trái: đặt/tăng quân ở ô hợp lệ
- M: đổi chế độ PvP/PvE trong màn gameplay
- R: chơi lại ván hiện tại
- H: bật/tắt lớp hướng dẫn
- F11: bật/tắt toàn màn hình
- Esc: quay lại màn trước hoặc đóng overlay

## Luật chơi cốt lõi

- Chiếm ô trống: +3 chấm
- Tăng quân vào ô của mình: +1 chấm
- Ô đạt 4 chấm sẽ nổ
- Nổ dây chuyền lan sang ô kề và đổi chủ theo người vừa kích nổ

## Kiến trúc

Phân tách chính:

- Engine: luật hợp lệ nước đi, tăng chấm, nổ dây chuyền
- Controller: áp dụng nước đi, đổi lượt, xác định thắng/thua
- Game runtime: state, loop, core systems, audio manager, app settings
- AI: policy theo mức easy/medium/hard
- View: bố cục, scene, HUD, overlay và các thành phần vẽ

Runtime core hiện tại:

- CoreSystems: điều phối scene mức ứng dụng (home/gameplay/quit)
- AppSettings: lưu trạng thái âm thanh, âm lượng, fullscreen, ngôn ngữ
- MusicManager: quản lý nhạc nền dùng chung giữa menu và gameplay

## Cấu trúc thư mục

```text
asset/
  aud/                     nhạc nền (.mp3)
  gameplay/                ảnh chụp màn hình + video demo mp4
  img/                     ảnh nền, icon, UI assets
src/
  main.py                  entrypoint ứng dụng
  controller.py            apply move, score, xác định thắng
  ai/
    ai.py                  router chọn bot theo difficulty
    ez_AI.py               easy AI (ưu tiên nước đi yếu)
    med_AI.py              medium AI (lookahead nông + nhiễu)
    hard_AI.py             hard AI (alpha-beta)
  engine/
    rules.py               luật nước đi và hằng số người chơi
    explosion.py           xử lý chuỗi nổ
  game/
    core.py                scene state machine + orchestration
    settings.py            AppSettings + clamp
    audio.py               MusicManager
    loop.py                vòng lặp gameplay chính
    state.py               GameState dataclass
    analysis.py            ước lượng tỷ lệ thắng cho HUD
  view/
    constants.py           màu sắc và hằng số UI
    layout.py              responsive layout + mapping chuột->ô
    window.py              tạo màn hình và fullscreen
    base/                  lớp scene base
    commons/               component dùng chung (button, overlay, icon)
    home_scene/            home flow + render
    choose_gamemode_scene/ scene chọn chế độ
    choose_diff_scene/     scene chọn độ khó
    gameplay_scene/        board, hud, effects, compose scene
    setting_scene/         scene cài đặt
    tutorial_scene/        scene/hỗ trợ hướng dẫn
    win_scene/             overlay chiến thắng
tests/
  ai/                      test router + hard/medium/easy AI
  game_logic/              test controller/rules/explosion
  game/                    test game runtime modules
  view/                    test scene contract/layout/hud/overlay
```

## Hành vi âm thanh và scene

Hành vi hiện tại theo code:

- Khi vào home session, hệ thống chọn 1 bài theme ngẫu nhiên trong asset/aud.
- Gameplay dùng cùng track đang chạy, không ép đổi bài trong lúc chơi.
- Bật/tắt âm thanh dùng pause/unpause, không stop/restart cưỡng bức.
- Âm lượng được clamp về [0.0, 1.0] trước khi áp dụng.
- Thoát gameplay về home sẽ đưa context nhạc về menu.
- Fullscreen có thể toggle bằng F11 và cập nhật vào AppSettings.

## Chuẩn hiển thị UI

Các chuẩn UI đang áp dụng:

- Bố cục responsive theo kích thước cửa sổ (layout động theo screen size).
- Nút bấm dùng shared interaction (hover/pressed) qua component chung.
- Home scene tối giản 4 điều khiển chính: Bắt đầu, Thoát, Tutorial, Settings.
- Nhãn tiếng Việt nhất quán ở các scene chính (menu, settings, tutorial, HUD).
- Tutorial overlay có kích thước lớn theo tỉ lệ màn hình để giảm tràn chữ.
- HUD hiển thị trạng thái chế độ, điều khiển, lịch sử nước đi và tỷ lệ thắng.

## Media preview

Tài nguyên demo nằm trong asset/gameplay.

### Ảnh chụp

- [Màn hình chính](asset/gameplay/home.png)
- [Chọn chế độ](asset/gameplay/chonMode.png)
- [Chọn độ khó](asset/gameplay/chonDiff.png)
- [Gameplay](asset/gameplay/gameplay.png)
- [Cài đặt](asset/gameplay/setting.png)
- [Tutorial](asset/gameplay/tutorial.png)
- [Màn hình thắng](asset/gameplay/win.png)

### Video demo

- [Gameplay video (.mp4)](asset/gameplay/gameplay_video.mp4)

## Quy trình phát triển

### Thiết lập local (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Chạy game và test

```bash
python -m src.main
pytest -q
```

### Local Demo Completion Check

Checklist kiểm tra nhanh bản demo local:

1. Tất cả nút chính có trạng thái hover/pressed rõ ràng.
2. Chữ trong panel và button không bị tràn khi đổi kích thước cửa sổ.
3. Tutorial overlay hiển thị đầy đủ nội dung và nút Đóng hoạt động.
4. Settings cho phép bật/tắt âm thanh và kéo thanh âm lượng, bấm Áp dụng có hiệu lực.
5. F11 toggle fullscreen ổn định ở cả home và gameplay.
6. Esc quay lại đúng ngữ cảnh (đóng overlay trước, sau đó về scene trước).
7. PvP không hiển thị thông tin độ khó bot trên HUD.
8. Kết thúc trận hiển thị đúng overlay thắng với nút Chơi lại và Trang chủ.

## Testing

- Trạng thái hiện tại: 54 passed
- Cấu trúc test:
  - tests/ai: router + easy/medium/hard bot
  - tests/game_logic: engine/controller
  - tests/game: core settings/audio/analysis/state/loop guard
  - tests/view: scene contract, layout/window, gameplay HUD/effects
- Khoảng trống còn lại:
  - chưa có integration test full event loop cho run_home_menu
  - chưa có visual snapshot/regression test khung hình render thật
  - chưa có benchmark hiệu năng cho AI theo nhiều trạng thái bàn cờ lớn

## Xử lý sự cố

- Không có nhạc:
  - kiểm tra file .mp3 trong asset/aud
  - kiểm tra mixer/audio device khả dụng trên máy
- Video demo không mở từ README:
  - mở trực tiếp file asset/gameplay/gameplay_video.mp4 bằng player cục bộ
- Màn hình hiển thị sai tỉ lệ:
  - dùng F11 để đổi trạng thái fullscreen
  - resize lại cửa sổ để layout tính toán lại
- Test fail cục bộ:
  - chạy lệnh tại thư mục gốc repo
  - đảm bảo môi trường đã cài requirements.txt

## Roadmap

1. Chuẩn hóa bảng text đa ngôn ngữ (vi/en) cho toàn bộ scene.
2. Bổ sung integration test cho luồng home -> chọn mode -> gameplay.
3. Bổ sung snapshot test cho một số khung hình UI quan trọng.
4. Cải thiện giải thích quyết định của AI cho người chơi.

## Đóng góp

Đóng góp PR được chào đón.

Nguyên tắc chính:

- Giữ ranh giới kiến trúc engine/controller/game/view rõ ràng.
- Thay đổi hành vi cần đi kèm cập nhật test.
- Ưu tiên PR nhỏ, rõ phạm vi, dễ review.

Checklist gợi ý trước khi mở PR:

- [ ] pytest -q pass tại máy local
- [ ] không phá vỡ ranh giới kiến trúc
- [ ] cập nhật tài liệu nếu thay đổi hành vi

## License

Dự án đang dùng giấy phép MIT. Xem chi tiết tại file [LICENSE](LICENSE).
