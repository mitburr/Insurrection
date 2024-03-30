from src.models.actions import Income, Foreign_Aid, Coup
from rich import print


class Player:
    """Represents a player in the game."""
    def __init__(self, name, bot):
        self.name = name
        self.cards = []  # Holds the player's cards (influence)
        self.coins = 7   # Starting coins
        self.alive = True
        self.is_bot = bot
        self.basic_actions = {
            "income": Income(self),
            "foreign aid": Foreign_Aid(self),
            "coup": Coup(self) 
        }

    def lose_influence(self):
        """A player loses an influence (a card)."""
        if self.cards:
            card = self.cards.pop()
            print(f"{self.name} has lost an influence: {card.card_style}.")
"""
import random     
import time   
from rich.prompt import Prompt, Confirm

def decision(text, choices, player):
    if player.is_bot:
        print(f"{player.name} is thinking...\n")
        time.sleep(1)
        if choices == ["y", "n"]:
            return random.choice([True, False])
        return random.choice(choices)
    else:
        if choices == ["y","n"]:
            return Confirm.ask(f"{text}")
        else:
            return Prompt.ask(text, choices=choices)
"""


    
