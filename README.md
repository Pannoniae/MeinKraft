# MeinKraft

We're trying to implement some of features of Minecraft. 
It's written in Python and it uses the pyglet framework and the PyOpenGL graphics library.
We want it to be be more realistic than Minecraft in some regard, example there should be no tree punching, no diamond finding, etc.

The code is based on fogleman's code:

https://github.com/fogleman/



## How to Run It

* Install pyglet
    pip install pyglet
* Install PyOpenGL
  http://pyopengl.sourceforge.net/documentation/installation.html


    git clone https://bitbucket.org/prisz/meinkraft
    cd meinkraft
    python main.py

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
- Mouse left-click: remove block
- Mouse right-click: create block

### Quitting

- ESC: release mouse, then close window