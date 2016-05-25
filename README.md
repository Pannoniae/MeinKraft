# MeinKraft


Yes, I do know that "force" or "power" is "die Kraft" in German, so the correct form would be "MeineKraft". :) 

I'm trying to implement some features of Minecraft in this project. The code is written in Python and it uses the pyglet framework and the PyOpenGL graphics library. I want the game to be be more realistic than Minecraft in some regards. For example, there should be no tree punching any more, no diamond finding, etc.

It's based on fogleman's code: (also check out Konstructs, another game by him, forked by others)

https://github.com/fogleman/


## How to run the program for the time being 

* Install Python 2.7
    3.x maybe or maybe not do it
* Install pyglet
    run this command from cmd: pip install pyglet
* Install PyOpenGL
  http://pyopengl.sourceforge.net/documentation/installation.html
* Install Git
  Just google for it :)
* type these commands:
    git clone https://bitbucket.org/prisz/meinkraft
    cd meinkraft
    python main.py

## Changes

* code restructuring
* texture map is automatically assembled from individual bitmaps
* blocks have been changed into objects from list of numbers
* fast updates are performed only for graphics
* blocks may be transparent (i.e. can have a shape)

## How to Play

### Moving

- W: forward
- S: back
- A: strafe left
- D: strafe right
- Mouse: look around
- Space: jump
- Tab: toggle flying mode

### Building

- Selecting type of block to create:
    - 1: brick
    - 2: grass
    - 3: sand
    - 4: path
- Mouse left-click: remove block
- Mouse right-click: create block

### Quitting

- ESC: release mouse, then close window