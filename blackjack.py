import random


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

def get_new_shuffled_deck() -> list[tuple[str, str]]:
    """
    Gets a brand new, freshly shuffled deck to play with
    Has all 52 cards. Jokers removed.

    Return:
        list[tuple[str, str]]: (face, suit)
    """

    card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    deck = [(card, category) for category in card_categories for card in cards_list]
    random.shuffle(deck)

    return deck

def main():
    deck = [] # initialize deck list
    play_again = True # initialize loop
    while play_again: # Keep playing while the player wants to play
        play_round(deck) # Converting to a loop simplifies logic about restarting
        play_again = ask_to_play_again() # And removes potential stack overflow


            
def play_round(deck):
    """
    This is the game. Play a round with a deck.

    Returns:
        None
    """
    has_player_stayed = False # Merging some code paths on the way the dealer plays
    # This will also simplify checking wins for the dealer

    # Initialize Deck
    if len(deck) < 9:
        print(f"{len(deck)} cards in deck, shuffling...")
        deck = get_new_shuffled_deck()

    player_card = [deck.pop(), deck.pop()]
    dealer_card = [deck.pop(), deck.pop()]
    
    while True: # Keep playing until a winner is found
        if len(deck) < 9: # Grab a new deck
            print(f"{len(deck)} cards in deck, shuffling...")
            deck = get_new_shuffled_deck()
         
        player_score = evaluate_hand(player_card)
        dealer_score = evaluate_hand(dealer_card)


        game_state = evaluate_state(player_card,player_score,dealer_card,dealer_score,deck)
        display_game_state(**game_state)

        # If the game is over, restart the game
        if game_state["is_game_over"]:
            break # Stop playing, exit loop

        # Check if player has already stayed
        # If they have, don't ask them again
        # Otherwise, present choice
        if not has_player_stayed:
            choice = input("Another card sir/madame? 'h' to Hit it, 'p' to quit it: \n").lower()
            #If player hits, go to player_hits function
            if choice == "h":
                player_hits(player_card, deck)
                game_state = evaluate_state(player_card,player_score,dealer_card,dealer_score,deck)
                if game_state["is_game_over"]:
                    break # Restarts game
            elif choice == "p":
                has_player_stayed = True
            else: #self explanatory
                print("Invalid choice. Please try again.")

        # No matter what, dealer gets a play
        # dealer score in while loop handles calling this over and over until done
        # No need to do game over check or display yet, it will happen at start of next loop
        # Which is a bit of a defect, but will refactor that later
        dealer_turn(dealer_card, deck)


# Evaluate game state
# TODO: game_state should be a class
def evaluate_state(player_cards,player_score,dealer_cards,dealer_score,deck) -> dict[str,any]:
        """
        Evaluate Game State. Returns dict of evaluated state

        Returns:
            dict[str,yolo]: 
        """
        #evaluate cards for win/lose or tie, Some automation is here - may seem line error during play but NOT.

        # arguments to pass to display_cards()
        # These will get set after game state is evaluated
        # TODO: Game should be a class to prevent so many args being passed around
        game_state = {
            "player_cards":player_cards,
            "player_score":player_score,
            "dealer_cards":dealer_cards,
            "dealer_score":dealer_score,
            "win_message":None, #No default win message
            "deck":deck,
            "is_game_over":False,
            "player_stays":False
        }
        if dealer_score > 21:
            game_state["win_message"] = "-*PLAYER WON!*-"
            # BUG: Currently tied, but the game shouldn't be over until the player decides to stay
            # NOTE: In casino play, if the player and dealer both bust, just the player loses
            # I think this is covered elsewhere, I'm still untangling things
        elif dealer_score == player_score and player_score >= 17:
            game_state["win_message"] = "-*You tied*-"
        elif dealer_score in range(17, 21+1) and player_score in range(17, 21+1) and player_score > dealer_score:
            game_state["win_message"] = "-*PLAYER WON!*-"
        elif dealer_score in range(17, 21+1) and player_score in range(18, 21+1) and player_score < dealer_score:
            game_state["win_message"] = "Dealer won"
        else:
            # Game not over, still players turn
            pass # Really we could remove this clause, pass for now
        
        # If no one has a win message, and there's no tie, game on
        game_state["is_game_over"] = (game_state["win_message"] is not None)
        return game_state


#get player card when 'hit'
def player_hits(player_card, deck):
    new_card = deck.pop()
    player_card.append(new_card)

#Dealer/computer card selection
def dealer_turn(dc, deck):
    new_card = deck.pop()
    dc.append(new_card)



# display scoreboard and just the scoreboard.
# the "**_" is to let me still use dictionary unpacking
# **_ takes the rest of the dict arguments not named as parameters
# This is temporary, I will move the game_state to a seperate class in the future
def display_game_state(player_cards, player_score, dealer_cards, dealer_score, win_message, **_):
    """
    Render game state, and do not end the game

    Returns:
        None
    """

    print(f"Players cards: {player_cards}\n")
    print(f"Dealers cards: {dealer_cards}")
    print(f"\n---*** Your scores are: Dealer: {dealer_score} --***-- Player: {player_score} {(win_message or '')}  ***---\n")



# Check if player wants to play again
def ask_to_play_again():
    """
    Ask player if they want to play again

    Returns:
        bool: True if they want more
    """
    go_again = input("0 to quit or Enter to start ") # Keep as string, avoids TypeErrors.
    return not (go_again == "0") # anything other than "0" will return False, no errors.

main()