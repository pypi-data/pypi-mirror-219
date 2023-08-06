import pygame

import Project.project as project
import Project.standard as standard
import Project.drawable as drawable
import gamgam.Center

def KEYPRESSEVENT(gameEvent):
    if gameEvent.key == pygame.K_a:
        standard.Input.Press("A")
    elif gameEvent.key == pygame.K_b:
        standard.Input.Press("B")
    elif gameEvent.key == pygame.K_c:
        standard.Input.Press("C")
    elif gameEvent.key == pygame.K_d:
        standard.Input.Press("D")
    elif gameEvent.key == pygame.K_e:
        standard.Input.Press("E")
    elif gameEvent.key == pygame.K_f:
        standard.Input.Press("F")
    elif gameEvent.key == pygame.K_g:
        standard.Input.Press("G")
    elif gameEvent.key == pygame.K_h:
        standard.Input.Press("H")
    elif gameEvent.key == pygame.K_i:
        standard.Input.Press("I")
    elif gameEvent.key == pygame.K_j:
        standard.Input.Press("J")
    elif gameEvent.key == pygame.K_k:
        standard.Input.Press("K")
    elif gameEvent.key == pygame.K_l:
        standard.Input.Press("L")
    elif gameEvent.key == pygame.K_m:
        standard.Input.Press("M")
    elif gameEvent.key == pygame.K_n:
        standard.Input.Press("N")
    elif gameEvent.key == pygame.K_o:
        standard.Input.Press("O")
    elif gameEvent.key == pygame.K_p:
        standard.Input.Press("P")
    elif gameEvent.key == pygame.K_q:
        standard.Input.Press("Q")
    elif gameEvent.key == pygame.K_r:
        standard.Input.Press("R")
    elif gameEvent.key == pygame.K_s:
        standard.Input.Press("S")
    elif gameEvent.key == pygame.K_t:
        standard.Input.Press("T")
    elif gameEvent.key == pygame.K_u:
        standard.Input.Press("U")
    elif gameEvent.key == pygame.K_v:
        standard.Input.Press("V")
    elif gameEvent.key == pygame.K_w:
        standard.Input.Press("W")
    elif gameEvent.key == pygame.K_x:
        standard.Input.Press("X")
    elif gameEvent.key == pygame.K_y:
        standard.Input.Press("Y")
    elif gameEvent.key == pygame.K_z:
        standard.Input.Press("Z")
    elif gameEvent.key == pygame.K_0:
        standard.Input.Press("NUM_0")
    elif gameEvent.key == pygame.K_1:
        standard.Input.Press("NUM_1")
    elif gameEvent.key == pygame.K_2:
        standard.Input.Press("NUM_2")
    elif gameEvent.key == pygame.K_3:
        standard.Input.Press("NUM_3")
    elif gameEvent.key == pygame.K_4:
        standard.Input.Press("NUM_4")
    elif gameEvent.key == pygame.K_5:
        standard.Input.Press("NUM_5")
    elif gameEvent.key == pygame.K_6:
        standard.Input.Press("NUM_6")
    elif gameEvent.key == pygame.K_7:
        standard.Input.Press("NUM_7")
    elif gameEvent.key == pygame.K_8:
        standard.Input.Press("NUM_8")
    elif gameEvent.key == pygame.K_9:
        standard.Input.Press("NUM_9")
    elif gameEvent.key == pygame.K_BACKSPACE:
        standard.Input.Press("BACK")
    elif gameEvent.key == pygame.K_TAB:
        standard.Input.Press("TAB")
    elif gameEvent.key == pygame.K_CLEAR:
        standard.Input.Press("CLEAR")
    elif gameEvent.key == pygame.K_CLEAR:
        standard.Input.Press("CLEAR")
    elif gameEvent.key == pygame.K_RETURN:
        standard.Input.Press("ENTER")
    elif gameEvent.key == pygame.K_PAUSE:
        standard.Input.Press("PAUSE")
    elif gameEvent.key == pygame.K_ESCAPE:
        standard.Input.Press("ESCAPE")
    elif gameEvent.key == pygame.K_SPACE:
        standard.Input.Press("SPACE")
    elif gameEvent.key == pygame.K_EXCLAIM:
        standard.Input.Press("EXCLAIM")
    elif gameEvent.key == pygame.K_QUOTEDBL:
        standard.Input.Press("QUOTEDBL")
    elif gameEvent.key == pygame.K_HASH:
        standard.Input.Press("HASH")
    elif gameEvent.key == pygame.K_DOLLAR:
        standard.Input.Press("DOLLAR")
    elif gameEvent.key == pygame.K_QUOTE:
        standard.Input.Press("QUOTE")
    elif gameEvent.key == pygame.K_LEFTPAREN:
        standard.Input.Press("LEFTPAREN")
    elif gameEvent.key == pygame.K_RIGHTPAREN:
        standard.Input.Press("RIGHTPAREN")
    elif gameEvent.key == pygame.K_ASTERISK:
        standard.Input.Press("ASTERISK")
    elif gameEvent.key == pygame.K_PLUS:
        standard.Input.Press("PLUS")
    elif gameEvent.key == pygame.K_COMMA:
        standard.Input.Press("COMMA")
    elif gameEvent.key == pygame.K_MINUS:
        standard.Input.Press("MINUS")
    elif gameEvent.key == pygame.K_PERIOD:
        standard.Input.Press("PERIOD")
    elif gameEvent.key == pygame.K_SLASH:
        standard.Input.Press("SLASH")
    elif gameEvent.key == pygame.K_COLON:
        standard.Input.Press("COLON")
    elif gameEvent.key == pygame.K_SEMICOLON:
        standard.Input.Press("SEMICOLON")
    elif gameEvent.key == pygame.K_LESS:
        standard.Input.Press("LESS")
    elif gameEvent.key == pygame.K_EQUALS:
        standard.Input.Press("EQUALS")
    elif gameEvent.key == pygame.K_GREATER:
        standard.Input.Press("GREATER")
    elif gameEvent.key == pygame.K_QUESTION:
        standard.Input.Press("QUESTION")
    elif gameEvent.key == pygame.K_AT:
        standard.Input.Press("AT")
    elif gameEvent.key == pygame.K_LEFTBRACKET:
        standard.Input.Press("LEFTBRACKET")
    elif gameEvent.key == pygame.K_RIGHTBRACKET:
        standard.Input.Press("RIGHTBRACKET")
    elif gameEvent.key == pygame.K_BACKSLASH:
        standard.Input.Press("BACKSLASH")
    elif gameEvent.key == pygame.K_CARET:
        standard.Input.Press("CARET")
    elif gameEvent.key == pygame.K_UNDERSCORE:
        standard.Input.Press("UNDERSCORE")
    elif gameEvent.key == pygame.K_BACKQUOTE:
        standard.Input.Press("BACKQUOTE")
    elif gameEvent.key == pygame.K_DELETE:
        standard.Input.Press("DELETE")
    elif gameEvent.key == pygame.K_KP0:
        standard.Input.Press("KEY_0")
    elif gameEvent.key == pygame.K_KP1:
        standard.Input.Press("KEY_1")
    elif gameEvent.key == pygame.K_KP2:
        standard.Input.Press("KEY_2")
    elif gameEvent.key == pygame.K_KP3:
        standard.Input.Press("KEY_3")
    elif gameEvent.key == pygame.K_KP4:
        standard.Input.Press("KEY_4")
    elif gameEvent.key == pygame.K_KP5:
        standard.Input.Press("KEY_5")
    elif gameEvent.key == pygame.K_KP6:
        standard.Input.Press("KEY_6")
    elif gameEvent.key == pygame.K_KP7:
        standard.Input.Press("KEY_7")
    elif gameEvent.key == pygame.K_KP8:
        standard.Input.Press("KEY_8")
    elif gameEvent.key == pygame.K_KP9:
        standard.Input.Press("KEY_9")
    elif gameEvent.key == pygame.K_KP_PERIOD:
        standard.Input.Press("KEY_PERIOD")
    elif gameEvent.key == pygame.K_KP_DIVIDE:
        standard.Input.Press("KEY_DIVIDE")
    elif gameEvent.key == pygame.K_KP_MINUS:
        standard.Input.Press("KEY_MINUS")
    elif gameEvent.key == pygame.K_KP_PLUS:
        standard.Input.Press("KEY_PLUS")
    elif gameEvent.key == pygame.K_KP_ENTER:
        standard.Input.Press("KEY_ENTER")
    elif gameEvent.key == pygame.K_KP_EQUALS:
        standard.Input.Press("KEY_EQUALS")
    elif gameEvent.key == pygame.K_UP:
        standard.Input.Press("UP")
    elif gameEvent.key == pygame.K_DOWN:
        standard.Input.Press("DOWN")
    elif gameEvent.key == pygame.K_LEFT:
        standard.Input.Press("LEFT")
    elif gameEvent.key == pygame.K_RIGHT:
        standard.Input.Press("RIGHT")
    elif gameEvent.key == pygame.K_INSERT:
        standard.Input.Press("INSERT")
    elif gameEvent.key == pygame.K_HOME:
        standard.Input.Press("HOME")
    elif gameEvent.key == pygame.K_PAGEUP:
        standard.Input.Press("PAGEUP")
    elif gameEvent.key == pygame.K_PAGEDOWN:
        standard.Input.Press("PAGEDOWN")
    elif gameEvent.key == pygame.K_F1:
        standard.Input.Press("F1")
    elif gameEvent.key == pygame.K_F2:
        standard.Input.Press("F2")
    elif gameEvent.key == pygame.K_F3:
        standard.Input.Press("F3")
    elif gameEvent.key == pygame.K_F4:
        standard.Input.Press("F4")
    elif gameEvent.key == pygame.K_F5:
        standard.Input.Press("F5")
    elif gameEvent.key == pygame.K_F6:
        standard.Input.Press("F6")
    elif gameEvent.key == pygame.K_F7:
        standard.Input.Press("F7")
    elif gameEvent.key == pygame.K_F8:
        standard.Input.Press("F8")
    elif gameEvent.key == pygame.K_F9:
        standard.Input.Press("F9")
    elif gameEvent.key == pygame.K_F10:
        standard.Input.Press("F10")
    elif gameEvent.key == pygame.K_F11:
        standard.Input.Press("F11")
    elif gameEvent.key == pygame.K_F12:
        standard.Input.Press("F12")
    elif gameEvent.key == pygame.K_F13:
        standard.Input.Press("F13")
    elif gameEvent.key == pygame.K_F14:
        standard.Input.Press("F14")
    elif gameEvent.key == pygame.K_F15:
        standard.Input.Press("F15")
    elif gameEvent.key == pygame.K_NUMLOCK:
        standard.Input.Press("NUMLOCK")
    elif gameEvent.key == pygame.K_CAPSLOCK:
        standard.Input.Press("CAPSLOCK")
    elif gameEvent.key == pygame.K_SCROLLOCK:
        standard.Input.Press("SCROLLOCK")
    elif gameEvent.key == pygame.K_RSHIFT:
        standard.Input.Press("RSHIFT")
    elif gameEvent.key == pygame.K_LSHIFT:
        standard.Input.Press("LSHIFT")
    elif gameEvent.key == pygame.K_RCTRL:
        standard.Input.Press("RCTRL")
    elif gameEvent.key == pygame.K_LCTRL:
        standard.Input.Press("LCTRL")
    elif gameEvent.key == pygame.K_RALT:
        standard.Input.Press("RALT")
    elif gameEvent.key == pygame.K_LALT:
        standard.Input.Press("LALT")
    elif gameEvent.key == pygame.K_RMETA:
        standard.Input.Press("RMETA")
    elif gameEvent.key == pygame.K_LMETA:
        standard.Input.Press("LMETA")
    elif gameEvent.key == pygame.K_LSUPER:
        standard.Input.Press("LSUPER")
    elif gameEvent.key == pygame.K_RSUPER:
        standard.Input.Press("RSUPER")
    elif gameEvent.key == pygame.K_MODE:
        standard.Input.Press("MODE")
    elif gameEvent.key == pygame.K_HELP:
        standard.Input.Press("HELP")
    elif gameEvent.key == pygame.K_PRINT:
        standard.Input.Press("PRINT")
    elif gameEvent.key == pygame.K_SYSREQ:
        standard.Input.Press("SYSREQ")
    elif gameEvent.key == pygame.K_BREAK:
        standard.Input.Press("BREAK")
    elif gameEvent.key == pygame.K_MENU:
        standard.Input.Press("MENU")
    elif gameEvent.key == pygame.K_POWER:
        standard.Input.Press("POWER")
    elif gameEvent.key == pygame.K_EURO:
        standard.Input.Press("EURO")


def KEYPRESSOUTEVENT(gameEvent):
    if gameEvent.key == pygame.K_a:
        standard.Input.PressOut("A")
    elif gameEvent.key == pygame.K_b:
        standard.Input.PressOut("B")
    elif gameEvent.key == pygame.K_c:
        standard.Input.PressOut("C")
    elif gameEvent.key == pygame.K_d:
        standard.Input.PressOut("D")
    elif gameEvent.key == pygame.K_e:
        standard.Input.PressOut("E")
    elif gameEvent.key == pygame.K_f:
        standard.Input.PressOut("F")
    elif gameEvent.key == pygame.K_g:
        standard.Input.PressOut("G")
    elif gameEvent.key == pygame.K_h:
        standard.Input.PressOut("H")
    elif gameEvent.key == pygame.K_i:
        standard.Input.PressOut("I")
    elif gameEvent.key == pygame.K_j:
        standard.Input.PressOut("J")
    elif gameEvent.key == pygame.K_k:
        standard.Input.PressOut("K")
    elif gameEvent.key == pygame.K_l:
        standard.Input.PressOut("L")
    elif gameEvent.key == pygame.K_m:
        standard.Input.PressOut("M")
    elif gameEvent.key == pygame.K_n:
        standard.Input.PressOut("N")
    elif gameEvent.key == pygame.K_o:
        standard.Input.PressOut("O")
    elif gameEvent.key == pygame.K_p:
        standard.Input.PressOut("P")
    elif gameEvent.key == pygame.K_q:
        standard.Input.PressOut("Q")
    elif gameEvent.key == pygame.K_r:
        standard.Input.PressOut("R")
    elif gameEvent.key == pygame.K_s:
        standard.Input.PressOut("S")
    elif gameEvent.key == pygame.K_t:
        standard.Input.PressOut("T")
    elif gameEvent.key == pygame.K_u:
        standard.Input.PressOut("U")
    elif gameEvent.key == pygame.K_v:
        standard.Input.PressOut("V")
    elif gameEvent.key == pygame.K_w:
        standard.Input.PressOut("W")
    elif gameEvent.key == pygame.K_x:
        standard.Input.PressOut("X")
    elif gameEvent.key == pygame.K_y:
        standard.Input.PressOut("Y")
    elif gameEvent.key == pygame.K_z:
        standard.Input.PressOut("Z")
    elif gameEvent.key == pygame.K_0:
        standard.Input.PressOut("NUM_0")
    elif gameEvent.key == pygame.K_1:
        standard.Input.PressOut("NUM_1")
    elif gameEvent.key == pygame.K_2:
        standard.Input.PressOut("NUM_2")
    elif gameEvent.key == pygame.K_3:
        standard.Input.PressOut("NUM_3")
    elif gameEvent.key == pygame.K_4:
        standard.Input.PressOut("NUM_4")
    elif gameEvent.key == pygame.K_5:
        standard.Input.PressOut("NUM_5")
    elif gameEvent.key == pygame.K_6:
        standard.Input.PressOut("NUM_6")
    elif gameEvent.key == pygame.K_7:
        standard.Input.PressOut("NUM_7")
    elif gameEvent.key == pygame.K_8:
        standard.Input.PressOut("NUM_8")
    elif gameEvent.key == pygame.K_9:
        standard.Input.PressOut("NUM_9")
    elif gameEvent.key == pygame.K_BACKSPACE:
        standard.Input.PressOut("BACK")
    elif gameEvent.key == pygame.K_TAB:
        standard.Input.PressOut("TAB")
    elif gameEvent.key == pygame.K_CLEAR:
        standard.Input.PressOut("CLEAR")
    elif gameEvent.key == pygame.K_CLEAR:
        standard.Input.PressOut("CLEAR")
    elif gameEvent.key == pygame.K_RETURN:
        standard.Input.PressOut("ENTER")
    elif gameEvent.key == pygame.K_PAUSE:
        standard.Input.PressOut("PAUSE")
    elif gameEvent.key == pygame.K_ESCAPE:
        standard.Input.PressOut("ESCAPE")
    elif gameEvent.key == pygame.K_SPACE:
        standard.Input.PressOut("SPACE")
    elif gameEvent.key == pygame.K_EXCLAIM:
        standard.Input.PressOut("EXCLAIM")
    elif gameEvent.key == pygame.K_QUOTEDBL:
        standard.Input.PressOut("QUOTEDBL")
    elif gameEvent.key == pygame.K_HASH:
        standard.Input.PressOut("HASH")
    elif gameEvent.key == pygame.K_DOLLAR:
        standard.Input.PressOut("DOLLAR")
    elif gameEvent.key == pygame.K_QUOTE:
        standard.Input.PressOut("QUOTE")
    elif gameEvent.key == pygame.K_LEFTPAREN:
        standard.Input.PressOut("LEFTPAREN")
    elif gameEvent.key == pygame.K_RIGHTPAREN:
        standard.Input.PressOut("RIGHTPAREN")
    elif gameEvent.key == pygame.K_ASTERISK:
        standard.Input.PressOut("ASTERISK")
    elif gameEvent.key == pygame.K_PLUS:
        standard.Input.PressOut("PLUS")
    elif gameEvent.key == pygame.K_COMMA:
        standard.Input.PressOut("COMMA")
    elif gameEvent.key == pygame.K_MINUS:
        standard.Input.PressOut("MINUS")
    elif gameEvent.key == pygame.K_PERIOD:
        standard.Input.PressOut("PERIOD")
    elif gameEvent.key == pygame.K_SLASH:
        standard.Input.PressOut("SLASH")
    elif gameEvent.key == pygame.K_COLON:
        standard.Input.PressOut("COLON")
    elif gameEvent.key == pygame.K_SEMICOLON:
        standard.Input.PressOut("SEMICOLON")
    elif gameEvent.key == pygame.K_LESS:
        standard.Input.PressOut("LESS")
    elif gameEvent.key == pygame.K_EQUALS:
        standard.Input.PressOut("EQUALS")
    elif gameEvent.key == pygame.K_GREATER:
        standard.Input.PressOut("GREATER")
    elif gameEvent.key == pygame.K_QUESTION:
        standard.Input.PressOut("QUESTION")
    elif gameEvent.key == pygame.K_AT:
        standard.Input.PressOut("AT")
    elif gameEvent.key == pygame.K_LEFTBRACKET:
        standard.Input.PressOut("LEFTBRACKET")
    elif gameEvent.key == pygame.K_RIGHTBRACKET:
        standard.Input.PressOut("RIGHTBRACKET")
    elif gameEvent.key == pygame.K_BACKSLASH:
        standard.Input.PressOut("BACKSLASH")
    elif gameEvent.key == pygame.K_CARET:
        standard.Input.PressOut("CARET")
    elif gameEvent.key == pygame.K_UNDERSCORE:
        standard.Input.PressOut("UNDERSCORE")
    elif gameEvent.key == pygame.K_BACKQUOTE:
        standard.Input.PressOut("BACKQUOTE")
    elif gameEvent.key == pygame.K_DELETE:
        standard.Input.PressOut("DELETE")
    elif gameEvent.key == pygame.K_KP0:
        standard.Input.PressOut("KEY_0")
    elif gameEvent.key == pygame.K_KP1:
        standard.Input.PressOut("KEY_1")
    elif gameEvent.key == pygame.K_KP2:
        standard.Input.PressOut("KEY_2")
    elif gameEvent.key == pygame.K_KP3:
        standard.Input.PressOut("KEY_3")
    elif gameEvent.key == pygame.K_KP4:
        standard.Input.PressOut("KEY_4")
    elif gameEvent.key == pygame.K_KP5:
        standard.Input.PressOut("KEY_5")
    elif gameEvent.key == pygame.K_KP6:
        standard.Input.PressOut("KEY_6")
    elif gameEvent.key == pygame.K_KP7:
        standard.Input.PressOut("KEY_7")
    elif gameEvent.key == pygame.K_KP8:
        standard.Input.PressOut("KEY_8")
    elif gameEvent.key == pygame.K_KP9:
        standard.Input.PressOut("KEY_9")
    elif gameEvent.key == pygame.K_KP_PERIOD:
        standard.Input.PressOut("KEY_PERIOD")
    elif gameEvent.key == pygame.K_KP_DIVIDE:
        standard.Input.PressOut("KEY_DIVIDE")
    elif gameEvent.key == pygame.K_KP_MINUS:
        standard.Input.PressOut("KEY_MINUS")
    elif gameEvent.key == pygame.K_KP_PLUS:
        standard.Input.PressOut("KEY_PLUS")
    elif gameEvent.key == pygame.K_KP_ENTER:
        standard.Input.PressOut("KEY_ENTER")
    elif gameEvent.key == pygame.K_KP_EQUALS:
        standard.Input.PressOut("KEY_EQUALS")
    elif gameEvent.key == pygame.K_UP:
        standard.Input.PressOut("UP")
    elif gameEvent.key == pygame.K_DOWN:
        standard.Input.PressOut("DOWN")
    elif gameEvent.key == pygame.K_LEFT:
        standard.Input.PressOut("LEFT")
    elif gameEvent.key == pygame.K_RIGHT:
        standard.Input.PressOut("RIGHT")
    elif gameEvent.key == pygame.K_INSERT:
        standard.Input.PressOut("INSERT")
    elif gameEvent.key == pygame.K_HOME:
        standard.Input.PressOut("HOME")
    elif gameEvent.key == pygame.K_PAGEUP:
        standard.Input.PressOut("PAGEUP")
    elif gameEvent.key == pygame.K_PAGEDOWN:
        standard.Input.PressOut("PAGEDOWN")
    elif gameEvent.key == pygame.K_F1:
        standard.Input.PressOut("F1")
    elif gameEvent.key == pygame.K_F2:
        standard.Input.PressOut("F2")
    elif gameEvent.key == pygame.K_F3:
        standard.Input.PressOut("F3")
    elif gameEvent.key == pygame.K_F4:
        standard.Input.PressOut("F4")
    elif gameEvent.key == pygame.K_F5:
        standard.Input.PressOut("F5")
    elif gameEvent.key == pygame.K_F6:
        standard.Input.PressOut("F6")
    elif gameEvent.key == pygame.K_F7:
        standard.Input.PressOut("F7")
    elif gameEvent.key == pygame.K_F8:
        standard.Input.PressOut("F8")
    elif gameEvent.key == pygame.K_F9:
        standard.Input.PressOut("F9")
    elif gameEvent.key == pygame.K_F10:
        standard.Input.PressOut("F10")
    elif gameEvent.key == pygame.K_F11:
        standard.Input.PressOut("F11")
    elif gameEvent.key == pygame.K_F12:
        standard.Input.PressOut("F12")
    elif gameEvent.key == pygame.K_F13:
        standard.Input.PressOut("F13")
    elif gameEvent.key == pygame.K_F14:
        standard.Input.PressOut("F14")
    elif gameEvent.key == pygame.K_F15:
        standard.Input.PressOut("F15")
    elif gameEvent.key == pygame.K_NUMLOCK:
        standard.Input.PressOut("NUMLOCK")
    elif gameEvent.key == pygame.K_CAPSLOCK:
        standard.Input.PressOut("CAPSLOCK")
    elif gameEvent.key == pygame.K_SCROLLOCK:
        standard.Input.PressOut("SCROLLOCK")
    elif gameEvent.key == pygame.K_RSHIFT:
        standard.Input.PressOut("RSHIFT")
    elif gameEvent.key == pygame.K_LSHIFT:
        standard.Input.PressOut("LSHIFT")
    elif gameEvent.key == pygame.K_RCTRL:
        standard.Input.PressOut("RCTRL")
    elif gameEvent.key == pygame.K_LCTRL:
        standard.Input.PressOut("LCTRL")
    elif gameEvent.key == pygame.K_RALT:
        standard.Input.PressOut("RALT")
    elif gameEvent.key == pygame.K_LALT:
        standard.Input.PressOut("LALT")
    elif gameEvent.key == pygame.K_RMETA:
        standard.Input.PressOut("RMETA")
    elif gameEvent.key == pygame.K_LMETA:
        standard.Input.PressOut("LMETA")
    elif gameEvent.key == pygame.K_LSUPER:
        standard.Input.PressOut("LSUPER")
    elif gameEvent.key == pygame.K_RSUPER:
        standard.Input.PressOut("RSUPER")
    elif gameEvent.key == pygame.K_MODE:
        standard.Input.PressOut("MODE")
    elif gameEvent.key == pygame.K_HELP:
        standard.Input.PressOut("HELP")
    elif gameEvent.key == pygame.K_PRINT:
        standard.Input.PressOut("PRINT")
    elif gameEvent.key == pygame.K_SYSREQ:
        standard.Input.PressOut("SYSREQ")
    elif gameEvent.key == pygame.K_BREAK:
        standard.Input.PressOut("BREAK")
    elif gameEvent.key == pygame.K_MENU:
        standard.Input.PressOut("MENU")
    elif gameEvent.key == pygame.K_POWER:
        standard.Input.PressOut("POWER")
    elif gameEvent.key == pygame.K_EURO:
        standard.Input.PressOut("EURO")

pygame.init()

Scenes = []

for i in Scenes:
    standard.Game.add_scene(i)

while True:
    if standard.Game.state == "END":
        break
    pygame.time.Clock().tick(standard.Frame.fps_limit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            standard.Game.run("END")
        if event.type == pygame.KEYDOWN:
            KEYPRESSEVENT(event)
        if event.type == pygame.KEYUP:
            KEYPRESSOUTEVENT(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                standard.Input.Press("MOUSE_LEFT")
            if event.button == 2:
                standard.Input.Press("MOUSE_WHEEL")
            if event.button == 3:
                standard.Input.Press("MOUSE_RIGHT")
            if event.button == 4:
                standard.Input.Press("MOUSE_UP")
            if event.button == 5:
                standard.Input.Press("MOUSE_DOWN")
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                standard.Input.PressOut("MOUSE_LEFT")
            if event.button == 2:
                standard.Input.PressOut("MOUSE_WHEEL")
            if event.button == 3:
                standard.Input.PressOut("MOUSE_RIGHT")
            if event.button == 4:
                standard.Input.PressOut("MOUSE_UP")
            if event.button == 5:
                standard.Input.PressOut("MOUSE_DOWN")
    standard.Input.mouse_pos = project.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    if type(standard.Game.scenes[standard.Game.now].back) == drawable.Color:
        standard.Game.screen.fill(standard.Game.scenes[standard.Game.now].back.color)
    else:
        standard.Game.screen.blit(standard.Game.scenes[standard.Game.now].back.image, (0, 0))
    standard.Game.update()
    standard.Input.init()
    standard.Time.update()
    standard.Frame.fps_pls()
    standard.Frame.fps_check()
    pygame.display.flip()
