
from HandRanking import HandRanking
from Card import Card

# playerHand is list of cards size 2, commonPool is list of cards size 5

# each method returns a tuple:
# [rank (int), 5 card hand]
# if rank is positive, then the hand is a valid instance of that ranking. 1 = high card, 2 = pair ... 10 = royal flush

def getAllCardsAndFMap(playerHand, commonPool):
    allCards = playerHand + commonPool

    freq_map = {}  # for all 7 cards, it maps card rank (A,2..) -> frequency. Will help determine pairs, 2 pair etc.
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
    allCards.sort(key=lambda card: card.frequency * 1000 + card.rank, reverse=True)

    return allCards, freq_map

def getHandRanking(playerHand, commonPool):
    # todo: testing that all is() functions work correctly. (3 for each fn)
    # todo: incorporate the enum into this mess.
    # todo: fix naming convention (freq_map, allCards) etc

    allCards, freq_map = getAllCardsAndFMap(playerHand, commonPool)

    functions = [isHighCard, isPair, isTwoPair, isThreeOfAKind, isStraight,
                 isFlush, isFullHouse, isFourOfAKind, isStraightFlush, isRoyalFlush]
    functions.reverse()  # check in reverse order. If true instance found, then return that since that is the highest ranking.

    for function in functions:
        rankCheck = function(allCards, freq_map)
        if rankCheck[0] > 0:
            return rankCheck

def isHighCard(allCards, freq_map):
    best5cards = allCards[:5]

    return (HandRanking.HIGH_CARD, best5cards)

def isPair(allCards, freq_map):
    best5cards = allCards[:5]

    if 2 in freq_map.values():
        return (HandRanking.PAIR, best5cards)
    else:
        return (HandRanking.NONE, None)

def isTwoPair(allCards, freq_map):
    best5cards = allCards[:5]
    countOfPairs = 0

    for freq in freq_map.values():
        if freq == 2:
            countOfPairs += 1
        if countOfPairs == 2:
            # is 2 pair does exist, then the 5th card of the best 5 cards should be the max of the cards NOT included in 2 pair.
            # here is why: it is possible that there are 3 pairs in allCards. This leads to the 5th and 6th card being the low ranked pair.
            # In the case, the 7th card could be higher in rank than the 5th card, so swap them if that is the case.

            maxCard = max(allCards[4:], key= lambda card: card.rank)
            best5cards.pop()
            best5cards.append(maxCard)
            return (HandRanking.TWO_PAIR, best5cards)

    return (HandRanking.NONE, None)

def isThreeOfAKind(allCards, freq_map):
    best5cards = allCards[:5]

    if 3 in freq_map.values():
        return (HandRanking.THREE_OF_A_KIND, best5cards)
    else:
        return (HandRanking.NONE, None)

def isStraight(allCards, freq_map):
    # temporarily sort by ranking. will be sorted back to original ordering later
    allCards.sort(key=lambda card: card.rank, reverse=True)

    # corner case of A,2,3,4,5: temporarily add a card A with rank of 1 todo: remove that card from all cards
    extraCardFlag = False

    for card in allCards:
        if card.rank == 14:
            allCards.append(Card(1, card.suite))
            extraCardFlag = True
            break
    valid_seq_count = 0
    valid_seq = [allCards[0]]

    # todo: find a more efficient way to determine if sequence exists in hand
    for i in range(len(allCards)-1):
        if (allCards[i].rank - 1 == allCards[i+1].rank): # valid sequence step found
            valid_seq_count += 1
            valid_seq.append(allCards[i+1])
        elif not (allCards[i].rank == allCards[i+1].rank): # condition is to ensure that duplicate cards (in rank) are skipped
            valid_seq_count = 0
            valid_seq.clear()
            valid_seq.append(allCards[i + 1])

        if valid_seq_count == 4:
            # find and return card
            if extraCardFlag:
                allCards.pop()
            valid_seq.reverse()
            allCards.sort(key=lambda card: card.frequency * 1000 + card.rank, reverse=True)
            return (HandRanking.STRAIGHT, valid_seq)

    if extraCardFlag:
        allCards.pop()
    allCards.sort(key=lambda card: card.frequency * 1000 + card.rank, reverse=True)
    return (HandRanking.NONE, None)

def isFlush(allCards, freq_map):
    suite_map = {}

    for card in allCards:
        if card.suite in suite_map:
            suite_map[card.suite] += 1
        else:
            suite_map[card.suite] = 1

    if 5 in suite_map.values():
        flush_suite = max(suite_map, key=suite_map.get) # get() function returns a value for a given key
        flushCards = sorted(allCards, key=lambda card: card.suite == flush_suite, reverse=True)

        return (HandRanking.FLUSH, flushCards[:5])

    return (HandRanking.NONE, None)

def isFullHouse(allCards, freq_map):
    best5cards = allCards[:5]

    if 2 in freq_map.values() and 3 in freq_map.values():
        return (HandRanking.FULL_HOUSE, best5cards)
    else:
        return (HandRanking.NONE, None)

def isFourOfAKind(allCards, freq_map):
    best5cards = allCards[:5]

    if 4 in freq_map.values():
        # is 4 OaK does exist, then the 5th card of the best 5 cards should be the max of the cards NOT included in 4 Of a Kind.
        # here is why: it is possible that there is a 4 of a kind and a pair in allCards. This leads to the 5th and 6th card being the  pair.
        # The 7th card could be higher in rank than the pair card, so swap them if that is the case.

        maxCard = max(allCards[4:], key=lambda card: card.rank)
        best5cards.pop()
        best5cards.append(maxCard)
        return (HandRanking.FOUR_OF_A_KIND, best5cards)
    else:
        return (HandRanking.NONE, None)

def isStraightFlush(allCards, freq_map):
    # todo: memoize the results so that isFlush() and isStraight do not need to be called multiple times

    (straightNum, straightCards) = isStraight(allCards, freq_map)
    (flushNum, flushCards) = isFlush(allCards, freq_map)

    if (straightNum > 0 and flushNum > 0):
        return (HandRanking.STRAIGHT_FLUSH, straightCards)

    return (HandRanking.NONE, None)

def isRoyalFlush(allCards, freq_map):
    # todo: memoize the results so that isFlush() and isStraight do not need to be called multiple times

    straightFlushNum, straightFlushCards = isStraightFlush(allCards, freq_map)

    if straightFlushCards == None:
        return (HandRanking.NONE, None)

    # straight flush beginning with a 10 = royal flush, given cards are in order.
    if straightFlushCards[0].rank == 10:
        return (HandRanking.ROYAL_FLUSH, straightFlushCards)
    return (HandRanking.NONE, None)