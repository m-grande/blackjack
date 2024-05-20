import random
from loguru import logger


# Deck Initialization:
def deck_initialization():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    deck = [(rank, suit) for suit in suits for rank in ranks]
    return deck


# Shuffle Deck:
def shuffle_deck(deck):
    random.shuffle(deck)
    return deck


# Deal Cards:
def deal_cards(deck):
    return [deck.pop(), deck.pop()]


# Display the player's and dealer's initial cards
def display_initial_cards(player_hand, dealer_hand):
    logger.info("Player's initial hand:")
    for card in player_hand:
        logger.info(f"{card[0]} of {card[1]}")
    logger.info("Dealer's initial hand:")
    logger.info(f"{dealer_hand[0][0]} of {dealer_hand[0][1]}")
    logger.info("One card face down")


# Calculate Hand Value:
def hand_value(hand):
    value = 0
    aces = 0
    value_10 = ["Jack", "Queen", "King"]

    for card in hand:
        if card[0] in value_10:
            value += 10
        elif card[0] == "Ace":
            aces += 1
            value += 11
        else:
            value += int(card[0])

    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value


# Player Decision Handling:
def decision_player(player_hand, deck):
    while True:
        logger.info("Would you like an additional card (y / n): ")
        y_or_not = input().lower()

        if y_or_not == "y":
            new_card = deck.pop()
            player_hand.append(new_card)
            logger.info(f"You drew: {new_card[0]} of {new_card[1]}")
            logger.info("Your actual hand is:")
            for card in player_hand:
                logger.info(f"{card[0]} of {card[1]}")
            if hand_value(player_hand) > 21:
                logger.info("The player busts and loses.")
                return player_hand, True  # Player busts
        elif y_or_not == "n":
            break
        else:
            logger.info("Please enter 'y' or 'n'.")
    return player_hand, False


# Dealer Decision Handling:
def decision_handling(dealer_hand, deck):
    while hand_value(dealer_hand) < 17:
        new_card = deck.pop()
        dealer_hand.append(new_card)
        logger.info(f"Dealer draws: {new_card[0]} of {new_card[1]}")
        logger.info("Dealer's hand is:")
        for card in dealer_hand:
            logger.info(f"{card[0]} of {card[1]}")
        logger.info(f"Dealer's hand value is: {hand_value(dealer_hand)}")
        if hand_value(dealer_hand) > 21:
            logger.info("The dealer busts and loses.")
            break
    return dealer_hand


# Evaluate Result:
def evaluate_result(player_hand, dealer_hand):
    player_points = hand_value(player_hand)
    dealer_points = hand_value(dealer_hand)

    logger.info(f"Player's hand value: {player_points}")
    logger.info(f"Dealer's hand value: {dealer_points}")

    if player_points > 21:
        logger.info("The dealer wins!")
        return False
    elif dealer_points > 21 or player_points > dealer_points:
        logger.info("The player wins!")
        return True
    elif player_points < dealer_points:
        logger.info("The dealer wins!")
        return False
    else:
        logger.info("The game is tied!")
        return None


# Betting Handling:
def manage_bets(initial_sum):
    logger.info("How much money do you want to bet?")
    while initial_sum > 0:
        try:
            money_to_bet = int(input())
            if money_to_bet <= 0:
                logger.info("Please enter a valid amount greater than zero.")
            elif money_to_bet > initial_sum:
                logger.info("Your funds are not sufficient. Please enter a lower amount.")
            else:
                break
        except ValueError:
            logger.info("Please enter a valid amount.")
    return money_to_bet


# Manage money:
def manage_money(initial_sum, money_to_bet, player_hand, dealer_hand):
    result = evaluate_result(player_hand, dealer_hand)
    if result is True:
        logger.info("Congratulations! You win!")
        return initial_sum + money_to_bet
    elif result is False:
        logger.info("Sorry, you lost.")
        return initial_sum - money_to_bet
    else:
        logger.info("It's a tie!")
        return initial_sum


def new_game():
    while True:
        logger.info("Do you want to play again? (y / n)")
        new_game = input().lower()
        if new_game == "y":
            return True
        elif new_game == "n":
            return False
        else:
            logger.info("Please enter 'y' or 'n'.")


def main():
    play_again = True
    initial_sum = 1000

    print("Welcome to the Blackjack game. You start with $1000.")

    while play_again and initial_sum > 0:
        money_to_bet = manage_bets(initial_sum)

        # Shuffle the deck
        shuffled_deck = shuffle_deck(deck_initialization())

        # The player receives two face-up cards.
        player_hand = deal_cards(shuffled_deck)

        # The dealer receives one face-up card and one face-down card.
        dealer_hand = deal_cards(shuffled_deck)

        # Cards are being displayed
        display_initial_cards(player_hand, dealer_hand)

        # The player decides whether to request an additional card ("hit") to get closer to 21 or to stay with the current hand ("stand").
        player_hand, player_busted = decision_player(player_hand, shuffled_deck)

        # If player didn't bust, the dealer takes their turn
        if not player_busted:
            dealer_hand = decision_handling(dealer_hand, shuffled_deck)

        # Result Evaluation:
        initial_sum = manage_money(initial_sum, money_to_bet, player_hand, dealer_hand)
        print(f"Your current balance is: ${initial_sum}.")

        if initial_sum > 0:
            play_again = new_game()
        else:
            logger.info("You have run out of money. Game over.")
            play_again = False


if __name__ == "__main__":
    main()
