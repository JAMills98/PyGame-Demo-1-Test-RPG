# PyGame-Demo0
PyGame Demo I made in 2016, allows you to make a Mother 3 Style Background
I release this code into the public domain.
Some sprites within are ripped from Mother 3 and Earthbound.

# Requirements
* Python 3.x is recommended, but you can run in 2.x due to __future__
* Modules: pygame, random, ctypes, pickle, os, math, fractions, datetime (Some can be removed if you can't run, trial and error it)

# About
There are 3 Game States, you can change by editing the Game_State variable:
* 0 - Run main menu, doesn't do much except a fancy animation and basic browsing. If you wait for 180 frames, a demo should play but it doesn't work
* 1 - Game World, allows you to walk around a tile map grid but the colors are messed up. Hold space to charge run and release to run.
* 2 - Battle Background, the main attraction, allows you to view EarthBound style backgrounds.

# Background Help
* REFER to README - Background Examples.txt
* Replace the All_BGS variable with values inside
* Edit BACKGROUND.png to add new backgrounds, REMEMBER TO SAVE AS AN 8-BIT PNG
* Press ALT + B while in Game_State 2 to enable the Background editor, use the arrow keys to change parameter, and scroll wheel to change the value.

# 
