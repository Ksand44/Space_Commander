import pygame
# import math
from random import randint, random
from pygame.math import Vector2
from gamelib import vectool


# class Player(pygame.sprite.Sprite):
# 	"""docstring for Player class"""
# 	def __init__(self, x, y, game):
# 		pygame.sprite.Sprite.__init__(self)
# 		self.game = game
#
# 		self.image = self.game.spaceshipImage
#
# 		self.rect = self.image.get_rect()
#
# 		self.px = x
# 		self.py = y
#
# 		self.rect.topleft = (self.px, self.py)
#
# 		self.vx, self.vy = (0, 0)
# 		self.ax, self.ay = (0, 0)
#
# 		self.health = 10
#
# 	def update(self, dt):
# 		# SPACE GRAVITY
# 		self.ax = 0
# 		self.ay = 0
#
# 		keyList = self.game.keyList
#
# 		# Movement controls
# 		if keyList[pygame.K_a]:
# 			self.ax = -800
# 		if keyList[pygame.K_d]:
# 			self.ax = 800
# 		if keyList[pygame.K_w]:
# 			self.ay = -800
# 		if keyList[pygame.K_s]:
# 			self.ay = 800
#
# 		# Limit diagonal acc
# 		if self.ax != 0 and self.ay != 0:
# 			self.ax *= 0.8
# 			self.ay *= 0.8
#
# 		# Update vel
# 		self.vx += self.ax * dt
# 		self.vy += self.ay * dt
#
# 		# Apply Drag
# 		drag = 1 - 1 / 90
# 		self.vx *= drag
# 		self.vy *= drag
#
# 		# Limit vel
# 		if self.vx > 300: self.vx = 300
# 		if self.vx < -300: self.vx = -300
# 		if self.vy > 300: self.vy = 300
# 		if self.vy < -300: self.vy = -300
#
# 		# Update Position
# 		self.px += self.vx * dt
# 		self.py += self.vy * dt
#
# 		if self.px > self.game.WIDTH:
# 			self.px = -self.rect.w
# 		if self.px < -self.rect.w:
# 			self.px = self.game.WIDTH
# 		if self.py > self.game.HEIGHT - self.rect.h / 2:
# 			self.py = self.game.HEIGHT - self.rect.h /2
#
# 		# Update rec position
# 		self.rect.topleft = (self.px, self.py)
#
# 		hitEnemy = pygame.sprite.spritecollide(self, self.game.enemy_sprites, True)
#
# 		for hit in hitEnemy:
# 			self.health -= 1
# 			Enemy.spawn(self.game)
#
# 	def shoot(self):
# 		Bullet(self.game, self.rect.midtop)


class Bullet(pygame.sprite.Sprite):
	"""docstring for Bullet, created 2nd June 2019"""
	def __init__(self, game, pos, direc=0, speed=7):
		pygame.sprite.Sprite.__init__(self, game.all_sprites, game.bullet_sprites)
		self.game = game

		self.pos = Vector2(pos)
		self.direc = direc
		self.speed = speed

		self.rotate_img()

		self.vel = vectool.from_angle(self.direc) * self.speed

	def update(self, dt):
		self.pos += self.vel
		self.rect.center = self.pos

		if not self.rect.colliderect(self.game.win_rec):
			self.kill()

	def rotate_img(self):
		if not self.img:
			print("NO self.img set")
			self.img = self.game.img["projectile-green.png"]
		self.image = pygame.transform.rotate(self.img, self.direc)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.mask = pygame.mask.from_surface(self.image)


class BulletEnemy(Bullet):
	"""docstring for BulletEnemy"""
	def __init__(self, game, center, direc):
		self.img = game.img["projectile-blue.png"]
		super().__init__(game, center, direc)

	def update(self, dt):
		super().update(dt)

		player = self.game.player_sprite
		playerShipHit = pygame.sprite.spritecollide(self, player, False, pygame.sprite.collide_mask)

		for hit in playerShipHit:
			hit.damage(50)
			self.kill()


class BulletGood(Bullet):
	"""docstring for BulletGood"""
	def __init__(self, game, center, direc):
		self.img = game.img["projectile-green.png"]
		super().__init__(game, center, direc, 10)

	def update(self, dt):
		super().update(dt)

		enemy_sprites = self.game.enemy_sprites
		enemyShipHits = pygame.sprite.spritecollide(self, enemy_sprites, False, pygame.sprite.collide_mask)

		for hit in enemyShipHits:
			hit.health -= 1
			self.kill()


class Explosion(pygame.sprite.Sprite):
	"""docstring for Explosion, created 2nd June 2019"""
	def __init__(self, game, pos):
		pygame.sprite.Sprite.__init__(self, game.all_sprites)
		self.game = game

		self.img_frame = 0
		self.explosion_images = list(self.game.img["Explosion"].values())
		self.image = self.explosion_images[self.img_frame]

		self.rect = self.image.get_rect()
		self.rect.center = pos

	def update(self, dt):
		self.img_frame += 1

		if self.img_frame >= len(self.explosion_images):
			self.kill()
		else:
			self.image = self.explosion_images[self.img_frame]


class PlayerShip(pygame.sprite.Sprite):
	"""This is a rectangle class, created 2nd June 2019"""
	def __init__(self, game, x, y):
		pygame.sprite.Sprite.__init__(self, game.all_sprites, game.player_sprite)
		self.game = game

		self.direc = 90

		self.img = self.game.img["tankbase-green.png"]
		self.image = pygame.transform.rotate(self.img, self.direc)

		self.start_pos = Vector2(x, y)
		self.pos = Vector2(x, y)
		self.rect = self.image.get_rect()
		self.rect.center = Vector2(self.pos)
		self.vel = Vector2(0, 0)
		self.acc = Vector2(0, 0)
		self.speed = 10

		self.health = 1000
		self.turrets = [Turret(self.game, self, (12, 0)),
						Turret(self.game, self, (-12, 0))]
		# self.turret = Turret(self.game, self)
		self.time_shot = -1000
		self.shoot_speed = 5

		self.metal = 0

	def update(self, dt):
		self.acc = Vector2(0, 0)

		# Movement controls
		key_list = self.game.keyList
		if key_list[pygame.K_w] or key_list[pygame.K_UP]:
			self.acc.y = -self.speed
		if key_list[pygame.K_s] or key_list[pygame.K_DOWN]:
			self.acc.y = self.speed
		if key_list[pygame.K_a] or key_list[pygame.K_LEFT]:
			self.acc.x = -self.speed
		if key_list[pygame.K_d] or key_list[pygame.K_RIGHT]:
			self.acc.x = self.speed

		if self.acc.x != 0 and self.acc.y != 0:
			self.acc *= 0.8

		# Update Velocity
		self.vel += self.acc * dt

		# Apply Drag
		drag = 1 - 1 / 90
		self.vel *= drag

		# Limit Velocity
		max_speed = 4
		if self.vel.x > max_speed: self.vel.x = max_speed
		if self.vel.x < -max_speed: self.vel.x = -max_speed
		if self.vel.y > max_speed: self.vel.y = max_speed
		if self.vel.y < -max_speed: self.vel.y = -max_speed

		# Update movement
		self.pos += self.vel
		self.rect.center = Vector2(self.pos)

		for t in self.turrets:
			t.update()

		# Click to shoot
		click = pygame.mouse.get_pressed()

		if click[0] and self.check_shoot():
			for t in self.turrets:
				t.shoot()

	def check_shoot(self):
		time_mili = pygame.time.get_ticks()

		if self.time_shot + (1000 / self.shoot_speed) <= time_mili:
			self.time_shot = time_mili
			return True
		else:
			return False

	def damage(self, dmg):
		# TODO add damage calculations, maybe using armor
		self.health -= dmg
		print(f'HEALTH: {self.health}points')

		if self.health <= 0:
			self.game.game_over()

	def reset(self):
		self.pos = Vector2(self.start_pos)
		self.vel = Vector2(0, 0)
		self.acc = Vector2(0, 0)
		self.speed = 10

		self.health = 1000
		self.turrets = [Turret(self.game, self, (12, 0)),
						Turret(self.game, self, (-12, 0))]
		self.time_shot = -1000
		self.shoot_speed = 10

		self.metal = 0


class Turret(pygame.sprite.Sprite):
	"""docstring for Turret, created 2nd June 2019"""
	def __init__(self, game, tank, offset):
		pygame.sprite.Sprite.__init__(self, game.all_sprites)
		self.game = game
		self.tank = tank
		self.offset = Vector2(offset)

		# self.img_frame = 0
		self.img = self.game.img["tankcannon-green.png"]
		self.rect = self.tank.rect

		self.direc = vectool.angle_to_mouse(self)

		self.rotate_img()

		self.turret_end = self.rect.center

	def rotate_img(self):
		self.image = pygame.transform.rotate(self.img, self.direc)
		self.rect = self.image.get_rect()
		self.rect.center = self.tank.rect.center + self.offset

	def update(self, dt=None):
		self.direc = vectool.angle_to_mouse(self)
		self.rotate_img()
		self.turret_end = self.rect.center + (vectool.from_angle(self.direc) * 26)

	def shoot(self):
		BulletGood(self.game, self.turret_end, self.direc)


class Enemy(pygame.sprite.Sprite):
	"""docstring for EnemyShip, created 2nd June 2019"""
	def __init__(self, game):
		pygame.sprite.Sprite.__init__(self, game.all_sprites, game.enemy_sprites)
		self.game = game
		self.player = self.game.player
		self.time_shot = 0

	def update(self, dt):
		if self.health <= 0:
			Explosion(self.game, self.rect.center)
			Debri.create_field(self.game, self.rect.center, self.size)
			self.kill()
			try:
				self.turret.kill()
			except:
				pass

		player_sprite = self.game.player_sprite
		playerShipHit = pygame.sprite.spritecollide(self, player_sprite, False, pygame.sprite.collide_mask)

		for hit in playerShipHit:
			Explosion(self.game, self.rect.center)
			hit.damage(self.health * 20)
			self.kill()	
			try:
				self.turret.kill()
			except:
				pass

	def rotate_img(self):
		self.image = pygame.transform.rotate(self.img, self.direc)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.mask = pygame.mask.from_surface(self.image)

	def spawnPos(self):
		self.pos = Vector2(0,0)

	def checkShoot(self):
		time_mili = pygame.time.get_ticks()

		if self.time_shot + (1000 / self.shoot_speed) <= time_mili:
			self.time_shot = time_mili
			return True
		else:
			return False

	def angle_to(self, target):
		return vectool.angle_to(self, target)

	def direc_vec(self):
		return vectool.from_angle(self.direc)
	

class EnemyShip(Enemy):
	"""docstring for EnemyShip, created 2nd June 2019"""
	def __init__(self, game):
		super().__init__(game)

		self.pos = self.spawnPos()
		self.direc = self.angle_to(self.player)

		self.img = self.game.img["red_02.png"]
		self.rotate_img()

		self.speed = 2
		self.vel = self.direc_vec() * self.speed

		self.health = 3
		self.size = 6

	def update(self, dt):
		super().update(dt)

		self.direc = self.angle_to(self.player)

		self.vel = self.direc_vec() * self.speed
		self.pos += self.vel

		self.rotate_img()

	def spawnPos(self):
		pos = Vector2(0, 0)
		pos.x = randint(0, self.game.WIDTH)
		if random() > 0.5:
			pos.y = -50
		else:
			pos.y = self.game.HEIGHT + 50
		return pos


class EnemyOrbitShip(Enemy):
	"""docstring for EnemyShip, created 2nd June 2019"""
	def __init__(self, game):
		super().__init__(game)

		self.pos = self.spawnPos()
		self.direc = self.angle_to(self.player)

		self.img = self.game.img["red_01.png"]
		self.rotate_img()

		self.speed = 2
		self.orbit = 1 if random() < 0.5 else -1
		self.vel = vectool.from_angle(self.direc + (self.orbit * 90)) * self.speed

		self.health = 2
		self.shoot_speed = 0.25

		self.size = 4

	def update(self, dt):
		super().update(dt)

		self.direc = self.angle_to(self.player)

		if self.pos.distance_to(self.player.rect.center) < 300:
			self.vel = vectool.from_angle(self.direc + (self.orbit * 90)) * self.speed
		else:
			self.vel = vectool.from_angle(self.direc + (self.orbit * 45)) * self.speed

		self.pos += self.vel

		self.rotate_img()

		if self.checkShoot():
			self.shoot()

	def shoot(self):
		BulletEnemy(self.game, self.rect.center, self.direc)

	def spawnPos(self):
		pos = Vector2(0, 0)
		pos.x = randint(0, self.game.WIDTH)
		if random() > 0.5:
			pos.y = -50
		else:
			pos.y = self.game.HEIGHT + 50
		return pos


class EnemyTank(Enemy):
	"""docstring for EnemyTank, created 2nd June 2019"""
	def __init__(self, game):
		super().__init__(game)
		
		self.pos = self.spawnPos()
		self.direc = 0

		self.img = self.game.img["tankbase-red.png"]
		self.rotate_img()

		self.speed = 1
		self.vel = vectool.from_angle(self.direc) * self.speed

		self.health = 5

		self.turret = EnemyTurret(self.game, self)
		self.shoot_speed = 0.5

		self.size = 8

	def update(self, dt):
		super().update(dt)
		self.pos += self.vel
		self.rect.center = self.pos

		if self.rect.left > self.game.WIDTH:
			self.kill()
			self.turret.kill()

		self.turret.update()

		if self.checkShoot():
			self.turret.shoot()

	def spawnPos(self):
		pos = Vector2(0, 0)
		pos.x = -50
		pos.y = randint(50, self.game.HEIGHT - 50)
		return pos

	def checkShoot(self):
		time_mili = pygame.time.get_ticks()

		if self.time_shot + (1000 / self.shoot_speed) <= time_mili:
			self.time_shot = time_mili
			return True
		else:
			return False


class EnemyTurret(pygame.sprite.Sprite):
	"""docstring for EnemyTurret, created 2nd June 2019"""
	def __init__(self, game, base):
		pygame.sprite.Sprite.__init__(self, game.all_sprites, game.enemy_sprites)
		self.game = game
		self.base = base

		# self.img_frame = 0
		self.img = self.game.img["tankcannon-red.png"]
		self.image = self.img
		self.rect = self.base.rect

		self.target = self.game.player

		self.direc = vectool.angle_to(self, self.target)
		self.health = 100

		self.rotate_img()

		self.turret_end = self.rect.center

	def rotate_img(self):
		self.image = pygame.transform.rotate(self.img, self.direc)
		self.rect = self.image.get_rect()
		self.rect.center = self.base.rect.center

	def update(self, dt=None):
		self.direc = vectool.angle_to(self, self.target)
		self.rotate_img()
		self.turret_end = self.rect.center + (vectool.from_angle(self.direc) * 26)

	def shoot(self):
		BulletEnemy(self.game, self.turret_end, self.direc)


class Debri(pygame.sprite.Sprite):
	"""docstring for Debri"""
	def create_field(game, center, size):
		imgs = list(game.img["Debris"].values())
		for i in range(randint(size - 3, size)):
			j = randint(0, len(imgs) - 1)
			Debri(game, center, imgs.pop(j))

	def __init__(self, game, center, img):
		pygame.sprite.Sprite.__init__(self, game.all_sprites, game.collect_sprites)
		self.game = game

		self.pos = Vector2(center)

		self.direc = randint(0, 359)
		self.vel = vectool.from_angle(self.direc) * randint(2, 5)

		self.image = img
		self.image = pygame.transform.rotate(self.image, self.direc)

		self.rect = self.image.get_rect()
		self.rect.center = self.pos

	def update(self, dt):
		player = self.game.player

		player_sprite = self.game.player_sprite
		playerShipHit = pygame.sprite.spritecollide(self, player_sprite, False, pygame.sprite.collide_mask)

		for hit in playerShipHit:
			player.metal += 5
			self.game.points += 5
			self.kill()

		if self.pos.distance_to(player.rect.center) < 100:
			self.vel = vectool.vec_to(self, player) * 2

		self.vel *= 0.95
		self.pos += self.vel
		self.rect.center = self.pos


def spawn(game, spr, count=1):
	for i in range(count):
		spr(game)