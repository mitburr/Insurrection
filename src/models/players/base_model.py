from rich import print


class Player:
    """Represents a player in the game."""
    def __init__(self, name, bot):
        self.name = name
        self.cards = []  # Holds the player's cards (influence)
        self.coins = 3   # Starting coins
        self.alive = True
        self.is_bot = bot


    def lose_influence(self):
        """A player loses an influence (a card)."""
        if self.cards:
            card = self.cards.pop()
            print(f"{self.name} has lost an influence: {card.card_style}.")

    
