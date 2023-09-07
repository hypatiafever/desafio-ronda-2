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
        screen.blit(TEXTURES["press_any_white"], (SCREEN_WIDTH // 2 - 450 // 2, 570 + m.sin(pygame.time.get_ticks()/100) * 10))

class NameMenu(object):
    def __init__(self, screen: pygame.Surface):
        self.small_font = pygame.font.Font("res/font/PixelOperator.ttf", 38)
        self.screen = screen
        self.user_text = ""
        self.input_rect = pygame.Rect(0, 0, 400, 46)
        self.input_rect.center = screen.get_rect().center
        self.input_rect_bigger = pygame.Rect(0, 0, 416, 62)
        self.input_rect_bigger.center = screen.get_rect().center
        self.color_active = (102, 41, 53)
        self.color_passive = (172, 89, 106)
        self.input_color = self.color_passive
        self.input_text_color = WHITE
        self.active = False

    def draw(self):
        self.screen.blit(TEXTURES["insert_name"], (SCREEN_WIDTH // 2 - 700 // 2, SCREEN_HEIGHT // 2 - 50))
        
        self.input_color = self.color_active if self.active else self.color_passive

        pygame.draw.rect(self.screen, self.color_passive, self.input_rect_bigger)
        pygame.draw.rect(self.screen, self.input_color, self.input_rect)

        input_text = self.small_font.render(self.user_text, True, self.input_text_color)
        input_text_rect = input_text.get_rect(centerx = self.screen.get_rect().centerx,
                                              centery = self.screen.get_rect().centery + 100)
        self.screen.blit(input_text, input_text_rect)

        self.input_rect.w = max(512, input_text_rect.w + 10)
        self.input_rect.center = self.screen.get_rect().center
        self.input_rect.centery += 100
        self.input_rect_bigger.w = max(528, input_text_rect.w + 26)
        self.input_rect_bigger.center = self.screen.get_rect().center
        self.input_rect_bigger.centery += 100

    def handle_writing(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # click derecho
                if self.input_rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and self.active:
                self.user_text = self.user_text[:-1]
            elif self.active and not event.key in {pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_TAB}:
                self.user_text += event.unicode
            if event.key == pygame.K_RETURN and self.user_text and self.user_text[0] != " ":
                self.active = False
                name_return = self.user_text
                self.user_text = ""
                return name_return

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
        screen.blit(TEXTURES["mov_choose"], (SCREEN_WIDTH // 2 - 900 // 2, SCREEN_HEIGHT // 2 - 50))
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
