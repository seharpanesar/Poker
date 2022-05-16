from Card import Card
import random

class Deck:
    drawnCards = []

    def __init__(self):
        suites = ['s', 'd', 'h', 'c']
        ranks = list(range(1,14))

        self.cards = []

        for suite in suites:
            for rank in ranks:
                self.cards.append(Card(rank, suite))

        self.shuffle()

        for i in self.cards:
            print(i)

    def shuffle(self):
        # inplace shuffle
        random.shuffle(self.cards)

    def drawCard(self):
        card = self.cards.pop(0)
        self.drawnCards.append(card)
        return card

    def drawXCards(self, x):
        return [self.drawCard() for i in range(x)]


    def getSize(self):
        return len(self.cards)

    def collect(self):
        self.cards = self.cards + self.drawnCards
        self.drawnCards.clear()
        self.shuffle()