class Card:

    def __init__(self, rank, suite):
        # rank corresponds to number. 2 = 2, ..., 10 = 10, 11 = J, 12 = Q, 13 = K 14 = A
        self.rank = rank

        # suite: 's' = "spades", 'd' = "diamonds", 'h' = "hearts", 'c' = "clubs"
        self.suite = suite

        # in the 7 cards (hand+common pool) how many times does a card of this rank appear?
        # this variable will change with every instance
        self.frequency = 0


    def __str__(self):
        return "{} of {}".format(self.rank, self.suite)

    def __eq__(self, other):
        return self.rank == other.rank and self.suite == other.suite