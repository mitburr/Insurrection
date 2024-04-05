from rich import print

type Player_Chat = tuple[ Player, str ]

class Player:
    """Represents a player in the game."""
    def __init__(self, name, bot):
        self.name = name
        self.cards = []  # Holds the player's cards (influence)
        self.coins = 3   # Starting coins
        self.alive = True
        self.is_bot = bot
        self.chat = Player_Chat


    def lose_influence(self):
        """A player loses an influence (a card)."""
        if self.cards:
            card = self.cards.pop()
            print(f"{self.name} has lost an influence: {card.card_style}.")

    def record_chat(self, text: str) -> None:
        """
        Records most recent instance of a bot's text
            - text: the chat to be recorded.
        """
        new_chat = (self, text)
        self.chat = new_chat

    
