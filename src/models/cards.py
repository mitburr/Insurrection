"""from enum import Enum

class CardType(str, Enum):
    contessa = "Contessa" #red
    duke = "Duke" #purple
    assassin = "Assassin" #black
    captain = "Captain" #blue
    ambassador = "Ambassador" #green"""

color_map = {
    "Contessa": "deep_pink4",
    "Duke": "purple3",
    "Assassin": "black",
    "Captain": "dodger_blue3",
    "Ambassador": "spring_green4"
}

class Card:
    def __init__(self, type):
        self.card_type= type
        self.card_style= f"[{color_map[type]}]{type}[/]"
