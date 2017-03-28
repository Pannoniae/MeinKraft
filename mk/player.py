import math

from .render.geometry import normalize, FACES, sectorize
from .blocks import *
from .config import *

class Player(object):
    """
    information related to the player

    """
    def __init__(self):


        # the world around us
        self.model = None

        # When flying gravity has no effect and speed is increased.
        self.flying = False

        # Strafing is moving lateral to the direction you are facing,
        # e.g. moving to the left or right while continuing to face forward.
        #
        # First element is -1 when moving forward, 1 when moving back, and 0
        # otherwise. The second element is -1 when moving left, 1 when moving
        # right, and 0 otherwise.
        self.strafe = [0, 0]

        # When jumping
        self.jumping = False

        # Current (x, y, z) position in the world, specified with floats. Note
        # that, perhaps unlike in math class, the y-axis is the vertical axis.
        self.position = (0, 5, 0)

        # First element is rotation of the player in the x-z plane (ground
        # plane) measured from the z-axis down. The second is the rotation
        # angle from the ground plane up. Rotation is in degrees.
        #
        # The vertical plane rotation ranges from -90 (looking straight down) to
        # 90 (looking straight up). The horizontal rotation range is unbounded.
        self.rotation = (90, 0)

        # Which sector the player is currently in.
        self.sector = None

        # A list of blocks the player can place. Hit num keys to cycle.
        self.inventory = [BRICK, GRASS, SAND, PATH]

        # The current block the user can place. Hit num keys to cycle.
        self.block = self.inventory[0]

        # Velocity in the y (upward) direction.
        self.dy = 0


    def move_forward(self):
        self.strafe[0] -= 1

    def move_backward(self):
        self.strafe[0] += 1

    def move_left(self):
        self.strafe[1] -= 1

    def move_right(self):
        self.strafe[1] += 1

    def halt(self):
        self.strafe[0] = 0
        self.strafe[1] = 0

    def world_changed(self, model):
        self.model = model


    def update_sector(self):
        # compute which sector we're in

        sector = sectorize(self.position)
        if sector != self.sector:
            self.model.change_sectors(self.sector, sector)

            # XXX Zsombor
            # this is what causes the long delay at startup
            #if self.sector is None:
            #    self.model.process_entire_queue()

            self.sector = sector

    def jump(self):
        self.jumping = True
        if self.dy == 0:
            self.dy = JUMP_SPEED

    def toggle_flying(self):
        self.flying = not self.flying

    def change_active_block(self, index):
        self.block = self.inventory[index]

    def get_sight_vector(self):
        """ Returns the current line of sight vector indicating the direction
        the player is looking.

        """
        x, y = self.rotation
        # y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
        # is 1 when looking ahead parallel to the ground and 0 when looking
        # straight up or down.
        m = math.cos(math.radians(y))
        # dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
        # looking straight up.
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

    def get_motion_vector(self):
        """ Returns the current motion vector indicating the velocity of the
        player.

        Returns
        -------
        vector : tuple of len 3
            Tuple containing the velocity in x, y, and z respectively.

        """
        if any(self.strafe):

            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            y_angle = math.radians(y)
            x_angle = math.radians(x + strafe)

            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.strafe[1]:
                    # Moving left or right.
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    # Moving backwards.
                    dy *= -1
                # When you are flying up or down, you have less left and right
                # motion.
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)


    def update(self, dt):
        """
        clock tick for player

        :param dt:
        :return:
        """
        self.update_sector()

        dt = min(dt, 0.2)
        self._update(dt)

    def _update(self, dt):
        """ Private implementation of the `update()` method. This is where most
        of the motion logic lives, along with gravity and collision detection.

        Parameters
        ----------
        dt : float
            The change in time since the last call.
        """
        # walking
        speed = FLYING_SPEED if self.flying else WALKING_SPEED
        d = dt * speed  # distance covered this tick.
        dx, dy, dz = self.get_motion_vector()
        # New position in space, before accounting for gravity.
        dx, dy, dz = dx * d, dy * d, dz * d
        # gravity
        if not self.flying:
            # Update your vertical speed: if you are falling, speed up until you
            # hit terminal velocity; if you are jumping, slow down until you
            # start falling.
            self.dy -= dt * GRAVITY
            self.dy = max(self.dy, -TERMINAL_VELOCITY)
            dy += self.dy * dt
        # collisions
        x, y, z = self.position
        x, y, z = self.collide((x + dx, y + dy, z + dz), PLAYER_HEIGHT)
        self.position = (x, y, z)

    def collide(self, position, height):
        """ Checks to see if the player at the given `position` and `height`
        is colliding with any blocks in the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check for collisions at.
        height : int or float
            The height of the player.

        Returns
        -------
        position : tuple of len 3
            The new position of the player taking into account collisions.

        """
        # How much overlap with a dimension of a surrounding block you need to
        # have to count as a collision. If 0, touching terrain at all counts as
        # a collision. If .49, you sink into the ground, as if walking through
        # tall grass. If >= .5, you'll fall through the ground.
        pad = 0.25
        p = list(position)
        np = normalize(position)
        for face in FACES:  # check all surrounding blocks
            for i in range(3):  # check each dimension independently
                if not face[i]:
                    continue
                # How much overlap you have with this dimension.
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in range(height):  # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if (tuple(op) not in self.model.world) or (self.model.get_block(tuple(op)).collision is False):
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0):
                        # You are colliding with the ground, so stop falling.
                        if self.jumping:
                            self.dy = JUMP_SPEED
                        else:
                            self.dy = 0
                    if face == (0, 1, 0):
                        # You are colliding with the ceiling, so stop rising.
                        if self.jumping:
                            self.dy = -1
                    break
        return tuple(p)


    def move(self, x, y, dx, dy):
        m = SENSIVITY
        x, y = self.rotation
        x, y = x + dx * m, y + dy * m
        y = max(-90, min(90, y))
        self.rotation = (x, y)

