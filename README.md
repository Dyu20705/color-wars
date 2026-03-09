
# Color Wars - Game chiến thuật

## Giới thiệu
Color Wars là một game chiến thuật theo lượt, mô phỏng cuộc chiến giữa hai người chơi (Xanh và Đỏ) trên một bàn cờ 5x5. Mỗi người chơi sẽ đặt các dot (chấm) vào ô, khi số dot đạt ngưỡng sẽ gây nổ, lan sang các ô lân cận và đồng hóa ô đối phương. Mục tiêu là kiểm soát toàn bộ bàn cờ.

## Cách hoạt động & các bước xử lý
1. **Khởi tạo**:
	- Sử dụng Pygame để tạo cửa sổ game.
	- Tạo board 5x5 gồm hai ma trận: `BOARD` (chủ sở hữu ô), `DOTS` (số dot trong ô).

2. **Vẽ board**:
	- Hàm `drawBoard` vẽ từng ô, viền và các dot theo trạng thái hiện tại.
	- Chỉ vẽ dot cho ô còn thuộc về người chơi và có dot.

3. **Xử lý click**:
	- Khi người chơi click vào ô, kiểm tra hợp lệ (ô trống hoặc của mình).
	- Thêm dot vào ô, chuyển lượt cho người chơi tiếp theo.

4. **Logic nổ và đồng hóa**:
	- Nếu số dot đạt ngưỡng (4), ô sẽ nổ: xóa dot và chủ sở hữu.
	- Dot lan sang 4 ô lân cận, đồng hóa ô trống hoặc ô đối phương.
	- Kiểm tra chuỗi nổ liên tiếp.

5. **Cập nhật hiển thị**:
	- Sau mỗi lượt, board được vẽ lại, loại bỏ dot ở ô đã nổ hoặc bị đồng hóa.

## Hướng dẫn chạy game
1. Cài đặt Python và Pygame:
    https://www.python.org/downloads/
	```bash
	pip install pygame
	```
2. Chạy game:
	```bash
	python src/main.py
	```

## Liên kết tài liệu
[Giới thiệu sơ bộ](https://docs.google.com/document/d/18cPllvrMK9fyZQlwbo_KntGp_xMdruhEOYKIm8ZsenQ/edit?usp=sharing)