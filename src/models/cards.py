color_map = {
    "Contessa": "deep_pink4",
    "Duke": "purple3",
    "Assassin": "black",
    "Captain": "dodger_blue3",
    "Ambassador": "spring_green4"
}

class Card:
    def __init__(self):
        self.card_type= ""
        self.actions={}

class Duke(Card):
    def __init__(self):
        super().__init__()
        self.card_type = "Duke"
        self.card_style= f"[{color_map[self.card_type]}]{self.card_type}[/]"



class Assassin(Card):
    def __init__(self):
        super().__init__()
        self.card_type = "Assassin"
        self.card_style= f"[{color_map[self.card_type]}]{self.card_type}[/]"



class Contessa(Card):
    def __init__(self):
        super().__init__()
        self.card_type = "Contessa"
        self.card_style= f"[{color_map[self.card_type]}]{self.card_type}[/]"