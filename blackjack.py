#!python3.6
#coding: utf8

from random import sample
from time import sleep

# Possible values for value: 2,3,4,5,6,7,8,9,T,J,Q,K,A 
# Possible values for suit: "C" = clubs, "D" = diamonds, "H" = hearts, "S" = spades
class Card:
    def __init__(self,value,suit):
        if value == 'T':
            self.value = "10"
        else:
            self.value = str(value)
        suit_dict = {'C': 1, 'D': 2, 'H': 3, 'S': 4}
        self.suit = '♣♦♥♠'[suit_dict[str(suit)]-1] # 1,2,3,4 = ♣♦♥♠

    def card_front(self):
        return[
                '┌───────┐',
                f'| {self.value:<2}    |', 
                '|       |',
                f'|   {self.suit}   |',
                '|       |',
                f'|    {self.value:>2} |',
                '└───────┘'
                ]
    def card_back(self):
        """creates back of card as a list of strings, used mainly for dealer"""
        return[
                '┌───────┐',
                '│░░░░░░░│', 
                '│░░░░░░░│',
                '│░░░░░░░│',
                '│░░░░░░░│',
                '│░░░░░░░│',
                '└───────┘'
                ]
    def get_value(self):
        """Returns the card's numerical value"""
        if self.value in ['T', 'J', 'Q', 'K']:
            card_value = 10
        elif self.value == "A":
            card_value = [1,11]
        else:
            card_value = int(self.value)
        return card_value

            
def create_deck():
    """ Generates a full deck of 52 cards using the Card class. The deck is
    returned as a list of Card objects, and is shuffled."""
    suits = ["C", "D", "H", "S"]
    values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
    deck = []
    for suit in suits:
        for value in values:
            deck.append(Card(value,suit))
    deck = sample(deck, 52) # shuffles the deck we just created
    return deck

def shuffle_deck(deck):
    """ Takes in a list of card objects, shuffles them using sampling without 
    replacement, and returns a new list of card objects in random order"""
    return sample(deck, len(deck))

def check_hand_value(hand):
    """Checks the numerical value of the cards in the given hand. A hand is a
    list of card objects"""
    hand_value = 0
    num_aces = 0
    # Sum up all non-Ace card values first
    for card in hand:
        card_value = card.get_value()
        if type(card_value) == list: # Only Ace cards return a list for their value
            card_value = 0
            num_aces += 1
        hand_value += card_value
    # Now check if the value of an Ace should be 1 or 11 in the given hand
    if num_aces == 0:
        return hand_value
    elif (hand_value + 11 + 1*(num_aces-1)) > 21:
        hand_value += num_aces*1
        return hand_value
    else:
        hand_value += 11 + 1*(num_aces-1)
        return hand_value
    
def start_of_game_deal(deck):
    """Used at the start of a game, deals the player and the dealer two 
    cards each"""
    dealer_hand = []
    player_hand = []
    for i in range(2):
        player_hand.append(deck.pop())
        dealer_hand.append(deck.pop())
    return player_hand, dealer_hand

def show_hand_unhidden_cards(hand):
    player_hand_graphics = []
    for card in hand:
        player_hand_graphics.append(card.card_front())
    for i in range(7):
        card_str = ""
        for j in range(len(player_hand_graphics)):
            card_str += player_hand_graphics[j][i] + " "
        print(card_str)
        
def show_hand_hidden_cards(hand):
    dealer_hand_graphics = [hand[0].card_front()]
    for i in range(1, len(hand)):
        dealer_hand_graphics.append(hand[i].card_back())
    for i in range(7):
        card_str = ""
        for j in range(len(dealer_hand_graphics)):
            card_str += dealer_hand_graphics[j][i] + " "
        print(card_str)

def dealer_turn(deck, hand):
    dealer_stands_on = 17
    print("Now it's the dealer's turn! The dealer stands on %s." % dealer_stands_on )
    print("Dealer's hand:")
    show_hand_unhidden_cards(hand)
    while check_hand_value(hand) < dealer_stands_on:
        print("The dealer draws a card.")
        hit(deck,hand)
        show_hand_unhidden_cards(hand)
        sleep(2.5)
    if check_hand_value(hand) > 21:
        print("The dealer busts!")
        return 0
    else:
        print("The dealer is finished drawing cards.")
        print("Dealer's final hand:")
        show_hand_unhidden_cards(hand)
        sleep(2.5)
        return check_hand_value(hand)

def hit(deck, hand):
    """Allows a player to hit and draw one more card"""
    hand.append(deck.pop())
    return hand

## define the main game loop function
def game_loop():
    player_chips = 500
    print("Welcome to Python Blackjack! You start with %s chips." % (player_chips))
    print("The dealer's hand is shown first, followed by your hand.")
    while player_chips > 0:
        print("New hand!")
        print("You currently have %s chips." % player_chips)
        bet = int(input("What is your initial bet? "))
        while bet > player_chips or bet < 0:
            bet = int(input("That was an invalid bet. Make sure you aren't betting more than you have! Please enter a bet: "))
        deck = create_deck()
        player_hand, dealer_hand = start_of_game_deal(deck)
        print("Dealer's hand:")
        show_hand_hidden_cards(dealer_hand)
        print("Player's hand:")
        show_hand_unhidden_cards(player_hand)
        player_answer = "N/A"
        if check_hand_value(player_hand) == 21:
            print("You had a natural 21! Let's see what the dealer had:")
            show_hand_unhidden_cards(dealer_hand)
            sleep(2.5)
            if check_hand_value(dealer_hand) == 21:
                print("The dealer also had 21, so you tie. End of hand.")
            else:
                print("You win! Since you had a natural 21, you get your 1.5 times your bet back. Nice!")
                player_chips += int(bet*1.5)
        else: 
            player_turn = True
            while player_turn:
                print("The current value of the cards in your hand is %s. What would you like to do?"% (check_hand_value(player_hand)))
                player_answer = input("Type hit, stand, double down. Enter something else to quit the game: " )
                if player_answer == "hit":
                    player_hand = hit(deck, player_hand)
                    print("Dealer's hand:")
                    show_hand_hidden_cards(dealer_hand)
                    print("Player's hand:")
                    show_hand_unhidden_cards(player_hand)
                    if check_hand_value(player_hand) > 21:
                        player_turn = False
                elif player_answer == "double down":
                    hit(deck, player_hand)
                    print("Dealer's hand:")
                    show_hand_hidden_cards(dealer_hand)
                    print("Player's hand:")
                    show_hand_unhidden_cards(player_hand)
                    player_turn = False
                elif player_answer == "stand":
                    player_turn = False
                else:
                    print("GAME OVER")
                    print("You finished with %s chips." % player_chips)
                    player_turn = False
                    return None
            player_final_value = check_hand_value(player_hand)
            if player_final_value > 21:
                print("Dealer's final hand:")
                show_hand_unhidden_cards(dealer_hand)
                print("Player's final hand:")
                show_hand_unhidden_cards(player_hand)
                if player_answer == "double down":
                    bet = 2*bet
                    print("Oh no! You drew too many cards and busted. You lose this hand and %s chips." % bet)
                    player_chips -= bet
                else:
                    print("Oh no! You drew too many cards and busted. You lose this hand and %s chips." % bet)
                    player_chips -= bet
            else:
                dealer_final_value = dealer_turn(deck, dealer_hand)
                print("Player's final hand:")
                show_hand_unhidden_cards(player_hand)
                if dealer_final_value > 21:
                    print("The dealer busted. You win this hand! You received %s chips." % bet)
                    player_chips += bet
                else:
                   #print("Both the player and the dealer are finished drawing. Let's see who won!")
                   if player_final_value > dealer_final_value:
                       if player_answer == "double down":
                           bet = bet*2
                           print("You won this hand! Since you doubled down, you received %s chips." % bet)
                           player_chips += bet
                       else:
                           print("You won this hand! You received %s chips." % bet)
                           player_chips += int(bet)
                   elif player_final_value == dealer_final_value:
                       print("You tied with the dealer. You don't gain or lose any chips.")
                   else:
                       if player_answer == "double down":
                           bet = bet*2
                           print("The dealer had the better hand, you lose this hand and %s chips." % bet)
                           player_chips -= bet
                       else:
                           print("The dealer had the better hand, you lose this hand and %s chips." % bet)
                           player_chips -= bet
        if player_chips <= 0:                   
            print("You ran out of chips! Game over.")
        sleep(2.5)           
game_loop()
