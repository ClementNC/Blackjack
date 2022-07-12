from replit import clear
from blackjack_art import logo
import random

# create_deck(num_deck) accepts an integer which is the number of decks to be used during the game and creates a
# dictionary which represents the deck.
def create_deck(num_deck): 
    card_dict = {}
    non_num_cards = ['J', 'Q', 'K', 'A']
    for i in range(2,11):
        suits = ['♠', '♦', '♥', '♣']
        card_dict[str(i)] = num_deck * suits
    for item in non_num_cards:
        card_dict[item] = num_deck * suits
    return card_dict


# create_card_value() creates a dictionary where the keys are the cards and the values are the value of each card.
def create_card_value():
    card_value_dict = {}
    non_num_card = ['J', 'Q', 'K', 'A']
    for i in range(2,11):
        card_value_dict[str(i)] = i
    for item in non_num_card:
        if item == 'A':
            card_value_dict[item] = 11
        else:
            card_value_dict[item] = 10
    return card_value_dict


# reshuffle(deck_content) returns a boolean value which tells whether or not the deck should be reshuffled.
def reshuffle(deck_content):
    is_available = [len(deck_content[cards]) > 0 for cards in deck_content]
    return False in is_available


# count_total_value(card_list, value) accepts 2 arguments, one is a list of cards which represents either a user's or a dealer's hand and the other
# is a dictionary filled with the value of each counts and it calculates the total value of the list of cards.
def count_total_value(card_list, value):
    num_ace = 0
    for card in card_list:
        num_ace += card.count('A')
    total_value = 0
    for card in card_list:
        separate_card = card.split()
        total_value += value[separate_card[0]]
    if num_ace > 0:
        while total_value > 21 and num_ace > 0:
            total_value -= 10
            num_ace -= 1
    return total_value


# deal_cards(deck_content) accepts a dictionary which represents the current deck and randomly chooses a card from the
# dictionary
def deal_cards(deck_content):
    available_card = [card for card in deck_content if len(deck_content[card]) > 0]
    random_card = random.choice(available_card)
    random_suit = random.choice(deck_content[random_card])
    deck_content[random_card].remove(random_suit)
    card = random_card + ' ' + random_suit
    return card

    
# blackjack(cur_deck, each_value) simulates the blackjack game.
def blackjack(cur_deck, each_value):
    user_hand = []
    dealer_hand = []
    for i in range(2):
        user_hand.append(deal_cards(cur_deck))
        dealer_hand.append(deal_cards(cur_deck))
    user_score = count_total_value(user_hand, each_value)
    while user_score < 21:
        print("\tYour cards: ", end='')
        print(user_hand, ", current score: ", user_score)
        print("\tDealer's first card: ", dealer_hand[0])
        user_hit = ' '
        while user_hit.upper() != 'Y' and user_hit.upper() != 'N':
            user_hit = input("Type 'Y' to hit, type 'N' to stand: ")
            if user_hit.upper() != 'Y' and user_hit.upper() != 'N':
                print("Invalid input. Please only input Y or N")
        if user_hit.upper() == 'Y':
            user_hand.append(deal_cards(cur_deck))
            user_score = count_total_value(user_hand, each_value)
        else:
            break
    dealer_score = count_total_value(dealer_hand, each_value)
    if user_score > 21:
        print("   Your cards: ", user_hand, end='')
        print(", current score: ", user_score)
        print("   Dealer's cards: ", dealer_hand, end='')
        print(", final score: ", dealer_score)
        print("You went over. You lose! 😭")
        return 'L'
    else:
        while dealer_score < 17:
            dealer_hand.append(deal_cards(cur_deck))
            dealer_score = count_total_value(dealer_hand, each_value)
        print("   Your cards: ", user_hand, end='')
        print(", current score: ", user_score)
        print("   Dealer's cards: ", dealer_hand, end='')
        print(", final score: ", dealer_score)
        if dealer_score == user_score:
            print("It's a draw 🙃")
            return 'D'
        elif user_score == 21:
            print("Win with a Blackjack 😎")
            return 'W'
        elif dealer_score == 21:
            print("You lose! Opponent has a Blackjack 😱")
            return 'L'
        elif dealer_score > 21:
            print("Dealer went over. You win 😃!")
            return 'W'
        elif user_score > dealer_score:
            print("You win 😃!")
            return 'W'
        else:
            print("You lose! 😭")
            return 'L'


# add_bet(balance) is a function to ask the user how much chips he is willing to place
def add_bet(balance):
    chips = [1, 25, 50, 100, 500, 1000]
    if not balance in chips:
        chips.append(balance)
    user_bet = 0
    add_chip = 'Y'
    possible_chips = [chip for chip in chips if user_bet + chip <= balance]
    while add_chip.upper() == 'Y' and len(possible_chips) > 0:
        user_chip = 0
        while not user_chip in possible_chips and str(user_chip).lower() != 'all':
            user_chip = input(f"Select a chip from {possible_chips} or type 'all' to go all in: ")
            if user_chip.isnumeric():
                user_chip = int(user_chip)
        if str(user_chip).isnumeric():
            user_bet += int(user_chip)
        else:
            user_bet = balance
        possible_chips = [chip for chip in chips if user_bet + chip <= balance]
        if len(possible_chips) > 0:
            add_chip = ' '
            while add_chip.upper() != 'Y' and add_chip.upper() != 'N':
                add_chip = input("Do you still want to add more chips? Input Y/N: ")
                if add_chip.upper() != 'Y' and add_chip.upper() != 'N':
                    print("Invalid input. Please only input Y or N")
    return user_bet


# This is the main function
def main():
    play = 'Y'
    num_decks = 0
    # ask user for the number of decks the user wants
    while num_decks <= 0:
        num_decks = int(input("Enter the number of decks you would like to use: "))
        if num_decks <= 0:
            print("Invalid input. There should be at least 1 deck being used")
    deck = create_deck(num_decks)
    user_money = 1000
    card_value = create_card_value()
    while play.upper() == 'Y' and user_money > 0:
        if reshuffle(deck):
            print("Shuffling...")
            deck = create_deck(num_decks)
        clear()
        print(logo)
        print("Bank: $", user_money)
        bet = add_bet(user_money)
        user_win = blackjack(deck, card_value)
        if user_win == 'W':
            user_money += bet
        elif user_win == 'L':
            user_money -= bet
        if user_money > 0:
            play = ' '
            while play.upper() != 'Y' and play.upper() != 'N':
                play = input("Do you want to play again? Input Y/N: ")
                if play.upper() != 'Y' and play.upper() != 'N':
                    print("Invalid input. Please input Y or N.")
    if user_money == 0:
        print("Game Over. You have nothing in the bank. Thank you for playing!")
    else:
        print("Thank you for playing Blackjack!")


if __name__ == "__main__":
    main()