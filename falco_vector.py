import pygame
from fg_settings import Settings 

class Falco:
	"""A class to manage Falco."""

	def __init__(self, falco_game):
		"""Initialize Falco and set its starting position."""
		self.screen = falco_game.screen
		self.screen_rect = falco_game.screen.get_rect()
		self.settings = falco_game.settings 

		# Load the Falco image and get its rect. 
		self.image = pygame.image.load('images/falco_laser.bmp')
		self.rect = self.image.get_rect()

		# Start Falco at the center left of the screen. 
		self.rect.midleft = self.screen_rect.midleft

		# Movement flag
		self.moving_up = False
		self.moving_down = False

	def update(self):
		"""Update Falco's position based on the movement flag."""
		if self.moving_up and self.rect.top > 0:
			self.rect.y -= self.settings.falco_speed
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.rect.y += self.settings.falco_speed

	def blitme(self):
		"""Draw Falco at his current location."""
		self.screen.blit(self.image, self.rect)

	def center_falco(self):
		"""Center Falco on the screen."""
		self.rect.midleft = self.screen_rect.midleft
		self.y = float(self.rect.y)