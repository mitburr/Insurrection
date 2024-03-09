import random
from rich.prompt import Confirm


class Card:
    """Represents a role card in the game."""
    def __init__(self, name):
        self.name = name

class Player:
    """Represents a player in the game."""
    def __init__(self, name):
        self.name = name
        self.cards = []  # Holds the player's cards (influence)
        self.coins = 6   # Starting coins
        self.alive = True
        self.is_bot = True

    def lose_influence(self):
        """A player loses an influence (a card)."""
        if self.cards:
            card = self.cards.pop()
            print(f"{self.name} has lost an influence: {card.name}.")




class CoupGame:
    """Represents the Coup game."""
    def __init__(self, player_names):
        self.deck = [Card('Duke'), Card('Assassin'), Card('Captain'), Card('Ambassador'), Card('Contessa')] * 3
        self.players = [Player(name) for name in player_names]
        self.current_player_index = 0

        # Initial distribution of cards to players
        self.distribute_cards()

    def distribute_cards(self):
        """Distribute cards to players at the beginning."""
        random.shuffle(self.deck)
        for player in self.players:
            player.cards.append(self.deck.pop())
    
    def remove_defeated_player(self):
        for i, player in enumerate(self.players):
            if not player.cards and player.alive:
                player.alive = False

                return player
        return None
    
    def players_without_player(self, excluded_player):
        players_copy = self.players.copy()
        return [
            player
            for player in players_copy
            if player.alive and player.name != excluded_player.name
        ]

    def next_turn(self) -> bool:
        """Proceed to the next player's turn and the chosen execute basic action"""
        current_player = self.players[self.current_player_index]
        players_without_current_player = self.players_without_player(current_player)
        self.challenge_claim(current_player.name,"Duke")
#        print(f"\nalive? {current_player.alive} player? {current_player.name} index? {self.current_player_index}")
        if not current_player.alive:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            return True  # Skip players who have been eliminated
        elif current_player.coins >= 10:
            print(f"\nIt's {current_player.name}'s turn. They have more than 10 coins, and therefore must launch a coup.")
            self.handle_action(current_player, "coup")
        else:
            print(f"\nIt's {current_player.name}'s turn.")
            chosen_action = input(f"{current_player.name} what would you like to do on your turn?\n")
            self.handle_action(current_player, chosen_action)

        """Handle player loss"""
        while player := self.remove_defeated_player():
            if player.is_bot:
                print(f"\n{player.name} has crashed and burned.")
            else:
                print("\ngg scrub, gl next")
                gg = Confirm.ask("\nWould you like to watch the bots duke it out?")
                if not gg:
                    return False

        """Assess victory"""
        if sum(player.alive for player in self.players) == 1:
            print(f"{current_player.name}: 'I N V I C T U S !'")
            return False

        self.current_player_index = (self.current_player_index + 1) % len(self.players)

        return True


    def handle_action(self, player, action):
            """Allow a player to take an action."""
            actions = ["income", "foreign aid", "coup", "tax", "assassinate", "steal", "exchange"]
            print(f"\n{player.name} has chosen {action} for their turn.")
            if action == "income":
                player.coins += 1
                print(f"{player.name} takes 1 coin. Total coins: {player.coins}")
            elif action == "foreign aid":
                for p in self.players:
                    if p == player:
                        continue
                    if self.attempt_block(player, p, "Duke"):
                        break         
                player.coins += 2
                print(f"{player.name} takes 2 coins (foreign aid). Total coins: {player.coins}")
            elif action == "coup":
                if player.coins < 7:
                    print("Insufficient coins to coup. A coup costs 7 coins.")
                else:
                    player.coins -= 7
                    print(f"{player.name} has launched a coup. 7 coins have been spent.")
            elif action == "tax":
                if self.challenge_claim(player, "Duke"):
                    print(f"{player.name}'s tax action was challenged and failed!")
                    player.lose_influence()  # Assuming a failed challenge results in losing an influence
                else:
                    player.coins += 3
                    print(f"{player.name} collects 3 coins as tax.")
            elif action == "assassinate":
                if player.coins < 3:
                    print(f"{player.name} does not have enough coins to assassinate.")
                else:
                    target_name = input("Who would you like to assassinate? ")  # This would be a player input in a real game
                    target_player = next((p for p in self.players if p.name == target_name and p.alive), None)
                    if not target_player:
                        print("Invalid target.")
                    print(f"{player.name} is attempting to assassinate {target_player.name}.")
                    if self.attempt_block(player, target_player, "Contessa"):
                        print(f"{target_player.name}'s assassination was blocked!")
                    else:
                        player.coins -= 3
                        print(f"{player.name} spends 3 coins to assassinate {target_player.name}.")
                        target_player.lose_influence()

            # Additional logic for other actions would go here.

    def attempt_block(self, acting_player, blocker, role_name):
        # Prompt all other players if they want to block this action, claiming they have the blocking_role
        # For demonstration, simulate another player's decision to block
        blocking = input(f"\n{blocker.name} would you like to block? ")
        if blocking == "yes":
            print(f"{blocker.name} claims to have a {role_name} and attempts to block.")

            # Acting player can challenge the blocker's claim
            if self.challenge_claim(blocker.name, role_name):
                # Handle challenge outcome
                return False  # If the challenge is successful, the action goes through
            else:
                return True  # If the blocker's claim stands, the action is blocked
        elif blocking == "no":
            print(f"{blocker.name} has elected not to challenge")
        else:
            print("Please respond with yes or no.")
            self.attempt_block(acting_player, blocker)
        
    def challenge_claim(self, challenged_player_name, claimed_role):
        #
        # Find the challenged player object
        challenged_player = next(p for p in self.players if Confirm.ask(f"{p.name} would you like to challenge?"))
        
        # Check if the challenged player actually has the claimed role
        has_role = any(card.name == claimed_role for card in challenged_player.cards)
        if has_role:
            print(f"{challenged_player_name} reveals a {claimed_role} card. The challenge fails.")
            # In a real game, the challenged player would reshuffle the revealed card into the deck and draw a new one
            return False
        else:
            print(f"{challenged_player_name} could not reveal a {claimed_role} card. The challenge succeeds.")
            challenged_player.lose_influence()
            return True


    def show_game_state(self):
        """Display the current state of the game."""
        print("\nCurrent Game State:")
        for player in self.players:
            alive_status = "Alive" if player.alive else "Eliminated"
            print(f"{player.name} - {alive_status}, Coins: {player.coins}, Cards: {len(player.cards)}")

