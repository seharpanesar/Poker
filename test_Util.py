import unittest
import Util
from Card import Card
from HandRanking import HandRanking

class TestUtil(unittest.TestCase):
    # all function definitions must start with "test" for it to be run
    # def test_getAllCardsAndFMap(self):
    #     self.assertTrue()

    def test_isPair(self):
        # test 1: pair exists
        playerHand = [Card(2, "s"), Card(8, "d")]
        commonPool = [Card(10, "s"), Card(3, "h"), Card(11, "s"), Card(6, "c"), Card(8, "c")]

        signal1, hand1 = Util.getHandRanking(playerHand, commonPool)
        self.assertEqual(signal1, HandRanking.PAIR)
        self.assertEqual(hand1, [Card(8, "d"), Card(8, "c"), Card(11, "s"), Card(10, "s"), Card(6, "c")])

        # test 2: pair dne. only high card
        playerHand = [Card(2, "s"), Card(8, "d")]
        commonPool = [Card(7, "s"), Card(3, "h"), Card(11, "s"), Card(6, "c"), Card(4, "c")]

        signal2, hand2  = Util.getHandRanking(playerHand, commonPool)
        self.assertEqual(signal2, HandRanking.HIGH_CARD)
        self.assertEqual(hand2[0], Card(11, "s"))

    def test_isTwoPair(self):
        # test 1: 2 pair exists
        playerHand = [Card(2, "s"), Card(8, "s")]
        commonPool = [Card(2, "d"), Card(8, "d"), Card(11, "s"), Card(6, "c"), Card(3, "c")]

        signal1, hand1 = Util.getHandRanking(playerHand, commonPool)

        self.assertEqual(signal1, HandRanking.TWO_PAIR)

        expectedHandRank = [8,8,2,2,11]
        for i, rank in enumerate(expectedHandRank):
            self.assertEqual(hand1[i].rank, rank)

        # test 2: 2 pair dne. its a 3 of a kind
        playerHand = [Card(8, "s"), Card(8, "d")]
        commonPool = [Card(8, "h"), Card(3, "h"), Card(11, "s"), Card(6, "c"), Card(4, "c")]

        signal2, hand2 = Util.getHandRanking(playerHand, commonPool)

        self.assertEqual(signal2, HandRanking.THREE_OF_A_KIND)

        expectedHandRank = [8, 8, 8, 11, 6]
        for i, rank in enumerate(expectedHandRank):
            self.assertEqual(hand2[i].rank, rank)

    def test_isThreeOfAKind(self):
        # test 1: 3 of a kind exists
        playerHand = [Card(14, "s"), Card(10, "d")]
        commonPool = [Card(3, "h"), Card(3, "s"), Card(11, "d"), Card(3, "c"), Card(4, "c")]

        signal1, hand1 = Util.getHandRanking(playerHand, commonPool)

        self.assertEqual(signal1, HandRanking.THREE_OF_A_KIND)

        expectedHandRank = [3,3,3,14,11]
        for i, rank in enumerate(expectedHandRank):
            self.assertEqual(hand1[i].rank, rank)

        # test 2: 3 of a kind exists, but so does full house, so full house should be returned
        playerHand = [Card(14, "s"), Card(10, "d")]
        commonPool = [Card(3, "h"), Card(3, "s"), Card(11, "d"), Card(3, "c"), Card(14, "c")]

        signal2, hand2 = Util.getHandRanking(playerHand, commonPool)

        self.assertEqual(signal2, HandRanking.FULL_HOUSE)

        expectedHandRank = [3, 3, 3, 14, 14]
        for i, rank in enumerate(expectedHandRank):
            self.assertEqual(hand2[i].rank, rank)

    def test_isStraight(self):
        # test 1: 3-7 straight exists
        playerHand = [Card(6, "s"), Card(4, "d")]
        commonPool = [Card(3, "h"), Card(7, "s"), Card(5, "d"), Card(3, "c"), Card(14, "c")]

        signal1, hand1 = Util.getHandRanking(playerHand, commonPool)

        self.assertEqual(signal1, HandRanking.STRAIGHT)

        expectedHandRank = [3, 4, 5, 6, 7]
        for i, rank in enumerate(expectedHandRank):
            self.assertEqual(hand1[i].rank, rank)

        # test 2: A-5 straight exists (special case)
        playerHand = [Card(2, "s"), Card(4, "d")]
        commonPool = [Card(3, "h"), Card(7, "s"), Card(5, "d"), Card(3, "c"), Card(14, "c")]

        signal2, hand2 = Util.getHandRanking(playerHand, commonPool)

        self.assertEqual(signal2, HandRanking.STRAIGHT)

        expectedHandRank = [1, 2, 3, 4, 5]
        for i, rank in enumerate(expectedHandRank):
            self.assertEqual(hand2[i].rank, rank)

    def test_isFlush(self):
        # test 1: flush exists
        playerHand = [Card(6, "s"), Card(4, "s")]
        commonPool = [Card(13, "s"), Card(14, "s"), Card(5, "d"), Card(3, "c"), Card(10, "s")]

        signal1, hand1 = Util.getHandRanking(playerHand, commonPool)

        self.assertEqual(signal1, HandRanking.FLUSH)

        expectedHandRank = [14,13,10,6,4]
        for i, rank in enumerate(expectedHandRank):
            self.assertEqual(hand1[i].rank, rank)

        # test 2: flush exists, but straight flush exists too, so expected return is straight flush
        playerHand = [Card(11, "s"), Card(10, "s")]
        commonPool = [Card(12, "s"), Card(8, "s"), Card(5, "d"), Card(3, "c"), Card(9, "s")]

        signal2, hand2 = Util.getHandRanking(playerHand, commonPool)

        self.assertEqual(signal2, HandRanking.STRAIGHT_FLUSH)

        expectedHandRank = [8,9,10,11,12]
        for i, rank in enumerate(expectedHandRank):
            self.assertEqual(hand2[i].rank, rank)

        # test 3: only straight exists
        playerHand = [Card(11, "s"), Card(10, "s")]
        commonPool = [Card(12, "s"), Card(8, "d"), Card(5, "d"), Card(3, "c"), Card(9, "s")]

        signal3, hand3 = Util.getHandRanking(playerHand, commonPool)

        self.assertEqual(signal3, HandRanking.STRAIGHT)

        expectedHandRank = [8,9,10,11,12]
        for i, rank in enumerate(expectedHandRank):
            self.assertEqual(hand3[i].rank, rank)

    def test_isFullHouse(self):
        # test 1: 2 full house exists. it should return the better one
        playerHand = [Card(6, "s"), Card(4, "s")]
        commonPool = [Card(6, "c"), Card(14, "d"), Card(6, "d"), Card(14, "c"), Card(4, "h")]

        signal1, hand1 = Util.getHandRanking(playerHand, commonPool)

        self.assertEqual(signal1, HandRanking.FULL_HOUSE)

        expectedHandRank = [6,6,6,14,14]
        for i, rank in enumerate(expectedHandRank):
            self.assertEqual(hand1[i].rank, rank)

        # test 2: no full house exists
        playerHand = [Card(6, "s"), Card(4, "s")]
        commonPool = [Card(6, "c"), Card(14, "d"), Card(13, "d"), Card(14, "c"), Card(4, "h")]

        signal1, hand1 = Util.getHandRanking(playerHand, commonPool)

        self.assertEqual(signal1, HandRanking.TWO_PAIR)

        expectedHandRank = [14,14,6,6,13]
        for i, rank in enumerate(expectedHandRank):
            self.assertEqual(hand1[i].rank, rank)

    def test_isFourOfAKind(self):
        # test 1: 4 of a kind exists
        playerHand = [Card(13, "s"), Card(13, "d")]
        commonPool = [Card(6, "c"), Card(13, "h"), Card(6, "d"), Card(14, "c"), Card(13, "c")]

        signal1, hand1 = Util.getHandRanking(playerHand, commonPool)

        self.assertEqual(signal1, HandRanking.FOUR_OF_A_KIND)

        expectedHandRank = [13,13,13,13,14]
        for i, rank in enumerate(expectedHandRank):
            self.assertEqual(hand1[i].rank, rank)

        # test 1: 4 of a kind dne
        playerHand = [Card(13, "s"), Card(12, "d")]
        commonPool = [Card(6, "c"), Card(10, "h"), Card(5, "d"), Card(14, "c"), Card(3, "c")]

        signal1, hand1 = Util.getHandRanking(playerHand, commonPool)

        self.assertEqual(signal1, HandRanking.HIGH_CARD)

        expectedHandRank = [14,13,12,10,6]
        for i, rank in enumerate(expectedHandRank):
            self.assertEqual(hand1[i].rank, rank)


    def test_isStraightFlush(self):
        # test 1: there is a straight flush of spade 6-10
        playerHand = [Card(6, "s"), Card(10, "s")]
        commonPool = [Card(7, "s"), Card(3, "h"), Card(9, "s"), Card(13, "c"), Card(8, "s")]
        expectedHand = [Card(6, "s"), Card(7, "s"), Card(8, "s"), Card(9, "s"), Card(10, "s")]

        signal, hand = Util.getHandRanking(playerHand, commonPool)
        self.assertEqual(signal, HandRanking.STRAIGHT_FLUSH)
        self.assertEqual(hand, expectedHand)

        # test 2: only straight
        playerHand = [Card(6, "s"), Card(10, "d")]
        commonPool = [Card(7, "s"), Card(3, "h"), Card(9, "s"), Card(13, "c"), Card(8, "s")]
        expectedHand = [Card(6, "s"), Card(7, "s"), Card(8, "s"), Card(9, "s"), Card(10, "d")]

        signal, hand = Util.getHandRanking(playerHand, commonPool)
        self.assertEqual(signal, HandRanking.STRAIGHT)
        self.assertEqual(hand, expectedHand)

        # test 3: only flush
        playerHand = [Card(6, "s"), Card(11, "s")]
        commonPool = [Card(7, "s"), Card(3, "h"), Card(9, "s"), Card(13, "c"), Card(8, "s")]
        expectedHand = [Card(11, "s"), Card(9, "s"), Card(8, "s"), Card(7, "s"), Card(6, "s")]

        signal, hand = Util.getHandRanking(playerHand, commonPool)
        self.assertEqual(signal, HandRanking.FLUSH)
        self.assertEqual(hand, expectedHand)


    def test_isRoyalFlush(self):
        # test 1: there is a royal flush of spade
        playerHand = [Card(14, "s"), Card(10, "s")]
        commonPool = [Card(11, "s"), Card(3, "h"), Card(12, "s"), Card(13, "s"), Card(5, "c")]
        expectedHand = [Card(10, "s"), Card(11, "s"), Card(12, "s"), Card(13, "s"), Card(14, "s")]

        signal, hand = Util.getHandRanking(playerHand, commonPool)
        self.assertEqual(signal, HandRanking.ROYAL_FLUSH)
        self.assertEqual(hand, expectedHand)

        # test 2: NO royal flush of spades
        # difference between test 1 and 2 is the 12 of diamonds instead of 12 of spades
        # only makes a straight but not a straight flush
        playerHand = [Card(14, "s"), Card(10, "s")]
        commonPool = [Card(11, "s"), Card(3, "h"), Card(12, "d"), Card(13, "s"), Card(5, "c")]

        Ssignal, Shand = Util.getHandRanking(playerHand, commonPool)
        expectedHand = [Card(10, "s"), Card(11, "s"), Card(12, "d"), Card(13, "s"), Card(14, "s")]

        self.assertEqual(Ssignal, HandRanking.STRAIGHT)
        self.assertEqual(Shand, expectedHand)

# to avoid annoying command line args for "python test_Util.py"
# runs all the tests
if __name__ == "__main__":
    unittest.main()