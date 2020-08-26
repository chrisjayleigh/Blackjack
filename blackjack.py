from stack import Stack
from linkedlist import LinkedList
import random

faces = [
    'Hearts', 
    'Diamonds', 
    'Clubs', 
    'Spades'
]

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
    "A" : [1, 11]
}

chips = {
    "1" : 1,
    "5" : 5,
    "25" : 25,
    "100" : 100
}


#Constructs ordered list of cards for each value in each face.
unshuffled = []
for face in faces:
    for value in list(values.keys()):
        unshuffled.append({face : value})

class Deck(Stack):
    
    #Copies unshuffled to tempdeck, randomly assigns a card from tempdeck to pulled.
    #Pushes pulled to Deck, removes pulled from tempdeck.
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
        self.took_split = False
        self.took_double = False
        self.blackjack = False
        self.bust = False
    
    
    #Assigns card popped from Deck to pulled, checks for ace and possibility of soft hand. 
    #Pushes that card to player or dealer. Adds corresponding value to player or dealer total.
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
    
        if list(pulled.values())[0] == "A":
            if self.total < 11:
                self.total += values["A"][1]
                self.soft = True

            else:
                self.total += values["A"][0]

        else:
            self.total += values[list(pulled.values())[0]]
    
    #Pops a card from deck and stores it in an instance variable.
    #Pushes a face down card to the dealer.
    def face_down(self, pool):
    
        self.facedown = pool.pop()
        self.push("Face Down Card")
        print(
            self.name
            + " has been dealt a face down card. \n"
        )
    
    #Pops face down card from dealer, assigns instance variable .facedown to method variable flipped.
    #Pushes flipped to dealer, checks for ace and possibility of soft hand, adds corresponding value to dealer total.
    def flip_facedown(self):
    
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
    
        if list(flipped.values())[0] == "A":
            if self.total < 11:
                self.total += values["A"][1]
                self.soft = True
    
            else:
                self.total += values["A"][0]
    
        else:
            self.total += values[list(flipped.values())[0]]    

    #Calls the instance method .deal with a print indicating specific hit action.
    def hit(self, pool):

            print(
                "Player chooses to hit. \n"
            )
            self.deal(pool)
    
    #Checks for total of 21 on a soft hand with a size of 2. Returns bool value.
    def has_blackjack(self):
        
        if self.total == 21 and self.soft is True and self.size == 2:
            self.blackjack = True
            print(
                self.name
                + " has Blackjack. \n"
            )
            return True
        
        else:
            return False


class Chips:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.currentbet = 0
        self.ones = Stack("Ones")
        self.fives = Stack("Fives")
        self.twentyfives = Stack("Twenty Fives")
        self.hundreds = Stack("Hundreds")
        self.betstack = Stack("Current Bet")
        self.betphase = False
        if self.name == "Dealer Chips":
            for i in range(900):
                self.ones.push(1)
            for i in range(900):
                self.fives.push(5)
            for i in range(900):
                self.twentyfives.push(25)
            for i in range(900):
                self.hundreds.push(100)

        if self.name == "Player Chips":
            for i in range(10):
                self.hundreds.push(100)
            for i in range(20):
                self.twentyfives.push(25)
            for i in range(80):
                self.fives.push(5)
            for i in range(100):
                self.ones.push(1)

    def bet(self, value):
        if self.betphase == True:
            self.currentbet += value
        else:
            self.currentbet = value
        counter = value
        while counter >= 100 and self.hundreds.is_empty() is False:
            self.betstack.push(self.hundreds.pop())
            counter -= 100
        while counter >= 25 and self.twentyfives.is_empty() is False:
            self.betstack.push(self.twentyfives.pop())
            counter -= 25
        while counter >= 5 and self.fives.is_empty() is False:
            self.betstack.push(self.fives.pop())
            counter -= 5
        while counter >= 1 and self.ones.is_empty() is False:
            self.betstack.push(self.ones.pop())
            counter -= 1
        
        if self.name == "Player Chips":
            print(
                self.owner
                + " has bet $"
                + str(self.currentbet)
                + ". \n"
            
            )
    
    def get_total(self):
        totalcount = 0
        totalcount += (
            (self.ones.size * 1)
            + (self.fives.size) * 5
            + (self.twentyfives.size * 25)
            + (self.hundreds.size * 100)
        )
        return str(totalcount)
    
    def return_bet(self):
        counter = self.currentbet
        while counter > 0 and self.betstack.is_empty() is False:
            
            if self.betstack.top.data == 1:
                self.ones.push(self.betstack.pop())
                counter -= 1
                continue
            if self.betstack.top.data == 5:
                self.fives.push(self.betstack.pop())
                counter -= 5
                continue
            if self.betstack.top.data == 25:
                self.twentyfives.push(self.betstack.pop())
                counter -= 25
                continue
            if self.betstack.top.data == 100:
                self.hundreds.push(self.betstack.pop())
                counter -= 100
                continue
    
    def payout_bet(self, target):
        counter = self.currentbet
        while counter > 0 and self.betstack.is_empty() is False:
            if self.betstack.top.data == 1:
                target.ones.push(self.betstack.pop())
                counter -= 1
                continue
            if self.betstack.top.data == 5:
                target.fives.push(self.betstack.pop())
                counter -= 5
                continue
            if self.betstack.top.data == 25:
                target.twentyfives.push(self.betstack.pop())
                counter -= 25
                continue
            if self.betstack.top.data == 100:
                target.hundreds.push(self.betstack.pop())
                counter -= 100
                continue
        
            



#Stacks necessary for gameplay.
deck = Deck("Deck", 52)
player = Hand("Player")
playersplit = Hand("Player's second hand")
dealer = Hand("Dealer")
#p1s = Chips("Player Ones")
#p5s = Chips("Player Fives")
#p25s = Chips("Player Twenty Fives")
#p100s = Chips("Player One Hundreds")
#d1s = Chips("Dealer Ones")
#d5s = Chips("Dealer Fives")
#d25s = Chips("Dealer Twenty Fives")
#d100s = Chips("Dealer One HUndreds")

#while d1s.has_space() is True:
#    d1s.push(1)
#while d5s.has_space() is True:
#    d5s.push(5)
#while d25s.has_space() is True:
#    d25s.push(25)
#while d100s.has_space() is True:
#    d100s.push(100)

playerchips = Chips("Player Chips", "Player")
dealerchips = Chips("Dealer Chips", "Dealer")

#Game initialization function. Indicates player wallet amount and bet min/max. Moves to betting phase.
def play_game():

    print(
        "Welcome to Blackjack! \n\nPlayer has $"
        + playerchips.get_total()
        + ". \n"
        + "\nThe minimum bet is $10 and the maximum is $1000.\n"

    )

    betting_phase()

#Prompts player for bet amount. Moves to initial dealing phase.
def betting_phase():    
    
    try:
        while True:
            playerchips.betphase = True
            dealerchips.betphase = True
            chipselect = input(
                "Bet Input (Chip - Command): \n"
                + "One - 1 (Qty: "
                + str(playerchips.ones.size)
                + ") \n"
                + "Five - 5 (Qty: "
                + str(playerchips.fives.size)
                + ") \n"
                + "Twenty Five - 25 (Qty: "
                + str(playerchips.twentyfives.size)
                + ") \n"
                + "One Hundred - 100 (Qty: "
                + str(playerchips.twentyfives.size)
                + ") \n"
                + "Submit - S \n"
                + "Reset - R \n"
                + "Current Bet: "
                + str(playerchips.currentbet)
                + "\n")

            if chipselect == "100":
                playerchips.bet(100)
            
            elif chipselect == "25":
                playerchips.bet(25)
            
            elif chipselect == "5":
                playerchips.bet(5)
            
            elif chipselect == "1":
                playerchips.bet(1)

            elif chipselect == "R":
                while playerchips.betstack.is_empty() is False:
                    playerchips.return_bet()
                while dealerchips.betstack.is_empty() is False:
                    dealerchips.return_bet()

                playerchips.currentbet = 0
                dealerchips.currentbet = 0

                print(
                    "Player bet reset!"
                )
            
            elif chipselect == "S":
                if playerchips.currentbet < 10 or playerchips.currentbet > 1000:
                    print(
                        "Invalid bet. Please try again! \n"
                    )
                    while playerchips.betstack.is_empty() is False:
                        playerchips.return_bet()
                    while dealerchips.betstack.is_empty() is False:
                        dealerchips.return_bet()

                    playerchips.currentbet = 0
                    dealerchips.currentbet = 0
                
                else:
                    playerchips.betphase = False
                    dealerchips.betphase = False
                    print(
                        "Player has chosen to bet $"
                        + str(playerchips.currentbet)
                        + ". \n"
                    )
                    return initial_deal()

            else:
                print(
                    "Invalid input. Please try again!"
                )        
    except ValueError:
        print(
            "Invalid input. Please try again!"
        )


            




    
    #while True:
    #    betamount = input("How much would you like to bet?").strip("$")
    #    try:
    #        if int(betamount) >= 10 and int(betamount) <= 1000:
    #            playerchips.bet(int(betamount))
    #            dealerchips.bet(int(betamount))
    #            break
    #        else:
    #            print(
    #                "Invalid input. Please try again! \n"
    #            )
    #    except ValueError:
    #        print("Invalid input. Please try again! \n")

    initial_deal()


def initial_deal():
    
    #Shuffles the deck, deals one card to player, one to dealer, another to player and then one face down to dealer.
    deck.shuffle()
    
    #DEBUG LINES
    #-----------------------------
    deck.pop()
    deck.pop()
    deck.pop()
    deck.pop()
    deck.pop()
    deck.push({"Spades" : "A"})
    deck.push({"Clubs" : "2"})
    deck.push({"Hearts" : "K"})
    deck.push({"Clubs" : "Q"})
    deck.push({"Diamonds" : "Q"})
    #-----------------------------
    
    player.deal(deck)
    dealer.deal(deck)
    player.deal(deck)
    dealer.face_down(deck)
    
    #Checks for blackjack from player. If true, moves to dealer phase.
    if player.has_blackjack() is True:
        return dealer_phase()
    
    #Checks for splittable hand. Prompts player to choose to split. If accepted, changes instance variable .took_split to True and moves to split play.
    if (values[list(player.top.data.values())[0]] 
        == values[list(player.top.link.data.values())[0]]):
    
        while True:
            splitdecision = input(
                "Would you like to split? Y/N \n"
                )
    
            try:
                if splitdecision.upper() != "Y" and splitdecision.upper() != "N":
                    print(
                        "Invalid input. Please try again! \n"
                    )
                elif splitdecision.upper() == "N":
                    print(
                        "Player chooses not to split hand. \n"
                    )
                    return gameplay()
                elif splitdecision.upper() == "Y":
                    print(
                        "Player chooses to split hand. \n"
                    )
                    player.took_split = True
                    return gameplay()
    
            except ValueError:
                print(
                    "Invalid input. Please try again! \n"
                    )
    
    #Otherwise, moves to regular gameplay.                
    else:
        gameplay() 
        
            

def gameplay():
    
    #Create variable handlist containing player, and split hand.
    #Create variable completecount that is incremented when either player or playersplit stands, busts or doubles down.
    handlist = [player, playersplit]
    completecount = 0
    
    #Sets up game for split hand play by popping one card from player to splitcard variable and pushing to playersplit.
    if player.took_split is True:
        splitcard = player.pop()
        handlist[1].push(splitcard)
        handlist[0].total -= values[list(splitcard.values())[0]]
        handlist[1].total += values[list(splitcard.values())[0]]
        print(
            "Player moves the "
            + list(splitcard.values())[0]
            + " of "
            + list(splitcard.keys())[0]
            + " to a new hand.  \n"
            )
        
        #Removes second bet of same amount from playerchips and dealerchips, deals a card to each player hand and checks each for blackjack.
        playerchips.bet(playerchips.currentbet)
        dealerchips.bet(dealerchips.currentbet)
        
        handlist[0].deal(deck)
        if handlist[0].has_blackjack() is True:
            completecount += 1
            handlist[0] = None
        
        handlist[1].deal(deck)
        if handlist[1].has_blackjack() is True:
            completecount += 1
            handlist[1] = None
    
    #If player.splitplay is False, replaces playersplit in handlist with None and increments completecount by 1.
    else:
        handlist[1] = None
        completecount += 1
    
    #While loop containing for loop with range of 2, checks if index of handlist corresponding to current iteration is None, and if False, prompts player to select an action for corresponding hand.
    while True:
        
        for i in range(2):
            
            if handlist[i] is not None:
                
                #Prompts the player to select from hit, stand, or double down.
                move = input(
                    "What would you like to do? (Hand "
                    + str(i + 1) 
                    + ") Total: "
                    + str(handlist[i].total)
                    + "\n"
                    + "H to Hit. S to stand. D to double. \n"
                ).upper()
                
                try:                
                    #If player selects hit, calls hit function. If 21 is exceeded, checks for soft hand and converts ace to 1 if instance variable .soft is True.
                    if move == "H":
                        handlist[i].hit(deck)
                
                        if handlist[i].total > 21:                
                            if handlist[i].soft is True:
                                handlist[i].total -= 10
                                handlist[i].soft = False
                                print(
                                    "Hand "
                                    + str(i + 1)
                                    + " is no longer a soft hand. \n"
                                )

                            #If hand is not soft and 21 is exceeded, hand busts. Instance variable .bust set to true, hand replaced in handlist with None, completecount incremented by 1.
                            else:
                                print(
                                    "Hand "
                                    + str(i + 1)
                                    + " bust! "
                                    + "\n\n"
                                    + player.name
                                    + " loses $"
                                    + str(playerchips.currentbet)
                                    + ". \n"
                                )
                                                                
                                playerchips.payout_bet(dealerchips)
                                dealerchips.return_bet()
                                completecount += 1
                                handlist[i].bust = True
                                handlist[i] = None

                    #If player chooses to stand, completecount incremented by 1, instance variable .bust set to False, hand replaced in handlist with None.                                
                    if move == "S":
                        print(
                            "Player stands on Hand "
                            + str(i +1)
                            + ". \n"
                        )
                        completecount += 1
                        handlist[i].bust = False
                        handlist[i] = None
                    
                    #If player chooses to double down, instance variable .took_double is set to True, current bet amount removed from playerchips, hand hits and then checks for bust with soft hand functionality.
                    if move == "D":
                        print(
                            "Player doubles down on Hand "
                            + str(i + 1)
                            + ". \n"
                        )
                        handlist[i].took_double = True
                        playerchips.bet(playerchips.currentbet)
                        dealerchips.bet(dealerchips.currentbet)
                        handlist[i].hit(deck)
                        
                        if handlist[i].total > 21:
                            if handlist[i].soft is True:
                                handlist[i].total -= 10
                                handlist[i].soft = False
                                print(
                                    "Hand "
                                    + str(i + 1)
                                    + " is no longer a soft hand. \n"
                                    + "Player stands on Hand "
                                    + str(i + 1)
                                    + ". \n"
                                )
                                
                                completecount += 1
                                handlist[i] = None
                            
                            else:
                                print(
                                    "Hand "
                                    + str(i + 1)
                                    + " bust! \n\n"
                                    + player.name
                                    + " loses $"
                                    + str(playerchips.currentbet * 2)
                                    + ". \n"
                                )
                                                                                       
                                playerchips.payout_bet(dealerchips)
                                playerchips.payout_bet(dealerchips)
                                dealerchips.return_bet()
                                dealerchips.return_bet()
                                completecount += 1
                                handlist[i].bust = True
                                handlist[i] = None
                        
                        #If hand does not bust, auto stand.
                        else:
                            print(
                                "Player stands on Hand "
                                + str(i + 1)
                                + ". \n"
                                )
                            completecount += 1
                            handlist[i] = None

                    
                    if move != "H" and move != "S" and move != "D":
                        print(
                            "Invalid input. Please try again! \n"
                        )
                
                except ValueError:
                    print(
                        "Invalid input. PLease try again! \n"
                    )
        
        #If both hands have completed play, move to dealer phase.
        if completecount == 2:
            return dealer_phase()

def dealer_phase():
    #Checks if either player hand did not bust.
    if player.bust is False or (player.took_split is True and playersplit.bust is False):

        #Flips dealer facedown card and checks for blackjack. If true, moves to scoring phase.
        dealer.flip_facedown()
        if dealer.has_blackjack():
            return score_phase()
        
        #If dealer did not have blackjack, and dealer did not bust, dealer hits until dealer total reaches 17. If 17 is soft, dealer hits.
        if dealer.total <= 21:
            print(
                "Dealer total is "
                + str(dealer.total)
            + ". \n"
            )
        
        if dealer.soft is True:
            while dealer.total <= 17:
                dealer.deal(deck)
        
                if dealer.total > 21:
                    dealer.soft = False
                    dealer.total -= 10
                print(
                    "Dealer total is "
                    + str(dealer.total)
                    + ". \n"
                )
        
        elif dealer.soft is False:
            while dealer.total < 17:
                dealer.deal(deck)
                print(
                    "Dealer total is "
                    + str(dealer.total)
                    + ". \n"
                )
    
        #If dealer busts, checks if player or split hand did not bust, and if they doubled down, and adds appropriate winnings to wallet, prints earnings not including the original bet amounts.
        if dealer.total > 21:
            print(
                "Dealer bust! \n"
            )
            dealer.bust = True
            earnings = 0
            
            if player.bust is False:
                playerchips.return_bet()
                dealerchips.payout_bet(playerchips)
                earnings += playerchips.currentbet
            
                if player.took_double is True:
                    playerchips.return_bet()
                    dealerchips.payout_bet(playerchips)
                    earnings += playerchips.currentbet
            
            if player.took_split is True:
                if playersplit.bust is False:
                    playerchips.return_bet()
                    dealerchips.payout_bet(playerchips)
                    earnings += playerchips.currentbet
            
                    if playersplit.took_double is True:
                        playerchips.return_bet()
                        dealerchips.payout_bet(playerchips)
                        earnings += playerchips.currentbet 
            print(
                "Player wins $"
                + str(earnings)
                + ". \n"
            )
            
        #If dealer did not bust, and at least one player hand did not bust, go to score phase.    
        if dealer.bust is False:
            return score_phase()
    
    #If dealer busted, or if all active player hands busted, go to end prompt.
    return end_prompt()

    

def score_phase():
    earnings = 0
    losses = 0

    #Checks for player blackjack and compares to dealer blackjack. If player wins via blackjack, checks for double down. If double down is true, adds bet amount * 4 to player.wallet and prints bet amount * 2 as earnings.
    #Repeats this process for playersplit blackjack against dealer, and then again for dealer blackjack against both player hands. If player loses to dealer blackjack, prints corresponding amount of losses.
    if player.blackjack is True:
        print(
            "Player has Blackjack. \n"
        )
        if dealer.blackjack is False:
            print(
                "Dealer does not have Blackjack. \n"
            )
            if player.took_double is True:
                print(
                    "Player wins $"
                    + str(playerchips.currentbet * 2)
                    + "! \n"
                )
                playerchips.return_bet()
                playerchips.return_bet()
                dealerchips.payout_bet(playerchips)
                dealerchips.payout_bet(playerchips)
                earnings += (playerchips.currentbet * 2)
            else:
                print(
                    "Player wins $"
                    + str(playerchips.currentbet)
                    + "! \n"
                )
                playerchips.return_bet()
                dealerchips.payout_bet(playerchips)
                earnings += (playerchips.currentbet)
        else:
            print(
                "Player and dealer tied! \n"
                )
            playerchips.return_bet()
            dealerchips.return_bet()
            if player.took_double is True:
                playerchips.return_bet()
                dealerchips.return_bet()

    if player.took_split is True:
        if playersplit.blackjack is True:
            print(
                "Player's second hand has Blackjack. \n"
            )
            if dealer.blackjack is False:
                print(
                    "Dealer does not have Blackjack. \n"
                )
                if playersplit.took_double is True:
                    print(
                        playersplit.name
                        + " wins $"
                        + str(playerchips.currentbet * 2)
                        + "! \n"
                    )
                    playerchips.return_bet()
                    playerchips.return_bet()
                    dealerchips.payout_bet(playerchips)
                    dealerchips.payout_bet(playerchips)
                    earnings += (playerchips.currentbet * 2)
                else:
                    print(
                        playersplit.name
                        + " wins $"
                        + str(playerchips.currentbet)
                        + "! \n"
                        )
                    playerchips.return_bet()
                    dealerchips.payout_bet(playerchips)
                    earnings += (playerchips.currentbet)

            else:
                print(
                    "Player and dealer tied!"
                    )
                playerchips.return_bet()
                dealerchips.return_bet()
                if player.took_double is True:
                    playerchips.return_bet()
                    dealerchips.return_bet()

    if player.blackjack is False and player.bust is False:        

        if dealer.blackjack is True:
            print(
                "Player does not have Blackjack. \n"
            )
            if player.took_double is True:
                print(
                    player.name
                    + " loses $"
                    + str(playerchips.currentbet * 2)
                    + ". \n"
                )
                dealerchips.return_bet()
                dealerchips.return_bet()
                playerchips.payout_bet(dealerchips)
                playerchips.payout_bet(dealerchips)
                losses += (playerchips.currentbet * 2)
            else:
                print(
                    player.name
                    + " loses $"
                    + str(playerchips.currentbet)
                    + ". \n"
                )
                dealerchips.return_bet()
                playerchips.payout_bet(dealerchips)
                losses += playerchips.currentbet
    if player.took_split is True:
        if playersplit.blackjack is False and playersplit.bust is False:
            if dealer.blackjack is True:
                print(
                    "Player's second hand does not have Blackjack. \n"
                )
                if playersplit.took_double is True:
                    print(
                        playersplit.name
                        + " loses $"
                        + str(playerchips.currentbet * 2)
                        + ". \n"
                    )
                    dealerchips.return_bet()
                    dealerchips.return_bet()
                    playerchips.payout_bet(dealerchips)
                    playerchips.payout_bet(dealerchips)
                    losses += (playerchips.currentbet * 2)
                else:
                    print(
                        playersplit.name
                        + " loses $"
                        + str(playerchips.currentbet)
                        + ". \n"
                    )
                    dealerchips.return_bet()
                    playerchips.payout_bet(dealerchips)
                    losses += playerchips.currentbet

    #If player did not bust, and neither player nor dealer have blackjack, compares player total to dealer total. Checks if player took double down in each comparison, and adjusts player wallet and earnings printout accordingly for win or loss, with or without double down.
    #Repeats this process for player split hand if player took split.
    if player.bust is False and player.blackjack is False and dealer.blackjack is False:
        print(
            player.name
            + " total is "
            + str(player.total)
            + ". \n"
        )
        if player.total > dealer.total:
            if player.took_double is True:
                print(
                    "Player wins $"
                    + str(playerchips.currentbet * 2)
                    + "! \n"
                )
                playerchips.return_bet()
                playerchips.return_bet()
                dealerchips.payout_bet(playerchips)
                dealerchips.payout_bet(playerchips)
                earnings += (playerchips.currentbet * 2)
            else:
                print(
                    "Player wins $"
                    + str(playerchips.currentbet)
                    + "! \n"
                )
                playerchips.return_bet()
                dealerchips.payout_bet(playerchips)
                earnings += (playerchips.currentbet)
        
        if player.total == dealer.total:
            print(
                "Player and dealer tied! \n"
            )
            playerchips.return_bet()
            dealerchips.return_bet()
            if player.took_double is True:
                playerchips.return_bet()
                dealerchips.return_bet()

        elif player.total < dealer.total:
            if player.took_double is True:
                print(
                    "Player loses $"
                    + str(playerchips.currentbet * 2)
                    + ". \n"
                )
                dealerchips.return_bet()
                dealerchips.return_bet()
                playerchips.payout_bet(dealerchips)
                playerchips.payout_bet(dealerchips)
                losses += (playerchips.currentbet * 2)
                
            else:
                print(
                    "Player loses $"
                    + str(playerchips.currentbet)
                    + ". \n"
                )
                dealerchips.return_bet()
                playerchips.payout_bet(dealerchips)
                losses += (playerchips.currentbet)
                

    if player.took_split is True:
        if playersplit.bust is False and playersplit.blackjack is False and dealer.blackjack is False:
            print(
                playersplit.name
                + " total is "
                + str(playersplit.total)
                + ". \n"
            )
            if playersplit.total > dealer.total:
                if playersplit.took_double is True:
                    print(
                        playersplit.name
                        + " wins $"
                        + str(playerchips.currentbet * 2)
                        + "! \n"
                    )
                    playerchips.return_bet()
                    playerchips.return_bet()
                    dealerchips.payout_bet(playerchips)
                    dealerchips.payout_bet(playerchips)
                    earnings += (playerchips.currentbet * 2)
                else:
                    print(
                        playersplit.name
                        + " wins $"
                        + str(playerchips.currentbet)
                        + "! \n"
                    )
                    playerchips.return_bet()
                    dealerchips.payout_bet(playerchips)
                    earnings += (playerchips.currentbet)

            
            if playersplit.total == dealer.total:
                print(
                    "Player and dealer tied!"
                )
                playerchips.return_bet()
                dealerchips.return_bet()
                if player.took_double is True:
                    playerchips.return_bet()
                    dealerchips.return_bet()

            elif playersplit.total < dealer.total:
                if playersplit.took_double is True:
                    print(
                        playersplit.name
                        + " loses $"
                        + str(playerchips.currentbet * 2)
                        + ". \n"
                    )
                    dealerchips.return_bet()
                    dealerchips.return_bet()
                    playerchips.payout_bet(dealerchips)
                    playerchips.payout_bet(dealerchips)
                    losses -= (playerchips.currentbet * 2)
                    
                else:
                    print(
                        playersplit.name
                        + " loses $"
                        + str(playerchips.currentbet)
                        + ". \n"
                    )
                    dealerchips.return_bet()
                    playerchips.payout_bet(dealerchips)
                    losses -= (playerchips.currentbet)
                    
    #After completing comparisons, sends player to end prompt phase.
    return end_prompt()

    

#Prompts player to choose whether to play again or not. If player chooses yes, resets all gameplay related instance values for player, playersplit, and dealer except for player wallet, then sends player back to game initialization with new wallet amount.
def end_prompt():
    while True:
        replay = input("Would you like to play again? Y/N")
        try:
            if replay.upper() == "Y":
                player.total = 0
                player.soft = False    
                player.facedown = None
                player.took_split = False
                player.took_double = False     
                player.blackjack = False
                player.bust = False
                player.size = 0
                playersplit.total = 0
                playersplit.soft = False    
                playersplit.facedown = None
                playersplit.took_split = False
                playersplit.took_double = False    
                playersplit.blackjack = False
                playersplit.bust = False
                playersplit.size = 0
                dealer.total = 0
                dealer.soft = False    
                dealer.facedown = None
                dealer.took_split = False
                dealer.took_double = False
                dealer.blackjack = False
                dealer.bust = False
                dealer.size = 0
    
                return play_game()
        
            elif replay.upper() == "N":
                print(
                    "Thanks for playing!"
                )
                return
            else:
                print(
                    "Invalid input. Please try again!"
                )

        except ValueError:
            print(
                "Invalid input. Please try again!"
            )
        

    
    



play_game()
