# tetris\music.py
import os
import random
import pygame
from abc import ABC, abstractmethod

class MusicPlayerInterface(ABC):
    """
    Abstract base class for music player implementations.
    """
    @abstractmethod
    def load_songs(self):
        """
        Load available songs from the music directory.

        Returns:
            list: A list of available songs.
        """
        pass

    @abstractmethod
    def play_song(self, song):
        """
        Play the specified song.

        Args:
            song (str): The path to the song file.
        """
        pass

    @abstractmethod
    def check_music(self):
        """
        Check if the music is playing, and restart it if it has stopped.

        Returns:
            str: The filename of the currently playing song.
        """
        pass


class MusicPlayer(MusicPlayerInterface):
    """
    Class for managing music playback in the game.
    """
    def __init__(self):
        """
        Initialize the MusicPlayer instance.
        """
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
    """
    Class for decorating MusicPlayer with random song playback.
    """
    def __init__(self, music_player):
        """
        Initialize the RandomSongDecorator with a MusicPlayer instance.

        Args:
            music_player (MusicPlayer): A MusicPlayer instance.
        """
        self.music_player = music_player
        self.songs = self.music_player.load_songs()
    
    @property
    def current_song(self):
        """
        Get the current song being played by the decorated music player.

        Returns:
            str: The filename of the currently playing song.
        """
        return self.music_player.current_song

    def load_songs(self):
        return self.music_player.load_songs()

    def play_song(self, song):
        self.music_player.play_song(song)

    def play_random_song(self):
        """
        Play a random song from the available songs.

        Returns:
            str: The filename of the randomly chosen song.
        """
        song = random.choice(self.songs)
        self.play_song(song)
        return os.path.basename(song)

    def check_music(self):
        if not pygame.mixer.music.get_busy():
            self.play_random_song()
        return os.path.basename(self.current_song)
