"""Contiene las clases del menu y la pausa"""

import pygame
import math as m
from constants import *
from texturedata import TEXTURES

class StartMenu(object):
    def __init__(self):
        pass
    def draw(self, screen: pygame.Surface):
        screen.blit(TEXTURES["start_menu_background"], (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(TEXTURES["press_any_white"], (SCREEN_WIDTH // 2 - 450 // 2, 600 + m.sin(pygame.time.get_ticks()) * 10))

class MovementsMenu(object):
    def __init__(self):

        self.easy_button_rect: pygame.Rect = pygame.Rect(
            100, SCREEN_HEIGHT//2 + 50, TILE_SIZE*4, TILE_SIZE*4)
        self.normal_button_rect: pygame.Rect = pygame.Rect(
            500, SCREEN_HEIGHT//2 + 50, TILE_SIZE*4, TILE_SIZE*4)
        self.hard_button_rect: pygame.Rect = pygame.Rect(
            900, SCREEN_HEIGHT//2 + 50, TILE_SIZE*4, TILE_SIZE*4)

    def draw(self, screen: pygame.Surface):
        """Renderiza los elementos."""
        screen.blit(TEXTURES["mov_choose"], (SCREEN_WIDTH // 2 - , SCREEN_HEIGHT // 2 - 50))
        screen.blit(TEXTURES["easy_button"], self.easy_button_rect)
        screen.blit(TEXTURES["normal_button"], self.normal_button_rect)
        screen.blit(TEXTURES["hard_button"], self.hard_button_rect)

    def define_button_pressed(self) -> int:
        """Define el botón que es presionado para la dificultad,
        siendo fácil, normal y difícil 1, 2, y 3 respectivamente
        o devolviendo 0 si no se ha presionado un botón."""
        mouse_pos = pygame.mouse.get_pos()
        if self.easy_button_rect.collidepoint(mouse_pos):
            return 1
        if self.normal_button_rect.collidepoint(mouse_pos):
            return 2
        if self.hard_button_rect.collidepoint(mouse_pos):
            return 3
        return 0


class Pause(object):

    def __init__(self):
        self.continue_button_rect: pygame.Rect = pygame.Rect(
            500, SCREEN_HEIGHT//2 - 300, TILE_SIZE*4, TILE_SIZE*2)
        self.rules_button_rect: pygame.Rect = pygame.Rect(
            500, SCREEN_HEIGHT//2 - 100, TILE_SIZE*4, TILE_SIZE*2)
        self.exit_button_rect: pygame.Rect = pygame.Rect(
            500, SCREEN_HEIGHT//2 + 100, TILE_SIZE*4, TILE_SIZE*2)

    def draw(self, screen: pygame.Surface):
        """Dibuja los botones en pantalla."""
        screen.blit(TEXTURES["continue_button"], self.continue_button_rect)
        screen.blit(TEXTURES["exit_button"], self.exit_button_rect)
        screen.blit(TEXTURES["rules_button"], self.rules_button_rect)

    def define_button_pressed(self) -> int:
        """Define el botón presionado si es que ha sucedido, si no devuelve 0"""
        mouse_pos = pygame.mouse.get_pos()
        if self.continue_button_rect.collidepoint(mouse_pos):
            return 1
        if self.rules_button_rect.collidepoint(mouse_pos):
            return 3
        if self.exit_button_rect.collidepoint(mouse_pos):
            return 2
        return 0
