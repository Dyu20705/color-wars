"""Main Ứng dụng game Color Wars."""

import pygame
import sys

if __package__ is None or __package__ == "":
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.game.loop import run_game
from src.view.home_scene import run_home_menu


def main():
    """Khởi chạy game ở mode mặc định"""

    # Khởi tạo toàn bộ subsystem của pygame trước khi render/game loop.
    pygame.init()
    launch_config = run_home_menu()
    if launch_config is not None:
        run_game(
            game_mode=launch_config.get("game_mode", "pvbot"),
            difficulty=launch_config.get("difficulty", "easy"),
        )
    # Giải phóng tài nguyên pygame trước khi thoát tiến trình.
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()