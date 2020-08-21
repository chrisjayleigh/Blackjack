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
        self.took_split = False
        self.took_double = False
        self.currentbet = None
        self.double_bet = None
        self.blackjack = False
        self.bust = False
    
    def bet(self, amount):
        self.currentbet = amount
        self.wallet -= self.currentbet
        print(
            self.name
            + " bets $"
            + str(self.currentbet)
            + ". \n"
        )
    
    #def double_bet(self):
        #self.doublebet = self.currentbet *= 2
    #    self.wallet -= self.currentbet
    #    print(
    #        self.name
    #        + " bets another $"
    #        + str(self.currentbet)
    #        + ". \n"
    #    )


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
                    self.total += values["A"][1]
                    self.soft = True
                    #while True:                    
                        #acechoice = input("1 or 11?")
                        #try:
                            #if int(acechoice) == 1 or int(acechoice) == 11:
                                #print(
                                #    self.name
                                #    + " has chosen "
                                #    + acechoice
                                #    + " for the ace. \n")
                                #self.total += int(acechoice)
                                #if int(acechoice) == 11:
                                #    self.soft = True
                                #break
                            #else:
                            #    print(
                            #        "Invalid input. Please try again! \n")
                        #except ValueError:
                        #    print(
                        #        "Invalid input. Please try again! \n"
                        #    )

                else:
                    #print(
                    #    self.name
                    #    + " must take 1 for the ace. \n")
                    self.total += values["A"][0]
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
            print(
                "Player chooses to hit. \n"
            )
            self.deal(pool)
    
    def has_blackjack(self):
        if self.total == 21 and self.soft is True:
            print(
                self.name
                + " has Blackjack. \n"
            )
            return True
        else:
            return False


deck = Deck("Deck", 52)
player = Hand("Player")
playersplit = Hand("Player's second hand")
dealer = Hand("Dealer")

def play_game():
    print(
        "Welcome to Blackjack! \n\nPlayer has $"
        + str(player.wallet)
        + ". \n"
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
                    "Invalid input. Please try again! \n"
                )
        except ValueError:
            print("Invalid input. Please try again! \n")

    initial_deal()

def initial_deal():
    
    deck.shuffle()
    deck.pop()
    deck.pop()
    deck.pop()
    deck.pop()
    deck.pop()
    deck.push({"Spades" : "A"})
    deck.push({"Clubs" : "4"})
    deck.push({"Hearts" : "K"})
    deck.push({"Clubs" : "2"})
    deck.push({"Diamonds" : "Q"})
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
                    

    else:
        gameplay() 
        
            

def gameplay():
    #player.currentbet = player.currentbet
    handlist = [player, playersplit]
    completecount = 0
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
            + " to a new hand with a bet of $"
            + str(player.currentbet)
            + ". \n"
            )
        player.wallet -= player.currentbet
        #player.currentbet += player.currentbet
        handlist[0].deal(deck)
        if handlist[0].has_blackjack() is True:
            completecount += 1
            handlist[0] = None
        handlist[1].deal(deck)
        if handlist[1].has_blackjack() is True:
            completecount += 1
            handlist[1] = None
    else:
        handlist[1] = None
        completecount += 1
    
    while True:
        for i in range(2):
            if handlist[i] != None:
                move = input(
                    "What would you like to do? (Hand "
                    + str(i + 1) 
                    + ") Total: "
                    + str(handlist[i].total)
                    + "\n"
                    + "H to Hit. S to stand. D to double. \n"
                ).upper()
                try:
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
                            else:
                                print(
                                    "Hand "
                                    + str(i + 1)
                                    + " bust! "
                                    + "\n\n"
                                    + player.name
                                    + " loses $"
                                    + str(player.currentbet)
                                    + ". \n"
                                )
                                
                                #player.currentbet -= player.currentbet
                                completecount += 1
                                handlist[i].bust = True
                                handlist[i] = None
                                




                    
                    if move == "S":
                        print(
                            "Player stands on Hand "
                            + str(i +1)
                            + ". \n"
                        )
                        completecount += 1
                        handlist[i].bust = False
                        handlist[i] = None
                    
                    if move == "D":
                        print(
                            "Player doubles down on Hand "
                            + str(i + 1)
                            + ". \n"
                        )
                        player.wallet -= player.currentbet
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
                                    + str(player.currentbet * 2)
                                    + ". \n"
                                )
                                
                                #player.currentbet -= (player.currentbet * 2)
                                completecount += 1
                                handlist[i].bust = True
                                handlist[i] = None
                        
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
        if completecount == 2:
            return dealer_phase()

def dealer_phase():

    if player.bust is False or (player.took_split is True and playersplit.bust is False):


        dealer.flip_facedown()
        if dealer.has_blackjack():
            return score_phase()
        
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
    
        if dealer.total > 21:
            print(
                "Dealer bust! \n"
            )
            dealer.bust = True
            earnings = 0
            if player.bust == False:
                player.wallet += player.currentbet * 2
                earnings += player.currentbet
                if player.took_double == True:
                    player.wallet += player.currentbet * 4
                    earnings += player.currentbet * 2
            if player.took_split == True:
                if playersplit.bust == False:
                    player.wallet += player.currentbet * 2
                    earnings += player.currentbet
                    if playersplit.took_double == True:
                        player.wallet += player.currentbet * 4
                        earnings += player.currentbet * 2
            print(
                "Player wins $"
                + str(earnings)
                + ". \n"
            )
            
        
    if dealer.bust == False:
        return score_phase()
    
    return end_prompt()

        

def score_phase():
    earnings = 0
    losses = 0


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
                    + str(player.currentbet * 2)
                    + "! \n"
                )
                player.wallet += (player.currentbet * 4)
                earnings += (player.currentbet * 2)
            else:
                print(
                    "Player wins $"
                    + str(player.currentbet)
                    + "! \n"
                )
                player.wallet += (player.currentbet * 2)
                earnings += (player.currentbet)
        else:
            print(
                "Player and dealer tied! \n"
                )

    if player.took_split is True:
        if playersplit.blackjack is True:
            print(
                "Player's second hand has Blackjack. \n"
            )
            if dealer.has_blackjack() is False:
                print(
                    "Dealer does not have Blackjack. \n"
                )
                if playersplit.took_double is True:
                    print(
                        playersplit.name
                        + " wins $"
                        + str(player.currentbet * 2)
                        + "! \n"
                    )
                    player.wallet += (player.currentbet * 4)
                    earnings += (player.currentbet * 2)
                else:
                    print(
                        playersplit.name
                        + " wins $"
                        + str(player.currentbet)
                        + "! \n"
                        )
                    player.wallet += player.currentbet * 2
                    earnings += (player.currentbet)

            else:
                print(
                    "Player and dealer tied!"
                    )

    if player.blackjack is False:        
        if dealer.blackjack is True:
            print(
                "Player does not have Blackjack. \n"
            )
            if player.took_double is True:
                print(
                    player.name
                    + " loses $"
                    + str(player.currentbet * 2)
                    + ". \n"
                )
                losses += (player.currentbet * 2)
            else:
                print(
                    player.name
                    + " loses $"
                    + str(player.currentbet)
                    + ". \n"
                )
    if player.took_split is True:
        if playersplit.blackjack is False:
            if dealer.blackjack is True:
                print(
                    "Player's second hand does not have Blackjack. \n"
                )
                if playersplit.took_double is True:
                    print(
                        playersplit.name
                        + " loses $"
                        + str(player.currentbet * 2)
                        + ". \n"
                    )
                    losses += (player.currentbet * 2)
                else:
                    print(
                        playersplit.name
                        + " loses $"
                        + str(player.currentbet)
                        + ". \n"
                    )
                    losses += player.currentbet


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
                    + str(player.currentbet * 2)
                    + "! \n"
                )
                player.wallet += (player.currentbet * 4)
                earnings += (player.currentbet * 2)
            else:
                print(
                    "Player wins $"
                    + str(player.currentbet)
                    + "! \n"
                )
                player.wallet += (player.currentbet * 2)
                earnings += (player.currentbet)
        
        if player.total == dealer.total:
            print(
                "Player and dealer tied! \n"
            )
        
        elif player.total < dealer.total:
            if player.took_double is True:
                print(
                    "Player loses $"
                    + str(player.currentbet * 2)
                    + ". \n"
                )
                losses += (player.currentbet * 2)
                
            else:
                print(
                    "Player loses $"
                    + str(player.currentbet)
                    + ". \n"
                )
                losses += (player.currentbet)
                

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
                        + str(player.currentbet * 2)
                        + "! \n"
                    )
                    player.wallet += (player.currentbet * 4)
                    earnings += (player.currentbet * 2)
                else:
                    print(
                        playersplit.name
                        + " wins $"
                        + str(player.currentbet)
                        + "! \n"
                    )
                    player.wallet += player.currentbet * 2
                    earnings += (player.currentbet)

            
            if playersplit.total == dealer.total:
                print(
                    "Player and dealer tied!"
                )

            elif playersplit.total < dealer.total:
                if playersplit.took_double is True:
                    print(
                        playersplit.name
                        + " loses $"
                        + str(player.currentbet * 2)
                        + ". \n"
                    )
                    losses -= (player.currentbet * 2)
                    
                else:
                    print(
                        playersplit.name
                        + " loses $"
                        + str(player.currentbet)
                        + ". \n"
                    )
                    losses -= (player.currentbet)
                    

    return end_prompt()

    


def end_prompt():
    while True:
        replay = input("Would you like to play again? Y/N")
        try:
            if replay.upper() == "Y":
                player.total = 0
                player.soft = False    
                player.facedown = None
                player.currentbet = None
                player.took_split = False
                player.took_double = False     
                player.blackjack = False
                player.bust = False
                playersplit.total = 0
                playersplit.soft = False    
                playersplit.facedown = None
                playersplit.currentbet = None
                playersplit.took_split = False
                playersplit.took_double = False    
                playersplit.blackjack = False
                playersplit.bust = False
                dealer.total = 0
                dealer.soft = False    
                dealer.facedown = None
                dealer.currentbet = None
                dealer.took_split = False
                dealer.took_double = False
                dealer.blackjack = False
                dealer.bust = False
    
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
