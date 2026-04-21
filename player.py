from card import Card


# =======================
# player logic
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
# PC logic
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