from Player import Player
from Deck import Deck
import Util

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

        for player in self.players:
            player.signalAndCards = Util.getHandRanking(player.hand, commonPool)

        # sort players by their how good their hand is
        self.players.sort(key=lambda player: player.signalAndCards[0]*100 + Util.sumOfCards(player.signalAndCards[1]),
                          reverse=True)

        # data will be a list containing game data to be recorded. indices:
        #   0-5 = 6 tuples of (hand ranking, best 5 cards, starting 2 cards)
        #   6 = common pool cards

        data = []

        for player in self.players:
            data.append((player.signalAndCards[0], player.signalAndCards[1], player.hand))
            # player.clearHand()

        data.append(commonPool)
        self.deck.collect()
        self.deck.shuffle()

        return data