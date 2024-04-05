from rich import print
from types import FunctionType

from src.models.display import decision
from src.models.cards import Card, Duke, Contessa, Assassin
from src.models.players.base_model import Player

actions = ["income", "foreign aid", "coup", "tax", "assassinate"]


class Action:
    def __init__(self, player):
        self.action_type = ""
        self.action_card = None
        self.challenge = False # Boolean for whether the action can be challenged
        self.active_player = player # A Player Object, owner of the action
        self.bluff = bool #Indicates whether this choice would be a bluff based on the player's current cards. 


    def block_phase(self, players_without_player: FunctionType, target_player: Player = None ) -> tuple[bool,Player]:
        """
        Handles attempts by players to block actions by claiming specific roles.
        - players_without_blocker: List of player objects without the blocking player
        - target_player: Optional param if target of the block is attempting to assassinate. 
        """

        # Determine if a player wishes to block.
        # Assassinate can only be blocked by the target.  
        if self.action_card == Assassin():
            blocking_player = decision(f"{self.active_player.name} is attempting to assassinate {target_player.name}. Would you like to block your own assassination?", ["y","n"], target_player)
        else:
            blocking_player = next((p for p in players_without_player(self.active_player) if decision(f"{p.name} would you like to block?", ["y","n"], p)), False)

        if not blocking_player:
            return False, blocking_player
        
        print(f"{blocking_player.name} claims to have a {self.blocking_card.card_style} and attempts to block {self.active_player.name}'s {self.action_type}.")

        # Determine if anyone wishes to challenge the block. 
        challenge, challenging_player = self.challenge_phase(blocking_player, self.blocking_card, players_without_player)
        if challenge:
            return False, challenging_player  # The challenge to the block is successful, and the original action proceeds unblocked.
        else:
            print(f"The challenge against {blocking_player.name}'s claim failed. The block proceeds unchallenged.")
            # Optional: The challenger could lose an influence here if implementing that rule.
            return True, blocking_player  # The block stands, and the action is blocked without challenge or if the challenge fails.

    def challenge_phase(self, challenged_player: Player, claimed_role: Card, players_without_player: FunctionType) -> tuple[bool, Player]:
        """
        Handles challenges to players' role claims.
        - challenged_player: The player whose role claim could be challenged.
        - claimed_role: The role that has been claimed and is challenged.
        - players_without_player: Function which builds an array of players excluding the param player. 
        """
        # Determine if a player would like to challenge.
        challenging_player = next((p for p in players_without_player(challenged_player) if decision(f"{p.name} would you like to challenge {challenged_player.name}'s claimed to influence a {self.action_type}?", ["y","n"], p)), False)
        if not challenging_player:
            print(f"\n {challenging_player} \n")
            return False, challenging_player
        print(f"\n {challenging_player.name} \n")

        print(f"{challenging_player.name} is challenging {challenged_player.name}'s claim to have a {claimed_role.card_style}")
        # Check if the challenged player has the claimed role
        has_role = any(card.card_type == claimed_role.card_type for card in challenged_player.cards)
        if has_role:
            print(f"{challenged_player.name} reveals a {claimed_role.card_style} card, proving their claim.")
            challenging_player.lose_influence()
            return False, challenging_player # The challenge fails because the claim was true.
        else:
            print(f"The challenge against {challenged_player.name}'s claim was successful. {challenged_player.name} failed to reveal a {claimed_role.card_style} and lost an influence.")
            challenged_player.lose_influence()
            return True, challenging_player  # The challenge succeeds because the claim was false.

class Income(Action):
    def __init__(self, player):
        super().__init__( player)
        self.action_type = "income"

    def income_action(self):
            """
            Adds 1 coin to the player's inventory
            Income action is available to all players and it cannot be blocked. 
            """
            self.active_player.coins += 1
            print(f"{self.active_player.name} takes 1 coin. Total [grey30]coins[/]: {self.active_player.coins}")

class Foreign_Aid(Action):
    def __init__(self, player):
        super().__init__(player)
        self.action_type = "foreign_aid"
        self.blocking_card = Duke()
    
    def foreign_aid_action(self, players_without_player):
        """
        Adds 2 coins to the player's inventory
        Foreign Aid is available to all players and can be blocked by a player influencing a Duke. 
        """
        block, blocking_player = self.block_phase( players_without_player)
        if block:                    
            print(f"{self.active_player.name}'s foreign aid action was blocked by {blocking_player.name} and failed!")                 
        else:

            self.active_player.coins += 2
            print(f"{self.active_player.name} takes 2 [grey30]coins[/] (foreign aid). Total [grey30]coins[/]: {self.active_player.coins}")

class Coup(Action):

    def __init__(self, player):
        super().__init__(player)
        self.action_type = "coup"
    
    def coup_action(self, players_without_player):
        """
        Launches a coup against an opponent, forcing them to discard an influence. 
        A coup is available to all players, costs 7 coins, and cannot be blocked. 
        """
        players_without_current_player = players_without_player(self.active_player)
        coup_target_name = decision(f"Which player would you like to launch a coup against?", [p.name for p in players_without_current_player], self.active_player)
        coup_target = next(p for p in players_without_current_player if p.name == coup_target_name)
        self.active_player.coins -= 7
        print(f"{self.active_player.name} has launched a coup against {coup_target.name}. 7 [grey30]coins[/] have been spent.")
        coup_target.lose_influence()

class Tax(Action):
    def __init__(self, player):
        super().__init__(player)
        self.action_card = Duke()
        self.action_type = "tax"
        self.challenge = True

    def tax_action(self, players_without_player):
        """
        Adds 3 coins to the player's inventory
        Tax is only available to a player influencing a Duke, and therefore can be challenged. 
        """
        challenge, challenging_player = self.challenge_phase(self.active_player, self.action_card, players_without_player)
        if challenge:
            return
        else:
            self.active_player.coins += 3
            print(f"{self.active_player.name} collects 3 [grey30]coins[/] as tax.")

class Assassinate(Action):
    def __init__(self, player):
        super().__init__(player)
        self.action_card = Assassin()
        self.action_type = "assassinate"
        self.blocking_card = Contessa()
    
    def assassinate_action(self, players_without_player):
        """
        Forces a player to discard an influence
        Assassinate costs 3 coins, is only available to players influencing an assassin, and therefore can be challenged.
        Assassinate can also be blocked if the target player influences a Contessa. 
        """
        # Identify assassinate target
        players_without_current_player = players_without_player(self.active_player)
        target_name = decision("Who would you like to assassinate?", [p.name for p in players_without_current_player], self.active_player)                        
        print(f"{self.active_player.name} is attempting to assassinate {target_name}")
        
        # Challenge phase for the assassinate action
#        challenging_player = next((p for p in players_without_current_player if decision(f"{p.name} would you like to challenge?", ["y","n"], p)), False)
        challenge, challenging_player = self.challenge_phase(self.active_player, self.action_card, players_without_player)
        if challenge:
            return
        else:
            self.active_player.coins -= 3  
            target_player = next((p for p in players_without_current_player if p.name == target_name and p.alive), None)
            # Block phase for the assassination target
            block, blocking_player = self.block_phase(players_without_player, target_player)
            if block:
                print(f"{target_player.name}'s assassination blocked their own assassination! {self.active_player.name} still lose 3 [grey30]coins[/]")
            else:
                print(f"{self.active_player.name} spends 3 [grey30]coins[/] to assassinate {target_player.name}.")
                target_player.lose_influence()
