import random

dealer_score = 0
player_score = 0
player_card = []
dealer_card = []
choice = ""
one = ('1', 'ace')

def card_value(card):
    if card[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif card[0] == 'Ace':
        return 11
    else:
        return int(card[0])

def main(player_score, player_card, dealer_score, dealer_card, deck):
    card_list = []
    card_categories = []

    while dealer_score < 17 or player_score < 21 :
            #initialize and shuffle deck
        if len(deck) < 9: #Shuffle when there are 6 or less cards left - may cause error if more than 8 cards are
            # used at the end of the deck (rare)
            print(f"{len(deck)} cards in deck, shuffling...")
            card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
            cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
            deck = [(card, category) for category in card_categories for card in cards_list]
            random.shuffle(deck)
            #check if first round and deal 2 cards to each player.
        if player_score == 0:
            player_card = [deck.pop(), deck.pop()]
            dealer_card = [deck.pop(), deck.pop()]
            player_score = sum(card_value(card) for card in player_card)
            dealer_score = sum(card_value(card) for card in dealer_card)
            # If 2 aces are dealt convert one to "1"
            if dealer_score == 22:
                dealer_card.pop()
                dealer_card.append(one)
            if player_score == 22:
                player_card.pop()
                player_card.append(one)
        # if not first round, add up cards from last selections
        player_score = sum(card_value(card) for card in player_card)
        dealer_score = sum(card_value(card) for card in dealer_card)
        #evaluate cards for win/lose or tie, Some automation is here - may seem line error during play but NOT.
        if dealer_score > 21:
            display_cards(player_card, player_score, dealer_card, dealer_score, "-*PLAYER WON!*-", False, deck)
        elif dealer_score == player_score and player_score >= 17:
            display_cards(player_card, player_score, dealer_card, dealer_score, "", True, deck)
        elif dealer_score in range(17, 21+1) and player_score in range(17, 21+1) and player_score > dealer_score:
            display_cards(player_card, player_score, dealer_card, dealer_score, "-*PLAYER WON!*-", False, deck)
        elif dealer_score in range(17, 21+1) and player_score in range(18, 21+1) and player_score < dealer_score:
            display_cards(player_card, player_score, dealer_card, dealer_score, "Dealer won", False, deck)
        elif dealer_score < 17 and player_score in range(20, 21+1):
            player_stays(player_score, dealer_score, player_card, dealer_card, True, deck)
        else:
            display_cards(player_card, player_score, dealer_card, dealer_score, "", False, deck)
            #Player decision time
            choice = input("Another card sir/madame? 'h' to Hit it, 'p' to quit it: \n").lower()
        #If player hits, go to player_hits function
        if choice == "h":
            player_hits(player_score, player_card, dealer_score, dealer_card, deck)
        #If player stays, go to player_stays function
        elif choice == "p":
            player_stays(player_score, dealer_score, player_card, dealer_card, True, deck)
        else: #self esplanatory
            print("Invalid choice. Please try again.")
            continue
#get player card when 'hit'
def player_hits(player_score, player_card, dealer_score, dealer_card, deck):
    new_card = deck.pop()
    player_card.append(new_card)
    #if player has more than 10 and receives an ace, turn it into '1' and add 1 to score
    if player_score > 10 and new_card[0] == "Ace":
        player_card.pop()
        player_card.append(one)
        player_score = sum(int(one[0]) for card in player_card)
        #Dealers turn
        player_stays(player_score, dealer_score, player_card, dealer_card, False, deck)
    else:   #Add regular card to total score
        player_score = sum(card_value(card) for card in player_card)
    #if player busts over 21, player losed and new game starts without allowing dealer to select cards.
    if player_score > 21:
        display_cards(player_card, player_score, dealer_card, dealer_score, "Dealer won.", False, deck)
        enter_more(deck)
    #Dealers turn
    player_stays(player_score, dealer_score, player_card, dealer_card, False, deck)
#Dealer/computer card selection
def player_stays(ps, ds, pc, dc, trigger, deck):
    while ds < 17:
        new_card = deck.pop()
        dc.append(new_card)
        #if dealer receives ace when already has 11 or more points, turn into '1' and add 1 to score.
        if ds > 10 and new_card[0] == "Ace":
            dc.pop()
            dc.append(one)
            ds = sum(int(one[0]) for card in dc)
        #add regular card to score
        else:
            ds = sum(card_value(card) for card in dc)
        #when trigger is True, this means Player is passed and computer is free to pull cards sequentially til finished
        if trigger == False and ds < 22:
            main(ps, pc, ds, dc, deck)
    #when Player is finished and computer is finished evaluate for win, lose or tie, invoke scoreboard display
    while trigger and ds >= 17:

        if ds > 21:
            display_cards(pc, ps, dc, ds, "-*PLAYER WON!*", False, deck)

        elif ps > ds:
            display_cards(pc, ps, dc, ds, "-*PLAYER WON!*", False, deck)

        elif ds > ps:
            display_cards(pc, ps, dc, ds, "Dealer won.", False, deck)

        elif ds == ps:
            display_cards(pc, ps, dc, ds, "", True, deck)
        else:
            continue
        enter_more(deck)
#display scoreboard.
def display_cards(pc, ps, dc, ds, win, tie, d_count):
    if tie:
        print(f"Players cards: {pc}\n")
        print(f"Dealers cards: {dc}")
        print(f"\n\n ---*** Your scores are: Dealer: {ds} --***-- Player: {ps} -*You tied*-  ***---\n")
        enter_more(d_count)

    else:
        print(f"Players cards: {pc}\n")
        print(f"Dealers cards: {dc}")
        print(f"\n---*** Your scores are: Dealer: {ds} --***-- Player: {ps} {win}  ***---\n")
    if win != "":
        enter_more(d_count)
#Start new round
def enter_more(d_count):
    go_again = input("0 to quit or Enter to start ") # Keep as string, avoids TypeErrors.
    if go_again == "0": # anything other than "0" will return False, no errors.
        exit()
    else:
        main(0, [], 0, [], d_count)

main(0, [], 0, [], [])