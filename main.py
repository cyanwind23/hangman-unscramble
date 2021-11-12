# V 1.1

import pygame
import cfg
from model.components import Button, CircleButton, Image, Label
from random import shuffle, choice

pygame.init()

# global variables
TEXT_FONT = pygame.font.SysFont('comicsans', 24)
BIG_TEXT_FONT = pygame.font.SysFont('comicsans', 54)
window = None
clock = None
curr_screen = 0
screens = []
imgs = []
MAIN_SCREEN = 0
HANGMAN_SCREEN = 1
UNSCRAMBLE_SCREEN = 2
FINAL_SCREEN = 3
word_bank = []

# Hangman screen variable
hangman_status = 0
hangman_ans = ""
hangman_guessed = []

# Scramble screen variables
unscramble_ans = ""
unscramble_hint = ""
unscramble_guessed = []
unscramble_selected_btn = []

# def functions here
def load_words():
    global word_bank
    with open("words.txt") as f:
        for line in f:        
            words = line.split("!")
            for word in words:
                word_bank.append(word.upper())


def init_game():
    global window
    global clock

    window = pygame.display.set_mode((cfg.WIN_WIDTH, cfg.WIN_HEIGHT))
    pygame.display.set_caption("Python Game")
    clock = pygame.time.Clock()

    load_words()

    # init screens
    screens.append(init_main_screen())
    screens.append(init_hangman_screen())
    screens.append(init_unscramble_screen())
    screens.append(init_final_screen("", MAIN_SCREEN))

def init_main_screen():
    # main screen 
    main_screen = []
    btn_gap = 75
    btn_width = 150
    btn_height = 50
    x = cfg.WIN_WIDTH / 2 - btn_width - btn_gap / 2
    y = cfg.WIN_HEIGHT / 2
    main_screen.append(Button(240, y - (btn_height / 2), btn_width, btn_height, cfg.color.BLACK, TEXT_FONT, "Hangman", HANGMAN_SCREEN))
    main_screen.append(Button(570, y - (btn_height / 2), btn_width, btn_height, cfg.color.BLACK, TEXT_FONT, "Unscamble", UNSCRAMBLE_SCREEN))
    main_screen.append(Label(cfg.WIN_WIDTH / 2 - 125, y - 150, cfg.color.BLACK, BIG_TEXT_FONT, "2 in 1 Game"))
    
    return main_screen

def update_hangman_guessed():
    global hangman_ans, hangman_guessed

    display_word = ""
    for letter in hangman_ans:
        if letter in hangman_guessed:
            display_word += letter + " "
        else:
            display_word += "_ "

    return Label(400, 200, cfg.color.BLACK, BIG_TEXT_FONT, display_word)

def update_unscramble_guessed():
    global unscramble_ans, unscramble_guessed

    display_word = ""
    for i in range(len(unscramble_ans)):
        if i < len(unscramble_guessed):
            display_word += unscramble_guessed[i] + " "
        else:
            display_word += "_ "

    txt = BIG_TEXT_FONT.render(display_word, 1, cfg.color.BLACK)
    return Label((cfg.WIN_WIDTH - txt.get_width()) / 2, 100, cfg.color.BLACK, BIG_TEXT_FONT, display_word)

def init_hangman_screen():
    global word_bank, hangman_status, hangman_ans, hangman_guessed
    hangman_status = 0
    hangman_ans = choice(word_bank)
    hangman_guessed = []

    btn_width = 150
    btn_height = 50
    y = 20
    hangman_screen = []
    hangman_screen.append(Label(cfg.WIN_WIDTH / 2 - 125, y, cfg.color.BLACK, TEXT_FONT, "Hangman"))
    hangman_screen.append(Button(10, y / 2, btn_width, btn_height, cfg.color.BLACK, TEXT_FONT, "BACK", MAIN_SCREEN))
    hangman_screen.append(Image(100, 100, pygame.image.load(cfg.IMG_PATH + f"hangman{hangman_status}.png")))
    hangman_screen.append(update_hangman_guessed())
    
    radius = 20
    gap = 15
    startx = round((cfg.WIN_WIDTH - (radius * 2 + gap) * 13) / 2)
    starty = 400
    A = 65
    for i in range(26):
        x = startx + gap * 2 + (radius * 2 + gap) * (i % 13)
        y = starty + ((i // 13) * (gap + radius * 2))
        hangman_screen.append(CircleButton(x, y, radius, cfg.color.BLACK, TEXT_FONT, chr(A + i), HANGMAN_SCREEN)) # no change screen

    return hangman_screen

def init_unscramble_screen():
    global word_bank, hint_bank, unscramble_ans, unscramble_hint, unscramble_guessed

    unscramble_ans = choice(word_bank)
    unscramble_guessed = []

    shuffle_word = list(unscramble_ans)
    shuffle(shuffle_word)

    btn_width = 150
    btn_height = 50
    
    y = 20
    unscramble_screen = []
    unscramble_screen.append(Button(10, y / 2, btn_width, btn_height, cfg.color.BLACK, TEXT_FONT, "Back", MAIN_SCREEN))
    unscramble_screen.append(Label(cfg.WIN_WIDTH / 2 - 60, y, cfg.color.BLACK, TEXT_FONT, "Unscramble"))
    unscramble_screen.append(update_unscramble_guessed())
    unscramble_screen.append(Label(50, 200, cfg.color.BLACK, TEXT_FONT, "Hint: The word begins with " + unscramble_ans[0]))
    unscramble_screen.append(Button(cfg.WIN_WIDTH - btn_width - 20, 300, btn_width, btn_height, cfg.color.BLACK, TEXT_FONT, "DELETE", UNSCRAMBLE_SCREEN))

    # create button
    radius = 20
    gap = 15
    startx = round((cfg.WIN_WIDTH - (radius * 2 + gap) * 13) / 2)
    starty = 400
    for i in range(len(shuffle_word)):
        x = startx + gap * 2 + (radius * 2 + gap) * (i % 13)
        y = starty + ((i // 13) * (gap + radius * 2))
        unscramble_screen.append(CircleButton(x, y, radius, cfg.color.BLACK, TEXT_FONT, shuffle_word[i], UNSCRAMBLE_SCREEN)) # no change screen

    return unscramble_screen

def init_final_screen(msg, from_screen):
    final_screen = []
    btn_gap = 50
    btn_width = 150
    btn_height = 50
    x = cfg.WIN_WIDTH / 2 - btn_width - btn_gap / 2
    y = cfg.WIN_HEIGHT / 2
    # final_screen.append(Label(cfg.WIN_WIDTH / 2, cfg.WIN_HEIGHT / 2, cfg.color.BLACK, TEXT_FONT, "O"))
    final_screen.append(Button(240, y - (btn_height / 2), btn_width, btn_height, cfg.color.BLACK, TEXT_FONT, "Yes", from_screen))
    final_screen.append(Button(570, y - (btn_height / 2), btn_width, btn_height, cfg.color.BLACK, TEXT_FONT, "No", MAIN_SCREEN))
    
    if (from_screen == HANGMAN_SCREEN):
        final_screen.append(Label(cfg.WIN_WIDTH / 2 - 300, cfg.WIN_HEIGHT / 2 - 125, cfg.color.BLACK, TEXT_FONT, msg + " Do you want to play again?"))
    elif (from_screen == UNSCRAMBLE_SCREEN):
        final_screen.append(Label(cfg.WIN_WIDTH / 2 - 300, cfg.WIN_HEIGHT / 2 - 125, cfg.color.BLACK, TEXT_FONT, msg))
        final_screen.append(Label(cfg.WIN_WIDTH / 2 - 150, cfg.WIN_HEIGHT / 2 - 100, cfg.color.BLACK, TEXT_FONT, " Do you want to play again?"))

    return final_screen

def draw():
    window.fill(cfg.color.WHITE)

    for component in screens[curr_screen]:
        component.draw(window)

    pygame.display.update()

def main():
    """Do something more or this function can be deprecated"""
    draw()

def handle_on_click(x, y, screen):
    global curr_screen
    global hangman_status, hangman_ans, hangman_guessed
    global unscramble_ans, unscramble_guessed, unscramble_selected_btn

    if curr_screen == HANGMAN_SCREEN:
        for component in screen:
            if component.onclick(x, y):
                if component.get_intent() == HANGMAN_SCREEN:
                    component.set_visible(False)
                    ltr = component.get_text()
                    hangman_guessed.append(ltr)
                    if ltr not in hangman_ans:
                        hangman_status += 1
                        screens[HANGMAN_SCREEN][2].set_img(pygame.image.load(cfg.IMG_PATH + f"hangman{hangman_status}.png"))
                    else:
                        screens[HANGMAN_SCREEN][3] = update_hangman_guessed()
                
                else:
                    curr_screen = component.get_intent()
    
        won = True
        for letter in hangman_ans:
            if letter not in hangman_guessed:
                won = False
                break
        if won:
            draw()
            curr_screen = FINAL_SCREEN
            screens[FINAL_SCREEN] = init_final_screen("You win. Thanks for playing!", HANGMAN_SCREEN)

        if hangman_status == 6:
            draw()
            curr_screen = FINAL_SCREEN
            screens[FINAL_SCREEN] = init_final_screen("You lose. Thanks for playing!", HANGMAN_SCREEN)
        
        if curr_screen == FINAL_SCREEN:
            pygame.time.delay(500)
    
    elif curr_screen == UNSCRAMBLE_SCREEN:
        
        for component in screen:
            if component.onclick(x, y):
                if component.get_intent() == UNSCRAMBLE_SCREEN:
                    if component.get_text() == "DELETE":
                        if len(unscramble_guessed) > 0:
                            unscramble_guessed.pop()
                            btn = unscramble_selected_btn.pop()
                            btn.set_visible(True)
                    else:
                        component.set_visible(False)
                        unscramble_selected_btn.append(component)
                        ltr = component.get_text()
                        unscramble_guessed.append(ltr)

                    screens[UNSCRAMBLE_SCREEN][2] = update_unscramble_guessed()
                
                else:
                    curr_screen = component.get_intent()

        if len(unscramble_guessed) == len(unscramble_ans):
            msg = ""
            if "".join(unscramble_guessed) == unscramble_ans:
                msg = "You win. Thanks for playing!"
            else:
                msg = "You lose, the word was " + unscramble_ans + ". Thanks for playing!"
            
            draw()
            curr_screen = FINAL_SCREEN
            screens[FINAL_SCREEN] = init_final_screen(msg, UNSCRAMBLE_SCREEN)

        if curr_screen == FINAL_SCREEN:
            pygame.time.delay(1000)

    elif curr_screen == FINAL_SCREEN or curr_screen == MAIN_SCREEN:
        for component in screen:
            if component.onclick(x, y):
                curr_screen = component.get_intent()
                if curr_screen == HANGMAN_SCREEN:
                    screens[HANGMAN_SCREEN] = init_hangman_screen()
                if curr_screen == UNSCRAMBLE_SCREEN:
                    screens[UNSCRAMBLE_SCREEN] = init_unscramble_screen()
    
    else:
        for component in screen:
            if component.onclick(x, y):
                curr_screen = component.get_intent()


# main
init_game()

run = True

while run:
    clock.tick(cfg.FPS)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            handle_on_click(x, y, screens[curr_screen])

    # main game
    main()

pygame.quit()