import random     
import time

from src.models.players.base_model import Player
from src.models.actions import Action, Income, Foreign_Aid, Coup, Assassinate, Tax
from src.models.ai_threads.assistant import Assistant
from openai.types.beta.threads import Text, TextDelta
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta
#from rich.prompt import Prompt, Confirm
_assistant = Assistant()

# when running a bot's stream the bot's Thread instance is passed to the Assistant's bot_thread variable.

type Player_Resources = dict[str, int | str]

type Public_State = dict[ str, Player_Resources ]

class Bot(Player):
    def __init__(self, name, bot):
        super().__init__(name, bot)
        self.thread = _assistant.create_thread(self)
    
    
    def generate_action_choices(self) -> list[Action]:
        choices = [Income(Player), Tax(Player)]
        if self.coins >= 3:
            choices.append(Assassinate(Player))
        if self.coins >= 7:
            choices.append(Coup(Player))
        if self.coins >= 10:
            choices = [Coup(Player)]
            return choices

        return choices

    def decision(self, game_state: Public_State,  choices: str=""):

        print(f"{self.name} is thinking...\n")
 #       time.sleep(1)
        if choices == ["y", "n"]:
            return random.choice([True, False])
        
        choices = self.generate_action_choices()
        _assistant.add_message(self.thread, game_state, choices, self)
        _assistant.create_run(self.thread)

#        print(f"\n Decision: {self.thread.decision}\n Player: {self.name}\n Actions:{choices}")
        self.record_chat(self.thread.newest_chat)
        decision = next(action for action in choices if action.action_type == self.thread.decision)

        return decision
    
