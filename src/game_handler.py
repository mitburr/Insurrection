import random
from rich.prompt import Prompt, Confirm
from rich import print

from src.models.actions import attempt_block, challenge_action
from src.models.display import decision
from src.models.cards import Card


class Player:
    """Represents a player in the game."""
    def __init__(self, name, bot):
        self.name = name
        self.cards = []  # Holds the player's cards (influence)
        self.coins = 7   # Starting coins
        self.alive = True
        self.is_bot = bot

    def lose_influence(self):
        """A player loses an influence (a card)."""
        if self.cards:
            card = self.cards.pop()
            print(f"{self.name} has lost an influence: {card.name}.")




class CoupGame:
    """Represents the Coup game."""
    def __init__(self, player_names):
        self.deck = [Card('Duke'), Card('Assassin'), Card('Captain'), Card('Ambassador'), Card('Contessa')] * 3
        self.players = []
        for name in player_names:
            if name == "genius":
                self.players.append(Player(name, False))
            else:
                self.players.append(Player(name, True))
        self.current_player_index = 0

        # Initial distribution of cards to players
        self.distribute_cards()

    def distribute_cards(self):
        """Distribute cards to players at the beginning."""
        random.shuffle(self.deck)
        for player in self.players:
            player.cards.append(self.deck.pop())
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
        print(current_player.cards[1].card_style)
        players_without_current_player = self.players_without_player(current_player)
        if not current_player.alive:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            return True  # Skip players who have been eliminated
        elif current_player.coins >= 10:
            print(f"\nIt's {current_player.name}'s turn. They have more than 10 coins, and therefore must launch a coup.")
            self.handle_action(current_player, "coup")
        else:
            print(f"\nIt's {current_player.name}'s turn.")
            self.handle_action(current_player)

        """Handle player loss"""
        while player := self.remove_defeated_player():
            if player.is_bot:
                print(f"\n{player.name} has crashed and burned.")
            else:
                print("\ngg scrub, gl next")
                gg = Confirm.ask("\nWatch the bots duke it out?")
                if not gg:
                    return False

        """Assess victory"""
        if sum(player.alive for player in self.players) == 1:
            print(f"{current_player.name}: 'I N V I C T U S !'")
            return False

        self.current_player_index = (self.current_player_index + 1) % len(self.players)

        return True


    def handle_action(self, player, action=""):
            players_without_current_player = self.players_without_player(player)
            if action == "coup":
                coup_target_name = Prompt.ask(f"Which player would you like to launch a coup against?", choices= [p.name for p in players_without_current_player])
                coup_target = next(p for p in players_without_current_player if p.name == coup_target_name)
                player.coins -= 7
                print(f"{player.name} has launched a coup against {coup_target.name}. 7 coins have been spent.")
                coup_target.lose_influence()
                return


            """Allow a player to take an action."""
            actions = ["income", "foreign aid", "coup", "tax", "assassinate"]
            action = decision(f"{player.name} what would you like to do on your turn?\n", actions, player)
            #Prompt.ask(f"{player.name} what would you like to do on your turn?\n",choices=actions)
            print(f"\n{player.name} has chosen {action} for their turn.")
            if action == "income":
                player.coins += 1
                print(f"{player.name} takes 1 coin. Total coins: {player.coins}")
            elif action == "foreign aid":
                blocking_player = next((p for p in players_without_current_player if decision(f"{p.name} would you like to block?", ["y","n"], p)), False)
                if blocking_player.alive & attempt_block( action, "Card('Duke').card_style", player, blocking_player, self.players_without_player(blocking_player)):                    
                    print(f"{player.name}'s foreign aid action was blocked by {blocking_player.name} and failed!")                 
                else:
                    player.coins += 2
                    print(f"{player.name} takes 2 coins (foreign aid). Total coins: {player.coins}")
            elif action == "coup":
                if player.coins < 7:
                    print("Insufficient coins to launch a coup. A coup costs 7 coins.")
                    self.handle_action(player)
                else:
                    coup_target_name = decision(f"Which player would you like to launch a coup against?", [p.name for p in players_without_current_player], player)
                    coup_target = next(p for p in players_without_current_player if p.name == coup_target_name)
                    player.coins -= 7
                    print(f"{player.name} has launched a coup against {coup_target.name}. 7 coins have been spent.")
                    coup_target.lose_influence()
            elif action == "tax":
                challenging_player = next((p for p in players_without_current_player if Confirm.ask(f"{p.name} would you like to challenge?", choices=["y","n"])), False)
                if challenging_player:
                    challenge_action(player, "Card('Duke').card_style", challenging_player) 
                else:
                    player.coins += 3
                    print(f"{player.name} collects 3 coins as tax.")
            elif action == "assassinate":
                if player.coins < 3:
                    print(f"{player.name} does not have enough coins to assassinate.")
                    self.handle_action(player)
                else:
                    target_name = decision("Who would you like to assassinate?", [p.name for p in players_without_current_player], player)                        
                    print(f"{player.name} is attempting to assassinate {target_name}")
                    challenging_player = next((p for p in players_without_current_player if Confirm.ask(f"{p.name} would you like to challenge?", choices=["y","n"])), False)
                    if challenging_player and challenge_action(player, "Assassin", challenging_player):
                        return
                    else:
                        player.coins -= 3  
                        target_player = next((p for p in self.players if p.name == target_name and p.alive), None)
                        blocking_player = Confirm.ask(f"{player.name} is attempting to assassinate {target_player.name}. Would you like to block your own assassination?", choices=["y","n"])
                        if blocking_player & attempt_block(action, "Contessa", player, target_player, self.players_without_player(target_player)):
                            print(f"{target_player.name}'s assassination was blocked! They still lose 3 coins")
                        else:
                            print(f"{player.name} spends 3 coins to assassinate {target_player.name}.")
                            target_player.lose_influence()

            # Additional logic for other actions would go here.


    def show_game_state(self):
        """Display the current state of the game."""
        print("\nCurrent Game State:")
        for player in self.players:
            alive_status = "Alive" if player.alive else "Eliminated"
            print(f"{player.name} - {alive_status}, Coins: {player.coins}, Cards: {len(player.cards)}")

