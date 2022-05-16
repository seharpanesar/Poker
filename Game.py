from Player import Player
from Deck import Deck

class Game:
    commonPool = [] # 5 cards in the middle (available to every one of the 6 players)

    def __init__(self):
        self.players = []

        for i in range(6):
            self.players.append(Player())

        self.deck = Deck()

    def runGame(self):
        for player in self.players:
            player.setHand(self.deck)

        commonPool = self.deck.drawXCards(5)
