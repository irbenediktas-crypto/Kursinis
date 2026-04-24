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
        assert card.value() == 12   

    def test_card_str(self):
        card = Card('Hearts', 'A')
       
        assert 'A' in str(card)
        assert '♥' in str(card)


class TestCardFactory:
    def test_create_deck(self):
        deck = CardFactory.create_deck()
        assert len(deck) == 52  
        assert all(isinstance(card, Card) for card in deck)


class TestDeck:
    def test_deck_creation(self):
        deck = Deck()
        assert len(deck.cards) == 51  
        assert deck.trump_card is not None

    def test_draw(self):
        deck = Deck()
        card = deck.draw()
        assert card is not None
        assert len(deck.cards) == 50  


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
        
        game = DurakGame([pc])
        card = pc.choose_attack(game)
        
        assert card is not None
        assert isinstance(card, Card)  


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



class TestEdgeCases:
    def test_draw_empty_deck(self):
        deck = Deck()
        
        for _ in range(51):
            deck.draw()
        
        assert deck.draw() is None

    def test_player_no_cards_attack(self):
        player = Player("Test")
        
        assert not player.has_cards()
        
        game = DurakGame([player])
        assert player.has_cards()  

    def test_player_no_cards_defense(self):
        player = Player("Test")
        game = DurakGame([player])
        attack_card = Card('Hearts', '7')
        
        defense = player.choose_defense(attack_card, game) if hasattr(player, 'choose_defense') else None
        assert defense is None

    def test_game_with_three_players(self):
        players = [Player("P1"), Player("P2"), Player("P3")]
        game = DurakGame(players)
        assert len(game.players) == 3
       
        total_cards = sum(len(p.get_hand()) for p in game.players)
        assert total_cards <= 52

    def test_game_with_four_players(self):
        players = [Player("P1"), Player("P2"), Player("P3"), Player("P4")]
        game = DurakGame(players)
        assert len(game.players) == 4




