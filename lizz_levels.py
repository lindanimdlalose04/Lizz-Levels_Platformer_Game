"""Lizz Levels, a tile based platformer.

Run this file to play:

    python lizz_levels.py

Controls
    arrow keys or A and D   move
    space, W or up arrow    jump
    P or escape             pause, where you can save
    M                       mute or unmute the music
    R                       give up on the level and restart it
"""

import json
import os
import sys

import pygame

from levels import STAGES, total_levels
from settings import (
    BLACK, CREAM, FPS, GOLD, GREEN, RED, SAVE_FILE, SCREEN_HEIGHT,
    SCREEN_WIDTH, SHADOW, START_LIVES, WHITE, IMG_DIR, load_assets, load_font,
    load_sounds,
)
from sprites import Player, World

MENU = 'menu'
STAGE_INTRO = 'stage_intro'
PLAYING = 'playing'
PAUSED = 'paused'
LEVEL_CLEAR = 'level_clear'
STAGE_CLEAR = 'stage_clear'
GAME_OVER = 'game_over'
VICTORY = 'victory'

COIN_POINTS = 10
LEVEL_BONUS = 50
STAGE_BONUS = 250


class Button:
    """A clickable image. Clicks are handled from the event queue."""

    def __init__(self, image, centre_x, top):
        self.image = image
        self.rect = image.get_rect(topleft=(centre_x - image.get_width() // 2, top))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def hit(self, position):
        return self.rect.collidepoint(position)


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Lizz Levels')
        self.clock = pygame.time.Clock()

        self.assets = load_assets()
        self.sounds = load_sounds()
        self.font_huge = load_font(84)
        self.font_big = load_font(52)
        self.font = load_font(30)
        self.font_small = load_font(22)

        centre = SCREEN_WIDTH // 2
        self.start_button = Button(self.assets['start_btn'], centre, 420)
        self.load_button = Button(self.assets['load_btn'], centre, 570)
        self.menu_exit_button = Button(self.assets['exit_btn'], centre, 700)
        self.restart_button = Button(self.assets['restart_btn'], centre, 540)
        self.over_exit_button = Button(self.assets['exit_btn'], centre, 660)
        self.save_button = Button(self.assets['save_btn'], centre, 520)
        self.pause_exit_button = Button(self.assets['exit_btn'], centre, 650)

        self.music_on = True
        self.start_music()

        self.state = MENU
        self.timer = 0
        self.message = ''
        self.stage_index = 0
        self.level_index = 0
        self.score = 0
        self.lives = START_LIVES
        self.coins_this_level = 0
        self.world = None
        self.player = None

    # ------------------------------------------------------------------ audio

    def start_music(self):
        try:
            pygame.mixer.music.load(os.path.join(IMG_DIR, 'music.wav'))
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1, 0.0, 4000)
        except pygame.error:
            self.music_on = False

    def play(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def toggle_music(self):
        self.music_on = not self.music_on
        try:
            pygame.mixer.music.set_volume(0.25 if self.music_on else 0.0)
        except pygame.error:
            pass

    # ------------------------------------------------------------- game flow

    @property
    def stage(self):
        return STAGES[self.stage_index]

    @property
    def level_name(self):
        return self.stage['level_names'][self.level_index]

    def levels_done(self):
        done = sum(len(s['levels']) for s in STAGES[:self.stage_index])
        return done + self.level_index

    def new_game(self):
        self.stage_index = 0
        self.level_index = 0
        self.score = 0
        self.lives = START_LIVES
        self.enter_stage_intro()

    def enter_stage_intro(self):
        self.state = STAGE_INTRO
        self.timer = 0
        self.build_level()

    def build_level(self):
        stage = self.stage
        self.world = World(
            stage['levels'][self.level_index],
            self.assets,
            enemy_speed=stage['enemy_speed'],
            enemy_range=stage['enemy_range'],
        )
        self.player = Player(*self.world.spawn, assets=self.assets)
        self.coins_this_level = 0

    def restart_level(self):
        self.build_level()
        self.state = PLAYING

    def next_level(self):
        self.level_index += 1
        if self.level_index < len(self.stage['levels']):
            self.build_level()
            self.state = PLAYING
            return
        # stage finished
        self.score += STAGE_BONUS
        self.level_index = 0
        self.stage_index += 1
        if self.stage_index >= len(STAGES):
            self.state = VICTORY
            self.timer = 0
            return
        self.state = STAGE_CLEAR
        self.timer = 0

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.play('game_over')
            self.state = GAME_OVER
            self.timer = 0
        else:
            self.restart_level()

    # ------------------------------------------------------------ save, load

    def save_game(self):
        data = {
            'stage': self.stage_index,
            'level': self.level_index,
            'score': self.score,
            'lives': self.lives,
        }
        try:
            with open(SAVE_FILE, 'w', encoding='utf-8') as handle:
                json.dump(data, handle, indent=2)
            self.message = 'Progress saved'
        except OSError:
            self.message = 'Could not save'
        self.timer = 0

    def load_game(self):
        try:
            with open(SAVE_FILE, encoding='utf-8') as handle:
                data = json.load(handle)
            self.stage_index = max(0, min(int(data['stage']), len(STAGES) - 1))
            levels = len(STAGES[self.stage_index]['levels'])
            self.level_index = max(0, min(int(data['level']), levels - 1))
            self.score = int(data['score'])
            self.lives = max(1, int(data['lives']))
        except (OSError, ValueError, KeyError, TypeError):
            self.message = 'No save to load'
            self.timer = 0
            return False
        self.enter_stage_intro()
        return True

    def has_save(self):
        return os.path.exists(SAVE_FILE)

    # ---------------------------------------------------------------- events

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.toggle_music()
                elif event.key in (pygame.K_p, pygame.K_ESCAPE):
                    if self.state == PLAYING:
                        self.state = PAUSED
                    elif self.state == PAUSED:
                        self.state = PLAYING
                elif event.key == pygame.K_r and self.state == PLAYING:
                    self.restart_level()
                elif self.state in (STAGE_INTRO, STAGE_CLEAR):
                    self.state = PLAYING

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.handle_click(event.pos):
                    return False
        return True

    def handle_click(self, position):
        """Returns False only when the player chose to quit."""
        if self.state == MENU:
            if self.start_button.hit(position):
                self.new_game()
            elif self.load_button.hit(position) and self.has_save():
                self.load_game()
            elif self.menu_exit_button.hit(position):
                return False

        elif self.state == GAME_OVER:
            if self.restart_button.hit(position):
                self.new_game()
            elif self.over_exit_button.hit(position):
                return False

        elif self.state == PAUSED:
            if self.save_button.hit(position):
                self.save_game()
            elif self.pause_exit_button.hit(position):
                self.state = MENU

        elif self.state == VICTORY:
            if self.restart_button.hit(position):
                self.state = MENU
            elif self.over_exit_button.hit(position):
                return False

        elif self.state in (STAGE_INTRO, STAGE_CLEAR):
            self.state = PLAYING

        return True

    def read_inputs(self):
        keys = pygame.key.get_pressed()
        return {
            'left': keys[pygame.K_LEFT] or keys[pygame.K_a],
            'right': keys[pygame.K_RIGHT] or keys[pygame.K_d],
            'jump': keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w],
        }

    # ----------------------------------------------------------------- logic

    def update(self):
        self.timer += 1

        if self.state == PLAYING:
            self.world.update()
            status, coins = self.player.update(self.read_inputs(), self.world)
            if self.player.just_jumped:
                self.play('jump')
            if coins:
                self.play('coin')
                self.score += coins * COIN_POINTS
                self.coins_this_level += coins
            if status == 'dead':
                self.lose_life()
            elif status == 'exit':
                self.score += LEVEL_BONUS
                self.state = LEVEL_CLEAR
                self.timer = 0

        elif self.state == LEVEL_CLEAR:
            if self.timer > 90:
                self.next_level()

        elif self.state == STAGE_INTRO:
            if self.timer > 150:
                self.state = PLAYING

        elif self.state == STAGE_CLEAR:
            if self.timer > 180:
                self.enter_stage_intro()

    # --------------------------------------------------------------- drawing

    def draw_background(self):
        stage = self.stage
        self.screen.blit(self.assets[stage['background']], (0, 0))
        if stage['tint']:
            veil = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            veil.fill(stage['tint'])
            self.screen.blit(veil, (0, 0))

    def text(self, message, font, colour, centre_x, top, shadow=True):
        if shadow:
            dark = font.render(message, True, SHADOW)
            self.screen.blit(dark, (centre_x - dark.get_width() // 2 + 3, top + 3))
        surface = font.render(message, True, colour)
        self.screen.blit(surface, (centre_x - surface.get_width() // 2, top))
        return surface.get_height()

    def draw_hud(self):
        self.screen.blit(self.assets['coin_hud'], (20, 20))
        label = self.font.render(str(self.score), True, WHITE)
        self.screen.blit(label, (60, 24))

        for index in range(self.lives):
            self.screen.blit(self.assets['life'],
                             (SCREEN_WIDTH - 40 - index * 30, 18))

        where = '%s  %d-%d  %s' % (self.stage['name'], self.stage_index + 1,
                                   self.level_index + 1, self.level_name)
        caption = self.font_small.render(where, True, CREAM)
        self.screen.blit(caption, (SCREEN_WIDTH // 2 - caption.get_width() // 2, 24))

    def veil(self, alpha=170):
        shade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, alpha))
        self.screen.blit(shade, (0, 0))

    def draw_menu(self):
        self.screen.blit(self.assets['sky'], (0, 0))
        self.veil(90)
        self.text('LIZZ LEVELS', self.font_huge, GOLD, SCREEN_WIDTH // 2, 200)
        self.text('%d levels across 3 stages' % total_levels(),
                  self.font, CREAM, SCREEN_WIDTH // 2, 310)
        self.start_button.draw(self.screen)
        if self.has_save():
            self.load_button.draw(self.screen)
        self.menu_exit_button.draw(self.screen)
        self.text('arrows to move, space to jump, P to pause',
                  self.font_small, WHITE, SCREEN_WIDTH // 2, 860)
        if self.message and self.timer < 150:
            self.text(self.message, self.font_small, RED, SCREEN_WIDTH // 2, 820)

    def draw_stage_intro(self):
        self.draw_background()
        self.world.draw(self.screen)
        self.veil()
        self.text('Stage %d' % (self.stage_index + 1), self.font,
                  CREAM, SCREEN_WIDTH // 2, 330)
        self.text(self.stage['name'], self.font_huge, GOLD,
                  SCREEN_WIDTH // 2, 390)
        self.text(self.stage['tagline'], self.font, WHITE,
                  SCREEN_WIDTH // 2, 500)
        self.text('click or press any key', self.font_small, CREAM,
                  SCREEN_WIDTH // 2, 620)

    def draw_level_clear(self):
        self.draw_background()
        self.world.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.veil(120)
        self.text('Level clear', self.font_big, GREEN, SCREEN_WIDTH // 2, 400)
        self.text('%d of %d coins' % (self.coins_this_level,
                                      self.world.total_coins),
                  self.font, WHITE, SCREEN_WIDTH // 2, 480)

    def draw_stage_clear(self):
        self.draw_background()
        self.veil()
        finished = STAGES[self.stage_index - 1]
        self.text('%s cleared' % finished['name'], self.font_big, GOLD,
                  SCREEN_WIDTH // 2, 380)
        self.text('bonus %d points' % STAGE_BONUS, self.font, WHITE,
                  SCREEN_WIDTH // 2, 470)
        self.text('next up: %s' % self.stage['name'], self.font, CREAM,
                  SCREEN_WIDTH // 2, 540)

    def draw_paused(self):
        self.draw_background()
        self.world.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.veil()
        self.text('Paused', self.font_huge, CREAM, SCREEN_WIDTH // 2, 280)
        self.text('score %d  |  lives %d' % (self.score, self.lives),
                  self.font, WHITE, SCREEN_WIDTH // 2, 400)
        self.save_button.draw(self.screen)
        self.pause_exit_button.draw(self.screen)
        self.text('P to carry on', self.font_small, CREAM,
                  SCREEN_WIDTH // 2, 800)
        if self.message and self.timer < 120:
            self.text(self.message, self.font_small, GREEN,
                      SCREEN_WIDTH // 2, 470)

    def draw_game_over(self):
        self.draw_background()
        self.world.draw(self.screen)
        self.veil()
        self.text('Game over', self.font_huge, RED, SCREEN_WIDTH // 2, 280)
        self.text('you reached %s %d-%d' % (self.stage['name'],
                                            self.stage_index + 1,
                                            self.level_index + 1),
                  self.font, WHITE, SCREEN_WIDTH // 2, 400)
        self.text('final score %d' % self.score, self.font_big, GOLD,
                  SCREEN_WIDTH // 2, 450)
        self.restart_button.draw(self.screen)
        self.over_exit_button.draw(self.screen)

    def draw_victory(self):
        self.screen.blit(self.assets['sky_ruins'], (0, 0))
        self.veil(110)
        self.text('You did it', self.font_huge, GOLD, SCREEN_WIDTH // 2, 220)
        self.text('all %d levels, all 3 stages' % total_levels(),
                  self.font, CREAM, SCREEN_WIDTH // 2, 340)
        self.text('final score %d' % self.score, self.font_big, WHITE,
                  SCREEN_WIDTH // 2, 410)
        self.text('lives left %d' % self.lives, self.font, CREAM,
                  SCREEN_WIDTH // 2, 490)
        self.restart_button.draw(self.screen)
        self.over_exit_button.draw(self.screen)

    def draw(self):
        if self.state == MENU:
            self.draw_menu()
        elif self.state == STAGE_INTRO:
            self.draw_stage_intro()
        elif self.state == PLAYING:
            self.draw_background()
            self.world.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            self.draw_hud()
        elif self.state == PAUSED:
            self.draw_paused()
        elif self.state == LEVEL_CLEAR:
            self.draw_level_clear()
        elif self.state == STAGE_CLEAR:
            self.draw_stage_clear()
        elif self.state == GAME_OVER:
            self.draw_game_over()
        elif self.state == VICTORY:
            self.draw_victory()
        pygame.display.update()

    # ------------------------------------------------------------- main loop

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            if running:
                self.update()
                self.draw()
        pygame.quit()
        sys.exit(0)


if __name__ == '__main__':
    Game().run()
