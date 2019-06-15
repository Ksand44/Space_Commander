import pygame

class Button(pygame.sprite.Sprite):
	def __init__(self, game, group, x, y, but, but_press, action=None):
		pygame.sprite.Sprite.__init__(self, group)
		self.game = game

		self.but = self.game.img[but]
		self.but_press = self.game.img[but_press]

		self.image = self.but

		self.rect = self.image.get_rect()
		self.rect.midbottom = (x, y)

		self.action = action

	def update(self, dt):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()[0]
		released = False

		for event in self.game.eventList:
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				released = True

		if self.rect.collidepoint(mouse):
			if click:
				self.image = self.but_press
			if released:
				self.image = self.but
				if self.action:
					self.action()
		else:
			self.image = self.but