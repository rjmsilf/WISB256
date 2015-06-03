import random

class Card(object):

    def __init__(self,suit=0,rank=2):
        self.suit=suit
        self.rank=rank

    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = [None,'Ace', '2', '3', '4', '5', '6', '7','8', '9', '10', 'Jack', 'Queen', 'King']

    def __str__(self):
        return '%s of %s' %(Card.rank_names[self.rank],Card.suit_names[self.suit])


    #hier volgt een lijst voor als we gebruiken:
    # <   lt
    # <=  le
    # ==  eq
    # !=  ne
    # >   gt
    # >=  ge
    
    def __lt__(self,other):
        t1=self.suit,self.rank
        t2=other.suit,other.rank
        return t1<t2
    def __le__(self,other):
        t1=self.suit,self.rank
        t2=other.suit,other.rank
        return t1<=t2
    def __eq__(self,other):
        t1=self.suit,self.rank
        t2=other.suit,other.rank
        return t1 == t2
    def __ne__(self,other):
        t1=self.suit,self.rank
        t2=other.suit,other.rank
        return t1!=t2
    def __gt__(self,other):
        t1=self.suit,self.rank
        t2=other.suit,other.rank
        return t1>t2
    def __ge__(self,other):
        t1=self.suit,self.rank
        t2=other.suit,other.rank
        return t1>=t2

class Deck(object):

    def __init__(self):
        self.cards=[]
        for i in range(4):
            for j in range(1,14):
                card=Card(i,j)
                self.cards.append(card)

    def __str__(self):
        res=[]
        for i in self.cards:
            res.append(str(i))
        return '\n'.join(res)

    def pop_card(self,i=-1): #haalt standaard de laatste uit de self.cards lijst weg
        return self.cards.pop(i)

    def remove_card(self,card):
        self.cards.remove(card)

    def add_card(self,card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        self.cards.sort()

    def move_cards(self, hand, num):
        for i in range(num):
            hand.add_card(self.pop_card())

    def deal_hands(self, ahands, acards):
        players1=[]
        players=[]
        for j in range(ahands):
            players1.append('player'+str(j+1))
        for i in players1:
            i=Hand(str(i))
            self.move_cards(i,acards)
            players.append(i)
        return players

def cheating(spelers,kaarten):
    deck=Deck()
    deck.shuffle()
    delen=deck.deal_hands(spelers,kaarten)
    for i in range(spelers):
        print('\n'+delen[i].label+':')
        print(delen[i])
    print('\nin deck:')
    print(deck)
    print('\ncheater!!\n')


class Hand(Deck):

    def __init__(self, label=' '):
        self.cards=[]    #geef zelfde naam als bij Deck voor overwriten!!
        self.label=label

if __name__ == '__main__': #wordt alleen uitgevoerd als dit bestand expliciet wordt geopend
    print('iets')          #NIET als deze wordt geïmporteerd!
