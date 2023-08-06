import pygame

class SoundManager:
    def __init__(self):
        self.sounds = []
        self.backs = []

    def set_sound(self, sound):
        self.sounds.append(sound)

    def set_back(self, back):
        self.backs.append(back)

    def play_sound(self, sound_name):
        for i in range(len(self.sounds)):
            if self.sounds[i].name == sound_name:
                self.sounds[i].sound.set_volume(self.sounds[i].volume)
                self.sounds[i].sound.play(self.sounds[i].loop)

    def stop_sound(self, sound_name):
        for i in range(len(self.sounds)):
            if self.sounds[i].name == sound_name:
                self.sounds[i].sound.stop()

    def play_back(self, back_name):
        for i in range(len(self.backs)):
            if self.backs[i].name == back_name:
                pygame.mixer.music.load(self.backs[i].sound)
                pygame.mixer.music.set_volume(self.backs[i].volume)
                pygame.mixer.stop(self.backs[i].loop)

    def pause_back(self, back_name):
        for i in range(len(self.backs)):
            if self.backs[i].name == back_name:
                pygame.mixer.music.pause()

    def pause_back(self, back_name):
        for i in range(len(self.backs)):
            if self.backs[i].name == back_name:
                pygame.mixer.music.pause()

    def unpause_back(self, back_name):
        for i in range(len(self.backs)):
            if self.backs[i].name == back_name:
                pygame.mixer.music.unpause()

    def stop_back(self, back_name):
        for i in range(len(self.backs)):
            if self.backs[i].name == back_name:
                pygame.mixer.music.stop()


class Sound:
    def __init__(self, sound, volume, loop):
        self.sound = pygame.mixer.Sound(sound)
        self.sound.set_volume(volume)
        self.volume = volume
        self.loop = loop


class Background:
    def __init__(self, sound, volume, loop):
        self.sound = sound
        self.volume = volume
        self.loop = loop
