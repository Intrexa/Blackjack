import random

dealer_score = 0
player_score = 0
player_card = []
dealer_card = []
choice = ""
one = ('1', 'ace')

def card_value(card) -> int:
    """
    Evaluates a cards value. It treats 'Ace' as 1.
    Any code that has special rules for value of ace
    should handle its own edge cases

    Returns:
        int: The value of the card
    """
    # Style choice for returns
    # I prefer not to do elif when we are just returning values
    if card[0] in ['Jack', 'Queen', 'King']:
        return 10
    if card[0] == 'Ace':
        return 1
    
    return int(card[0])

def evaluate_hand(cards: list) -> int:
    """
    Evaluate a hand for score

    Returns:
        int: Score of the hand
    """

    # We are going to evaluate the hand assuming the aces are 1.
    # Then, we can determine if it's safe to promote an ace
    #  to its full value of 11.
    # Yes, I'm traversing the deck twice and then aces a third time
    #   when a loop and math could do it in one pass. Sue me.
    hand_value = sum([card_value(card) for card in cards])
    ace_count = len([card for card in cards if card[0] == 'Ace'])
        
    # See how many aces we can promote from value of 1 to 11
    while ace_count > 0 and (hand_value + 10) <= 21:
        ace_count -= 1
        hand_value += 10
    
    return hand_value



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
        
        player_score = evaluate_hand(player_card)
        dealer_score = evaluate_hand(dealer_card)

        # We don't really need is_game_over, because of so many exit points in the functions
        # But we will end up making use of is_game_over
        is_game_over = evaluate_state(player_card,player_score,dealer_card,dealer_score,deck)
        if not is_game_over:
            choice = input("Another card sir/madame? 'h' to Hit it, 'p' to quit it: \n").lower()
        #If player hits, go to player_hits function
        if choice == "h":
            player_hits(player_score, player_card, dealer_score, dealer_card, deck)
        #If player stays, go to player_stays function
        elif choice == "p":
            player_stays(player_score, dealer_score, player_card, dealer_card, True, deck)
        else: #self explanatory
            print("Invalid choice. Please try again.")
            continue

# Evaluate game state for game over
# TODO: This function is still overloaded, should not be displaying state as well
# TODO: Refactor display to be seperate function
def evaluate_state(player_cards,player_score,dealer_cards,dealer_score,deck) -> bool:
        """
        Evaluate Game State

        Returns:
            bool: Is the game over
        """
        is_game_over = False
        #evaluate cards for win/lose or tie, Some automation is here - may seem line error during play but NOT.

        # arguments to pass to display_cards()
        # These will get set after game state is evaluated
        # TODO: Game should be a class to prevent so many args being passed around
        args = {
            "player_cards":player_cards,
            "player_score":player_score,
            "dealer_cards":dealer_cards,
            "dealer_score":dealer_score,
            # BUG: I introduced this bug
            # display isn't playing nice with "None"
            # Exaple:
            # ---*** Your scores are: Dealer: 9 --***-- Player: 9 None  ***---
            "win_message":None, #No default win message
            "deck":deck
        }
        if dealer_score > 21:
            args["win_message"] = "-*PLAYER WON!*-"
        elif dealer_score == player_score and player_score >= 17:
            args["win_message"] = "-*You tied*-"
        elif dealer_score in range(17, 21+1) and player_score in range(17, 21+1) and player_score > dealer_score:
            args["win_message"] = "-*PLAYER WON!*-"
        elif dealer_score in range(17, 21+1) and player_score in range(18, 21+1) and player_score < dealer_score:
            args["win_message"] = "Dealer won"
        elif dealer_score < 17 and player_score in range(20, 21+1):
            # The below was super tricky, I didn't notice this was a seperate function at first
            # Long lists of conditions are hard enough, but you kind of snuck a different function in the middle
            # This makes it hard to realize what's happening
            # Try to either not do this, or make it obvious
            # It's also really sneaky that a new game can start in this function
            player_stays(player_score, dealer_score, player_cards, dealer_cards, True, deck)
        else:
            # Game not over, still players turn
            pass # Really we could move this clause, pass for now
        
        # dictionary unpacking as arguments to the function
        display_cards(**args)
        
        # If no one has a win message, and there's no tie, game on
        is_game_over = (args["win_message"] is not None)
        return is_game_over


#get player card when 'hit'
def player_hits(player_score, player_card, dealer_score, dealer_card, deck):
    new_card = deck.pop()
    player_card.append(new_card)
    player_score = evaluate_hand(player_card)
    #if player busts over 21, player lost and new game starts without allowing dealer to select cards.
    if player_score > 21:
        display_cards(player_card, player_score, dealer_card, dealer_score, "Dealer won.", deck)
        enter_more(deck)
    #Dealers turn
    # NOTE: In casino play, dealers don't take turns until the players are done
    # We are going to refactor this further
    player_stays(player_score, dealer_score, player_card, dealer_card, False, deck)

#Dealer/computer card selection
def player_stays(ps, ds, pc, dc, trigger, deck):
    while ds < 17:
        new_card = deck.pop()
        dc.append(new_card)
        ds = evaluate_hand(dc)
        #when trigger is True, this means Player is passed and computer is free to pull cards sequentially til finished
        # TODO: Remove recursion
        # main() is a bit overloaded, and the below is confusing
        # main really is "Take a turn"
        # So it should be called "take_turn"
        # when you have a line of code like "main(0, [], 0, [], [])"
        # You're creating a new game, then telling main() to take a turn in that new game
        # This should be split out into seperate functions and made more clear
        if trigger == False and ds < 22:
            main(ps, pc, ds, dc, deck)
    #when Player is finished and computer is finished evaluate for win, lose or tie, invoke scoreboard display
    while trigger and ds >= 17:

        if ds > 21:
            display_cards(pc, ps, dc, ds, "-*PLAYER WON!*", deck)

        elif ps > ds:
            display_cards(pc, ps, dc, ds, "-*PLAYER WON!*", deck)

        elif ds > ps:
            display_cards(pc, ps, dc, ds, "Dealer won.", deck)

        elif ds == ps:
            display_cards(pc, ps, dc, ds, "-*You tied*-", deck)
        else:
            continue
        enter_more(deck)

#display scoreboard.
def display_cards(player_cards, player_score, dealer_cards, dealer_score, win_message, deck):
    # No need for a special case for a tie
    # This is a display, it's more of just an "outcome" message
    print(f"Players cards: {player_cards}\n")
    print(f"Dealers cards: {dealer_cards}")
    print(f"\n---*** Your scores are: Dealer: {dealer_score} --***-- Player: {player_score} {(win_message or '')}  ***---\n")

    # TODO: Remove game restart from display functionality
    # This is really confusing design. Calling a display function shouldn't have a chance to restart the game
    # There is a principle called "Side effects"
    # A simple explanation is that a function should do 1 focused thing.
    # If it changes anything outside of just doing that 1 thing, it's a side effect
    # Try to minimize side effects.
    # The reason is that when another programmer comes along, and wants to display cards,
    # And they see a function "display_cards()", they shouldn't have to worry if calling it can restart the game
    if win_message:
        enter_more(deck)

#Start new round
# BUG: This should be a loop, not recursion
# This can overflow the stack + crash if player plays enough rounds
# This function has way too many entry points
# When debugging/troubleshooting, it's hard to tell when/where/why it's getting called
def enter_more(d_count):
    go_again = input("0 to quit or Enter to start ") # Keep as string, avoids TypeErrors.
    if go_again == "0": # anything other than "0" will return False, no errors.
        exit()
    else:
        main(0, [], 0, [], d_count)

main(0, [], 0, [], [])