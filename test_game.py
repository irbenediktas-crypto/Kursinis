import pytest
from card import Card, CardFactory
from deck import Deck
from player import Player, PCPlayer
from game import DurakGame


class TestCard:
    def test_card_creation(self):
        card = Card('Hearts', 'A')
        assert card.suit == 'Hearts'
        assert card.rank == 'A'

    def test_card_value(self):
        card = Card('Hearts', 'A')
        assert card.value() == 8  # A is last in RANKS

    def test_card_str(self):
        card = Card('Hearts', 'A')
        # Assuming colorama is working, but for test, check structure
        assert 'A' in str(card)
        assert '♥' in str(card)


class TestCardFactory:
    def test_create_deck(self):
        deck = CardFactory.create_deck()
        assert len(deck) == 36  # 4 suits * 9 ranks
        assert all(isinstance(card, Card) for card in deck)


class TestDeck:
    def test_deck_creation(self):
        deck = Deck()
        assert len(deck.cards) == 35  # 36 - 1 trump
        assert deck.trump_card is not None

    def test_draw(self):
        deck = Deck()
        card = deck.draw()
        assert card is not None
        assert len(deck.cards) == 34


class TestPlayer:
    def test_player_creation(self):
        player = Player("Test")
        assert player._name == "Test"
        assert player._hand == []

    def test_add_card(self):
        player = Player("Test")
        card = Card('Hearts', 'A')
        player.add_card(card)
        assert len(player._hand) == 1
        assert player._hand[0] == card

    def test_remove_card(self):
        player = Player("Test")
        card = Card('Hearts', 'A')
        player.add_card(card)
        player.remove_card(card)
        assert len(player._hand) == 0

    def test_has_cards(self):
        player = Player("Test")
        assert not player.has_cards()
        player.add_card(Card('Hearts', 'A'))
        assert player.has_cards()


class TestPCPlayer:
    def test_inheritance(self):
        pc = PCPlayer("PC")
        assert isinstance(pc, Player)

    def test_choose_attack_empty_table(self):
        pc = PCPlayer("PC")
        pc.add_card(Card('Hearts', '6'))
        pc.add_card(Card('Hearts', '7'))
        game = DurakGame([pc])
        card = pc.choose_attack(game)
        assert card.rank == '6'  # lowest value


class TestDurakGame:
    def test_game_creation(self):
        players = [Player("P1"), Player("P2")]
        game = DurakGame(players)
        assert len(game.players) == 2
        assert game.deck is not None

    def test_deal_cards(self):
        players = [Player("P1"), Player("P2")]
        game = DurakGame(players)
        assert len(players[0].get_hand()) == 6
        assert len(players[1].get_hand()) == 6

    def test_valid_defense(self):
        game = DurakGame([])
        attack = Card('Hearts', '7')
        defense = Card('Hearts', '8')
        assert game.valid_defense(defense, attack)

        defense_trump = Card('Spades', '6')
        game.deck.trump_suit = 'Spades'
        assert game.valid_defense(defense_trump, attack)