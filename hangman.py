import random
def show_rules():
    print("GAME RULES")
    print("1.computer selects a random word.")
    print("2.you have limited attempts to guess the letters")
    print("3.each word guess reduces your chances")
    print("4.Guess all letters correctly to win!\n")

def play_game():
    words=["python","hangman","program","developer","science","college","project"]
    word=random.choice(words)
    guessed=['_']*len(word)
    attempts=6
    guessed_letters=[]
    print("Lets play hangman game!")
    print("word:","".join(guessed))
    while attempts>0 and '_'in guessed:
        guess=input("\n enter a letter:").lower()
        if not guess.isalpha() or len(guess)!=1:
            print("enter single alphabet only:")
            continue

        if guess in guessed_letters:
            print("you already guessed that letter!")
            continue

        guessed_letters.append(guess)
        if guess in word:
            print ("correct guess!")
            for i in range(len(word)):
                if word[i]==guess:
                    guessed[i]=guess
        else:
            attempts-=1
            print(f"wrong guess:{attempts}")
            print("word:","".join(guessed))
        if'_' not in guessed:
            print("congratulations! you won the game.You guessed the word.The word is",word)
        
    print("game over.The word was:",word)

def exit_game():
    print("Thanks for playing hangman game!")

def main():
    while True:
        print("\\n ------HANGMAN GAME-------")
        print("1.play game")
        print("2.show rules")
        print("3.exit")
        choice =input("Enter your choice:")
        match choice:
            case '1':
                play_game()
            case '2':
                show_rules()
            case '3':
                exit_game()
                break
            case _:
                print("Invalid choice")
if __name__=="__main__":
    main()