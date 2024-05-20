import random
import io
import logging
import sys
from io import StringIO
from unittest.mock import patch


from loguru import logger

from ..script import (
    deal_cards,
    decision_player,
    deck_initialization,
    display_initial_cards,
    hand_value,
    shuffle_deck,
)


def test_deck_initialization():
    logger.info("Testing deck_initialization...")
    deck = deck_initialization()

    # Verify the number of cards in the deck is correct
    assert len(deck) == 52, "Number of cards in the deck is incorrect"

    # Some sample checks
    assert ("Ace", "Hearts") in deck, "Ace of Hearts card missing in the deck"
    assert ("King", "Spades") in deck, "King of Spades card missing in the deck"

    logger.info("All tests passed successfully!")


# Test shuffle deck


def shuffle_deck(deck):
    random.shuffle(deck)
    return deck


def test_shuffle_deck():
    logger.info("Testing shuffle_deck...")

    original_deck = deck_initialization()
    shuffled_deck = shuffle_deck(original_deck.copy())

    # Verify that all cards from the original deck are present in the shuffled deck
    for card in original_deck:
        assert card in shuffled_deck, f"Card {card} missing in the shuffled deck"

    # Verify that the shuffled deck is of the same length as the original deck
    assert len(original_deck) == len(
        shuffled_deck
    ), "Length of shuffled deck differs from original deck"

    # Verify that the shuffled decks are not the same as the original deck
    assert original_deck != shuffled_deck, "Shuffled deck is the same as the original deck"

    # Verify that multiple shuffles result in different deck orders
    num_tests = 100
    shuffled_decks = []
    for _ in range(num_tests):
        shuffled_deck = shuffle_deck(deck_initialization().copy())
        shuffled_decks.append(shuffled_deck)

    different_deck_count = 0
    for i in range(num_tests):
        for j in range(i + 1, num_tests):
            if shuffled_decks[i] != shuffled_decks[j]:
                different_deck_count += 1

    assert different_deck_count > 0, "Shuffled decks are not different"

    logger.info("All tests passed successfully!")


# Test deal cards


def test_deal_cards():
    logger.info("Testing deal cards...")
    deck = deck_initialization()

    # Verify the number of the cards in the hand is two
    assert len(deal_cards(deck)) == 2, "The number of cards are not two"

    logger.info("All tests passed successfully!")


# Test display initial cards


def test_display_initial_cards(caplog):
    caplog.set_level(logging.INFO)
    logger.info("Testing display initial cards...")

    # setup the environment

    deck = deck_initialization()
    shuffled_deck = shuffle_deck(deck)
    player_cards = deal_cards(shuffled_deck)
    dealer_cards = deal_cards(shuffled_deck)

    player_hand_1 = f"{player_cards[0][0]} of {player_cards[0][1]}"
    player_hand_2 = f"{player_cards[1][0]} of {player_cards[1][1]}"
    dealer_hand_1 = f"{dealer_cards[0][0]} of {dealer_cards[0][1]}"
    dealer_hand_2 = f"{dealer_cards[1][0]} of {dealer_cards[1][1]}"

    display_initial_cards(player_cards, dealer_cards)

    records = caplog.records
    printed_output = [output.message for output in records]

    # Verify if print the two cards of player
    assert player_hand_1 in printed_output

    assert player_hand_2 in printed_output

    # Verify if print just the first card of dealer and the second face down
    assert dealer_hand_1 in printed_output

    assert dealer_hand_2 not in printed_output

    logger.info("All tests passed successfully!")


# Test hand value


def test_hand_value():
    logger.info("Testing hand_value...")

    # Base case test: a hand with only one ace
    hand1 = [("Ace", "Hearts")]
    assert hand_value(hand1) == 11, "Test failed for a hand with only one ace"

    # Test a hand with an ace and a ten-point card
    hand2 = [("Ace", "Spades"), ("King", "Diamonds")]
    assert hand_value(hand2) == 21, "Test failed for a hand with an ace and a ten-point card"

    # Test a hand with a ten-point card, a five-point card, and an ace
    hand3 = [("King", "Hearts"), ("5", "Spades"), ("Ace", "Clubs")]
    assert (
        hand_value(hand3) == 16
    ), "Test failed for a hand with an ace, a ten-point card, and a five-point card"

    logger.info("All tests passed successfully!")


# Test decision player


def test_decision_player():
    logger.info("Testing decision player...")

    def test_decision_player_with_input_y_one_card():
        logger.info("Testing decision player with input 'y' for one card...")
        player_hand = [("10", "Diamonds")]
        deck = [("Ace", "Clubs")]

        with patch("builtins.input", side_effect=["y"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                decision_player(player_hand, deck)

        expected_output = (
            "You drew: Ace of Clubs\nYour actual hand is:\n10 of Diamonds - Ace of Clubs - \n"
        )
        assert fake_out.getvalue() == expected_output
        assert len(player_hand) == 2

    def test_decision_player_with_input_y_more_cards():
        logger.info("Testing decision player with input 'y' for more cards...")
        player_hand = [("10", "Diamonds")]
        deck = [("Ace", "Clubs"), ("2", "Hearts"), ("3", "Diamonds")]

        with patch("builtins.input", side_effect=["y", "y", "n"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                decision_player(player_hand, deck)

        expected_output = "You drew: Ace of Clubs\nYour actual hand is:\n10 of Diamonds - Ace of Clubs - 2 of Hearts - \nYou drew: 2 of Hearts\nYour actual hand is:\n10 of Diamonds - Ace of Clubs - 2 of Hearts - 3 of Diamonds - \nYour hand is:\n10 of Diamonds - Ace of Clubs - 2 of Hearts - 3 of Diamonds - \n"
        assert fake_out.getvalue() == expected_output
        assert len(player_hand) == 4

    def test_decision_player_with_input_n():
        logger.info("Testing decision player with input 'n'...")
        player_hand = [("10", "Diamonds")]
        deck = [("Ace", "Clubs")]

        with patch("builtins.input", side_effect=["n"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                decision_player(player_hand, deck)

        expected_output = "Your hand is:\n10 of Diamonds - \n"
        assert fake_out.getvalue() == expected_output
        assert len(player_hand) == 1

    def test_decision_player_with_invalid_input_then_valid():
        logger.info("Testing decision player with invalid input followed by valid input...")
        player_hand = [("10", "Diamonds")]
        deck = [("Ace", "Clubs")]

        with patch("builtins.input", side_effect=["invalid", "y"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                decision_player(player_hand, deck)

        expected_output = "Please enter 'y' or 'n'.\nYou drew: Ace of Clubs\nYour actual hand is:\n10 of Diamonds - Ace of Clubs - \n"
        assert fake_out.getvalue() == expected_output
        assert len(player_hand) == 2

    if __name__ == "__main__":
        test_decision_player_with_input_y_one_card()
        test_decision_player_with_input_y_more_cards()
        test_decision_player_with_input_n()
        test_decision_player_with_invalid_input_then_valid()
        logger.info("All tests passed successfully!")


if __name__ == "__main__":
    test_deck_initialization()
    test_shuffle_deck()
    test_deal_cards()
    test_display_initial_cards()
    test_hand_value()
    test_decision_player()
