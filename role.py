from abc import ABC, abstractmethod
from player import PCPlayer


# =======================
# roles
# =======================

class Role(ABC):
    @abstractmethod
    def play(self, game):
        pass


class Attacker(Role):
    def play(self, game):
        p = game.current_player

        if isinstance(p, PCPlayer):
            card = p.choose_attack(game)
            if not card:
                print(f"{p} passes")
                return False
            print(f"{p} attacks with {card}")
            game.table.append((card, None))
            p.remove_card(card)
            return True

        print("\n >>>YOUR TURN<<<")
        print("Table:", game.show_table())
        print("Your hand:")
        hand = p.get_hand()
        for i, c in enumerate(hand):
            print(f"{i}:{c}", end="  ")
        print()

        while True:
            choice = input("Please choose indexes on screen or 'pass': ").strip().lower()
            if choice == "pass":
                return False

            try:
                indexes = list(map(int, choice.split()))

                if any(i < 0 or i >= len(hand) for i in indexes):
                    print("This card doesn't exist in your hand!")
                    continue

                cards = [hand[i] for i in indexes]

                if len(set(c.rank for c in cards)) != 1:
                    print("You can only deal cards of the same rank!")
                    continue

                if game.table and cards[0].rank not in game.table_ranks():
                    print("This card doesn't exist on the table!")
                    continue

                for c in cards:
                    game.table.append((c, None))
                    p.remove_card(c)
                return True

            except ValueError:
                print(
                    "Error: Please input a number (f.e., 0 1) or input 'pass'."
                )


class Defender(Role):
    def play(self, game):
        p = game.current_player

        for i in range(len(game.table)):
            if game.table[i][1] is not None:
                continue

            attack = game.table[i][0]

            if isinstance(p, PCPlayer):
                card = p.choose_defense(attack, game)

                if card:
                    print(f"{p} defends {attack} with {card}")
                    game.table[i] = (attack, card)
                    p.remove_card(card)
                else:
                    print(f"{p} Cannot defend and takes cards!")
                    game.take_cards(p)
                    return False
                continue

            while True:
                print(f"\n🛡 Defend {attack}")
                print("Table:", game.show_table())
                hand = p.get_hand()
                for j, c in enumerate(hand):
                    print(f"{j}:{c}", end="  ")
                print()

                choice = input("Index or 'take': ").strip().lower()
                if choice == "take":
                    game.take_cards(p)
                    return False

                try:
                    idx = int(choice)
                    if idx < 0 or idx >= len(hand):
                        print("Error: This index doesn't exist!")
                        continue

                    card = hand[idx]
                    if game.valid_defense(card, attack):
                        game.table[i] = (attack, card)
                        p.remove_card(card)
                        break
                    else:
                        print("Error: This card is to weak!")
                except ValueError:
                    print("Error: Input a number or 'take'.")
        return True