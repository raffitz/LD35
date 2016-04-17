# Ludum Dare 35 entry

Theme is _Shapeshift_.

I'll be using python and pygame.

## How to play

_WASD_ moves the player's polygon.

_↑↓_ changes the player's polygon (up increases number of sides, wraps around at the heptagon, down decreases, wraps at the triangle).

_←→_ changes the player's color (Red,Green,Blue,Yellow,Cyan,Magenta,Azure,Violet,Rose,Orange,Chartreuse,Spring Green)

_Space_ pauses and unpauses the game.

_R_ while game is paused sends you back to title splash.

## Game mechanics

If you're the same color and shape than the polygons you're colliding with, you get a health bonus (your radius increases).

If you're just the same shape, you're not damaged.

If you're a different shape and color than the polygons, you're damaged. Too much damage will inevitably lead to Game Over.

Trying to get bonuses gets really hard really quickly, because the polygons tend to swarm, and you can't shapeshift quick enough to absorb them right.
