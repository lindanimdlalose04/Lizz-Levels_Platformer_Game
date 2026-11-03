# Lizz Levels

A tile based platformer in Python and Pygame. Twelve levels across three
stages, with coins, enemies, lava, moving lifts, a save slot and a score.

## Running it

```
pip install pygame
python lizz_levels.py
```

## Controls

| Key | What it does |
| --- | --- |
| arrow keys, or A and D | move left and right |
| space, W or up arrow | jump |
| P or escape | pause, and save from there |
| M | mute or unmute the music |
| R | restart the level you are on |

## The stages

1. **Grasslands** - gentle ground, your first blobs, a lava crossing on a lift.
2. **The Caverns** - darker, faster blobs, ghosts that drift straight through
   walls, and a lot more lava.
3. **Sky Ruins** - the floor is gone. Miss a platform and you fall off the
   world.

## How the code is laid out

| File | What is in it |
| --- | --- |
| `lizz_levels.py` | entry point, game loop, menus, heads up display, saving |
| `sprites.py` | the player, world, blobs, ghosts, lifts, coins, lava, exit |
| `levels.py` | the twelve level maps and the three stage definitions |
| `settings.py` | every constant in one place, plus asset loading |
| `check_levels.py` | proves every level can actually be finished |
| `build1.py` | the original part two tutorial file, kept as a checkpoint |

## Adding or editing a level

Levels in `levels.py` are written as pictures, twenty rows of twenty
characters, one screen each:

```
.  empty            C  coin
D  dirt             B  blob, walks a short patrol
G  grass            H  ghost, drifts sideways through walls
P  platform         V  ghost, drifts up and down through walls
X  lift, sideways   E  exit door
Y  lift, up down    S  where Lizz starts
L  lava
```

The physics decide which levels can actually be finished, and the rules are
written out at the top of `levels.py`. The short version: a step up may be at
most two rows, a climb needs its rows two apart with one empty column between
steps, a climb must march in one direction rather than zig-zag, and a lift
goes beside a platform, never above one.

After editing a level, run the checker:

```
python check_levels.py
```

It runs the real player physics over every reachable position in each level
and reports whether the exit can be reached at all. Six of the twelve levels
here failed it on the first attempt, so it is worth running.

## Credits

Built by following **Coding With Russ** and his tutorial series *PyGame Tile
Based Platformer Game Beginner Tutorial in Python*. The art and sound in
`img/` come from his asset pack at
<https://github.com/russs123/pygame-platformer-assets>. His tutorial code is
MIT licensed. The levels, stages, ghosts, lifts, menus, scoring and save
system here are my own work on top of that foundation.
