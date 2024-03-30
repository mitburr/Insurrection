from rich import print

from src.models.display import decision

actions = ["income", "foreign aid", "coup", "tax", "assassinate"]


class Action:
    def __init__(self, player):
        self.action_type = ""
        self.challenge = False # Boolean for whether the action can be challenged (is a )
        self.block = False # Boolean for whether the action is blockable
        self.active_player = player # A Player Object, owner of the action

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
        self.block = True
    
    def foreign_aid_action(self, block_card, players_without_player):
        """
        Adds 2 coins to the player's inventory
        Foreign Aid is available to all plays and can be blocked
        """
        blocking_player = next((p for p in players_without_player(self.active_player) if decision(f"{p.name} would you like to block?", ["y","n"], p)), False)
        if attempt_block(self.action_type, block_card, self.active_player, blocking_player, players_without_player(blocking_player)):                    
            print(f"{self.active_player.name}'s foreign aid action was blocked by {blocking_player.name} and failed!")                 
        else:
            self.active_player.coins += 2
            print(f"{self.active_player.name} takes 2 [grey30]coins[/] (foreign aid). Total [grey30]coins[/]: {self.active_player.coins}")

class Coup(Action):
    def __init__(self, player):
        super().__init__(player)
        self.action_type = "coup"
    
    def coup_action(self, players_without_player):
        players_without_current_player = players_without_player(self.active_player)
        coup_target_name = decision(f"Which player would you like to launch a coup against?", [p.name for p in players_without_current_player], self.active_player)
        coup_target = next(p for p in players_without_current_player if p.name == coup_target_name)
        self.active_player.coins -= 7
        print(f"{self.active_player.name} has launched a coup against {coup_target.name}. 7 [grey30]coins[/] have been spent.")
        coup_target.lose_influence()

class Tax(Action):
    def __init__(self, player):
        super().__init__(player)
        self.action_type = "tax"
        self.challenge = True

    def tax_action(self, claimed_role, players_without_player):
        players_without_current_player = players_without_player(self.active_player)
        challenging_player = next((p for p in players_without_current_player if decision(f"{p.name} would you like to challenge?", ["y","n"], p)), False)
        if challenge_action(self.active_player, claimed_role, challenging_player):
            return
        else:
            self.active_player.coins += 3
            print(f"{self.active_player.name} collects 3 [grey30]coins[/] as tax.")

class Assassinate(Action):
    def __init__(self, player):
        super().__init__(player)
        self.action_type = "assassinate"
    
    def assassinate_action(self, claimed_role, blocker_role, players_without_player):
        players_without_current_player = players_without_player(self.active_player)
        target_name = decision("Who would you like to assassinate?", [p.name for p in players_without_current_player], self.active_player)                        
        print(f"{self.active_player.name} is attempting to assassinate {target_name}")
        challenging_player = next((p for p in players_without_current_player if decision(f"{p.name} would you like to challenge?", ["y","n"], p)), False)
        if challenge_action(self.active_player, claimed_role , challenging_player):
            return
        else:
            self.active_player.coins -= 3  
            target_player = next((p for p in players_without_current_player if p.name == target_name and p.alive), None)
            blocking_player = decision(f"{self.active_player.name} is attempting to assassinate {target_player.name}. Would you like to block your own assassination?", ["y","n"], target_player)
            if blocking_player & attempt_block(self.action_type, blocker_role, self.active_player, target_player, players_without_player(target_player)):
                print(f"{target_player.name}'s assassination was blocked! They still lose 3 [grey30]coins[/]")
            else:
                print(f"{self.active_player.name} spends 3 [grey30]coins[/] to assassinate {target_player.name}.")
                target_player.lose_influence()

def attempt_block(action, claimed_role, acting_player, blocker, players_without_blocker):
            """
            Handles attempts by players to block actions by claiming specific roles.
            - action: The action being blocked.
            - claimed_role: The role claimed by the blocker to stop the action.
            - acting_player: The player performing the action.
            - blocker: The player attempting to block the action.
            - players_without_blocker: List of player objects without the blocking player
            """

            if not blocker:
                return

            print(f"{blocker.name} claims to have a {claimed_role.card_style} and attempts to block {action}.")
            # Check if the acting player or other players want to challenge the blocker's claim
            challenger = next((p for p in players_without_blocker if decision(f"{p.name} would you like to challenge?", ["y","n"], p)), False)
            if challenger:
                # Process the challenge
                if challenge_action(blocker, claimed_role, challenger):
                    return False  # The block is unsuccessful, and the action proceeds.
                else:
                    print(f"The challenge against {blocker.name}'s claim failed. The action is blocked.")
                    # Optional: The challenger could lose an influence here if implementing that rule.
            return True  # The block stands, and the action is blocked without challenge or if the challenge fails.

def challenge_action( challenged_player, claimed_role, challenging_player):
    """
    Handles challenges to players' role claims.
    - challenged_player: The player whose role claim is being challenged.
    - claimed_role: The role that has been claimed and is challenged.
    - challenging_player: the player who's doubting the challenged player's role
    """
    if not challenging_player:
        return
    print(f"{challenging_player.name} is challenging {challenged_player.name}'s claim to have a {claimed_role.card_style}")
    # Check if the challenged player has the claimed role
    has_role = any(card.card_type == claimed_role.card_type for card in challenged_player.cards)
    if has_role:
        print(f"{challenged_player.name} reveals a {claimed_role.card_style} card, proving their claim.")
        challenging_player.lose_influence()
        return False  # The challenge fails because the claim was true.
    else:
        print(f"The challenge against {challenged_player.name}'s claim was successful. {challenged_player.name} failed to reveal a {claimed_role.card_style} and lost an influence.")
        challenged_player.lose_influence()
        return True  # The challenge succeeds because the claim was false.
