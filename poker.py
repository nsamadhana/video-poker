import VideoPoker
import random

hand_values = ((0,'Bust!'),(1,'Pair!'),(2,'Two pair'),(3,'Three of a kind'),(4,'Straight'),(6,'Flush'),(9,'Full house'),(25,'Four of a kind'),(50,'Straight flush'),(250,'Royal Flush')) #Help from Arnab

def shuffle_return(): #This function shuffles appends into a list a "deck" of shuffled cards and returns five randomly chosen cards (Got help from Oceane)
    suits = 'CDHS'
    rank = '23456789TJQKA'
    cards = []
    for b in suits:
        for a in rank:
            cards.append(a+b)
    random.shuffle(cards)
    return cards

def suit_counter(randomhand): #This function prints the frequency of the occurence of each suit in the users hand as a string (exact same skeleton as rank_counter function)
    suit_list = [0,0,0,0]
    for card in randomhand:
        if card[1] == 'C':
            suit_list[0] += 1
        elif card[1] == 'D':
            suit_list[1] += 1
        elif card[1] == 'H':
            suit_list[2] += 1
        elif card[1] == 'S':
            suit_list[3] += 1
    str_suit_list = ''.join(str(e)for e in suit_list)
    return str_suit_list

def rank_counter(randomhand): #This function prints the frequency of the occurrence of each rank in the users hand as a string
    rank_list = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    for card in randomhand:
        if card[0] == '2':
            rank_list[0] += 1
        elif card[0] == '3':
            rank_list[1] += 1
        elif card[0] == '4':
            rank_list[2] += 1
        elif card[0] == '5':
            rank_list[3] += 1
        elif card[0] == '6':
            rank_list[4] += 1
        elif card [0] == '7':
            rank_list[5] += 1
        elif card[0] == '8':
            rank_list[6] += 1
        elif card[0] == '9':
            rank_list[7] += 1
        elif card[0] == 'T':
            rank_list[8] += 1
        elif card[0] == 'J':
            rank_list[9] += 1
        elif card[0] == 'Q':
            rank_list[10] += 1
        elif card[0] == 'K':
            rank_list[11] += 1
        elif card[0] == 'A':
            rank_list[12] += 1
    str_rank_list =''.join(str(e)for e in rank_list) #Found out how to convert a list of integers to strings by searching online. query:"how to convert list of integers to strings"
    return str_rank_list

def ranker(rank_string,suit_string,pair_counter): #This function determines the type of hand that the user has (Help from Arnab for the return)
    if '0000000011111' in rank_string and '5' in suit_string:
        return 9
    elif '1111100000000' in rank_string and '5' in suit_string or '0111110000000' in rank_string and '5' in suit_string or '0011111000000' in rank_string and '5' in suit_string or '0001111100000' in rank_string and '5' in suit_string or '0000111110000' in rank_string and '5' in suit_string or '0000011111000' in rank_string and '5' in suit_string or '0000001111100' in rank_string and '5' in suit_string or '0000000111110' in rank_string and '5' in suit_string:
        return 8
    elif '4' in rank_string:
        return 7
    elif '3' in rank_string and '2' in rank_string:
        return 6
    elif '5' in suit_string:
        return 5
    elif '1111000000001' in rank_string or '1111100000000' in rank_string or '0111110000000' in rank_string or '0011111000000' in rank_string or '0001111100000' in rank_string or '0000111110000' in rank_string or '0000011111000' in rank_string or '0000001111100' in rank_string or '0000000111110' in rank_string or '0000000011111' in rank_string:
        return 4
    elif '3' in rank_string and '1' in rank_string:
        return 3
    elif pair_counter == 2:
        return 2
    elif rank_string[9]== '2' or rank_string[10] =='2' or rank_string[11] == '2' or rank_string[12] == '2':
        return 1
    else:
       return 0

def pair_counter(rstring): #This function is a counter that is used to indicate a two pair
    x = 0
    for i in range(len(rstring)):
        if rstring[i] == '2':
            x += 1
    return x

def credit_input(): #This function asks for the starting number of credits and also ensures that the number is between 1 and 1000
    credits = int(input('Welcome to video poker! How many credits would you like to start with? (10-1000)''\n'))
    while credits < 10 or credits >1000:
        credits = int(input('Please choose a credit amount between 10 and 1000'))
    return credits

def hold_return(hand,held_card_indexes,deck): #This function holds onto cards and ensures they remain in the same position after new cards are dealt (Help from Jennifer Sawyer)
    for i in range(len(hand)):
        if i not in held_card_indexes:
            hand[i] = deck.pop(0)
    return hand, deck

def removed_deck(deck,removed): #This function removes cards from the original deck when they are taken out
    new_deck = deck[removed:]
    return new_deck

def credit_multiplier(credits_bet,result): #This function multiplies a credit score depending on the credits the user chose to bet
    if credits_bet == 1:
        result = result
    elif credits_bet == 2:
        result = result * 2
    elif credits_bet == 3:
        result = result *3
    elif credits_bet == 4:
        result = result *4
    elif credits_bet == 5:
        if credits_bet == 5 and result == 250: #This if statement is specific to the result of a royal flush and returns 4000 credits
            result = 4000
        else:
            result = result *5
    return result

credits = credit_input()
vp = VideoPoker.VideoPoker()

def playing_poker(): #This is the main program which runs the poker game
    new_credits = credits
    while new_credits > 0: #This while loop will only run when the user has any credits at all to bet with and if not the program quits
        vp.display_credits(new_credits)
        vp.set_status('How many credits would you like to bet?')
        subtract = vp.get_credits_bet()
        while subtract > new_credits:#This while loop makes sure that the will only bet an amount that they can afford
            vp.set_status('Please bet only what you can afford!')
            subtract = vp.get_credits_bet()
        new_credits = new_credits - subtract #This subtracts the amount of credits the user bets from their original amount of credits
        vp.display_credits(new_credits)
        deck = shuffle_return()
        first_five = deck[:5]
        del deck[:5] #This deletes the five cards that were taken from the deck from the original deck to make sure that no duplicates occur
        vp.set_cards(first_five)
        vp.set_status('Click on the cards that you would like to hold')
        held_cards = vp.get_held_cards()
        new_hand,deck = hold_return(first_five,held_cards,deck)
        vp.set_cards(new_hand)
        rstring = rank_counter(new_hand)
        sstring = suit_counter(new_hand)
        pairs = pair_counter(rstring)
        xx=ranker(rstring,sstring,pairs) #After passing the hand after cards have been held and dealt, it is passed through the ranker function which evaluates the type of hand
        x,y = hand_values[xx]
        end_credits = credit_multiplier(subtract,x)
        vp.set_status(y + ' ' + 'You won ' + str(end_credits) + ' credits') #This lets the user know how many credits they have won
        new_credits = end_credits + new_credits
        if new_credits == 0:
            vp.set_status('Sorry, you are broke. Game over!')
        vp.await_continue_button()

playing_poker()
