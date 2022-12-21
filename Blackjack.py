import random
import os
from datetime import time, datetime

FILENAME = "money.txt"


def display_header():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    print("Enter 'x' for bet to exit")


def read_money():
    with open(FILENAME, "r") as file:
        if os.stat(FILENAME).st_size == 0:
            print("Data file missing, resetting starting amount to 1000.")
            money = 1000
            write_money(money)
            return money
        else:
            line = file.readline()
            return float(line)


def write_money(money):
    with open(FILENAME, "w") as file:
        file.write(str(money))


def get_deck():
    deck = []
    ranks = {"Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10",
             "Jack", "Queen", "King"}
    suits = {"Clubs", "Diamonds", "Spades", "Hearts"}
    for suit in suits:
        for rank in ranks:
            if rank == "Ace":
                card_value = 11
            elif rank == "Jack" or rank == "Queen" or rank == "King":
                card_value = 10
            else:
                card_value = int(rank)
            card = [rank, suit, card_value]
            deck.append(card)
    return deck


def calculate_hand_points(hand):
    points = 0
    ace_count = 0
    for card in hand:
        if card[0] == "Ace":
            ace_count += 1
        points += card[2]
    if ace_count > 0 and points > 21:
        points = points - (ace_count * 10)
    if ace_count > 1 and points <= 11:
        points += 10
    return points


def add_card(hand, card):
    hand.append(card)


def shuffle(deck):
    random.shuffle(deck)


def get_empty_hand():
    hand = []
    return hand


def deal_card(deck):
    card = deck.pop()
    return card


def print_hand(hand):
    for card in hand:
        print(card)


def ask_again():
    while True:
        again = input("\nPlay again? (y/n): ")
        if again.lower() == "y" or again.lower() == "n":
            return again
        else:
            print("Invalid command. Try again")
            continue


def display_card(card):
    return card[0] + " of " + card[1]


def player_play(player_hand, deck):
    while True:
        play = input("\nHit or stand? (h/s): ")
        if play.lower() == "h":
            print("YOUR CARDS:")
            add_card(player_hand, deal_card(deck))
            for i in range(len(player_hand)):
                print(display_card(player_hand[i - 1]))
            if calculate_hand_points(player_hand) >= 21:
                break
            continue
        elif play.lower() == "s":
            break
        else:
            print("Invalid command. Try again.")
            continue


def main():
    display_header()
    start_time = datetime.now()
    time_format = "%X %p"
    print(start_time.strftime(time_format))
    print()

    money = read_money()

    print("Starting money: " + "${:,.2f}".format(money))

    while True:
        deck = get_deck()
        shuffle(deck)
        player_hand = get_empty_hand()
        dealer_hand = get_empty_hand()
        while True:
            try:
                bet = float(input("Bet amount: "))
                if bet > money:
                    print("You don't have enough money. Try again.")
                    continue
                elif bet < 10:
                    print("Bet amount should be at least 10. Try again.")
                    continue
                else:
                    break
            except ValueError:
                print("Invalid amount, try again.")
                continue
        print("\nDEALER'S SHOW CARD:")
        add_card(dealer_hand, deal_card(deck))
        add_card(dealer_hand, deal_card(deck))
        print(display_card(dealer_hand[0]))

        print("\nYOUR CARDS:")
        add_card(player_hand, deal_card(deck))
        add_card(player_hand, deal_card(deck))
        for i in range(len(player_hand)):
            print(display_card(player_hand[i - 1]))

        while True:
            player_play(player_hand, deck)
            if calculate_hand_points(player_hand) <= 21:
                while True:
                    if calculate_hand_points(dealer_hand) <= 16:
                        add_card(dealer_hand, deal_card(deck))
                        continue
                    elif calculate_hand_points(dealer_hand) > 16:
                        break
            print("\nDEALER'S CARDS:")
            for i in range(len(dealer_hand)):
                print(display_card(dealer_hand[i - 1]))

            print("\nYOUR POINTS:     " + str(calculate_hand_points(player_hand)))
            print("DEALER'S POINTS: " + str(calculate_hand_points(dealer_hand)))
            print()

            if calculate_hand_points(player_hand) > 21:
                print("Sorry. You lose.")
                money -= bet
            elif calculate_hand_points(dealer_hand) > 21:
                print("You won.")
                money += bet
            elif calculate_hand_points(player_hand) > calculate_hand_points(dealer_hand):
                print("You won.")
                money += bet
            elif calculate_hand_points(player_hand) < calculate_hand_points(dealer_hand):
                print("Sorry. You lose.")
                money -= bet
            else:
                print("You got push.")

            print("Money: " + "${:,.2f}".format(money))
            write_money(money)

            again = ask_again()
            print()

            break
        if again == "y":
            continue
        else:
            stop_time = datetime.now()
            elapsed_time = stop_time - start_time

            elapsed_minutes = elapsed_time.seconds // 60
            elapsed_seconds = elapsed_time.seconds % 60
            elapsed_hours = elapsed_minutes // 60
            elapsed_minutes = elapsed_minutes % 60

            elapsed_time_object = time(elapsed_hours, elapsed_minutes, elapsed_seconds)

            print("Stop Time:      ", stop_time.strftime(time_format))
            print("Elapsed time:   ", elapsed_time_object)
            print()
            break

    print("Thanks for playing...")
    print("\nCome back soon!")


if __name__ == "__main__":
    main()
