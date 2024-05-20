#!/usr/bin/env python
import script


def main():
    play_again = True
    initial_sum = 1000

    print("Welcome to the Blackjack game. You start with $1000.")

    while play_again:
        # Check if the player still has funds to bet
        if initial_sum <= 0:
            print("You have run out of money. Game over.")
            break

        money_to_bet = script.manage_bets(initial_sum)

        # Shuffle the deck
        shuffled_deck = script.shuffle_deck(script.deck_initialization())

        # The player receives two face-up cards.
        player_hand = script.deal_cards(shuffled_deck)

        # The dealer receives one face-up card and one face-down card.
        dealer_hand = script.deal_cards(shuffled_deck)

        # Cards are being displayed
        script.display_initial_cards(player_hand, dealer_hand)

        # The player decides whether to request an additional card ("hit") to get closer to 21 or to stay with the current hand ("stand").
        player_hand, player_busted = script.decision_player(player_hand, shuffled_deck)

        # Check if the player busts; if so, skip the dealer's turn and handle the loss
        if player_busted:
            initial_sum = script.manage_money(initial_sum, money_to_bet, player_hand, dealer_hand)
            print(f"Your current balance is: ${initial_sum}.")
            if initial_sum > 0:
                play_again = script.new_game()
            else:
                print("You have run out of money. Game over.")
                play_again = False
            continue

        # The dealer draws additional cards until they have a total of at least 17 points.
        dealer_hand = script.decision_handling(dealer_hand, shuffled_deck)

        # Result Evaluation and manage money based on the result
        initial_sum = script.manage_money(initial_sum, money_to_bet, player_hand, dealer_hand)
        print(f"Your current balance is: ${initial_sum}.")

        # Check if the player wants to play another round
        if initial_sum > 0:
            play_again = script.new_game()
        else:
            print("You have run out of money. Game over.")
            play_again = False

    print("Thanks for playing!")


if __name__ == "__main__":
    main()
