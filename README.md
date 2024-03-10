next steps I'd break actions into their own object with properties like "can_challenge" and "can_block" so that the handler can be less verbose and more readable. Also actions like "assassinate" can only be blocked by the target, and currently that difference means that scanning players for blockers has to be repeated at each action case in the handler because they differ.

Known bugs: AI will occasionally choose options which aren't possible (trying to assassinate with < 3 coins, not blocking an assassination when they have a contessa)
