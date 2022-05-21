from HandRanking import HandRanking

class Player:
    def __init__(self):
        self.hand = []
        self.signalAndCards = (HandRanking.NONE, None) # signal represents the poker ranking of the best 5 cards (see HandRanking.py)

    # gets 2 cards from deck
    def setHand(self, deck):
        self.signalAndCards = (HandRanking.NONE, None)
        self.hand = deck.drawXCards(2)

    def clearHand(self):
        self.hand.clear()
        self.signalAndCards = (HandRanking.NONE, None)

