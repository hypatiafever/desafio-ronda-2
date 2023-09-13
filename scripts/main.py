"""Equipo: 19014 - THEVECTORS
Institución: 300292400 - ESCUELA DEL CAE D-170
RONDA 2

Crea el juego (mainloop) e inicializa el módulo pygame.

Versión 2.8.2
Estándar de estilo utilizado: PEP8 (https://peps.python.org/pep-0008/)."""

import sys
import pygame
from constants import *
from gui import MovementsMenu, Pause, NameMenu, StartMenu, Options
from pygame import Surface
from scene import Scene
from texturedata import load_textures
from math import trunc


class Game():
    """Contiene la escena y procesa eventos"""

    def __init__(self):

        # definimos el tamaño de la pantalla
        self.screen: Surface = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()  # creamos un reloj para los fps
        load_textures()

        self.start_menu: StartMenu = StartMenu()
        self.name_menu: NameMenu = NameMenu(self.screen)
        self.options: Options = Options(self.screen, 5)
        self.mov_amount_ui: MovementsMenu = MovementsMenu()
        self.pause: Pause = Pause()
        self.scene: Scene = Scene(self.screen, self.mov_amount_ui, self.pause, self.name_menu, self.start_menu, self.options)

        self.paused = False
        self.running = True
        self.in_rounds = False

        self.username = ""
        self.data_recorded = False

        self.mouse_moved_amount = 0

    def run(self):
        """Inicia el mainloop del juego."""

        while (self.running):
            self.update()
        self.finish()

    def update(self):
        """Código que se ejecuta en cada frame."""

        # region --- Events ---

        self.in_rounds = self.scene.round > 0 and self.scene.round <= self.scene.grid.round_count

        # detecta los inputs del usuario
        for event in pygame.event.get():
            if self.scene.round == -2:
                self.username = self.name_menu.handle_writing(event)
                if self.username:
                    self.scene.round += 1  

            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and self.in_rounds:  # maneja la activación del estado de pausa
                if event.key == pygame.K_ESCAPE and not self.paused and not self.scene.dead:
                    self.paused = True
                    continue
                if event.key == pygame.K_ESCAPE and self.paused:
                    if self.scene.show_rules:
                        self.scene.show_rules = False
                    elif self.scene.show_options:
                        self.scene.show_options = False
                    else:
                        self.paused = False
                    continue

            if not self.paused and self.in_rounds:  # maneja el input de las rondas
                if event.type == pygame.KEYDOWN:
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
                if event.type == pygame.MOUSEMOTION and not self.scene.dead:
                    self.mouse_moved_amount += 1
                    if self.mouse_moved_amount >= MOUSE_MOV_REQ * sensitivity_level:
                        self.scene.move_virus()
                        self.mouse_moved_amount = 0
                if event.type == pygame.MOUSEBUTTONUP and not self.scene.dead:
                    self.scene.reset_virus_pos(event.pos)

            if event.type == pygame.KEYDOWN and not self.in_rounds:  # maneja el input fuera de las rondas
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r and not self.name_menu.active and not self.scene.round == -3:
                    self.data_recorded = False
                    self.scene.reset_game()
                if self.scene.round == 0 and self.scene.difficulty_set:  # toma cualquier input de tecla durante la intro
                    self.scene.continue_intro()
                if self.scene.round == -3:
                    self.scene.round += 1

            if event.type == pygame.MOUSEBUTTONUP:

                if self.paused and not self.scene.show_rules and not self.scene.show_options:  # toma la interacción con los botones de la pausa
                    result = self.pause.define_button_pressed()
                    if result == 1:
                        self.paused = False
                    if result == 2:
                        self.running = False
                    if result == 3:
                        self.scene.show_rules = True
                    if result == 4:
                        self.scene.show_options = True

                if self.scene.round == -1:  # toma la interacción con los botones de dificultad
                    result = self.mov_amount_ui.define_button_pressed()
                    if result:
                        self.scene.difficulty = result - 1
                        self.scene.difficulty_set = True
                        self.scene.round += 1

                if self.scene.round == -3:
                    self.scene.round += 1

                if self.scene.round == 0 and self.scene.difficulty_set:  # toma el paso de la intro
                    self.scene.continue_intro()
        # endregion

        if self.scene.round > self.scene.grid.round_count and not self.data_recorded:
            self.scene.won_game = True
            self.data_recorded = True
            self.write_to_scoreboard()

        self.scene.update(self.in_rounds, self.paused)
        pygame.display.update()
        self.clock.tick(FPS)

    def write_to_scoreboard(self):
        full_string = self.username
        with open("res/ranking.txt", "a") as sb:
            for index in range(self.scene.grid.round_count):
                full_string += f" | n{index + 1}: {self.scene.steps_used_per_round[index]} steps, {trunc(self.scene.time_spent_per_round[index])} seconds"
            full_string += "\n"
            sb.write(full_string)


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
