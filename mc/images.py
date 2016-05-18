from PIL import Image
from .constants import *

def image_process():
    #Process the image files to texture.png at every start.
    dirt = Image.open(TEXTURE_PATH_DIRT)
    grass_side = Image.open(TEXTURE_PATH_GRASS_SIDE)
    grass_top = Image.open(TEXTURE_PATH_GRASS_TOP)
    sand = Image.open(TEXTURE_PATH_SAND)
    brick = Image.open(TEXTURE_PATH_BRICK)
    stone = Image.open(TEXTURE_PATH_STONE)
    texture = Image.new('RGB', (256, 256))
        
    texture.paste(dirt, (0, 128))
    texture.paste(sand, (64, 128))
    texture.paste(stone, (128, 128))
    texture.paste(grass_side, (0, 192))
    texture.paste(grass_top, (64, 192))
    texture.paste(brick, (128, 192))
    texture.save('texture.png')