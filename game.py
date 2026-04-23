import json
import time
from deck import Deck
from player import Player, PCPlayer
from role import Attacker, Defender


# =======================
# game logic
# =======================

class DurakGame:
    def __init__(self, players, ranks=None):
        self.deck = Deck(ranks)
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
        # Same suit: must have higher value
        if d.suit == a.suit:
            return d.value() > a.value()
        # Trump card: beats non-trump, or higher trump beats lower trump
        if d.suit == self.deck.trump_suit:
            return a.suit != self.deck.trump_suit or d.value() > a.value()
        return False

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
        # Check if game should end before starting new round
        if self.is_game_over():
            return
            
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

        # Safety check: if no attackers (shouldn't happen), return
        if not attackers:
            return
            
        turn = 0
        passes = 0
        attack_count = 0
        max_attacks = min(6, len(defender.get_hand())) if defender.get_hand() else 0

        while attack_count < max_attacks:
            attacker = attackers[turn % len(attackers)]
            if attacker._name == "You":
                self.show_status()

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
            if defender._name == "You":
                self.show_status()

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
        if winner == "You":
            stats["human"] += 1
        else:
            stats["pc"] += 1

        with open(file, "w", encoding='utf-8') as f:
            json.dump(stats, f, indent=4)

    def show_stats(self):
        try:
            with open("stats.json", "r", encoding='utf-8') as f:
                stats = json.load(f)

            games = stats.get("games", 0)
            human = stats.get("human", 0)
            ai = stats.get("pc", 0)

            print("\n STATISTICS")
            print("-" * 30)
            print(f"Games played: {games}")
            print(f"Human wins: {human}")
            print(f"PC wins: {ai}")

            if games > 0:
                print(f"Human win rate: {round(human/games*100,2)}%")
                print(f"PC win rate: {round(ai/games*100,2)}%")

            print("-" * 30)

        except Exception:
            print("No stats yet.")

    def play(self):
        print(f"Trump: {self.deck.trump_card}")

        max_rounds = 1000  # Safety limit to prevent infinite loops
        round_num = 0
        
        while not self.is_game_over() and round_num < max_rounds:
            self.play_round()
            round_num += 1
        
        if round_num >= max_rounds:
            print("\n Game ended due to round limit.")

        # Find the winner - player with no cards
        winners = [p for p in self.players if not p.has_cards()]
        
        if winners:
            winner = winners[0]._name
        else:
            # Edge case: no winner found, pick player with fewest cards
            winner = min(self.players, key=lambda p: len(p.get_hand()))._name

        print("\n GAME OVER")
        print(f" Winner: {winner}")

        self.update_stats(winner)