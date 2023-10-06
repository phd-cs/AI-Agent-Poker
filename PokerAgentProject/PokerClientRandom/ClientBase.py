class BettingAnswer:
    '''
    ACTION_OPEN = 0
    ACTION_CHECK = 1
    ACTION_CALL = 2
    ACTION_RAISE = 3
    ACTION_FOLD = 4
    ACTION_ALLIN = 5
    '''
    ACTION_OPEN = 'Open'
    ACTION_CHECK = 'Check'
    ACTION_CALL = 'Call'
    ACTION_RAISE = 'Raise'
    ACTION_FOLD = 'Fold'
    ACTION_ALLIN = 'All-in'

class Card:
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3
    BAD_CARD = -1
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12
    NUM_SUITS = 4
    NUM_RANKS = 13
    NUM_CARDS = 52
