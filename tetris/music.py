# tetris\music.py
import os
import random
import pygame
from abc import ABC, abstractmethod

class MusicPlayerInterface(ABC):
    @abstractmethod
    def load_songs(self):
        pass

    @abstractmethod
    def play_song(self, song):
        pass

    @abstractmethod
    def check_music(self):
        pass


class MusicPlayer(MusicPlayerInterface):
    def __init__(self):
        self.current_song = ""

    def load_songs(self):
        songs = []
        music_path = "assets/music"
        for song in os.listdir(music_path):
            if song.endswith('.mp3') or song.endswith('.ogg'):
                songs.append(os.path.join(music_path, song))
        return songs

    def play_song(self, song):
        self.current_song = song
        pygame.mixer.music.load(self.current_song)
        pygame.mixer.music.play(0)

    def check_music(self):
        if not pygame.mixer.music.get_busy():
            self.play_song(self.current_song)
        return os.path.basename(self.current_song)


class RandomSongDecorator(MusicPlayerInterface):
    def __init__(self, music_player):
        self.music_player = music_player
        self.songs = self.music_player.load_songs()
    
    @property
    def current_song(self):
        return self.music_player.current_song

    def load_songs(self):
        return self.music_player.load_songs()

    def play_song(self, song):
        self.music_player.play_song(song)

    def play_random_song(self):
        song = random.choice(self.songs)
        self.play_song(song)
        return os.path.basename(song)

    def check_music(self):
        if not pygame.mixer.music.get_busy():
            self.play_random_song()
        return os.path.basename(self.current_song)
