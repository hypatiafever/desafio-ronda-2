"""Equipo: 19014 - THEVECTORS
Institución: 300292400 - ESCUELA DEL CAE D-170
RONDA 2

Crea el juego (mainloop) e inicializa el módulo pygame.

Versión 1.1.0
Estándar de estilo utilizado: PEP8 (https://peps.python.org/pep-0008/)"""

import sys
import pygame
from constants import *
from gui import Menu, Pause
from pygame import Surface
from scene import Scene
from texturedata import load_textures


class Game():
    """Contiene la escena y procesa eventos"""

    def __init__(self):

        # definimos el tamaño de la pantalla
        self.screen: Surface = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()  # creamos un reloj para los fps
        load_textures()

        self.menu: Menu = Menu()
        self.pause: Pause = Pause()
        self.scene: Scene = Scene(self.screen, self.menu, self.pause)

        self.paused = False
        self.running = True
        self.in_rounds = False

    def run(self):
        """Inicia el mainloop del juego."""

        while (self.running):
            self.update()
        self.finish()

    def update(self):
        """Código que se ejecuta en cada frame."""

        # region --- Events ---

        self.in_rounds = self.scene.round > 0 and self.scene.round < self.scene.grid.round_count

        # detecta los inputs del usuario
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and self.in_rounds:  # maneja la activación del estado de pausa
                if event.key == pygame.K_ESCAPE and not self.paused and not self.scene.dead:
                    self.paused = True
                    continue
                if event.key == pygame.K_ESCAPE and self.paused:
                    if self.scene.show_rules:
                        self.scene.show_rules = False
                    else:
                        self.paused = False
                    continue
            if event.type == pygame.KEYDOWN and not self.paused and self.in_rounds:  # maneja el input de las rondas
                if event.key == pygame.K_ESCAPE and not self.in_rounds:
                    self.running = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.scene.move("right")
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.scene.move("left")
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.scene.move("up")
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.scene.move("down")
                if event.key == pygame.K_r:
                    self.scene.restart()
                if event.key == pygame.K_e:
                    self.scene.change_robot()

            if event.type == pygame.KEYDOWN and not self.in_rounds:  # maneja el input fuera de las rondas
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r:
                    self.scene.reset_game()
                if self.scene.round == 0 and self.scene.difficulty_set:  # toma cualquier input de tecla durante la intro
                    if self.scene.intro_frame_num < 7:  # pasa al siguiente frame o termina la animaciòn
                        self.scene.intro_frame_num += 1
                    else:
                        self.scene.intro_finished = True

            if event.type == pygame.MOUSEBUTTONUP:

                if self.paused and not self.scene.show_rules:  # toma la interacción con los botones de la pausa
                    result = self.pause.define_button_pressed()
                    if result == 1:
                        self.paused = False
                    if result == 2:
                        self.running = False
                    if result == 3:
                        self.scene.show_rules = True

                if self.scene.round == 0 and self.scene.difficulty_set:  # toma el paso de la intro
                    if self.scene.intro_frame_num < 7:  # pasa al siguiente frame o termina la animaciòn
                        self.scene.intro_frame_num += 1
                    else:
                        self.scene.intro_finished = True

                if not self.scene.difficulty_set:  # toma la interacción con los botones de dificultad
                    result = self.menu.define_button_pressed()
                    if result:
                        self.scene.difficulty = result - 1
                        self.scene.difficulty_set = True
                        self.scene.audio_player.stop_music()

        # endregion

        self.scene.update(self.in_rounds, self.paused)
        pygame.display.update()
        self.clock.tick(FPS)

    def finish(self):
        """Finaliza el programa."""
        self.scene.audio_player.stop_music()
        pygame.quit()
        sys.exit()


# Inicio del programa
if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
