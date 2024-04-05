import random
from rich import print

from src.models.actions import Action, Income, Foreign_Aid, Coup, Tax, Assassinate
from src.models.display import decision
from src.models.cards import Duke, Contessa, Assassin
from src.models.players.base_model import Player
from src.models.players.bot import Bot

type Player_Resources = dict[str, int | str]

type Public_State = dict[ str, Player_Resources ]

type Player_Chat = tuple[ Player, str ]

type Chat_History = list[ Player_Chat ]


class CoupGame:
    

    """this object is a list of players, and a list of the game resources that player controls."""

    """Represents the Coup game."""
    def __init__(self, player_names):
        self.deck = [Duke(), Assassin(), Contessa()] * 100
        self.players = []
        for name in player_names:
            if name == "VerySmartAndCool VolterEmployee":
                self.players.append(Player(name, True))
            else:
                self.players.append(Bot(name, True))
        self.current_player_index = 0
        self.player_states = self.generate_game_state()
        self.game_chat_history = []
        self.turn_chat_history : Chat_History = []


        # Initial distribution of cards to players
        self.distribute_cards()

    def distribute_cards(self):
        """Distribute cards to players at the beginning."""
        random.shuffle(self.deck)
        for player in self.players:
            if player.name == "VerySmartAndCool VolterEmployee":
                player.cards.append(Duke())
                player.cards.append(Contessa())
                player.cards.append(Assassin())
            player.cards.append(self.deck.pop())
            player.cards.append(self.deck.pop())

    def remove_defeated_player(self):
        for i, player in enumerate(self.players):
            if not player.cards and player.alive:
                player.alive = False

                return player
        return None
    
    def players_without_player(self, excluded_player):
        if not excluded_player:
            return
        players_copy = self.players.copy()
        return [
            player
            for player in players_copy
            if player.alive and player.name != excluded_player.name
        ]

    def record_chat(self, player: Player) -> None:
        self.turn_chat_history.append((player, player.chat))

    def record_turn_chat_history(self) -> None:
        self.game_chat_history.append(self.turn_chat_history)
        self.turn_chat_history = []

    def next_turn(self) -> bool:
        """Proceed to the next player's turn and the chosen execute basic action"""
        current_player = self.players[self.current_player_index]
        if not current_player.alive:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            return True  # Skip players who have been eliminated
        else:
            print(f"\nIt's {current_player.name}'s turn.")
            self.handle_action(current_player)

        """Handle player loss"""
        while player := self.remove_defeated_player():
            if player.is_bot:
                print(f"\n{player.name} has crashed and burned.")
            else:
                print("\ngg scrub, gl next")
                gg = decision("\nWatch the bots duke it out?", ["y","n"], player)
                if not gg:
                    return False

        """Assess victory"""
        if sum(player.alive for player in self.players) == 1:
            print(f"{current_player.name}: 'I N V I C T U S !'")
            return False

        self.current_player_index = (self.current_player_index + 1) % len(self.players)

        return True


    def handle_action(self, player):

            """Refresh player states data"""
            self.player_states = self.generate_game_state()

            """Player Logic"""
 #           action = decision(f"{player.name} what would you like to do on your turn?\n", actions, player)

            """Bot action decision"""
            action = player.decision(self.player_states)
            self.record_chat(player)


            print(f"\n{player.name} has chosen {action.action_type} for their turn.")
            
            match action.action_type:
                case "income":
                    Income(player).income_action()
                case "foreign_aid":
                    Foreign_Aid(player).foreign_aid_action(self.players_without_player)
                case "coup":
                    Coup(player).coup_action(self.players_without_player)
                case "tax":
                    Tax(player).tax_action( self.players_without_player)
                case "assassinate":
                    Assassinate(player).assassinate_action(self.players_without_player)


            # Additional logic for other actions would go here.


    def display_game_state(self):
        """Display the current state of the game."""
        print("\nCurrent Game State:")
        for player in self.players:
            alive_status = "Alive" if player.alive else "Eliminated"
            if player.is_bot:
                print(f"{player.name} - {alive_status}, [grey30]Coins[/]: {player.coins}, Cards: ")
                print('\n'.join(card.card_style for card in player.cards)) 
            else:
                print(f"\n{player.name} - {alive_status}, [grey30]Coins[/]: {player.coins}, Cards: {len(player.cards)}. Your cards are:\n")
                print('\n'.join(card.card_style for card in player.cards)) 


    def generate_game_state(self) -> Public_State:
        contemporary_state = {}
        for player in self.players:
            alive_status = "Alive" if player.alive else "Eliminated"
            player_resources = {
                "coins": player.coins,
                "cards": len(player.cards),
                "player_status": alive_status
            }
            contemporary_state[player.name] = player_resources
        return contemporary_state
            
"""
each player has their own thread
each thread should have to available information
available information should include:
    player state data (coins, cards)
    previous actions and statements from all other players

bot player creation will happen in game setup:
    only one Assistant is needed, the assistant will create a thread for each Player instance. 
"""