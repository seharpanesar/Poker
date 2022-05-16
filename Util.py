class Util:
    # playerHand is list of cards size 2, commonPool is list of cards size 5

    # each method returns a tuple:
    # [rank (int), 5 card hand]
    # if rank is positive, then the hand is a valid instance of that ranking. 1 = high card, 2 = pair ... 10 = royal flush

    def getHandRanking(self, playerHand, commonPool):
        # todo: testing that all is() functions work correctly. (3 for each fn)
        # todo: split getHandRanking into 2 fns and test the fn with frequency map
        # todo: incorporate the enum into this mess.


        functions = [self.isHighCard, self.isPair, self.isTwoPair, self.isThreeOfAKind, self.isStraight,
                     self.isFlush, self.isFullHouse, self.isFourOfAKind, self.isStraightFlush, self.isRoyalFlush]
        functions.reverse() # check in reverse order. If true instance found, then return that since that is the highest ranking.

        allCards = playerHand + commonPool

        freq_map = {} # for all 7 cards, it maps card rank (A,2..) -> frequency. Will help determine pairs, 2 pair etc.
        for card in allCards:
            if card.rank in freq_map:
                freq_map[card.rank] += 1
            else:
                freq_map[card.rank] = 1

        # assign frequency for all cards in hand
        for card in allCards:
            card.frequency = freq_map[card.rank]

        # now that we know card frequency, we can sort the hand by placing cards with higher frequency in the beginning,
        # this helps us easily identify the following hands: pair, 2 pair, 3 of a kind, full house, 4 of a kind
        # lambda function helps us sort in this manner
        allCards.sort(key=lambda card : card.frequency*1000 + card.rank, reverse=True)

        for function in functions:
            rankCheck = function(allCards, freq_map)
            if rankCheck[0] > 0:
                return rankCheck

    def isHighCard(self, allCards, freq_map):
        best5cards = allCards[:5]

        return (1, best5cards)

    def isPair(self, allCards, freq_map):
        best5cards = allCards[:5]

        if 2 in freq_map.values():
            return (2, best5cards)
        else:
            return (0, None)

    def isTwoPair(self, allCards, freq_map):
        best5cards = allCards[:5]
        countOfPairs = 0

        for freq in freq_map.values():
            if freq == 2:
                countOfPairs += 1
            if countOfPairs == 2:
                return (3, best5cards)

        return (0, None)

    def isThreeOfAKind(self, allCards, freq_map):
        best5cards = allCards[:5]

        if 3 in freq_map.values():
            return (4, best5cards)
        else:
            return (0, None)

    def isStraight(self, allCards, freq_map):
        ranks = sorted(freq_map.values)

        # corner case of A,2,3,4,5
        if 14 in freq_map.keys():
            ranks.insert(0, 1)

        valid_seq_count = 0
        valid_seq = [ranks[0]]

        # todo: find a more efficient way to determine if sequence exists in hand
        for i in range(len(ranks)-1):
            if (ranks[i] + 1 == ranks[i+1]):
                valid_seq_count += 1
                valid_seq.append(ranks[i+1])
            else:
                valid_seq_count = 0
                valid_seq.clear()
                valid_seq.append(ranks[i+1])

            if valid_seq_count == 4:
                return (5, valid_seq)

        return (0, None)

    def isFlush(self, allCards, freq_map):
        suite_map = {}

        for card in allCards:
            if card.suite in suite_map:
                suite_map[card.suite] += 1
            else:
                suite_map[card.suite] = 1

        if 5 in suite_map.values():
            flush_suite = max(suite_map, key=suite_map.get) # get() function returns a value for a given key
            flushCards = sorted(allCards, key=lambda card: card.suite == flush_suite, reverse=True)

            return (6, flushCards[:5])

        return (0, None)

    def isFullHouse(self, allCards, freq_map):
        best5cards = allCards[:5]

        if 2 in freq_map.values() and 3 in freq_map.values():
            return (7, best5cards)
        else:
            return (0, None)

    def isFourOfAKind(self, allCards, freq_map):
        best5cards = allCards[:5]

        if 4 in freq_map.values():
            return (8, best5cards)
        else:
            return (0, None)

    def isStraightFlush(self, allCards, freq_map):
        # todo: memoize the results so that isFlush() and isStraight do not need to be called multiple times

        (straightNum, straightCards) = self.isStraight(allCards, freq_map)
        (flushNum, flushCards) = self.isFlush(allCards, freq_map)

        if (straightNum > 0 and flushNum > 0):
            return (9, straightCards)

    def isRoyalFlush(self, allCards, freq_map):
        # todo: memoize the results so that isFlush() and isStraight do not need to be called multiple times

        straightFlushNum, straightFlushCards = self.isStraightFlush(allCards, freq_map)

        # straight flush beginning with a 10 = royal flush, given cards are in order.
        if straightFlushCards[0].rank == 10:
            return (10, straightFlushCards)

        return (0, straightFlushCards)