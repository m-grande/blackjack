import random

from loguru import logger


# Deck Initialization:
# Function to create a deck of cards, represented as a list of tuples, each representing a card (e.g., ('Ace', 'Hearts')).
def deck_initialization():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    deck = [(rank, suit) for suit in suits for rank in ranks]
    return deck


# Shuffle Deck:
# Function to shuffle the deck of cards randomly.
def shuffle_deck(deck):
    # Save the original deck
    shuffled_deck = deck[:]

    # Create the new one
    new_deck = []
    while shuffled_deck:
        random_index = random.randint(0, len(shuffled_deck) - 1)
        random_card = shuffled_deck.pop(random_index)
        new_deck.append(random_card)
    return new_deck


# Deal Cards:
# Function to deal two cards to each player (the player and the dealer) initially.
def deal_cards(deck):
    two_cards = []
    for _ in range(2):
        two_cards.append(deck.pop())
    return two_cards


# Display the player's and dealer's initial cards
def display_initial_cards(player_hand, dealer_hand):
    logger.info("Player's initial hand:")
    for card in player_hand:
        logger.info(f"{card[0]} of {card[1]}")
    logger.info("Dealer's initial hand:")
    logger.info(f"{dealer_hand[0][0]} of {dealer_hand[0][1]}")
    logger.info("One card face down")


# Calculate Hand Value:
# Function to calculate the total value of the cards in a hand, taking into account the value of an ace (1 or 11 points).
def hand_value(hand):
    total = 0
    value_10 = ["Jack", "Queen", "King"]
    for card in hand:
        if total > 10:
            if card[0] == "Ace":
                total += 1
            elif card[0] in value_10:
                total += 10
            else:
                total += int(card[0])
        if total <= 10:
            if card[0] == "Ace":
                total += 11
            elif card[0] in value_10:
                total += 10
            else:
                total += int(card[0])
    return total


# Player Decision Handling:
# Function to allow the player to decide whether to hit (request an additional card) or stand (keep the current hand).
def decision_player(player_hand, deck):
    keep_playing = True

    while keep_playing:
        logger.info("Would you like an additional card (y / n): ")
        y_or_not = input().lower()

        if y_or_not == "y":
            new_card = deck.pop()
            player_hand.append(new_card)
            logger.info(f"You drew: {new_card[0]} of {new_card[1]}")
            logger.info("Your actual hand is:")
            for card in player_hand:
                logger.info(f"{card[0]} of {card[1]}", end=" - ")
            if hand_value(player_hand) > 21:
                keep_playing = False
        elif y_or_not == "n":
            keep_playing = False
            logger.info("Your hand is:")
            for card in player_hand:
                logger.info(f"{card[0]} of {card[1]}", end=" - ")
        else:
            logger.info("Please enter 'y' or 'n'.")

    return player_hand


# Dealer Decision Handling:
# Function to play the dealer's hand, who will draw cards until reaching a total of at least 17 points.
def decision_handling(dealer_hand, deck):
    total = hand_value(dealer_hand)
    while total < 17:
        new_card = deck.pop()
        dealer_hand.append(new_card)
        logger.info(f"Dealer draws: {new_card[0]} of {new_card[1]}")
        logger.info("His actual hand is:")
        for card in dealer_hand:
            logger.info(f"{card[0]} of {card[1]}", end=" - ")
        total = hand_value(dealer_hand)

    return dealer_hand


# Evaluate Result:
# Function to evaluate the outcome of a hand (win, lose, tie) based on the player's and dealer's scores.
def evaluate_result(player_hand, dealer_hand):
    player_points = hand_value(player_hand)
    dealer_points = hand_value(dealer_hand)

    if player_points > dealer_points:
        logger.info("The player wins!")
        return True
    elif player_points < dealer_points:
        logger.info("The dealer wins!")
        return False
    else:
        logger.info("The game is tied!")


# Betting Handling:
# If the player wins, they win an amount equal to their bet.
# If the player loses, they lose their bet.
def manage_bets(initial_sum):
    logger.info("How much money do you want to bet?")
    while True:
        money_to_bet = int(input())
        if money_to_bet <= 0:
            logger.info("Please enter a valid amount greater than zero.")
        elif money_to_bet > initial_sum:
            logger.info("Your funds are not sufficient. Please enter a lower amount.")
        else:
            break
    return money_to_bet


# Manage money:
def manage_money(initial_sum, money_to_bet, player_hand, dealer_hand):
    if evaluate_result(player_hand, dealer_hand):
        logger.info("Congratulations! You win!")
        return initial_sum + money_to_bet
    else:
        logger.info("Sorry, you lost.")
        return initial_sum - money_to_bet


def new_game(initial_sum):
    if initial_sum > 0:
        play_again = True

        while play_again:
            logger.info("Do you want to play again? y / n")
            new_game = input().lower()
            if new_game == "y":
                play_again = True
                break
            elif new_game == "n":
                play_again = False
            else:
                logger.info("Please enter 'y' or 'n'.")
        return play_again
