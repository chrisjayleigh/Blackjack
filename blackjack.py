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
        while len(tempdeck) != 0:
            pulled = random.choice(tempdeck)
            self.push(pulled)
            tempdeck.remove(pulled)
        print(self.name + " has been shuffled. \n")

class Hand(Stack):
    
    def __init__(self, name, limit=1000):
        super().__init__(name, limit=1000)
        self.total = 0
        self.soft = False    
        self.facedown = None
        self.wallet = 2000
        self.currentbet = None
        self.blackjack = False
    
    def bet(self, amount):
        self.currentbet = amount
        self.wallet -= self.currentbet
        print(
            self.name
            + " bets $"
            + str(self.currentbet)
            + ". \n"
        )

    def deal(self, pool):
        pulled = pool.pop()
        self.push(pulled)
        print(
            self.name 
            + " has been dealt the " 
            + list(pulled.values())[0] 
            + " of " 
            + list(pulled.keys())[0]
            + ". \n")
        if list(pulled.values())[0] is "A":
            if self.name is not "Dealer":
                if self.total < 11:
                    while True:                    
                        acechoice = input("1 or 11?")
                        try:
                            if int(acechoice) == 1 or int(acechoice) == 11:
                                print(
                                    self.name
                                    + " has chosen "
                                    + acechoice
                                    + " for the ace. \n")
                                self.total += int(acechoice)
                                if int(acechoice) == 11:
                                    self.soft = True
                                break
                            else:
                                print(
                                    "Invalid selection. Try again! \n")
                        except ValueError:
                            print(
                                "Invalid selection. Try again! \n"
                            )

                else:
                    print(
                        self.name
                        + " must take 1 for the ace. \n")
                    self.total += 1
            else:
                if self.total < 11:
                    self.total += values["A"][1]
                    self.soft == True
                else:
                    self.total += values["A"][0]
        else:
            self.total += values[list(pulled.values())[0]]
    
    def face_down(self, pool):
        if self.name == "Dealer":
            self.facedown = pool.pop()
            self.push("Face Down Card")
            print(
                self.name
                + " has been dealt a face down card. \n"
            )
    def flip_facedown(self):
        if self.name == "Dealer":
            self.pop()
            flipped = self.facedown
            self.push(flipped)
            print(
                self.name 
                + " has flipped over the " 
                + list(flipped.values())[0] 
                + " of " 
                + list(flipped.keys())[0]
                + ". \n")
            if list(flipped.values())[0] is "A":
                if self.total < 11:
                    self.total += values["A"][1]
                    self.soft == True
                else:
                    self.total += values["A"][0]
            else:
                self.total += values[list(flipped.values())[0]]    

    def hit(self, pool):
        if self.name == "Player":
            print(
                self.name
                + " chooses to hit. \n"
            )
            self.deal(pool)
    
    def has_blackjack(self):
        if self.total == 21 and self.soft is True:
            print(
                self.name
                + " has Blackjack! \n"
            )
            return True
        else:
            return False


deck = Deck("Deck", 52)
player = Hand("Player")
dealer = Hand("Dealer")

def play_game():
    print(
        "Welcome to Blackjack! \nPlayer starts with $2000."
        + "\nThe minimum bet is $10 and the maximum is $1000.\n"

    )
    betting_phase()

def betting_phase():    
    
    while True:
        betamount = input("How much would you like to bet?").strip("$")
        try:
            if int(betamount) >= 10 and int(betamount) <= 1000:
                player.bet(int(betamount))
                break
            else:
                print(
                    "Bet must be between $10 and $1000. Please try again! \n"
                )
        except ValueError:
            print("That is not a valid input. \n")

    gameplay()

def gameplay():
    
    deck.shuffle()
    #deck.pop()
    #deck.pop()
    #deck.pop()
    #deck.push({"Hearts" : "K"})
    #deck.push({"Clubs" : "2"})
    #deck.push({"Diamonds" : "A"})
    player.deal(deck)
    dealer.deal(deck)
    player.deal(deck)
    dealer.face_down(deck)
    if player.has_blackjack() is True:
        return dealer_phase()
    if (values[list(player.top.data.values())[0]] 
        == values[list(player.top.link.data.values())[0]]):
        while True:
            splitdecision = input(
                "Would you like to split? Y/N \n"
                )
            try:
                if splitdecision != "Y" and splitdecision != "N":
                    print(
                        "Invalid input. Please try again!"
                    )
                elif splitdecision == "N":
                    print(
                        "Player chooses not to split hand. \n"
                    )
                    break
                else:
                    print(
                        "Player chooses to split hand. \n"
                    )
                    playersplit = Hand("Player")
                    splitcard = player.pop()
                    playersplit.push(splitcard)
                    print(
                        "Player moves the "
                        + list(splitcard.values())[0]
                        + " of "
                        + list(splitcard.keys())[0]
                        + " to a new hand. \n"
                    )
                    return split_play()
            except ValueError:
                print(
                    "Invalid input. Please try again!"
                    )
                    

    else:
        while True:
            input(
                "What would you like to do? \n"
                + "H to Hit. S to stand. D to double."
                )

def split_play():
    print("Split play placeholder.")

def dealer_phase():
    print("Dealer phase placeholder.")
    


    
play_game()
