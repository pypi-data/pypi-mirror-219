import pygame
import pygame as py
from time import time
from threading import Thread
import Project.drawable as drawable


def err_print(message):
    print(f"\033[31m{message}\033[0m")


class Scene:
    def __init__(self, name, back):
        self.number = -1
        self.name = name
        self.back = back
        self.rule = []
        self.objects = []

    def set_object(self, object):
        self.objects.append(object)
        object.start()

    def del_object(self, object_id_or_name):
        for i in range(len(self.objects)):
            if self.objects[i].id == object_id_or_name or self.objects[i].name == object_id_or_name:
                d = self.objects[i]
                d.end()
                self.objects.pop(i)
                return d
        err_print("Project: no such object.")

    def find_object(self, object_id_or_name):
        for i in range(len(self.objects)):
            if self.objects[i].id == object_id_or_name or self.objects[i].name == object_id_or_name:
                return self.objects[i]
        err_print("Project: no such object.")

    def change_object(self, object_id_or_name, object):
        for i in range(len(self.objects)):
            if self.objects[i].id == object_id_or_name or self.objects[i].name == object_id_or_name:
                d = self.objects[i]
                d.end()
                object.start()
                self.objects[i] = object
                return d
        err_print("Project: no such object.")

    def end(self):
        for i in self.objects:
            i.end()


class GameManager:
    def __init__(self, name, icon, size, mode):
        self.scenes = []
        self.rules = []
        self.now = 0
        self.mode = mode
        self.name = name
        self.icon = icon
        self.size = size
        self.state = ""
        self.variables = {}
        self.screen = pygame.display.set_mode(size, mode)
        pygame.display.set_caption(name)
        pygame.display.set_icon(icon.image)

    def set_rule(self, rule):
        self.rules.append(rule)

    def get_rule(self, rule_name):
        for i in range(len(self.rules)):
            if self.rules[i].name == rule_name:
                return self.rules[i]
        err_print("Project: no such scene.")

    def change_rule(self, rule_name, rule):
        for i in range(len(self.rules)):
            if self.rules[i].name == rule_name:
                self.rules[i] = rule
                return
        err_print("Project: no such rule.")

    def del_rule(self, rule_name):
        for i in range(len(self.rules)):
            if self.rules[i].name == rule_name:
                self.rules[i].destroy()
                self.rules.pop(i)
                break
        if len(self.rules) == i:
            err_print("Project: no such rule.")

    def add_scene(self, scene):
        scene.number = len(self.scenes)
        self.scenes.append(scene)

    def del_scene(self, scene_name_or_num):
        i = 0
        for i in range(len(self.scenes)):
            if self.scenes[i].number == scene_name_or_num or self.scenes[i].name == scene_name_or_num:
                self.scenes.pop(i)
                break
        if len(self.scenes) == i:
            err_print("Project: no such scene.")
        for i in range(i, len(self.scenes)):
            self.scenes[i].number -= 1

    def change_scene(self, scene_name_or_num, scene):
        for i in range(len(self.scenes)):
            if self.scenes[i].number == scene_name_or_num or self.scenes[i].name == scene_name_or_num:
                self.scenes[i] = scene
                return
        err_print("Project: no such scene.")

    def get_scene(self, scene_name_or_num):
        for i in range(len(self.scenes)):
            if self.scenes[i].number == scene_name_or_num or self.scenes[i].name == scene_name_or_num:
                return self.scenes[i]
        err_print("Project: no such scene.")

    def go_scene(self, scene_name_or_num):
        for i in range(len(self.scenes)):
            if self.scenes[i].number == scene_name_or_num or self.scenes[i].name == scene_name_or_num:
                now = i
                return
        for i in self.rules:
            i.start()
        err_print("Project: no such scene.")

    def set_object(self, object):
        self.scenes[self.now].set_object(object)
        if self.state == "RUN":
            object.start()

    def del_object(self, object_id_or_name):
        d = self.scenes[self.now].del_object(object_id_or_name)
        if self.state == "RUN":
            d.end()

    def find_object(self, object_id_or_name):
        return self.scenes[self.now].find_object(object_id_or_name)

    def change_object(self, object_id_or_name, object):
        d = self.scenes[self.now].change_object(object_id_or_name, object)
        if self.state == "RUN":
            d.end()
            object.start()

    def move_scene(self, num):
        if len(self.scenes) > self.now + num:
            self.now += num
            for i in self.rules:
                i.start()
        else:
            err_print("Project: index is out of range.")

    def run(self, state):
        if state == "RUN":
            self.state = state
        elif state == "END":
            self.state = state
            self.scenes[self.now].end()
            for i in self.rules:
                i.end()
            exit()
        else:
            err_print("Project: illegal state.")

    def update(self):
        for i in self.rules:
            i.update()
        for i in self.scenes[self.now].objects:
            i.update()
            i.show()


class FrameManager:
    def __init__(self, fps_limit):
        self.fps_limit = fps_limit
        self.fps_tick = 0
        self.fps_now = 0
        self.time = time() / 1000000

    def fps_check(self):
        if ((time() / 1000000) - self.time) >= 60:
            self.fps_now = self.fps_tick
            self.fps_tick = 0
            self.time = time()

    def fps_pls(self):
        self.fps_tick += 1


class TimeManager:
    def __init__(self, multi):
        self.timers = []
        self.invokes = []
        self.multi = multi

    def invoke(self, function):
        function.time = time() / 1000000
        self.invokes.append([function, 0])

    def wait_function(self, function_name):
        for i in range(len(self.invokes)):
            if self.invokes[i][0].name == function_name:
                self.invokes[i][0].state == 0
                return
        err_print("Project: no such function.")

    def run_function(self, function_name):
        for i in range(len(self.invokes)):
            if self.invokes[i][0].name == function_name:
                self.invokes[i][0].state == 1
                self.invokes[i][0].time == time() / 1000000
                return
        err_print("Project: no such function.")

    def del_function(self, function_name):
        for i in range(len(self.invokes)):
            if self.invokes[i][0].name == function_name:
                self.invokes.pop(i)
                return
        err_print("Project: no such function.")

    def set_timer(self, num):
        self.timers.append([num, time() / 1000000, 0])

    def start_timer(self, num):
        for i in range(len(self.timers)):
            if self.timers[i][0] == num:
                self.timers[i][2] == 1
                self.timers[i][1] == time() / 1000000
                return
        err_print("Project: no such timer.")

    def stop_timer(self, num):
        for i in range(len(self.timers)):
            if self.timers[i][0] == num:
                self.timers[i][2] == 0
                return
        err_print("Project: no such timer.")

    def del_timer(self, num):
        for i in range(len(self.timers)):
            if self.timers[i][0] == num:
                self.timers.pop(i)
                return
        err_print("Project: no such timer.")

    def get_state(self, num):
        for i in range(len(self.timers)):
            if self.timers[i][0] == num:
                return self.timers[i][2]

    def update(self):
        if self.multi:
            now = time() / 1000000
            for i in self.invokes:
                if i[0].state == 1:
                    if now - i[0].time >= i[0].num:
                        f = Thread(target=i[0].function)
                        f.start()
                        f.join()
                        i[0].time = time() / 1000000
                        i[1] += 1
            for i in self.timers:
                if i[2] == 1:
                    i[0] -= now - i[1]
                    i[1] = time() / 1000000

            for i in self.invokes:
                if i[0].count == i[1]:
                    self.del_function(i[0].name)
            for i in range(len(self.timers)):
                if self.timers[i][0] <= 0:
                    self.stop_timer(i)
        else:
            now = time() / 1000000
            for i in self.invokes:
                if i[0].state == 1:
                    if now - i[0].time >= i[0].num:
                        i[0].function()
                        i[0].time = time() / 1000000
                        i[1] += 1
            for i in self.timers:
                if i[2] == 1:
                    i[0] -= now - i[1]
                    i[1] = time() / 1000000

            for i in self.invokes:
                if i[0].count == i[1]:
                    self.del_function(i[0].name)
            for i in range(len(self.timers)):
                if self.timers[i][0] <= 0:
                    self.stop_timer(i)


class Function:
    def __init__(self, name, function, time, num, count):
        self.name = name
        self.function = function
        self.time = time
        self.num = num
        self.count = count


class InputManager:
    def __init__(self):
        self.mouse_pos = Vector2(0, 0)
        self.is_pressed = dict(
            MOUSE_LEFT=False,
            MOUSE_WHEEL=False,
            MOUSE_RIGHT=False,
            MOUSE_UP=False,
            MOUSE_DOWN=False,
            A=False,
            B=False,
            C=False,
            D=False,
            E=False,
            F=False,
            G=False,
            H=False,
            I=False,
            J=False,
            K=False,
            L=False,
            M=False,
            N=False,
            O=False,
            P=False,
            Q=False,
            R=False,
            S=False,
            T=False,
            U=False,
            V=False,
            W=False,
            X=False,
            Y=False,
            Z=False,
            NUM_0=False,
            NUM_1=False,
            NUM_2=False,
            NUM_3=False,
            NUM_4=False,
            NUM_5=False,
            NUM_6=False,
            NUM_7=False,
            NUM_8=False,
            NUM_9=False,
            BACK=False,
            TAB=False,
            CLEAR=False,
            ENTER=False,
            PAUSE=False,
            ESCAPE=False,
            SPACE=False,
            EXCLAIM=False,
            QUOTEDBL=False,
            HASH=False,
            DOLLAR=False,
            AMPERSAND=False,
            QUOTE=False,
            LEFTPAREN=False,
            RIGHTPAREN=False,
            ASTERISK=False,
            PLUS=False,
            COMMA=False,
            MINUS=False,
            PERIOD=False,
            SLASH=False,
            COLON=False,
            SEMICOLON=False,
            LESS=False,
            EQUALS=False,
            GREATER=False,
            QUESTION=False,
            AT=False,
            LEFTBRACKET=False,
            RIGHTBRACKET=False,
            BACKSLASH=False,
            CARET=False,
            UNDERSCORE=False,
            BACKQUOTE=False,
            DELETE=False,
            KEY_0=False,
            KEY_1=False,
            KEY_2=False,
            KEY_3=False,
            KEY_4=False,
            KEY_5=False,
            KEY_6=False,
            KEY_7=False,
            KEY_8=False,
            KEY_9=False,
            KEY_PERIOD=False,
            KEY_DIVIDE=False,
            KEY_MULTIPLY=False,
            KEY_MINUS=False,
            KEY_PLUS=False,
            KEY_ENTER=False,
            KEY_EQUALS=False,
            UP=False,
            DOWN=False,
            RIGHT=False,
            LEFT=False,
            INSERT=False,
            HOME=False,
            PAGEUP=False,
            PAGEDOWN=False,
            F1=False,
            F2=False,
            F3=False,
            F4=False,
            F5=False,
            F6=False,
            F7=False,
            F8=False,
            F9=False,
            F10=False,
            F11=False,
            F12=False,
            F13=False,
            F14=False,
            F15=False,
            NUMLOCK=False,
            CAPSLOCK=False,
            SCROLLOCK=False,
            RSHIFT=False,
            LSHIFT=False,
            RCTRL=False,
            LCTRL=False,
            RALT=False,
            LALT=False,
            RMETA=False,
            LMETA=False,
            LSUPER=False,
            RSUPER=False,
            MODE=False,
            HELP=False,
            PRINT=False,
            SYSREQ=False,
            BREAK=False,
            MENU=False,
            POWER=False,
            EURO=False
        )
        self.is_pressed_out = dict(
            MOUSE_LEFT=False,
            MOUSE_WHEEL=False,
            MOUSE_RIGHT=False,
            MOUSE_UP=False,
            MOUSE_DOWN=False,
            A=False,
            B=False,
            C=False,
            D=False,
            E=False,
            F=False,
            G=False,
            H=False,
            I=False,
            J=False,
            K=False,
            L=False,
            M=False,
            N=False,
            O=False,
            P=False,
            Q=False,
            R=False,
            S=False,
            T=False,
            U=False,
            V=False,
            W=False,
            X=False,
            Y=False,
            Z=False,
            NUM_0=False,
            NUM_1=False,
            NUM_2=False,
            NUM_3=False,
            NUM_4=False,
            NUM_5=False,
            NUM_6=False,
            NUM_7=False,
            NUM_8=False,
            NUM_9=False,
            BACK=False,
            TAB=False,
            CLEAR=False,
            ENTER=False,
            PAUSE=False,
            ESCAPE=False,
            SPACE=False,
            EXCLAIM=False,
            QUOTEDBL=False,
            HASH=False,
            DOLLAR=False,
            AMPERSAND=False,
            QUOTE=False,
            LEFTPAREN=False,
            RIGHTPAREN=False,
            ASTERISK=False,
            PLUS=False,
            COMMA=False,
            MINUS=False,
            PERIOD=False,
            SLASH=False,
            COLON=False,
            SEMICOLON=False,
            LESS=False,
            EQUALS=False,
            GREATER=False,
            QUESTION=False,
            AT=False,
            LEFTBRACKET=False,
            RIGHTBRACKET=False,
            BACKSLASH=False,
            CARET=False,
            UNDERSCORE=False,
            BACKQUOTE=False,
            DELETE=False,
            KEY_0=False,
            KEY_1=False,
            KEY_2=False,
            KEY_3=False,
            KEY_4=False,
            KEY_5=False,
            KEY_6=False,
            KEY_7=False,
            KEY_8=False,
            KEY_9=False,
            KEY_PERIOD=False,
            KEY_DIVIDE=False,
            KEY_MULTIPLY=False,
            KEY_MINUS=False,
            KEY_PLUS=False,
            KEY_ENTER=False,
            KEY_EQUALS=False,
            UP=False,
            DOWN=False,
            RIGHT=False,
            LEFT=False,
            INSERT=False,
            HOME=False,
            PAGEUP=False,
            PAGEDOWN=False,
            F1=False,
            F2=False,
            F3=False,
            F4=False,
            F5=False,
            F6=False,
            F7=False,
            F8=False,
            F9=False,
            F10=False,
            F11=False,
            F12=False,
            F13=False,
            F14=False,
            F15=False,
            NUMLOCK=False,
            CAPSLOCK=False,
            SCROLLOCK=False,
            RSHIFT=False,
            LSHIFT=False,
            RCTRL=False,
            LCTRL=False,
            RALT=False,
            LALT=False,
            RMETA=False,
            LMETA=False,
            LSUPER=False,
            RSUPER=False,
            MODE=False,
            HELP=False,
            PRINT=False,
            SYSREQ=False,
            BREAK=False,
            MENU=False,
            POWER=False,
            EURO=False
        )
        self.is_pressing = dict(
            MOUSE_LEFT=False,
            MOUSE_WHEEL=False,
            MOUSE_RIGHT=False,
            MOUSE_UP=False,
            MOUSE_DOWN=False,
            A=False,
            B=False,
            C=False,
            D=False,
            E=False,
            F=False,
            G=False,
            H=False,
            I=False,
            J=False,
            K=False,
            L=False,
            M=False,
            N=False,
            O=False,
            P=False,
            Q=False,
            R=False,
            S=False,
            T=False,
            U=False,
            V=False,
            W=False,
            X=False,
            Y=False,
            Z=False,
            NUM_0=False,
            NUM_1=False,
            NUM_2=False,
            NUM_3=False,
            NUM_4=False,
            NUM_5=False,
            NUM_6=False,
            NUM_7=False,
            NUM_8=False,
            NUM_9=False,
            BACK=False,
            TAB=False,
            CLEAR=False,
            ENTER=False,
            PAUSE=False,
            ESCAPE=False,
            SPACE=False,
            EXCLAIM=False,
            QUOTEDBL=False,
            HASH=False,
            DOLLAR=False,
            AMPERSAND=False,
            QUOTE=False,
            LEFTPAREN=False,
            RIGHTPAREN=False,
            ASTERISK=False,
            PLUS=False,
            COMMA=False,
            MINUS=False,
            PERIOD=False,
            SLASH=False,
            COLON=False,
            SEMICOLON=False,
            LESS=False,
            EQUALS=False,
            GREATER=False,
            QUESTION=False,
            AT=False,
            LEFTBRACKET=False,
            RIGHTBRACKET=False,
            BACKSLASH=False,
            CARET=False,
            UNDERSCORE=False,
            BACKQUOTE=False,
            DELETE=False,
            KEY_0=False,
            KEY_1=False,
            KEY_2=False,
            KEY_3=False,
            KEY_4=False,
            KEY_5=False,
            KEY_6=False,
            KEY_7=False,
            KEY_8=False,
            KEY_9=False,
            KEY_PERIOD=False,
            KEY_DIVIDE=False,
            KEY_MULTIPLY=False,
            KEY_MINUS=False,
            KEY_PLUS=False,
            KEY_ENTER=False,
            KEY_EQUALS=False,
            UP=False,
            DOWN=False,
            RIGHT=False,
            LEFT=False,
            INSERT=False,
            HOME=False,
            PAGEUP=False,
            PAGEDOWN=False,
            F1=False,
            F2=False,
            F3=False,
            F4=False,
            F5=False,
            F6=False,
            F7=False,
            F8=False,
            F9=False,
            F10=False,
            F11=False,
            F12=False,
            F13=False,
            F14=False,
            F15=False,
            NUMLOCK=False,
            CAPSLOCK=False,
            SCROLLOCK=False,
            RSHIFT=False,
            LSHIFT=False,
            RCTRL=False,
            LCTRL=False,
            RALT=False,
            LALT=False,
            RMETA=False,
            LMETA=False,
            LSUPER=False,
            RSUPER=False,
            MODE=False,
            HELP=False,
            PRINT=False,
            SYSREQ=False,
            BREAK=False,
            MENU=False,
            POWER=False,
            EURO=False
        )

    def key_down(self, keycode: str):
        if keycode == "ALL":
            pressed = []
            for i in self.is_pressed.keys():
                if self.is_pressed[i]:
                    pressed.append(i)
            return pressed
        return self.is_pressed[keycode]

    def key_up(self, keycode: str):
        if keycode == "ALL":
            pressed_out = []
            for i in self.is_pressed_out.keys():
                if self.is_pressed_out[i]:
                    pressed_out.append(i)
            return pressed_out
        return self.is_pressed_out[keycode]

    def key(self, keycode: str):
        if keycode == "ALL":
            pressing = []
            for i in self.is_pressing.keys():
                if self.is_pressing[i]:
                    pressing.append(i)
            return pressing
        return self.is_pressing[keycode]

    def Press(self, keycode: str):
        if self.is_pressed[keycode] is not True:
            self.is_pressed[keycode] = True
            self.is_pressing[keycode] = True
            self.is_pressed_out[keycode] = False
        else:
            self.is_pressed[keycode] = False
            self.is_pressing[keycode] = True
            self.is_pressed_out[keycode] = False

    def PressOut(self, keycode: str):
        self.is_pressed[keycode] = False
        self.is_pressing[keycode] = False
        self.is_pressed_out[keycode] = True

    def init(self):
        for i in self.is_pressed.keys():
            if self.is_pressed[i] is True:
                if self.is_pressing[i] is True:
                    self.is_pressed[i] = False
        for i in self.is_pressed_out.keys():
            if self.is_pressed_out[i] is True:
                if (self.is_pressing[i] and self.is_pressed[i]) is False:
                    self.is_pressed_out[i] = False


class Rule:
    def __init__(self, name):
        self.name = name

    def start(self):
        pass

    def update(self):
        pass

    def end(self):
        pass

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, value):
        return Vector2(self.x + value, self.y + value)

    def __sub__(self, value):
        return Vector2(self.x - value, self.y - value)

    def __mul__(self, value):
        return Vector2(self.x * value, self.y * value)

    def __truediv__(self, value):
        return Vector2(self.x / value, self.y / value)

    def __mod__(self, value):
        return Vector2(self.x % value, self.y % value)

    def __radd__(self, value):
        return Vector2(self.x + value, self.y + value)

    def __rsub__(self, value):
        return Vector2(self.x - value, self.y - value)

    def __rmul__(self, value):
        return Vector2(self.x * value, self.y * value)

    def __rtruediv__(self, value):
        return Vector2(self.x / value, self.y / value)

    def __rmod__(self, value):
        return Vector2(self.x % value, self.y % value)


class Transform:
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation

    def move(self, x, y):
        self.position = Vector2(self.position.x + x, self.position.y + y)

    def rotate(self, degree):
        self.rotation += degree
