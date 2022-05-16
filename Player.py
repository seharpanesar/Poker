class Player:
    def __init__(self):
        self.hand = []

    # gets 2 cards from deck
    def setHand(self, deck):
        self.hand = deck.drawXCards(2)

    def clearHand(self):
        self.hand.clear()

