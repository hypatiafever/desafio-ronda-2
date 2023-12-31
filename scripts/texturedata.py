"""Sprites que se utilizan en el juego."""

from constants import *
import pygame


_TEXTURE_DATA = {
    # robots
    "UAIBOT": {"file_path": "res/robots/UAIBOT.png", "size": (TILE_SIZE, TILE_SIZE)},
    "UAIBOTA": {"file_path": "res/robots/UAIBOTA.png", "size": (TILE_SIZE, TILE_SIZE)},
    "UAIBOTINO": {"file_path": "res/robots/UAIBOTINO.png", "size": (TILE_SIZE, TILE_SIZE)},

    # escenario
    "background": {"file_path": "res/scenery/fondo-ciberespacio.png", "size": (SCREEN_WIDTH, SCREEN_HEIGHT)},
    "wall": {"file_path": "res/scenery/pared.png", "size": (TILE_SIZE, TILE_SIZE)},
    "firewall": {"file_path": "res/scenery/firewall.png", "size": (TILE_SIZE, TILE_SIZE)},
    "protected_zone": {"file_path": "res/scenery/areaprotegida.png", "size": (TILE_SIZE, TILE_SIZE)},
    "door_1": {"file_path": "res/scenery/door5.png", "size": (TILE_SIZE, TILE_SIZE)},
    "door_2": {"file_path": "res/scenery/door4.png", "size": (TILE_SIZE, TILE_SIZE)},
    "door_3": {"file_path": "res/scenery/door3.png", "size": (TILE_SIZE, TILE_SIZE)},
    "door_4": {"file_path": "res/scenery/door2.png", "size": (TILE_SIZE, TILE_SIZE)},
    "door_0": {"file_path": "res/scenery/door1.png", "size": (TILE_SIZE, TILE_SIZE)},
    "win": {"file_path": "res/scenery/win.png", "size": (SCREEN_WIDTH, SCREEN_HEIGHT)},
    "mouse_crosshair": {"file_path": "res/menu/mouse_crosshair.png", "size": (TILE_SIZE//2, TILE_SIZE//2)},

    # virus
    "wandering_virus_lin": {"file_path": "res/virus/virus3.png", "size": (TILE_SIZE, TILE_SIZE)},
    "virus1": {"file_path": "res/virus/virus1.png", "size": (TILE_SIZE, TILE_SIZE)},
    "virus2": {"file_path": "res/virus/virus2.png", "size": (TILE_SIZE, TILE_SIZE)},
    "virus3": {"file_path": "res/virus/virus4.png", "size": (TILE_SIZE, TILE_SIZE)},
    "virus4": {"file_path": "res/virus/virus5.png", "size": (TILE_SIZE, TILE_SIZE)},
    "wandering_virus_sin": {"file_path": "res/virus/virus6.png", "size": (TILE_SIZE, TILE_SIZE)},
    "virus1_dead": {"file_path": "res/virus_dead/virus1_dead.png", "size": (TILE_SIZE, TILE_SIZE)},
    "virus2_dead": {"file_path": "res/virus_dead/virus2_dead.png", "size": (TILE_SIZE, TILE_SIZE)},
    "virus3_dead": {"file_path": "res/virus_dead/virus4_dead.png", "size": (TILE_SIZE, TILE_SIZE)},
    "virus4_dead": {"file_path": "res/virus_dead/virus5_dead.png", "size": (TILE_SIZE, TILE_SIZE)},
    "virus5_dead": {"file_path": "res/virus_dead/virus6_dead.png", "size": (TILE_SIZE, TILE_SIZE)},

    # intro
    "intro_frame1": {"file_path": "res/intro/intro_frame1.png", "size": (SCREEN_WIDTH, SCREEN_HEIGHT)},
    "intro_frame2": {"file_path": "res/intro/intro_frame2.png", "size": (SCREEN_WIDTH, SCREEN_HEIGHT)},
    "intro_frame3": {"file_path": "res/intro/intro_frame3.png", "size": (SCREEN_WIDTH, SCREEN_HEIGHT)},
    "intro_frame4": {"file_path": "res/intro/intro_frame4.png", "size": (SCREEN_WIDTH, SCREEN_HEIGHT)},
    "intro_frame5": {"file_path": "res/intro/intro_frame5.png", "size": (SCREEN_WIDTH, SCREEN_HEIGHT)},
    "game_rules": {"file_path": "res/rules/rules.png", "size": (SCREEN_WIDTH, SCREEN_HEIGHT)},

    # rules
    "press_any_black": {"file_path": "res/rules/pressany_black.png", "size": (450, 50)},
    "sin_virus_rules": {"file_path": "res/rules/sin_virus_rules.png", "size": (500, 100)},
    "door_rules": {"file_path": "res/rules/door_rules.png", "size": (500, 100)},
    "firewall_rules": {"file_path": "res/rules/firewall_rule.png", "size": (500, 70)},
    "press_any_white": {"file_path": "res/rules/pressany_white.png", "size": (450, 50)},
    "wandering_virus_rules": {"file_path": "res/rules/wandering_virus_rules.png", "size": (600, 90)},
    "r_return": {"file_path": "res/rules/r_to_go_back.png", "size": (590, 35)},
    "click_virus": {"file_path": "res/rules/click_virus_rules.png", "size": (527, 97)},
    "pause_rules": {"file_path": "res/rules/pause_rules.png", "size": (452, 31)},

    # menu
    "easy_button": {"file_path": "res/menu/button_easy.png", "size": (TILE_SIZE*4, TILE_SIZE*2)},
    "normal_button": {"file_path": "res/menu/button_normal.png", "size": (TILE_SIZE*4, TILE_SIZE*2)},
    "hard_button": {"file_path": "res/menu/button_hard.png", "size": (TILE_SIZE*4, TILE_SIZE*2)},
    "text_background_1": {"file_path": "res/menu/text_background_1.png", "size": (400, 46)},
    "text_background_2": {"file_path": "res/menu/text_background_2.png", "size": (156, 46)},
    "text_background_3": {"file_path": "res/menu/text_background_3.png", "size": (670, 60)},
    "start_menu_background": {"file_path": "res/menu/start_menu_bg.png", "size": (SCREEN_WIDTH, SCREEN_HEIGHT)},
    "insert_name": {"file_path": "res/menu/insert_name.png", "size": (252, 36)},
    "mov_choose": {"file_path": "res/menu/movement_choose.png", "size": (942, 108)},

    # pause
    "exit_button": {"file_path": "res/pause/button_exit.png", "size": (TILE_SIZE*4, TILE_SIZE*2)},
    "continue_button": {"file_path": "res/pause/button_continue.png", "size": (TILE_SIZE*4, TILE_SIZE*2)},
    "rules_button": {"file_path": "res/pause/button_rules.png", "size": (TILE_SIZE*4, TILE_SIZE*2)},
    "options_button": {"file_path": "res/pause/button_options.png", "size": (TILE_SIZE*4, TILE_SIZE*2)},
    "indicators_rect": {"file_path": "res/pause/input_rect.png", "size": (TILE_SIZE*2, TILE_SIZE*2)},
    "but_up": {"file_path": "res/pause/button_up.png", "size": (TILE_SIZE*2, TILE_SIZE*2)},
    "but_up_pressed": {"file_path": "res/pause/button_up_pressed.png", "size": (TILE_SIZE*2, TILE_SIZE*2)},
    "but_down": {"file_path": "res/pause/button_down.png", "size": (TILE_SIZE*2, TILE_SIZE*2)},
    "but_down_pressed": {"file_path": "res/pause/button_down_pressed.png", "size": (TILE_SIZE*2, TILE_SIZE*2)},
    "volume_text": {"file_path": "res/pause/volume_text.png", "size": (156, 46)},
    "hardness_text": {"file_path": "res/pause/hardness_text.png", "size": (196, 78)},

}

TEXTURES: dict = {}


def load_textures():
    """Carga un diccionario con los objetos de imágen."""
    for name, data in _TEXTURE_DATA.items():
        TEXTURES[name] = pygame.transform.scale(
            pygame.image.load(
                data["file_path"]).convert_alpha(), (data["size"]))
