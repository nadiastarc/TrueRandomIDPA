import random

def guessingGame():
    print("Welcome to Guessing game")
    print("Guess NR 1-100")

    secretNumber = random.randint(1, 100)
    attempts = 0

    while True:
        guess = int(input("Enter your Nr.: "))
        attempts += 1

        if guess == secretNumber:
            print(f"bravo, u had {attempts}")
            break
        elif guess < secretNumber:
            print("too low")
        else:
            print("too high")
if __name__ == "__main__":
    guessingGame()
