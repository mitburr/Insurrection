import random     
import time   
from rich.prompt import Prompt, Confirm

def decision(text, choices, player):
    if player.is_bot:
        print(f"{player.name} is thinking...\n")
        time.sleep(1)
        return random.choice(choices)
    else:
        if len(choices) == 2:
            return Confirm.ask(f"{text}", choices=choices)
        else:
            return Prompt.ask(text, choices=choices)

