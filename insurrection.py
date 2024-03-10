from rich.console import Console
from rich.prompt import Confirm

from src.game_handler import CoupGame 

console = Console()
console.clear()



def main():

    game_running = Confirm.ask("Wanna play a janky Coup knockoff?")
    while game_running:

        ur_winning = True            
        player_names = ["VerySmartAndCool VolterEmployee", "Alice", "Bob", "Charlie" ]
        game = CoupGame(player_names)
        
        while ur_winning:
            game.show_game_state()
            ur_winning = game.next_turn()


        game_running = Confirm.ask("Do you want to play again?")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\ngg scrub")


"""
1. I took the game phases as action, challenge, and block. They're represented as methods.
2. Restart instantiated here.
3.
4.
5.
6.
7.
8.

Shortcuts:
Only functional classes are Duke, Contessa, and Assassin
when players rebuke a challenge successfully they do not redraw a card

"""