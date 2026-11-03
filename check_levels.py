"""Check every level is well formed and can actually be finished.

Run it after editing levels.py:

    python check_levels.py

It opens no window. For each level it checks the shape of the map, then runs
the real player physics from sprites.py in a breadth first search over every
reachable (x, y, fall speed) state, and reports whether the exit can be
reached at all. A level that fails here cannot be finished by a human either.

Enemies are ignored, since they can be dodged by timing. Lava is fatal. A
sideways lift is treated as solid along its whole travel path, because the
player can wait for it. An up and down lift is treated as a platform at its
lowest point which then carries the player to its highest point.
"""

import os
import sys
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

import settings
from settings import COLS, PLATFORM_TRAVEL, ROWS, TILE_SIZE
from levels import STAGES
from sprites import Player, World

ASSETS = settings.load_assets()
TRAVEL_TILES = PLATFORM_TRAVEL // TILE_SIZE
LEGAL_CHARS = set('.DGPXYLCBHVES')

# every combination of held keys worth trying each frame
ACTIONS = [
    {'left': left, 'right': right, 'jump': jump}
    for left, right in ((False, False), (True, False), (False, True))
    for jump in (False, True)
]


def check_shape(level_map):
    problems = []
    if len(level_map) != ROWS:
        problems.append('has %d rows, expected %d' % (len(level_map), ROWS))
    for index, row in enumerate(level_map):
        if len(row) != COLS:
            problems.append('row %d is %d wide, expected %d'
                            % (index, len(row), COLS))
    flat = ''.join(level_map)
    for char, name in (('S', 'start'), ('E', 'exit')):
        if flat.count(char) != 1:
            problems.append('has %d %s markers, expected 1'
                            % (flat.count(char), name))
    unknown = set(flat) - LEGAL_CHARS
    if unknown:
        problems.append('unknown characters %s' % sorted(unknown))
    return problems


def freeze_lifts(level_map):
    """Turn the lifts into something a static search can reason about.

    A sideways lift becomes solid along its whole travel path. An up and down
    lift becomes a single platform at its lowest point, where the player
    boards it, plus a note saying it can carry them to the top. Filling its
    whole path instead would build a wall the player could never step into.
    """
    grid = [list(row) for row in level_map]
    y_lifts = []
    for row in range(ROWS):
        for col in range(COLS):
            char = level_map[row][col]
            if char == 'X':
                for offset in range(-TRAVEL_TILES, TRAVEL_TILES + 1):
                    target = col + offset
                    if 0 <= target < COLS and grid[row][target] == '.':
                        grid[row][target] = 'P'
                grid[row][col] = 'P'
            elif char == 'Y':
                grid[row][col] = '.'
                lowest = min(row + TRAVEL_TILES, ROWS - 1)
                grid[lowest][col] = 'P'
                y_lifts.append((col, lowest))
    return [''.join(row) for row in grid], y_lifts


def ride_up(player, y_lifts):
    """Where an up and down lift carries the player standing on it."""
    for col, lowest_row in y_lifts:
        on_band = player.rect.bottom == lowest_row * TILE_SIZE
        overlaps = (player.rect.right > col * TILE_SIZE
                    and player.rect.left < (col + 1) * TILE_SIZE)
        if on_band and overlaps:
            return player.rect.y - 2 * PLATFORM_TRAVEL
    return None


def exit_reachable(level_map, budget=700000):
    static_map, y_lifts = freeze_lifts(level_map)
    world = World(static_map, ASSETS)
    world.coin_group.empty()     # coins would be eaten during the search
    world.blob_group.empty()     # enemies can be dodged by timing
    world.ghost_group.empty()

    player = Player(*world.spawn, assets=ASSETS)
    start = (player.rect.x, player.rect.y, player.vel_y,
             player.in_air, player.jumped)
    seen = {start}
    queue = deque([start])
    visited = 0

    while queue:
        state = queue.popleft()
        visited += 1
        if visited > budget:
            return False, 'gave up after %d states' % budget

        for action in ACTIONS:
            player.rect.x, player.rect.y, player.vel_y = state[0], state[1], state[2]
            player.in_air, player.jumped = state[3], state[4]
            player.alive = True
            status, _ = player.update(action, world)

            if status == 'exit':
                return True, 'exit reachable, %d states searched' % visited
            if status != 'alive':
                continue

            nexts = [(player.rect.x, player.rect.y, player.vel_y,
                      player.in_air, player.jumped)]
            if not player.in_air:
                lifted = ride_up(player, y_lifts)
                if lifted is not None:
                    nexts.append((player.rect.x, lifted, 0, False,
                                  player.jumped))
            for nxt in nexts:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)

    return False, 'EXIT UNREACHABLE, %d states searched' % visited


def main():
    failures = 0
    for stage_index, stage in enumerate(STAGES, start=1):
        print('\nStage %d  %s' % (stage_index, stage['name']))
        for level_index, level_map in enumerate(stage['levels'], start=1):
            label = '%d-%d %s' % (stage_index, level_index,
                                  stage['level_names'][level_index - 1])
            problems = check_shape(level_map)
            if problems:
                failures += 1
                print('  FAIL %-24s %s' % (label, '; '.join(problems)))
                continue
            ok, note = exit_reachable(level_map)
            failures += 0 if ok else 1
            print('  %s %-24s %2d coins, %s'
                  % ('pass' if ok else 'FAIL', label,
                     ''.join(level_map).count('C'), note))

    print('\n%s' % ('all levels pass' if failures == 0
                    else '%d level(s) need work' % failures))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
