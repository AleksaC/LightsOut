# Turning the Lights Out with Python
This repository contains a [kivy](https://kivy.org/#home) implementation of lights out game.
It was done as one of the homework assignments for a computer graphics class at my university. 
The project specification was quite loose because this was meant to be kind of a warmup for 
the final project. We could use any tool or framework and we could add arbitrary features as 
long as core functionality is implemented which in this case is the game itself along with 
the solver. This was the first time I've used kivy, so don't take this repo as an example of 
idiomatic kivy code. I decided not to use kivy language because I felt it was overkill for this
project. The game was developed in a few short cycles with some time between them so there
might be some inconsistency when it comes to code style.
## Quick look at the game
Menu screen:  
![menu](./screenshots/menu.png?raw=true)  
Game screen:  
![game](./screenshots/game.png?raw=true)  
Scores screen:  
![scores](./screenshots/scores.png?raw=true)  

The game mostly uses kivy defaults when it comes to style so it looks 
kinda plain. That's because I was focused on providing core functionality plus 
making things look good is not something I excel at.
## About the game
The game is pretty straightforward, consisting of a 5 by 5 grid 
of lights randomly turned on or off. Pressing the light will toggle 
it along with the adjacent lights. The goal of the game is to turn all 
the lights out preferably with as little presses as possible.
It has been proven mathematically that not all initial configurations
are solvable. Thanks to the little help of linear algebra we also know how 
to initialize the puzzle in order for it to be solvable as well as how to 
solve it. If you want to know more about this stuff you should check out 
this [Wikipedia aricle](https://en.wikipedia.org/wiki/Lights_Out_(game)).
I found it very helpful and was able to implement a game as well as a solver 
for it (finds optimal solution) using only this article as a reference.
## Run the game
If you already have kivy installed enter the following commands in your terminal to download
and run the game:
```
git clone https://github.com/AleksaC/LightsOut.git
cd LightsOut/game
python app.py
```
## Produce a binary
You can use `create_exe.py` to generate an executable. It uses PyInstaller 3.3.1. The
script works on Windows and should work on Ubuntu as well. Note that PyInstaller may include
some unnecessary files, especially on Ubuntu so if the size of the dist folder exceeds ~40Mb 
you should look into that.
## Contact for further information
If for whatever reason you want to reach out to me you can find me at my
personal [website](https://aleksac.me) where you can contact
me directly or via social media linked there.
