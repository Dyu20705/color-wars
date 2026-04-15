"""Main Ứng dụng game Color Wars."""

import pygame
import sys

if __package__ is None or __package__ == "":
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.game.loop import run_game
from src.game.core import CoreSystems, LaunchConfig, SceneName
from src.view.home_scene import run_home_menu


def main():
    """Khởi chạy game ở mode mặc định"""

    # Khởi tạo toàn bộ subsystem của pygame trước khi render/game loop.
    pygame.init()
    core = CoreSystems()
    try:
        while core.current_scene != SceneName.QUIT:
            if core.current_scene == SceneName.HOME:
                core.begin_home_session()
                launch_config = run_home_menu(core=core)
                if launch_config is None:
                    core.request_quit()
                    continue
                core.enter_gameplay(
                    launch=LaunchConfig(
                        game_mode=launch_config.get("game_mode", "pvbot"),
                        difficulty=launch_config.get("difficulty", "easy"),
                    )
                )
                continue

            result = run_game(
                game_mode=core.active_launch.game_mode,
                difficulty=core.active_launch.difficulty,
                core=core,
            )
            if result is None:
                core.request_quit()
            else:
                core.enter_home()
    finally:
        # Giải phóng tài nguyên pygame ngay cả khi có exception ở menu hoặc gameplay.
        pygame.quit()

if __name__ == "__main__":
    main()