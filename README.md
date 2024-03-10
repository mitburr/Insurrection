# Insurrection: Off-Brand "The Resistance: Coup" [^1]

## Usage

Be sure you have Python 3.11 installed, and probably do a full system update since I'll bet you haven't in at least a month[^2]

1. clone the repo
   ```bash
   git clone git@github.com:mitburr/Insurrection.git
   cd Insurrection
   ```
2. Install dependencies with poetry
   `poetry install`
3. Run the game
   `python insurrection.py`

## Gameplay

The game's rules can be found [here](https://www.ultraboardgames.com/coup/game-rules.php). This is a simplified version of the original Coup.

- You will play against 3 opponents, and your name will be VerySmartAndCool VolterEmployee. Sick name btw, wish it were mine.
- Only the Contessa, Assassin, and Duke cards have been implemented.
- AI makes random decisions. Considering that you basically can't bluff because one of the other three AI will challenge 7/8 of the time, and AI will bluff extremely recklessly.
- Cards won't be redrawn after any player reveals to counter a challenge.
- The treasury has no coin limit.

### Requirement Considerations

"""

1. I took the game phases as action, challenge, and block. They're represented as methods.
2. Restart instantiated here.
3. Rough implementation of MVC paradigm by separating the display/styling logic out for coloration. Could be further improved by separating the text out of the game handler completely and creating new action models which would hold the text. I also wrote the card model to be more extensible as that would likely be the next improvement to the display.
4. Player 1 being VerySmartAndCool VolterEmployee, indicated by is_bot property on the Player class.
5. AI "decison making" implemented in the display model. This could be separate out eventually once the logic becomes more complicated.
6. AI "decison making" implemented in the display model. This could be separate out eventually once the logic becomes more complicated.
7. Choices offered are identical inputs to the "decision" method.
8. The Contessa, Assassin, and Duke classes are the only cards implemented. This could be improved by abstracting cards the character action methods to be owned by the cards.

Notes:
In this version players don't draw a new card after revealing a card in defense of a challenge.
"""

next steps I'd break actions into their own object with properties like "can_challenge" and "can_block" so that the handler can be less verbose and more readable. Also actions like "assassinate" can only be blocked by the target, and currently that difference means that scanning players for blockers has to be repeated at each action case in the handler because they differ.

Known bugs: AI will occasionally choose options which aren't possible (trying to assassinate with < 3 coins, not blocking an assassination when they have a contessa)

[^1] Shout out to ChatGPT for much of the boilerplate around basic classes and methods.
[^2] `sudo pacman -Syu` if you're on a linux flavor. Mac and Windows y'all are on your own.
