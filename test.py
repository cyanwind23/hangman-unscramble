from random import shuffle, choice

#Reads the words.txt file into a dictionary with keys and definitions
with open("words.txt") as f:
    word_dict = {}
    for line in f:
        # split into two parts, word and description
        word, hint = line.split(":")
        word_dict[word] = hint


def intro():
    print('Welcome to the scramble game\n')
    print('I will show you a scrambled word, and you will have to guess the word\n')


#Picks a random key from the dictionary b
def pick_word():
    word = choice(list(word_dict.keys()))
    return word


#Gives a hint to the user
def give_hint(word):
    # return the definition of the word
    descrip = word_dict[word]
    return descrip


#Below - Retrieves answer from user, rejects it if the answer is not alpha
def get_answer():
    while True:
        answer = input('Please enter a guess: ')
        if answer.isalpha():
            return answer
        else:
            print("Only letters in the word")


def main():
    intro()
    word = pick_word()
    # give user lives/tries
    tries = 3
    shffled_word = list(word)
    # shuffle the word 
    shuffle(shffled_word)
    # rejoin shuffled word
    shffled_word = "".join(shffled_word)
    # keep going for three tries as most
    while tries > 0:
        inp = input("Your scrambled word is {}\nEnter h if you want to see your hint or any key to continue".format(shffled_word))
        if inp == "h":
            print("The word definition is {}".format(give_hint(word)))
        ans = get_answer()
        if ans == word:
            print("Congratulations you win!")
            break
        tries -= 1
    # ask user if they want to play again, restarting main if they do
    play_again = input("Press 'y'  to play again or any key to exit")
    if play_again == "y":
        main()
    # else the user did not press y so say goodbye
    print("Goodbye")
main()