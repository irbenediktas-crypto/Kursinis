from game import DurakGame
from player import Player, PCPlayer
import random


PC_names = [
    "David",   
    "Alice",   
    "Robert",  
    "Kevin",   
    "Oliver",  
    "Nathan",  
    "Isaac",   
    "Oscar",   
    "Nolan"    
]


# =======================
# game menu
# =======================

if __name__ == "__main__":
    while True:
        print("\n1. Play")
        print("2. Stats")
        print("3. Exit")

        c = input("Choice: ").strip()

        if c == "1":
            while True:
                try:
                    num_ai = int(input("How many PC players (1–5)? ").strip())
                    if 1 <= num_ai <= 5:
                        break
                    else:
                        print("Please choose a number between 1 and 5.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            players = [Player("You")]
            selected_names = random.sample(PC_names, num_ai)
            for name in selected_names:
                players.append(PCPlayer(name))

            game = DurakGame(players)
            game.play()
        elif c == "2":
            DurakGame([]).show_stats()
        elif c == "3":
            print("Goodbye!")
            break
        else:
            print("Neteisingas pasirinkimas, bandykite dar kartą.")