import unittest
import Util
from Card import Card
from HandRanking import HandRanking



class TestUtil(unittest.TestCase):
    # all function definitions must start with test for it to be run
    def test_isPair(self):
        playerHand = [Card(2, "s"), Card(8, "d")]
        commonPool = [Card(10, "s"), Card(3, "h"), Card(11, "s"), Card(6, "c"), Card(5, "c")]

        allCards, freqMap = Util.getAllCardsAndFMap(playerHand, commonPool)
        pairNum, pairHand = Util.isPair(allCards, freqMap)
        self.assertTrue(pairNum, HandRanking.PAIR)


# to avoid annoying command line args for "python test_Util.py"
# runs all the tests
if __name__ == "__main__":
    unittest.main()