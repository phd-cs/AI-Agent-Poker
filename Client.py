import socket
import random
from collections import defaultdict

import ClientBase
import Evaluation

# IP address and port
TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

# Agent
POKER_CLIENT_NAME = 'Knights'
CURRENT_HAND = []

class pokerGames(object):
    def __init__(self):
        self.PlayerName = POKER_CLIENT_NAME
        self.Chips = 0
        self.CurrentHand = []
        self.Ante = 0
        self.playersCurrentBet = 0

def hand_info():
    return CURRENT_HAND

'''
* Gets the name of the player.
* @return  The name of the player as a single word without space. <code>null</code> is not a valid answer.
'''
def queryPlayerName(_name):
    if _name is None:
        _name = POKER_CLIENT_NAME
    return _name

'''
* Modify queryOpenAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what open
* action to choose.
* @param minimumPotAfterOpen   the total minimum amount of chips to put into the pot if the answer action is
*                              {@link BettingAnswer#ACTION_OPEN}.
* @param playersCurrentBet     the amount of chips the player has already put into the pot (dure to the forced bet).
* @param playersRemainingChips the number of chips the player has not yet put into the pot.
* @return                      An answer to the open query. The answer action must be one of
*                              {@link BettingAnswer#ACTION_OPEN}, {@link BettingAnswer#ACTION_ALLIN} or
*                              {@link BettingAnswer#ACTION_CHECK }. If the action is open, the answers
*                              amount of chips in the answer must be between <code>minimumPotAfterOpen</code>
*                              and the players total amount of chips (the amount of chips already put into
*                              pot plus the remaining amount of chips).
'''
def queryOpenAction(_hand,_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose an opening action.")
    # Random Open Action
    eva = Evaluation.evaluate_hand(_hand)
    print('Open',eva,' ', _hand)
    chance = random.random()
    if  eva == 'High':
        if (_playersRemainingChips > _minimumPotAfterOpen + 25):
            return ClientBase.BettingAnswer.ACTION_OPEN, _minimumPotAfterOpen + 25
        else:
            return ClientBase.BettingAnswer.ACTION_ALLIN
    elif eva == 'Very High':
        return ClientBase.BettingAnswer.ACTION_ALLIN
    elif eva == 'Low':
        if chance < 0.15:
            return ClientBase.BettingAnswer.ACTION_CHECK
        else:
            return ClientBase.BettingAnswer.ACTION_OPEN, int(_playersRemainingChips/16) + _minimumPotAfterOpen
    elif eva == 'Very Low':
        if chance < 0.3:
            return ClientBase.BettingAnswer.ACTION_CHECK
        else:
            return ClientBase.BettingAnswer.ACTION_OPEN, _minimumPotAfterOpen

'''
* Modify queryCallRaiseAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what call/raise
* action to choose.
* @param maximumBet                the maximum number of chips one player has already put into the pot.
* @param minimumAmountToRaiseTo    the minimum amount of chips to bet if the returned answer is {@link BettingAnswer#ACTION_RAISE}.
* @param playersCurrentBet         the number of chips the player has already put into the pot.
* @param playersRemainingChips     the number of chips the player has not yet put into the pot.
* @return                          An answer to the call or raise query. The answer action must be one of
*                                  {@link BettingAnswer#ACTION_FOLD}, {@link BettingAnswer#ACTION_CALL},
*                                  {@link BettingAnswer#ACTION_RAISE} or {@link BettingAnswer#ACTION_ALLIN }.
*                                  If the players number of remaining chips is less than the maximum bet and
*                                  the players current bet, the call action is not available. If the players
*                                  number of remaining chips plus the players current bet is less than the minimum
*                                  amount of chips to raise to, the raise action is not available. If the action
*                                  is raise, the answers amount of chips is the total amount of chips the player
*                                  puts into the pot and must be between <code>minimumAmountToRaiseTo</code> and
*                                  <code>playersCurrentBet+playersRemainingChips</code>.
'''
def queryCallRaiseAction(_hand,_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose a call/raise action.")
    # Random Open Action
    ev = Evaluation.evaluate_hand(_hand)
    print('CallRaise ',ev,' ', _hand)
    if ev == 'Very Low':
        chance = random.random()
        if chance < 0.2:
            return ClientBase.BettingAnswer.ACTION_FOLD
        else:
            return ClientBase.BettingAnswer.ACTION_CALL
    elif ev == 'Low':
        chance = random.random()
        if chance < 0.4:
            return ClientBase.BettingAnswer.ACTION_CALL
        else:
            if _minimumAmountToRaiseTo + int(_playersRemainingChips/16) > _playersRemainingChips:
                return ClientBase.BettingAnswer.ACTION_RAISE, _minimumAmountToRaiseTo + int(_playersRemainingChips/16)
            else:
                return ClientBase.BettingAnswer.ACTION_RAISE, _minimumAmountToRaiseTo
    elif ev == 'High':
        chance = random.random()
        if chance < 0.5:
            if (_playersRemainingChips > _minimumAmountToRaiseTo + 50):
                return ClientBase.BettingAnswer.ACTION_RAISE, _minimumAmountToRaiseTo + 50
            else:
                return ClientBase.BettingAnswer.ACTION_ALLIN
        else:
            return ClientBase.BettingAnswer.ACTION_RAISE, _minimumAmountToRaiseTo + int(_playersRemainingChips/8)
    elif ev == 'Very High':
         return ClientBase.BettingAnswer.ACTION_ALLIN


'''
* Modify queryCardsToThrow() and add your strategy to throw cards
* Called during the draw phase of the game when the player is offered to throw away some
* (possibly all) of the cards on hand in exchange for new.
* @return  An array of the cards on hand that should be thrown away in exchange for new,
*          or <code>null</code> or an empty array to keep all cards.
* @see     #infoCardsInHand(ca.ualberta.cs.poker.Hand)
'''
def queryCardsToThrow(_hand):
    print("Requested information about what cards to throw")
    print(_hand)
    ev = Evaluation.identify_hand(_hand)
    print('Throwing ', ev)
    # l = [0,1,2,3,4]
    # if ev == 1: #Keep highest card and discard the other 4
    #     index = Evaluation.ranks(_hand)
    #     l.pop(index)
    #     return _hand[l[0]] + _hand[l[1]] + _hand[l[2]] + _hand[l[3]]
    if ev == 2 or 3 or 4 or 8:
        index = Evaluation.find_non_grouped_cards(_hand)
        selected_cards = [_hand[i] for i in index]
        selected_cards_string = " ".join(selected_cards)
        print(selected_cards_string)
        return selected_cards_string
    else:
        ''

# InfoFunction:

'''
* Called when a new round begins.
* @param round the round number (increased for each new round).
'''
def infoNewRound(_round):
    #_nrTimeRaised = 0
    print('Starting Round: ' + _round )

'''
* Called when the poker server informs that the game is completed.
'''
def infoGameOver():
    print('The game is over.')

'''
* Called when the server informs the players how many chips a player has.
* @param playerName    the name of a player.
* @param chips         the amount of chips the player has.
'''
def infoPlayerChips(_playerName, _chips):
    print('The player ' + _playerName + ' has ' + _chips + 'chips')

'''
* Called when the ante has changed.
* @param ante  the new value of the ante.
'''
def infoAnteChanged(_ante):
    print('The ante is: ' + _ante)

'''
* Called when a player had to do a forced bet (putting the ante in the pot).
* @param playerName    the name of the player forced to do the bet.
* @param forcedBet     the number of chips forced to bet.
'''
def infoForcedBet(_playerName, _forcedBet):
    print("Player "+ _playerName +" made a forced bet of "+ _forcedBet + " chips.")


'''
* Called when a player opens a betting round.
* @param playerName        the name of the player that opens.
* @param openBet           the amount of chips the player has put into the pot.
'''
def infoPlayerOpen(_playerName, _openBet):
    print("Player "+ _playerName + " opened, has put "+ _openBet +" chips into the pot.")

'''
* Called when a player checks.
* @param playerName        the name of the player that checks.
'''
def infoPlayerCheck(_playerName):
    print("Player "+ _playerName +" checked.")

'''
* Called when a player raises.
* @param playerName        the name of the player that raises.
* @param amountRaisedTo    the amount of chips the player raised to.
'''
def infoPlayerRise(_playerName, _amountRaisedTo):
    print("Player "+_playerName +" raised to "+ _amountRaisedTo+ " chips.")

'''
* Called when a player calls.
* @param playerName        the name of the player that calls.
'''
def infoPlayerCall(_playerName):
    print("Player "+_playerName +" called.")

'''
* Called when a player folds.
* @param playerName        the name of the player that folds.
'''
def infoPlayerFold(_playerName):
    print("Player "+ _playerName +" folded.")

'''
* Called when a player goes all-in.
* @param playerName        the name of the player that goes all-in.
* @param allInChipCount    the amount of chips the player has in the pot and goes all-in with.
'''
def infoPlayerAllIn(_playerName, _allInChipCount):
    print("Player "+_playerName +" goes all-in with a pot of "+_allInChipCount+" chips.")

'''
* Called when a player has exchanged (thrown away and drawn new) cards.
* @param playerName        the name of the player that has exchanged cards.
* @param cardCount         the number of cards exchanged.
'''
def infoPlayerDraw(_playerName, _cardCount):
    print("Player "+ _playerName + " exchanged "+ _cardCount +" cards.")

'''
* Called during the showdown when a player shows his hand.
* @param playerName        the name of the player whose hand is shown.
* @param hand              the players hand.
'''
def infoPlayerHand(_playerName, _hand):
    print("Player "+ _playerName +" hand " + str(_hand))

'''
* Called during the showdown when a players undisputed win is reported.
* @param playerName    the name of the player whose undisputed win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundUndisputedWin(_playerName, _winAmount):
    print("Player "+ _playerName +" won "+ _winAmount +" chips undisputed.")

'''
* Called during the showdown when a players win is reported. If a player does not win anything,
* this method is not called.
* @param playerName    the name of the player whose win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundResult(_playerName, _winAmount):
    print("Player "+ _playerName +" won " + _winAmount + " chips.")

