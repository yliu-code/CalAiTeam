# CalAiTeam
Won Top 3 Algorithm for Berkeley's AI competition (Multiagent Pacman)

## Strategy
I used, of course, the minimax with alpha-beta pruning strategy for both agents, this relatively straightforward.

## Offensive Agent (Or, the Greedy Guerilla Tactic):

**Features:**
* current score
* distance to ghost
* distance to our territory
* distance to nearest enemy food pellet
* number of foods left
* number of capsules left

**Important:**

The stroke of ingenuity that won the game in the end was the thought of alternating between emphasizing the distance to the next food pellet and the distance to our side of the board. Essentially, when the enemy ghost is less than 2 distances away from the pacman, I encourage it to run back to our side using a distance metric. Otherwise, it picks up whichever food pellet is closest.

## Defensive Agent (Or, Shameless merciless Strategem)

**Features:**
* distance to enemy pacman

**Important:**

Another lightbulb manifested when I made my defensive agent flaunt and dance near the border (fluctuating between 1 or 2 steps away from the center line). This angered the enemy and lured them to our side, putting them at the mercy of our defensive chomps. This solved the issue of both side’s agents frozen in stalemate at the front lines and also sometimes tricked the enemy’s defensive agents to suicide and respawn from the starting point as well, giving my pacman time to forage.

