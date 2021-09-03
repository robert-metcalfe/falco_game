import pygame
from fg_settings import Settings 
from pygame.sprite import Sprite

class Icon(Sprite):
	"""A class to manage the stock icon."""

	def __init__(self, falco_game):
		"""Initialize Falco and set its starting position."""
		super().__init__()
		self.screen = falco_game.screen
		self.screen_rect = falco_game.screen.get_rect()
		self.settings = falco_game.settings 

		# Load the Falco image and get its rect. 
		self.image = pygame.image.load('images/icon.bmp')
		self.rect = self.image.get_rect()

		# Start Falco at the center left of the screen. 
		self.rect.midleft = self.screen_rect.midleft

		# Movement flag
		self.moving_up = False
		self.moving_down = False

	def blitme(self):
		"""Draw Falco at his current location."""
		self.screen.blit(self.image, self.rect)