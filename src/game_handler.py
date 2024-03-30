import random
from rich import print

from src.models.actions import Tax, Assassinate, attempt_block, challenge_action
from src.models.display import decision
from src.models.cards import Duke, Contessa, Assassin
from src.models.players.model import Player


class CoupGame:
    """Represents the Coup game."""
    def __init__(self, player_names):
        self.deck = [Duke(), Assassin(), Contessa()] * 100
        self.players = []
        for name in player_names:
            if name == "VerySmartAndCool VolterEmployee":
                self.players.append(Player(name, True))
            else:
                self.players.append(Player(name, True))
        self.current_player_index = 0

        # Initial distribution of cards to players
        self.distribute_cards()

    def distribute_cards(self):
        """Distribute cards to players at the beginning."""
        random.shuffle(self.deck)
        for player in self.players:
            if player.name == "VerySmartAndCool VolterEmployee":
                player.cards.append(Duke())
                player.cards.append(Contessa())
                player.cards.append(Assassin())
            player.cards.append(self.deck.pop())
            player.cards.append(self.deck.pop())

    def remove_defeated_player(self):
        for i, player in enumerate(self.players):
            if not player.cards and player.alive:
                player.alive = False

                return player
        return None
    
    def players_without_player(self, excluded_player):
        if not excluded_player:
            return
        players_copy = self.players.copy()
        return [
            player
            for player in players_copy
            if player.alive and player.name != excluded_player.name
        ]

    def next_turn(self) -> bool:
        """Proceed to the next player's turn and the chosen execute basic action"""
        current_player = self.players[self.current_player_index]
        if not current_player.alive:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            return True  # Skip players who have been eliminated
        elif current_player.coins >= 10:
            print(f"\nIt's {current_player.name}'s turn. They have more than 10 [grey30]coins[/], and therefore must launch a coup.")
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
                gg = decision("\nWatch the bots duke it out?", ["y","n"], player)
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
                coup_target_name = decision(f"Which player would you like to launch a coup against?", [p.name for p in players_without_current_player], player)
                coup_target = next(p for p in players_without_current_player if p.name == coup_target_name)
                player.coins -= 7
                print(f"{player.name} has launched a coup against {coup_target.name}. 7 [grey30]coins[/] have been spent.")
                coup_target.lose_influence()
                return


            """Allow a player to take an action."""
            actions = ["income", "foreign aid", "coup", "tax", "assassinate"]
            action = decision(f"{player.name} what would you like to do on your turn?\n", actions, player)
            print(f"\n{player.name} has chosen {action} for their turn.")
            if action == "income":
                player.basic_actions[action].income_action()
            elif action == "foreign aid":
                player.basic_actions[action].foreign_aid_action(Duke(), self.players_without_player)
            elif action == "coup":
                if player.coins < 7:
                    print("Insufficient [grey30]coins[/] to launch a coup. A coup costs 7 [grey30]coins[/].")
                    self.handle_action(player)
                else:
                    coup_target_name = decision(f"Which player would you like to launch a coup against?", [p.name for p in players_without_current_player], player)
                    coup_target = next(p for p in players_without_current_player if p.name == coup_target_name)
                    player.coins -= 7
                    print(f"{player.name} has launched a coup against {coup_target.name}. 7 [grey30]coins[/] have been spent.")
                    coup_target.lose_influence()
            elif action == "tax":
                Tax(player).tax_action( Duke() , self.players_without_player)
            elif action == "assassinate":
                Assassinate(player).assassinate_action(Assassin(), Contessa(), self.players_without_player)


            # Additional logic for other actions would go here.


    def show_game_state(self):
        """Display the current state of the game."""
        print("\nCurrent Game State:")
        for player in self.players:
            alive_status = "Alive" if player.alive else "Eliminated"
            if player.is_bot:
                print(f"{player.name} - {alive_status}, [grey30]Coins[/]: {player.coins}, Cards: {len(player.cards)}")
            else:
                print(f"\n{player.name} - {alive_status}, [grey30]Coins[/]: {player.coins}, Cards: {len(player.cards)}. Your cards are:\n")
                for card in player.cards:
                    print(f"{card.card_style}\n")
