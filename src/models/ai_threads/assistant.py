from json import load
from pathlib import Path
from typing_extensions import override

from openai import OpenAI, AssistantEventHandler
from src.models.actions import Action
from src.models.players.base_model import Player
from openai.types.beta.threads import Text, TextDelta, Message


type Player_Resources = dict[str, int | str]

type Public_State = dict[ str, Player_Resources ]

assistant_instructions = """
You are an AI playing the game Coup: The Resistance. 
I will give you information about the game state and the character you're playing, and you should respond from the first person as if you're playing the game. 

Coup: The Resistance is won when all of your opponents have been forced to discard their cards.

This version of Coup: The Reistance only has access to three cards, including the Duke card, the Assassin card, and the Contessa card.
Additionally, the deck has an unlimited supply of all cards.


"""

initializing_instructions = """
In a message will be given a text string explaining the game resources that are currently available to you. 
Game resources include: 
 - coins 
 - Duke cards 
 - Assassin cards
 - Contessa cards. 

You will also be given a JSON information about your opponents including:
 - The player's name
 - The number of coins that player has
 - The number of cards that player has
 - Whether that player has been eliminated
This information will be formatted similarly to a JSON object.
 

You will also be given a list of possible choices called CHOICES.

Your response should exactly follow the format "I choose BLANK" where BLANK is an item from CHOICES
"""


"""

openai integration flow:
 - Create an Assistant. Assistants have custom instructions and a model. 
    Files and other tools can be added and toggled here.
 - Create a Thread, which is a user (in our case, a bot player) conversation with the Assistant.
    Threads keep message history, which can include text, images, and other files. Messages are stored a list on the Thread.
 - Add Messages to the Thread, which are user inputted prompts or questions.
 - Run the Assistant on the Thread to generate a response. 
"""

class Thread:
    def __init__(self, thread) -> None:
        self.openai_thread_object = thread
        self.id = thread.id

        # stream access variables
        self.decision = ""

class Assistant():
    def __init__(self) -> None:
        ##bootstrapping the client
        super().__init__()
        self.client = OpenAI()        
        self.__assistant = self.client.beta.assistants.create(
        name="Coup:The Resistance Game Master ",
        instructions=assistant_instructions,
        model="gpt-4-turbo-preview",
        )

        # exposing relevant variables
        self.id = self.__assistant.id

        # temp bot_thread instance for the bot which the assistant is currently engaging with.
        self.bot_thread: Thread



    def create_thread(self, player: Player) -> Thread:
        # Create the thread object, one instance of an AI 'conversation'
        openai_thread_object = self.client.beta.threads.create()

        # Initializing message with instructions on how interactions in this thread should proceed.
        self.client.beta.threads.messages.create(
        thread_id=openai_thread_object.id,
        role="user",
        content = f"{initializing_instructions}"
        )


        return Thread(openai_thread_object)


    def add_message(self, thread: Thread, game_state: Public_State, choices: list[Action], player: Player):
        """
        Adds a message to the given thread object.
        - thread: Thread object to add the message to. 
        - game_state: Public_State object containing the current resources for each player
        - choices: a list of Action objects to be parsed into a Message
        - player: the player object who's currently deciding on an action.
        """
        action_list = []
        player_data = {
            "name":player.name,
            "coins":player.coins,
            "cards":player.cards
        }
        for action in choices:
            action_list.append(action.action_type)
        message = self.client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"""You are playing as {player_data['name']} and have the following resources: {player_data}. CHOICES: {action_list}. Please respond with and "I choose" statement. (Examples: "I choose tax", "I choose assassinate"). Make sure that your statement does not include punctuation"""
        )

    def create_run(self, thread: Thread):
        self.bot_thread = thread

        with self.client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=self.id,
        event_handler=EventHandler()
        ) as stream:
            message = stream.get_final_messages()[0].content[0].text.value
            self._parse_choice(message)
            #print(stream.current_message_snapshot())
            stream.until_done()


    def _parse_choice(self, text: Text) -> bool | str:
        marker_index = text.find("I choose")
        if marker_index is not -1:
            self.bot_thread.decision = text.split()[marker_index+2]

class EventHandler(AssistantEventHandler):
    # event_handler class to pass to the stream function
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)
        
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=False)

#    def on_text_done(self, text):
#        _parse_choice(text)

    def on_text_created(self, text: Text):
        pass
    def on_text_delta(self, delta: TextDelta, snapshot: Text):
        pass
    def on_text_done(self, text: Text):
        pass



