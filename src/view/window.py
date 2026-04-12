"""Window creation and fullscreen helpers."""

import pygame

from .constants import DEFAULT_HEIGHT, DEFAULT_WIDTH


def drawScreen(fullscreen=False, size=(DEFAULT_WIDTH, DEFAULT_HEIGHT)):
    """Create the game window."""
    flags = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
    screen_size = (0, 0) if fullscreen else size
    screen = pygame.display.set_mode(screen_size, flags)
    pygame.display.set_caption("Color Wars")
    return screen


def toggle_fullscreen(is_fullscreen, screen):
    """Toggle fullscreen mode and return the new screen and state."""
    if is_fullscreen:
        return drawScreen(fullscreen=False), False
    return drawScreen(fullscreen=True), True