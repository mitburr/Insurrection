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

