import random
import json
import time
from abc import ABC, abstractmethod


# =======================
# colors
# =======================

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Dummy:
        RED = WHITE = RESET_ALL = ""
    Fore = Style = Dummy()


# =======================
# card
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
    RANKS = [
        '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
    ]

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def value(self):
        return Card.RANKS.index(self.rank)

    def __str__(self):
        color = Card.COLORS[self.suit]
        symbol = Card.SYMBOLS[self.suit]
        return f"{color}{self.rank}{symbol}{Style.RESET_ALL}"


class CardFactory:
    @staticmethod
    def create_deck():
        return [Card(s, r) for s in Card.SUITS for r in Card.RANKS]