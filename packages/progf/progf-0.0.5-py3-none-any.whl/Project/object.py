import pygame
import Project.standard as standard
import random

ids = []

def makeId():
    text = "abcdefghijklmnopqrxtuvwxyz"
    code = ""
    for i in range(64):
        if random.randrange(0, 6) <= 3:
            code += str(random.randrange(0, 10))
        else:
            if random.randrange(0, 2) == 0:
                code += text[random.randrange(0, len(text))].upper()
            else:
                code += text[random.randrange(0, len(text))].lower()
    for i in ids:
        if i == code:
            code = makeId()
    ids.append(code)
    return code

class Object:
    def __init__(self, name, transform, back):
        self.name = name
        self.id = makeId()
        self.transform = transform
        self.components = []
        self.back = back

    def start(self):
        pass

    def update(self):
        self.show()
        for i in self.components:
            i.update()

    def end(self):
        pass

    def show(self):
        image = pygame.transform.scale(self.back.image, self.back.size)
        image = pygame.transform.rotozoom(image, self.transform.rotation, 1)
        rect = image.get_rect()
        rect.center = (self.transform.position.x, self.transform.position.y)
        standard.Game.screen.blit(image, rect)

    def set_component(self, component):
        self.components.append(component)
        component.now = self
        component.start()


class Component:
    def __init__(self, name):
        self.name = name
        self.now = None

    def start(self):
        pass

    def update(self):
        pass

    def end(self):
        pass
