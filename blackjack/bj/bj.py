import random

def str_point(card):
    if card[0] > 10:
        return 10
    elif card[0] == 1:
        return 11
    else:
        return card[0]
    
def count_card(cards):
    point = [str_point(i) for i in cards]
    cnt = point.count(11)
    card_sum = sum(point)
    for _ in range(cnt):
        if card_sum > 21:
            card_sum -= 10
    return card_sum

class Deck:
    def __init__(self):
        self.cards = [
            (i,j)
            for i in range(1,14)
            for j in ["s","h","d","c"]
            ]
        random.shuffle(self.cards)
    def emission(self):
        emission_card = self.cards.pop()
        return emission_card

class Player():
    def __init__(self):
        self.cards = []
    def draw(self, card):
        self.cards.append(card)