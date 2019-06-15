import math
import pygame
from pygame.math import Vector2


def angle_to_mouse(self):
	target = pygame.mouse.get_pos()

	return angle_to(self, target)


def angle_to(self, target):
	try:
		target = Vector2(target.rect.center)
	except:
		pass

	try:
		self = self.rect.center
	except:
		self = self.pos

	targetRel = Vector2(target) - Vector2(self)

	return math.degrees(math.atan2(-targetRel.y, targetRel.x) % (2 * math.pi))


def from_angle(angle):
	radAngle = math.radians(-angle)
	returnVec = Vector2(math.cos(radAngle), math.sin(radAngle))
	# print(returnVec)
	if angle % 90 == 0:
		if returnVec.x == 1 or returnVec.x == -1:
			returnVec.y = 0
		if returnVec.y == 1 or returnVec.y == -1:
			returnVec.x = 0
	return returnVec


def vec_to(self, target):
	return from_angle(angle_to(self, target))