from rich.prompt import Prompt, Confirm

from src.game_handler import CoupGame

def attempt_block(action, claimed_role, acting_player, blocker):
            """
            Handles attempts by players to block actions by claiming specific roles.
            - action: The action being blocked.
            - claimed_role: The role claimed by the blocker to stop the action.
            - acting_player: The player performing the action.
            - blocker: The player attempting to block the action.
            """
            players_without_blocker = CoupGame.players_without_player(blocker)
            print(f"{blocker.name} claims to have a {claimed_role} and attempts to block {action}.")
            # Check if the acting player or other players want to challenge the blocker's claim
            challenger = next(p for p in players_without_blocker if Confirm.ask(f"{p.name} would you like to challenge?"))
            if challenger:
                # Process the challenge
                if challenge_action( blocker, claimed_role, acting_player):
                    print(f"The challenge against {blocker.name}'s claim was successful. {blocker.name} failed to reveal a(n) {claimed_role} loses an influence.")
                    blocker.lose_influence()
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
    print(f"{challenged_player.name}'s claim to have a {claimed_role} is being challenged.")
    # Check if the challenged player has the claimed role
    has_role = any(card.name == claimed_role for card in challenged_player.cards)
    if has_role:
        print(f"{challenged_player.name} reveals a {claimed_role} card, proving their claim.")
        challenging_player.lose_influence()
        return False  # The challenge fails because the claim was true.
    else:
        print(f"{challenged_player.name} could not prove their claim and loses an influence.")
        challenged_player.lose_influence()
        return True  # The challenge succeeds because the claim was false.
