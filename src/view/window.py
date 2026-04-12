"""Window creation and display management."""

import pygame

from .constants import DEFAULT_HEIGHT, DEFAULT_WIDTH


def drawScreen(fullscreen=False, size=(DEFAULT_WIDTH, DEFAULT_HEIGHT)):
    """Create or recreate the game window.
    
    Args:
        fullscreen: bool, if True create fullscreen display
        size: (width, height) for windowed mode
        
    Returns:
        pygame display surface
    """
    flags = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
    screen_size = (0, 0) if fullscreen else size
    screen = pygame.display.set_mode(screen_size, flags)
    pygame.display.set_caption("Color Wars")
    return screen


def toggle_fullscreen(is_fullscreen, screen):
    """Toggle between fullscreen and windowed mode.
    
    Args:
        is_fullscreen: current fullscreen state
        screen: pygame display surface
        
    Returns:
        (new_screen, new_is_fullscreen) tuple
    """
    if is_fullscreen:
        return drawScreen(fullscreen=False), False
    return drawScreen(fullscreen=True), True
