"""Funcionalidades relacionadas a la música y sonidos del juego.

AudioHandler permite la implementación de pygame mixer y mixer.music,
de manera compacta y accesible."""


from constants import *
from pygame import mixer
from settings import GameSettings


class AudioHandler():

    def __init__(self, settings: GameSettings):
        self.settings = settings
        self.sounds_channel: mixer.Channel = mixer.Channel(1)
        self.sounds_channel.set_volume(0.3 * (self.settings.volume_level / 10))
        mixer.music.set_volume(1 * (self.settings.volume_level / 10))

    def play_sound(self, file_path: str):
        """Reproduce un sonido corto por un canal común."""
        self.sounds_channel.play(mixer.Sound(file_path))

    def play_music(self, file_path: str):
        """Si no se está reproduciendo música, la reproduce."""
        if not mixer.music.get_busy():
            mixer.music.load(file_path)
            mixer.music.play(-1)

    def stop_music(self):
        """Frena la reproducción de música y libera este espacio."""
        mixer.music.stop()
        mixer.music.unload()

    def interrupt_music(self, track_path: str, interruption_path: str):
        """Interrumpe brevemente la música para introducir un segundo sonido y luego continuar."""
        mixer.music.stop()
        mixer.music.load(interruption_path)
        mixer.music.play()
        mixer.music.queue(track_path, loops=-1)

    def lower_music_vol(self):
        """Baja el volúmen, pensado para el menú de pausa."""
        mixer.music.set_volume(0.3 * (self.settings.volume_level / 10))
        mixer.Channel(1).set_volume(0.1 * (self.settings.volume_level / 10))

    def reset_music_vol(self):
        """Reestablece el volúmen original."""
        mixer.music.set_volume(1 * (self.settings.volume_level / 10))
        mixer.Channel(1).set_volume(0.3 * (self.settings.volume_level / 10))
