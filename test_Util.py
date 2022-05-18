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

        pairNum, pairHand = Util.getHandRanking(playerHand, commonPool)
        self.assertEqual(pairNum, HandRanking.PAIR)
        self.assertEqual(pairHand, [Card(8, "d"), Card(8, "c"), Card(11, "s"), Card(10, "s"), Card(6, "c")])

        # test 2: pair dne. only high card
        playerHand = [Card(2, "s"), Card(8, "d")]
        commonPool = [Card(7, "s"), Card(3, "h"), Card(11, "s"), Card(6, "c"), Card(4, "c")]

        highCardNum, highCardHand = Util.getHandRanking(playerHand, commonPool)
        self.assertEqual(highCardNum, HandRanking.HIGH_CARD)
        self.assertEqual(highCardHand[0], Card(11, "s"))

    # def test_isTwoPair(self):
    #     self.assertTrue()

    # def test_isThreeOfAKind(self):
    #     self.assertTrue()
    #
    # def test_isStraight(self):
    #     self.assertTrue()
    #
    # def test_isFlush(self):
    #     self.assertTrue()
    #
    # def test_isFullHouse(self):
    #     self.assertTrue()
    #
    # def test_isFourOfAKind(self):
    #     self.assertTrue()
    #
    # def test_isStraightFlush(self):
    #     self.assertTrue()

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