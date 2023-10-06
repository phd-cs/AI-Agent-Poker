from collections import defaultdict



cardsnum = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "T":10,"J":11, "Q":12, "K":13, "A":14}
Types = {
    'HighCard':      1, #discard 4
    'OnePair':       2, #discard 3
    'TwoPairs':      3, #discard 1
    '3OfAKind':      4, #discard 2
    'Straight':      5,
    'Flush':         6,
    'FullHouse':     7,
    '4OfAKind':      8, #discard 1
    'StraightFlush': 9
}
hand = ['7s','6s' , '6s', '2s', '6s']
handh = ['As', 'Tc', '3s', '7d', '9h']  # high card
hando = ['Ts', 'Tc', '3s', '7d', '9h']  # one pair
handt = ['As', 'Ac', '7s', '7d', '9h']  # two pairs
handth = ['As', 'Ac', '7s', 'Ad', '9h']  # three of a kind
hands = ['As', 'Kc', 'Qs', 'Jd', 'Th']  # straight
handf = ['As', 'Js', '7s', '3s', '6s'] # flush
handfu = ['As', 'Ac', '7s', 'Ad', '7h']  # full house
handfo = ['As', 'Ac', '3s', 'Ad', 'Ah']  # four of a kind
handstr = ['As', 'Ks', 'Qs', 'Js', 'Ts']  # straigh
def find_non_grouped_cards(cards):
    card_counts = {}
    for i, card in enumerate(cards):
        card_value = card[:-1] # remove the last character (suit)
        if card_value in card_counts:
            card_counts[card_value] += 1
        else:
            card_counts[card_value] = 1
    non_grouped_cards = []
    for i, card in enumerate(cards):
        card_value = card[:-1]
        if card_counts[card_value] == 1:
            non_grouped_cards.append(i)
    return non_grouped_cards
index = find_non_grouped_cards(hando)
print(find_non_grouped_cards(hand))
print(find_non_grouped_cards(handh))
print(find_non_grouped_cards(hando))
print(find_non_grouped_cards(handt))
print(find_non_grouped_cards(handth))
print(find_non_grouped_cards(hands))
print(find_non_grouped_cards(handf))
print(find_non_grouped_cards(handfu))
print(find_non_grouped_cards(handfo))
print(find_non_grouped_cards(handstr))

selected_cards = [hand[i] for i in index]
selected_cards_string = "".join(selected_cards)
print('Here',selected_cards_string )


def identify_hand(_hand):
    Ranks = [i[0] for i in _hand]
    value_counts = defaultdict(lambda:0)
    for v in Ranks:
        value_counts[v]+=1
    if sorted(value_counts.values()) == [1,1,1,2]:
        return 2
    elif sorted(value_counts.values()) == [1,2,2]:
        return 3
    elif sorted(value_counts.values()) == [1,1,3]:
        return 4
    elif sorted(value_counts.values()) == [2, 3]:
        return 7
    elif sorted(value_counts.values()) == [1,4]:
        return 8
    else:
        return 1
def identifyFlush(_hand):
    values = [i[1] for i in _hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [5]:
        return 6

def cardTonumber(_hand):
    temp = []
    for i in _hand:
        if(i[0] == "A"):
            temp.append("14")
        elif(i[0]=="K"):
            temp.append("13")
        elif (i[0] == "Q"):
            temp.append("12")
        elif (i[0] == "J"):
            temp.append("11")
        elif (i[0] == "T"):
            temp.append("10")
        else:
            temp.append(i)
    return temp
def get_max_card_index(deck):
    def card_value(card):
        return int(card[:-1]), card[-1]
    return max(enumerate(deck), key=lambda x: card_value(x[1]))[0]


def ranks(_hand):
    highest = 0
    temp = 0
    for i, c in enumerate(_hand):
        if c.startswith('A'):
            highest = i
            break
        elif c.startswith('K') and temp < 13:
            highest = i
            temp = 13
        elif c.startswith('Q') and temp < 12:
            highest = i
            temp = 12
        elif c.startswith('J') and temp < 11:
            highest = i
            temp = 11
        elif c.startswith('T') and temp < 10:
            highest = i
            temp = 10
    if highest == 0:
        return get_max_card_index(hand)
    return highest



def identifyStright(_hand):
    values = [i[0] for i in _hand]
    temp = cardTonumber(_hand)
    value_counts = defaultdict(lambda:0)
    for v in values:
        value_counts[v]+=1
    rank_values = [cardsnum[i] for i in values]
    listsort = sorted(rank_values)
    flag = False
    if set(rank_values) == set([14, 2, 3, 4, 5]):
        return True
    for r in range(4):
        if(int(listsort[r+1]) == int(listsort[r])+1):
            flag = True
        else:
            return False
    return flag
def StraightFlush(_hand):
    if identifyStright(_hand) and identifyFlush(_hand) == 6:
        return 9


def evaluate_hand(_hand):
    if (identify_hand(_hand) == 1):
        return "Very Low"
    if (identify_hand(_hand) == 2):
        return "Low"
    if (identify_hand(_hand) == 3 or identify_hand(_hand) == 4):
        return "High"
    if (identify_hand(_hand) == 5 or identify_hand(_hand) == 6 or identify_hand(_hand) == 7 or identify_hand(_hand) == 8 or identify_hand(_hand) == 9):
        return "Very High"

print('here eva ', evaluate_hand(hando))




