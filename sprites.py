"""The things that live in a level: the world, the player, enemies and pickups."""

import pygame

from settings import (
    DEATH_VELOCITY, GHOST_SPEED, GHOST_TRAVEL, GRAVITY, JUMP_VELOCITY,
    MAX_FALL_SPEED, PLATFORM_SPEED, PLATFORM_THICKNESS, PLATFORM_TOLERANCE,
    PLATFORM_TRAVEL,
    PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH,
    TILE_SIZE,
)

# what each character in a level map means
EMPTY = '.'
DIRT = 'D'
GRASS = 'G'
PLATFORM = 'P'
PLATFORM_X = 'X'
PLATFORM_Y = 'Y'
LAVA = 'L'
COIN = 'C'
BLOB = 'B'
GHOST_H = 'H'
GHOST_V = 'V'
EXIT = 'E'
SPAWN = 'S'


class World:
    """Builds every sprite in a level from its character map."""

    def __init__(self, level_map, assets, enemy_speed=1, enemy_range=TILE_SIZE):
        self.tiles = []            # (image, rect) pairs, all solid
        self.lava_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.blob_group = pygame.sprite.Group()
        self.ghost_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.spawn = (TILE_SIZE, SCREEN_HEIGHT - PLAYER_HEIGHT)
        self.total_coins = 0

        for row_index, row in enumerate(level_map):
            for col_index, char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if char == DIRT:
                    self._add_tile(assets['dirt'], x, y, TILE_SIZE)
                elif char == GRASS:
                    self._add_tile(assets['grass'], x, y, TILE_SIZE)
                elif char == PLATFORM:
                    self._add_tile(assets['platform'], x, y, PLATFORM_THICKNESS)
                elif char == PLATFORM_X:
                    self.platform_group.add(
                        MovingPlatform(x, y, assets['platform_x'], PLATFORM_SPEED, 0))
                elif char == PLATFORM_Y:
                    self.platform_group.add(
                        MovingPlatform(x, y, assets['platform_y'], 0, PLATFORM_SPEED))
                elif char == LAVA:
                    self.lava_group.add(Lava(x, y, assets['lava']))
                elif char == COIN:
                    self.coin_group.add(Coin(x, y, assets['coin']))
                    self.total_coins += 1
                elif char == BLOB:
                    self.blob_group.add(
                        Blob(x, y, assets['blob'], enemy_speed, enemy_range))
                elif char in (GHOST_H, GHOST_V):
                    self.ghost_group.add(
                        Ghost(x, y, assets['ghost'], char == GHOST_H))
                elif char == EXIT:
                    self.exit_group.add(Exit(x, y, assets['exit']))
                elif char == SPAWN:
                    self.spawn = (
                        x + (TILE_SIZE - PLAYER_WIDTH) // 2,
                        y + TILE_SIZE - PLAYER_HEIGHT,
                    )

    def _add_tile(self, image, x, y, height):
        self.tiles.append((image, pygame.Rect(x, y, TILE_SIZE, height)))

    def update(self):
        self.platform_group.update()
        self.blob_group.update()
        self.ghost_group.update()

    def draw(self, surface):
        for image, rect in self.tiles:
            surface.blit(image, rect)
        self.lava_group.draw(surface)
        self.platform_group.draw(surface)
        self.coin_group.draw(surface)
        self.exit_group.draw(surface)
        self.blob_group.draw(surface)
        self.ghost_group.draw(surface)


class Lava(pygame.sprite.Sprite):
    """A half height strip of lava sitting at the bottom of its tile."""

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(topleft=(x, y + TILE_SIZE // 2))


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(
            center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))


class Exit(pygame.sprite.Sprite):
    """The door. It is taller than a tile, so it pokes into the tile above."""

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(topleft=(x, y - TILE_SIZE // 2))


class Blob(pygame.sprite.Sprite):
    """Walks back and forth over a fixed patrol range."""

    def __init__(self, x, y, image, speed, patrol_range):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.bottom = y + TILE_SIZE
        self.speed = speed
        self.patrol_range = patrol_range
        self.travelled = 0
        self.direction = 1

    def update(self):
        self.rect.x += self.direction * self.speed
        self.travelled += self.direction * self.speed
        if abs(self.travelled) > self.patrol_range:
            self.direction *= -1


class Ghost(pygame.sprite.Sprite):
    """Drifts through walls, so a platform is no protection from it."""

    def __init__(self, x, y, image, horizontal):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(
            center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        self.horizontal = horizontal
        self.travelled = 0
        self.direction = 1

    def update(self):
        step = self.direction * GHOST_SPEED
        if self.horizontal:
            self.rect.x += step
        else:
            self.rect.y += step
        self.travelled += step
        if abs(self.travelled) > GHOST_TRAVEL:
            self.direction *= -1


class MovingPlatform(pygame.sprite.Sprite):
    """A lift. Carries the player along with it when ridden."""

    def __init__(self, x, y, image, move_x, move_y):
        super().__init__()
        self.image = image
        # the image is half a tile tall but only the top band is solid, so a
        # lift passing below a platform does not shove the player about
        self.rect = pygame.Rect(x, y, TILE_SIZE, PLATFORM_THICKNESS)
        self.move_x = move_x
        self.move_y = move_y
        self.travelled = 0
        self.direction = 1

    def update(self):
        self.rect.x += self.direction * self.move_x
        self.rect.y += self.direction * self.move_y
        self.travelled += self.direction * max(self.move_x, self.move_y)
        if abs(self.travelled) > PLATFORM_TRAVEL:
            self.direction *= -1


class Player(pygame.sprite.Sprite):
    """Lizz herself.

    update() takes a plain dict of inputs rather than reading the keyboard
    directly, which keeps the physics testable with no window open.
    """

    def __init__(self, x, y, assets):
        super().__init__()
        self.frames_right = assets['player_frames']
        self.frames_left = [
            pygame.transform.flip(frame, True, False)
            for frame in self.frames_right
        ]
        self.death_image = pygame.transform.flip(self.frames_right[0], False, True)
        self.image = self.frames_right[0]
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.index = 0
        self.counter = 0
        self.vel_y = 0
        self.jumped = False
        self.direction = 1
        self.in_air = True
        self.alive = True
        self.just_jumped = False

    def update(self, inputs, world):
        """Advance one frame.

        Returns (status, coins) where status is alive, dying, dead or exit.
        """
        if not self.alive:
            return self._update_death(), 0

        dx, dy = 0, 0
        self._animate(inputs)

        if inputs.get('left'):
            dx -= PLAYER_SPEED
            self.direction = -1
        if inputs.get('right'):
            dx += PLAYER_SPEED
            self.direction = 1

        self.just_jumped = False
        if inputs.get('jump') and not self.jumped and not self.in_air:
            self.vel_y = JUMP_VELOCITY
            self.jumped = True
            self.just_jumped = True
        if not inputs.get('jump'):
            self.jumped = False

        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)
        dy += self.vel_y
        self.in_air = True

        dx, dy = self._collide_tiles(world, dx, dy)
        dx, dy = self._collide_platforms(world, dx, dy)

        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_WIDTH))

        coins = len(pygame.sprite.spritecollide(self, world.coin_group, True))

        if (pygame.sprite.spritecollide(self, world.lava_group, False)
                or pygame.sprite.spritecollide(self, world.blob_group, False)
                or pygame.sprite.spritecollide(self, world.ghost_group, False)
                or self.rect.top > SCREEN_HEIGHT):
            self.alive = False
            self.vel_y = DEATH_VELOCITY
            return 'dying', coins

        if pygame.sprite.spritecollide(self, world.exit_group, False):
            return 'exit', coins

        return 'alive', coins

    def _update_death(self):
        self.image = self.death_image
        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)
        self.rect.y += self.vel_y
        if self.rect.top > SCREEN_HEIGHT:
            return 'dead'
        return 'dying'

    def _animate(self, inputs):
        if not (inputs.get('left') or inputs.get('right')):
            self.index = 0
            self.counter = 0
        else:
            self.counter += 1
            if self.counter > 5:
                self.counter = 0
                self.index = (self.index + 1) % len(self.frames_right)
        frames = self.frames_right if self.direction == 1 else self.frames_left
        self.image = frames[self.index]

    def _collide_tiles(self, world, dx, dy):
        for _, tile in world.tiles:
            if tile.colliderect(self.rect.x + dx, self.rect.y,
                                PLAYER_WIDTH, PLAYER_HEIGHT):
                dx = 0
            if tile.colliderect(self.rect.x, self.rect.y + dy,
                                PLAYER_WIDTH, PLAYER_HEIGHT):
                if self.vel_y < 0:
                    dy = tile.bottom - self.rect.top
                    self.vel_y = 0
                else:
                    dy = tile.top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False
        return dx, dy

    def _collide_platforms(self, world, dx, dy):
        for platform in world.platform_group:
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y,
                                         PLAYER_WIDTH, PLAYER_HEIGHT):
                dx = 0
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy,
                                         PLAYER_WIDTH, PLAYER_HEIGHT):
                if abs((self.rect.top + dy) - platform.rect.bottom) < PLATFORM_TOLERANCE:
                    dy = platform.rect.bottom - self.rect.top
                    self.vel_y = 0
                elif abs((self.rect.bottom + dy) - platform.rect.top) < PLATFORM_TOLERANCE:
                    dy = platform.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False
                    # ride along with a lift that is moving sideways
                    if platform.move_x:
                        self.rect.x += platform.direction * platform.move_x
        return dx, dy
