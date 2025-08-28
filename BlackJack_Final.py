import random

# Represents a single playing card with a rank and suit
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

# Represents a standard deck of 52 cards
class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
		# Initialize and shuffle the deck
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)

    def get_card(self):
		# Deal one card from the top of the deck
        return self.cards.pop(0) if self.cards else None

# Represents a player's hand in the game
class PlayerHand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
		# Calculate the total value of the hand, accounting for Aces
        total = 0
        num_aces = 0

        for card in self.cards:
            if card.rank in ['J', 'Q', 'K']:
                total += 10
            elif card.rank == 'A':
                num_aces += 1
            else:
                total += int(card.rank)

        for _ in range(num_aces):
            total += 11 if total + 11 <= 21 else 1

        return total

    def is_blackjack(self): 
		 # Returns True if hand is a natural Blackjack (Ace + 10-point card)
        return len(self.cards) == 2 and self.calculate_value() == 21

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

# Main class to manage the Blackjack game flow
class BlackjackGame:
   def __init__(self):
        self.deck = Deck()
        self.player_hand = PlayerHand()
        self.dealer_hand = PlayerHand()
        self.player_name = ""
        self.round_number = 1
        self.games_played = 0

		# ✅ NEW: dictionary to store player score history
        self.player_scores = {}

        try:
            with open('blackjack_results.csv', 'r') as file:
                 pass
        except FileNotFoundError:
            with open('blackjack_results.csv', 'w') as file:
                file.write("Round,Player,Player_Score,Dealers_Score,Outcome\n")
         
   def start_game(self):
	    # Ask for player's name
        self.player_name = input("What's your name? ")
        print("\n\U0001F0CF \U0001F0CF \U0001F0CF")
        print("\n--- NEW GAME STARTED ---")
        print(f"Hello {self.player_name}, Welcome to Blackjack!")

        self.dealingCards()
        self.showCards()
        if self.check_initial_blackjack():
            self.declare_winner()
        else:
            self.playerCall()

   def dealingCards(self): # Deal two cards each to player and dealer
        for _ in range(2):
            self.player_hand.add_card(self.deck.get_card())
            self.dealer_hand.add_card(self.deck.get_card())

   def showCards(self): # Show player's cards and dealer's visible card
        print(f"\n{self.player_name}'s Cards: {self.player_hand}")
        print(f"Total value: {self.player_hand.calculate_value()}")

        print("\nDealer's Cards:")
        print(f"{self.dealer_hand.cards[0]}")
        print("Hidden card")

   def check_initial_blackjack(self): # Check if either player has blackjack at the start
        return self.player_hand.is_blackjack() or self.dealer_hand.is_blackjack()

   def playerCall(self): # Handle player's turn - hit or stand
        while self.player_hand.calculate_value() < 21:
            print(f"\nYour Current Hand: {self.player_hand}")
            print(f"Total Value: {self.player_hand.calculate_value()}")
            player_decision = input("Hit or Stand? (h/s): ").lower()

            if player_decision == 'h':
                card = self.deck.get_card()
                self.player_hand.add_card(card)
                print(f"You drew: {card}")
            elif player_decision == 's':
                print("You chose to stand. Dealer's turn now.")
                break
            else:
                print("Invalid input. Please choose 'h' or 's'.")

        if self.player_hand.calculate_value() > 21:
            self.declare_winner()
        else:
            self.dealerCall()

   def dealerCall(self): # Handle dealer's turn - must hit until reaching 17
        print("\nDealer's Turn:")

        while self.dealer_hand.calculate_value() < 17:
            card = self.deck.get_card()
            self.dealer_hand.add_card(card)
            print(f"Dealer draws: {card}")

        print("\nDealer's Final Hand:")
        for card in self.dealer_hand.cards:
            print(card)
        print(f"Dealer Total: {self.dealer_hand.calculate_value()}")

        self.declare_winner()

   def declare_winner(self): # Calculate final scores and determine winner
        player_total = self.player_hand.calculate_value()
        dealer_total = self.dealer_hand.calculate_value()
        outcome = "" # Initialize outcome variable to store result

        print("\n--- FINAL RESULTS ---")
        print(f"{self.player_name}'s Hand: {self.player_hand} → {player_total}")
        print(f"Dealer's Hand: {self.dealer_hand} → {dealer_total}")

        if self.player_hand.is_blackjack() and self.dealer_hand.is_blackjack():
            outcome = "Tie (Both Blackjack)"
            print("Both have BLACKJACK! It's a tie.")
        elif self.player_hand.is_blackjack():
            outcome = "Player Wins (Blackjack)"
            print(f"BLACKJACK! {self.player_name} wins!")
        elif self.dealer_hand.is_blackjack():
            outcome = "Dealer Wins (Blackjack)"
            print("Dealer has BLACKJACK! Dealer wins.")
        elif player_total > 21:
            outcome = "Dealer Wins (Player Bust)"
            print("You BUSTED! Dealer wins.")
        elif dealer_total > 21:
            outcome = "Player Wins (Dealer Bust)"
            print("Dealer BUSTED! You win!")
        elif player_total > dealer_total:
            outcome = f"Player Wins ({player_total} > {dealer_total})"
            print(f"You win, {self.player_name}!")
        elif player_total < dealer_total:
            outcome = f"Dealer Wins ({dealer_total} > {player_total})"
            print("Dealer wins.")
        else:
            outcome = f"Tie ({player_total})"
            print("It's a tie.")
            
        # Record the game result to file
        self.record_game_result(player_total, dealer_total, outcome)
        self.ask_newgame()

   def record_game_result(self, player_score, dealer_score, outcome):
        # Save the game result to the CSV file
        with open('blackjack_results.csv', 'a') as file:
            file.write(f"{self.round_number},{self.player_name},{player_score},{dealer_score},{outcome}\n")
        
        print(f"\n Game #{self.round_number} result saved to blackjack_results.csv")
        self.round_number += 1
        self.games_played += 1

   def ask_newgame(self):
		# Ask player if they want another round
        new_game = input("\nDo you want to play again? (y/n): ").lower()
        if new_game == 'y':
            self.__init__()
            self.start_game()
        else:
             if self.games_played > 0:
                print(f"\n--- SESSION SUMMARY ---")
                print(f"Player: {self.player_name}")
                print(f"Games played: {self.games_played}")
                print(f"Results saved to blackjack_results.csv")
                print("\nSee you Soon! \U00002660 Goodbye!\n \nTEAM BLACKJACK\n")

if __name__ == "__main__":
    game_begins = BlackjackGame()
    game_begins.start_game()
