"""Level and stage data for Lizz Levels.

Each level is 20 rows of 20 characters, one screen exactly. Writing them as
pictures rather than number grids means you can see the level while editing it.

    .  empty            C  coin
    D  dirt             B  blob, walks a short patrol
    G  grass            H  ghost, drifts sideways through walls
    P  platform         V  ghost, drifts up and down through walls
    X  lift, sideways   E  exit door
    Y  lift, up down    S  where Lizz starts
    L  lava

The physics decide which levels can actually be finished. The numbers below
come from settings.py, and every one of these rules was found by the level
checker refusing to finish a level, so do not bend them lightly.

  1. A jump rises 120px, so a step up may be at most 2 rows (100px).
  2. Standing surfaces sit at the top of their row, so a climb needs its rows
     2 apart: 18 (the ground), 16, 14, 12, 10 and so on.
  3. A jump carries about 50 to 105px sideways while high enough to land, so
     leave exactly one empty column between one step and the next.
  4. A climb must march in ONE direction, left or right, 4 columns per step.
     Zig-zagging back and forth puts the step two tiers up directly over the
     spot you jump from, and the player's head hits it mid flight and gets
     shoved back down, which loses the jump.
  5. Never put a lift directly above a surface the player stands on. Put it
     beside one, so the player steps on sideways and rides it.
  6. Leave rows 0 and 1 clear, the heads up display is drawn over them.
"""

LEVEL_1_1 = [
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '.............CCC..E.',
    '............GGGGGGGG',
    '.S..CCC..B..DDDDDDDD',
    'GGGGGGGGGGGGGGGGGGGG',
    'DDDDDDDDDDDDDDDDDDDD',
]

LEVEL_1_2 = [
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '..........CCC.......',
    '..........PPP.......',
    '....................',
    '......PPP...........',
    '.S....CC..B..CC...E.',
    'GGGGGGLLGGGGGLLGGGGG',
    'DDDDDDLLDDDDDLLDDDDD',
]

LEVEL_1_3 = [
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '.................CE.',
    '.................PPP',
    '.............CCC....',
    '.............PPP....',
    '.........CCC........',
    '.........PPP........',
    '.....CCC............',
    '.....PPP............',
    '.CCC................',
    '.PPP................',
    'S....B....C....C....',
    'GGGGGGGGGGGGGGGGGGGG',
    'DDDDDDDDDDDDDDDDDDDD',
]

LEVEL_1_4 = [
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '...........CCC......',
    '..........PPPPP.....',
    '....................',
    '........PP..........',
    '.....CC.............',
    '....PPPP............',
    '....................',
    '..PP................',
    '.S..B....XX....B..E.',
    'GGGGGGLLLLLLLLGGGGGG',
    'DDDDDDLLLLLLLLDDDDDD',
]

LEVEL_2_1 = [
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '................CCE.',
    '................PPPP',
    '.............CC.....',
    '.............PP.....',
    '................CC..',
    '................PP..',
    '.............CC.....',
    '..........V..PP.....',
    '................CC..',
    '.........PP.....PP..',
    '.S..CC........B.C...',
    'GGGGGGGGLLLLGGGGGGGG',
    'DDDDDDDDLLLLDDDDDDDD',
]

LEVEL_2_2 = [
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '.................CE.',
    '.................PPP',
    '.............CCC....',
    '.............PPP....',
    '.........CCC...V....',
    '.........PPP........',
    '.....CCC............',
    '.....PPP............',
    '.CCC...........H....',
    '.PPP................',
    'S..B................',
    'GGGGGLLLLLLLLLLLGGGG',
    'DDDDDLLLLLLLLLLLDDDD',
]

LEVEL_2_3 = [
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '...............CCE..',
    '...............PPPPP',
    '............CC......',
    '............PPP.....',
    '........CC.....V....',
    '........PPP.........',
    '............CC...H..',
    '............PPP.....',
    '........CC......V...',
    '........PPP.........',
    '....CC..............',
    '....PPP.............',
    '.S..CC...B......C...',
    'GGGGGGGGGGLLLLGGGGGG',
    'DDDDDDDDDDLLLLDDDDDD',
]

LEVEL_2_4 = [
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '...CEC..............',
    '...PPP..............',
    '.......CCC..........',
    '.......PPP..........',
    '...........CCC......',
    '...........PPP......',
    '...............CCC..',
    '.....XX..PP.XX.PPP..',
    'S.........H.........',
    'GGGGLLLLLLLLLLLLGGGG',
    'DDDDLLLLLLLLLLLLDDDD',
]

LEVEL_3_1 = [
    '....................',
    '....................',
    '....................',
    '..............BCCE..',
    '..............PPPPPP',
    '..............CCC...',
    '.............PPPP...',
    '..........CCC.......',
    '.........PPPP.......',
    '.....CC...V.........',
    '.....PPP............',
    '.........BCC........',
    '.........PPP........',
    '.....CC.............',
    '.....PPP............',
    '.SC.................',
    'PPPP................',
    '....................',
    '....................',
    '....................',
]

LEVEL_3_2 = [
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '.................CE.',
    '................PPP.',
    '............CCC.....',
    '............PPP.....',
    '.........CC.........',
    '.........YY.........',
    '.....BCC....V.......',
    '....PPPPP...........',
    'SCC.................',
    'PPP.................',
    '....................',
    '....................',
    '....................',
]

LEVEL_3_3 = [
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '....................',
    '.CEC................',
    '.PPP................',
    '.....CCC....H.......',
    '.....PPP............',
    '.........CC...V.....',
    '.........XX.........',
    '.............BCC....',
    '.............PPP....',
    '.................SC.',
    '.................PPP',
    '....................',
    '....................',
    '....................',
]

LEVEL_3_4 = [
    '....................',
    '....................',
    '....................',
    '...............CCEB.',
    '...............PPPP.',
    '....................',
    '...................Y',
    '................CCC.',
    '................PPP.',
    '............BCC.....',
    '............PPP.....',
    '........CCC....V....',
    '........XX..........',
    '....CCC.....H.......',
    '....PPP.............',
    'SCC.................',
    'PPP.................',
    '....................',
    'LLLLLLLLLLLLLLLLLLLL',
    'LLLLLLLLLLLLLLLLLLLL',
]


STAGES = [
    {
        'name': 'Grasslands',
        'tagline': 'Every Lizz legend starts somewhere',
        'background': 'sky',
        'tint': None,
        'enemy_speed': 1,
        'enemy_range': 50,
        'levels': [LEVEL_1_1, LEVEL_1_2, LEVEL_1_3, LEVEL_1_4],
        'level_names': ['First Steps', 'Over the Gap', 'Up the Hill',
                        'Lava Crossing'],
    },
    {
        'name': 'The Caverns',
        'tagline': 'Mind the drop, and whatever is humming down there',
        'background': 'sky',
        'tint': (18, 16, 58, 165),
        'enemy_speed': 2,
        'enemy_range': 50,
        'levels': [LEVEL_2_1, LEVEL_2_2, LEVEL_2_3, LEVEL_2_4],
        'level_names': ['Into the Dark', 'Lava Ladder', 'The Haunting',
                        'Collapse'],
    },
    {
        'name': 'Sky Ruins',
        'tagline': 'No floor left. Do not look down',
        'background': 'sky_ruins',
        'tint': (236, 124, 42, 130),
        'enemy_speed': 2,
        'enemy_range': 100,
        'levels': [LEVEL_3_1, LEVEL_3_2, LEVEL_3_3, LEVEL_3_4],
        'level_names': ['Rising Ruins', 'Sky Lifts', 'The Gauntlet',
                        'Last Climb'],
    },
]


def total_levels():
    return sum(len(stage['levels']) for stage in STAGES)
