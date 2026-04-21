import random
from card import Card, CardFactory


# =======================
# deck
# =======================

class Deck:
    def __init__(self):
        self.cards = CardFactory.create_deck()
        random.shuffle(self.cards)
        self.trump_card = self.cards.pop()
        self.trump_suit = self.trump_card.suit

    def draw(self):
        return self.cards.pop() if self.cards else None