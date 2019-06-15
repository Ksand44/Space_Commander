import pygame
from pathlib import Path

from gamelib import sprites
from gamelib import load
from gamelib import buttons


class Game:
	"""docstring for Game"""
	def __init__(self):
		pygame.init()
		pygame.mixer.init()

		display_info = pygame.display.Info()
		
		self.FPS = 60
		self.FULLSCREEN = False

		self.WIDTH = 1024
		self.HEIGHT = 720

		if self.FULLSCREEN:
			self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
			self.WIDTH = display_info.current_w
			self.HEIGHT = display_info.current_h
		else:
			self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

		# self.win_rec = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
		self.win_rec = self.win.get_rect()

		self.MIDX = self.WIDTH / 2
		self.MIDY = self.HEIGHT / 2

		pygame.display.set_caption("Space Commander")
		self.clock = pygame.time.Clock()

		self.gameFolder = Path.cwd()
		self.imgFolder = self.gameFolder.joinpath('img')
		self.img = load.load_images(self.imgFolder)

		# Create all sprite groups
		self.all_sprites = pygame.sprite.Group()
		self.player_sprite = pygame.sprite.GroupSingle()
		self.enemy_sprites = pygame.sprite.Group()
		self.bullet_sprites = pygame.sprite.Group()
		self.collect_sprites = pygame.sprite.Group()

		self.gui_sprites = pygame.sprite.Group()

		self.title_button_sprites = pygame.sprite.Group()
		self.pause_button_sprites = pygame.sprite.Group()
		
		# Create player
		self.player = sprites.PlayerShip(self, self.MIDX, self.MIDY)

		# Create buttons
		self.playButton = buttons.Button(self, self.pause_button_sprites,
										 self.MIDX, 300,
										 "green_play.png", "green_play_press.png",
										 self.play)
		self.exitButton = buttons.Button(self, self.pause_button_sprites,
										 self.MIDX, 400,
										 "green_exit.png", "green_exit_press.png",
										 self.exit)

		self.points = 0

		self.spawn_speed = 0.5
		self.time_spawn = 0
		self.time_group_spawn = 0

		self.game_state = "title"
		# self.paused = False
		self.pausedWait = 11

		self.keyList = 0
		self.eventList = 0

		self.mainLoop = True

	def run(self):
		self.mainLoop = True

		while self.mainLoop:
			dt = self.clock.tick(self.FPS) / 1000

			self.events()
			self.update(dt)
			self.draw(self.win)

		pygame.quit()

	def events(self):
		self.keyList = pygame.key.get_pressed()
		self.eventList = pygame.event.get()

		for event in self.eventList:
			if event.type == pygame.QUIT:
				self.exit()

		if self.keyList[pygame.K_ESCAPE] and self.pausedWait > 10:
			self.play()
			self.pausedWait = 0

		self.pausedWait += 1

	def update(self, dt):
		if self.game_state == "title":
			self.pause_button_sprites.update(dt)
		if self.game_state == "play":
			self.update_game(dt)
		if self.game_state == "pause":
			self.pause_button_sprites.update(dt)
		if self.game_state == "game over":
			self.pause_button_sprites.update(dt)

	def update_game(self, dt):
		self.all_sprites.update(dt)

		# TODO Spawn Enemies
		time_mili = pygame.time.get_ticks()

		if self.time_spawn + (2000 / self.spawn_speed) <= time_mili:
			sprites.spawn(self, sprites.EnemyShip)
			sprites.spawn(self, sprites.EnemyOrbitShip)
			self.time_spawn = time_mili

		if self.time_group_spawn + 8000 <= time_mili:
			sprites.spawn(self, sprites.EnemyShip)
			sprites.spawn(self, sprites.EnemyTank)
			self.time_group_spawn = time_mili

	def game_over(self):
		self.game_state = "game over"
		# print("--- GAME OVER ---")
		# print(f"Points: {self.points}")
		# time_sec = pygame.time.get_ticks() / 1000
		# print(f"Time: {time_sec}sec")

	def draw(self, win):
		self.win.blit(self.img["space_bk.png"], (0, 0))

		if self.game_state == "title":
			self.pause_button_sprites.draw(win)
		else:
			self.all_sprites.draw(win)
			self.gui_sprites.draw(win)

		if self.game_state == "pause":
			self.pause_button_sprites.draw(win)

		if self.game_state == "game over":
			self.pause_button_sprites.draw(win)

		pygame.display.update()

	def play(self):
		if self.game_state == "title":
			self.game_state = "play"
		elif self.game_state == "play":
			self.game_state = "pause"
		elif self.game_state == "pause":
			self.game_state = "play"
		elif self.game_state == "game over":
			self.reset_game()
			self.game_state = "play"

	def exit(self):
		self.mainLoop = False

	def reset_game(self):
		for s in self.enemy_sprites:
			s.kill()
		for s in self.bullet_sprites:
			s.kill()
		for s in self.collect_sprites:
			s.kill()

		self.points = 0
		self.spawn_speed = 0.5
		self.time_spawn = 0
		self.time_group_spawn = 0
		self.player.reset()

		self.game_state = "play"


def main():
	game = Game()
	game.run()


if __name__ == '__main__':
	main()