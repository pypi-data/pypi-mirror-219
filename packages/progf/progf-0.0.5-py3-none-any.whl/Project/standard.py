import Project.project as project
import Project.drawable as drawable
import Project.sound as sound
import pygame
import os

def make_project(Project_Name):
    os.mkdir(Project_Name)
    os.mkdir(f"{Project_Name}\\source")
    os.mkdir(f"{Project_Name}\\scripts")
    f1 = open(f"{Project_Name}\\scripts\\games.py", "w")
    f2 = open(f"{os.path.dirname(os.path.realpath(__file__))}\\games.py", "r")
    for i in f2.readlines():
        f1.write(i)
    f1.close()
    f2.close()



Game = project.GameManager("Project Game", drawable.Image(f"{os.path.dirname(os.path.realpath(__file__))}\\project_image.jpg", (500, 500)), (1000, 1000),
                           pygame.DOUBLEBUF | pygame.HWSURFACE)
Frame = project.FrameManager(60)
Time = project.TimeManager(False)
Input = project.InputManager()
Music = sound.SoundManager
