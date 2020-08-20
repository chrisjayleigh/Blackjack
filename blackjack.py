from stack import Stack
import random
faces = [
    'Hearts', 
    'Diamonds', 
    'Clubs', 
    'Spades']
values = {
    "K" : 10, 
    "Q" : 10, 
    "J" : 10,
    "10" : 10,
    "9" : 9,
    "8" : 8,
    "7" : 7,
    "6" : 6,
    "5" : 5,
    "4" : 4,
    "3" : 3,
    "2" : 2,
    "A" : [1, 11]}

unshuffled = []
for face in faces:
    for value in list(values.keys()):
        unshuffled.append({face : value})

class Deck(Stack):
    
    def shuffle(self):
        while not self.is_empty():
            self.pop()
        tempdeck = [card for card in unshuffled]
        for num in range(len(tempdeck)):
            pulled = random.choice(tempdeck)
            self.push(pulled)
            tempdeck.remove(pulled)
        print(self.name + " has been shuffled.")

class Hand(Stack):
    def __init__(self, name, limit=1000):
        super().__init__(name, limit=1000)
        self.total = 0    
    def deal(self, pool):
        pulled = pool.pop()
        self.push(pulled)
        print(
            self.name 
            + " has been dealt the " 
            + list(pulled.values())[0] 
            + " of " 
            + list(pulled.keys())[0]
            + ".")
        if list(pulled.values())[0] is "A":
            if self.name is not "Dealer":
                if self.total < 11:
                    while True:                    
                        acechoice = input("1 or 11?")
                        if acechoice == str(1) or acechoice == str(11):
                            print(
                                self.name
                                + " has chosen "
                                + acechoice
                                + " for the ace.")
                            self.total += int(acechoice)
                            break
                        else:
                            print(
                                "Invalid selection. Try again!")
                else:
                    print(
                        self.name
                        + " must take 1 for the ace.")
                    self.total += 1
            else:
                if self.total < 11:
                    self.total += values["A"][1]
                else:
                    self.total += values["A"][0]


deck = Deck("Deck", 52)
deck.shuffle()
deck.pop()
deck.push({"Hearts":"A"})
player = Hand("Player")
dealer = Hand("Dealer")
player.total += 11
player.deal(deck)