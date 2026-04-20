import random
import json
import time
from abc import ABC, abstractmethod
import sys
# =======================
# spalvos
# =======================

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:

    class Dummy:
        RED = WHITE = RESET_ALL = ""
    Fore = Style = Dummy()

# =======================
# kortos
# =======================

class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    SYMBOLS = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
    COLORS = {

        'Hearts': Fore.RED,
        'Diamonds': Fore.RED,
        'Clubs': Fore.WHITE,
        'Spades': Fore.WHITE
    }
    RANKS = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank


    def value(self):
        return Card.RANKS.index(self.rank)


    def __str__(self):
        return f"{Card.COLORS[self.suit]}{self.rank}{Card.SYMBOLS[self.suit]}{Style.RESET_ALL}"


class CardFactory:
    @staticmethod
    def create_deck():
        return [Card(s, r) for s in Card.SUITS for r in Card.RANKS]

# =======================
# kalade
# =======================

class Deck:
    def __init__(self):
        self.cards = CardFactory.create_deck()
        random.shuffle(self.cards)

        self.trump_card = self.cards.pop()
        self.trump_suit = self.trump_card.suit

    def draw(self):
        return self.cards.pop() if self.cards else None

# =======================

# zaidejo logika

# =======================

class Player:
    def __init__(self, name):
        self._name = name
        self._hand = []


    def add_card(self, card):
        if card:
            self._hand.append(card)
            self._hand.sort(key=lambda c: (c.value(), c.suit))


    def remove_card(self, card):
        self._hand.remove(card)


    def get_hand(self):
        return self._hand


    def has_cards(self):
        return len(self._hand) > 0


    def __str__(self):
        return self._name

# =======================
# PC logika
# =======================

class PCPlayer(Player):

    def choose_attack(self, game):
        if not game.table:
            return min(self._hand, key=lambda c: c.value())


        for c in self._hand:
            if c.rank in game.table_ranks():
                return c
        return None


    def choose_defense(self, attack_card, game):
        valid = [c for c in self._hand if game.valid_defense(c, attack_card)]
        return min(valid, key=lambda c: c.value()) if valid else None

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
                print("Error: Please input a number (f.e., 0 1) or input 'pass'.")

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

# =======================
# zaidimo logika
# =======================

class DurakGame:
    def __init__(self, players):
        self.deck = Deck()
        self.players = players
        self.table = []
        self.current_attacker_index = 0
        self.deal_cards()


    def deal_cards(self):
        for p in self.players:
            for _ in range(6):
                p.add_card(self.deck.draw())


    def show_status(self):
        print("\n" + "=" * 50)
        print(f"Trump: {self.deck.trump_card}")
        print(f"Deck: {len(self.deck.cards)} cards")


        for p in self.players:
            print(f"{p}: {len(p.get_hand())} cards")
        print("=" * 50)


    def show_table(self):
        if not self.table:
            return "Empty"
        return " | ".join(f"{a}->{d}" if d else f"{a}->?" for a, d in self.table)


    def table_ranks(self):
        r = []
        for a, d in self.table:
            r.append(a.rank)
            if d:
                r.append(d.rank)
        return r


    def valid_defense(self, d, a):
        return (d.suit == a.suit and d.value() > a.value()) or d.suit == self.deck.trump_suit


    def take_cards(self, p):
        for a, d in self.table:
            p.add_card(a)
            if d:
                p.add_card(d)
        self.table.clear()


    def refill(self):
        for p in self.players:
            while len(p.get_hand()) < 6:
                c = self.deck.draw()
                if not c:
                    break
                p.add_card(c)


    def play_round(self):
       
        defender_index = (self.current_attacker_index + 1) % len(self.players)
        defender = self.players[defender_index]

        attackers = []
        i = self.current_attacker_index
        while True:
            if i != defender_index:
                attackers.append(self.players[i])
            i = (i + 1) % len(self.players)
            if i == self.current_attacker_index:
                break


        turn = 0
        passes = 0
        attack_count = 0
        max_attacks = min(6, len(defender.get_hand()))


        while attack_count < max_attacks:
            self.show_status()

            attacker = attackers[turn % len(attackers)]
            self.current_player = attacker


            success = Attacker().play(self)
            if isinstance(attacker, PCPlayer) and success:
                time.sleep(1.5)


            if not success:
                passes += 1
                if passes >= len(attackers):
                    break
                turn += 1
                continue


            passes = 0
            attack_count += 1


            self.current_player = defender

            if not Defender().play(self):
                print(f"\n{defender} took the cards. Turn will be skipped!")
                self.refill()
                self.skip_turn = defender_index
                self.current_attacker_index = (defender_index + 1) % len(self.players)
                return

            turn += 1
    

        print("\n ***Defense successful!***")
        self.table.clear()
        self.refill()
        self.current_attacker_index = defender_index


    def is_game_over(self):
        return len([p for p in self.players if p.has_cards()]) <= 1


    def update_stats(self, winner):
        file = "stats.json"
        stats = {"games": 0, "human": 0, "pc": 0}
    
        try:
            with open(file, "r", encoding='utf-8') as f:
                stats = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        stats["games"] += 1
        if winner == "You": stats["human"] += 1
        else: stats["pc"] += 1

        with open(file, "w", encoding='utf-8') as f:
            json.dump(stats, f, indent=4)


    def show_stats(self):

        try:
            with open("stats.txt", "r") as f:
                stats = {}
                for line in f:

                    k, v = line.strip().split(":")

                    stats[k] = int(v)


            games = stats["games"]
            human = stats["human"]
            ai = stats["pc"]


            print("\n STATISTICS")
            print("-" * 30)
            print(f"Games played: {games}")
            print(f"Human wins: {human}")
            print(f"PC wins: {ai}")


            if games > 0:
                print(f"Human win rate: {round(human/games*100,2)}%")
                print(f"PC win rate: {round(ai/games*100,2)}%")

            print("-" * 30)


        except:
            print("No stats yet.")


    def play(self):
        print(f"Trump: {self.deck.trump_card}")

        while not self.is_game_over():
            self.play_round()


        winners = [p for p in self.players if not p.has_cards()]
        winner = winners[0]._name if winners else "PC"

        print("\n GAME OVER")
        print(f" Winner: {winner}")

        self.update_stats(winner)

# =======================
# zaidimo meniu
# =======================


if __name__ == "__main__":
    while True:
        print("\n1. Play")
        print("2. Stats")
        print("3. Exit")

        c = input("Choice: ").strip()

        if c == "1":
            game = DurakGame([
                Player("You"),
                PCPlayer("PC_1"),
                PCPlayer("PC_2")
            ])
            game.play()
        elif c == "2":
            
            DurakGame([]).show_stats()
        elif c == "3":
            print("Goodbye!")
            break
        else:
            print("Neteisingas pasirinkimas, bandykite dar kartą.")