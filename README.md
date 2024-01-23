# DuckHunt-WorldWar 
by Ankit, Nathan, Michael and Robert

Overview of the project:

This game is based on the popular 80's game "Duck Hunt" but with a twist: the duck (or birds) shoot back at the player
this turns the game into more of a First Person Shooter where they can move left and right and duck under cover. Another fun twist is the way you aim:
Either you can use the mouse or use the computer's camera to track a makeshift controller that the player can use to aim and shoot.  

In terms of design, we wanted to keep the 8-bit art style of the original game. The original game layout consists of a background, a middleground bush the enemy comes out of and a 
foreground bush that the player is behind. In our game, we made 3 maps: Africa, Australia and America. Each of the maps had their own respective background, middleground and 
foreground. Another thing we wanted was a simple and easy UI, with a similar style in button design with the 8-bit style of the game. After the completion of each level, there is 
a success screen, and we wanted that to break up the pace of the game as well as add to the user experience. The player aspect of the design (crosshair, weapon, etc) is not as 
similar to the base game. We wanted to improve one aspect of the game - ours has a crosshair which allows the player to aim and fire, making it easier to play the game. Finally, 
to add some sense of difficulty, we added a reload time, shown by the green circle around the crosshair and also, the enemy shooting which is shown by the red circle shrinking 
down on its target over time.

Instructions for running the game:
In VS Code, go into the terminal and pip install the following: pygame, numpy, opencv, cypy

Make sure the user has a camera and it is not covered or in a badly lit area as that is how the game tracks the controller. 
Make sure there is a functional mouse, whether that be a physical mouse or a track pad.
To run the game, run the "main.py" file in the "main" folder 
