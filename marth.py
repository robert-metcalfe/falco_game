import pygame
from pygame.sprite import Sprite 

class Marth(Sprite):
	"""A class to represent a single Marth in the gaggle of Marths."""

	def __init__(self, fg_game):
		"""Initialize the Marth and set its starting position."""
		super().__init__()
		self.screen = fg_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = fg_game.settings 

		# Load the Marth image and set its rect attribute.
		self.image = pygame.image.load('images/marth.bmp')
		self.rect = self.image.get_rect()

		# Start each new alien near the top-right of the screen.
		self.rect.x = self.screen_rect.right - self.rect.width
		self.rect.y = 0

		# Store the Marth's exact horizontal position. 
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

	def check_edges(self):
		"""Return True if Marths are at edge of screen."""
		screen_rect = self.screen.get_rect()

		if self.rect.bottom >= screen_rect.bottom or self.rect.top < 0:
			return True

	def update(self):
		"""Move the Marth up or down."""
		self.y += (self.settings.marth_speed * self.settings.gaggle_direction)
		self.rect.y = self.y
