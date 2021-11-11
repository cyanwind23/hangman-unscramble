import pygame
import cfg
from model.components import Button, CircleButton, Image, Label
import random

pygame.init()

# global variables
TEXT_FONT = pygame.font.SysFont('comicsans', 20)
BIG_TEXT_FONT = pygame.font.SysFont('comicsans', 40)
window = None
clock = None
curr_screen = 0
screens = []
imgs = []
MAIN_SCREEN = 0
HANGMAN_SCREEN = 1
SCRAMBLE_SCREEN = 2
FINAL_SCREEN = 3
word_bank = []
hint_bank = {}

# Hangman screen variable
hangman_status = 0
hangman_ans = ""
hangman_guessed = []

# Scramble screen variables
scramble_ans = ""
scramble_hint = ""
scramble_guessed = []
scramble_selected_btn = []

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
    pygame.display.set_caption("Python Game!")
    clock = pygame.time.Clock()

    load_words()

    # init screens
    screens.append(init_main_screen())
    screens.append(init_hangman_screen())
    screens.append(init_scramble_screen())
    screens.append(init_final_screen("", MAIN_SCREEN))

def init_main_screen():
    # main screen 
    main_screen = []
    btn_gap = 50
    btn_width = 150
    btn_height = 50
    x = cfg.WIN_WIDTH / 2 - btn_width - btn_gap / 2
    y = cfg.WIN_HEIGHT / 2
    main_screen.append(Button(x, y, btn_width, btn_height, cfg.color.BLACK, TEXT_FONT, "HANGMAN", HANGMAN_SCREEN))
    main_screen.append(Button(x + btn_width + btn_gap, y, btn_width, btn_height, cfg.color.BLACK, TEXT_FONT, "SCRAMBLE", SCRAMBLE_SCREEN))
    main_screen.append(Label(cfg.WIN_WIDTH / 2 - 125, cfg.WIN_HEIGHT / 2 - 75, cfg.color.BLACK, TEXT_FONT, "WELCOME TO PYGAME"))
    
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

def update_scramble_guessed():
    global scramble_ans, scramble_guessed

    display_word = ""
    for i in range(len(scramble_ans)):
        if i < len(scramble_guessed):
            display_word += scramble_guessed[i] + " "
        else:
            display_word += "_ "

    txt = BIG_TEXT_FONT.render(display_word, 1, cfg.color.BLACK)
    return Label((cfg.WIN_WIDTH - txt.get_width()) / 2, 100, cfg.color.BLACK, BIG_TEXT_FONT, display_word)

def init_hangman_screen():
    global word_bank, hangman_status, hangman_ans, hangman_guessed
    hangman_status = 0
    hangman_ans = random.choice(word_bank)
    hangman_guessed = []

    btn_width = 150
    btn_height = 50
    y = 20
    hangman_screen = []
    hangman_screen.append(Label(cfg.WIN_WIDTH / 2 - 125, y, cfg.color.BLACK, TEXT_FONT, "WELCOME TO HANGMAN"))
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

def init_scramble_screen():
    global word_bank, hint_bank, scramble_ans, scramble_hint, scramble_guessed

    scramble_ans = random.choice(word_bank)
    scramble_hint = hint_bank[scramble_ans]
    scramble_guessed = []

    btn_width = 150
    btn_height = 50
    
    y = 20
    scramble_screen = []
    scramble_screen.append(Button(10, y / 2, btn_width, btn_height, cfg.color.BLACK, TEXT_FONT, "BACK", MAIN_SCREEN))
    scramble_screen.append(Label(cfg.WIN_WIDTH / 2 - 125, y, cfg.color.BLACK, TEXT_FONT, "WELCOME TO SCRAMBLE"))
    scramble_screen.append(update_scramble_guessed())
    scramble_screen.append(Label(50, 200, cfg.color.BLACK, TEXT_FONT, "HINT: " + scramble_hint))
    scramble_screen.append(Button(cfg.WIN_WIDTH - btn_width - 20, 300, btn_width, btn_height, cfg.color.BLACK, TEXT_FONT, "DELETE", SCRAMBLE_SCREEN))

    # create button
    shuffle_word = list(scramble_ans)
    random.shuffle(shuffle_word)
    radius = 20
    gap = 15
    startx = round((cfg.WIN_WIDTH - (radius * 2 + gap) * 13) / 2)
    starty = 400
    for i in range(len(shuffle_word)):
        x = startx + gap * 2 + (radius * 2 + gap) * (i % 13)
        y = starty + ((i // 13) * (gap + radius * 2))
        scramble_screen.append(CircleButton(x, y, radius, cfg.color.BLACK, TEXT_FONT, shuffle_word[i], SCRAMBLE_SCREEN)) # no change screen

    return scramble_screen

def init_final_screen(msg, from_screen):
    final_screen = []
    btn_gap = 50
    btn_width = 150
    btn_height = 50
    x = cfg.WIN_WIDTH / 2 - btn_width - btn_gap / 2
    y = cfg.WIN_HEIGHT / 2
    final_screen.append(Button(x, y, btn_width, btn_height, cfg.color.BLACK, TEXT_FONT, "YES", from_screen))
    final_screen.append(Button(x + btn_width + btn_gap, y, btn_width, btn_height, cfg.color.BLACK, TEXT_FONT, "NO", MAIN_SCREEN))
    final_screen.append(Label(cfg.WIN_WIDTH / 2 - 100, cfg.WIN_HEIGHT / 2 - 75, cfg.color.BLACK, TEXT_FONT, msg + " AGAIN?"))

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
    global scramble_ans, scramble_guessed, scramble_selected_btn

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
            screens[FINAL_SCREEN] = init_final_screen("YOU WON!", HANGMAN_SCREEN)

        if hangman_status == 6:
            draw()
            curr_screen = FINAL_SCREEN
            screens[FINAL_SCREEN] = init_final_screen("YOU LOST!", HANGMAN_SCREEN)
        
        if curr_screen == FINAL_SCREEN:
            pygame.time.delay(1000)
    
    elif curr_screen == SCRAMBLE_SCREEN:
        for component in screen:
            if component.onclick(x, y):
                if component.get_intent() == SCRAMBLE_SCREEN:
                    if component.get_text() == "DELETE":
                        if len(scramble_guessed) > 0:
                            scramble_guessed.pop()
                            btn = scramble_selected_btn.pop()
                            btn.set_visible(True)
                    else:
                        component.set_visible(False)
                        scramble_selected_btn.append(component)
                        ltr = component.get_text()
                        scramble_guessed.append(ltr)

                    screens[SCRAMBLE_SCREEN][2] = update_scramble_guessed()
                
                else:
                    curr_screen = component.get_intent()

        if len(scramble_guessed) == len(scramble_ans):
            msg = ""
            if "".join(scramble_guessed) == scramble_ans:
                msg = "YOU WON!"
            else:
                msg = "YOU LOST!"
            
            draw()
            curr_screen = FINAL_SCREEN
            screens[FINAL_SCREEN] = init_final_screen(msg, SCRAMBLE_SCREEN)

        if curr_screen == FINAL_SCREEN:
            pygame.time.delay(1000)

    elif curr_screen == FINAL_SCREEN or curr_screen == MAIN_SCREEN:
        for component in screen:
            if component.onclick(x, y):
                curr_screen = component.get_intent()
                if curr_screen == HANGMAN_SCREEN:
                    screens[HANGMAN_SCREEN] = init_hangman_screen()
                if curr_screen == SCRAMBLE_SCREEN:
                    screens[SCRAMBLE_SCREEN] = init_scramble_screen()
    
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