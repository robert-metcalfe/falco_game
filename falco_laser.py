import pygame
from pygame.sprite import Sprite 
from fg_settings import Settings 

class FalcoLaser(Sprite):
	"""A class to manage the lasers Falco fires."""

	def __init__(self, falco_game):
		"""Create the laser object fired by Falco."""
		super().__init__()
		self.screen = falco_game.screen
		self.settings = falco_game.settings
		self.color = self.settings.laser_color


		# Create a bullet rect at (0, 0) and then set the correct position. 
		self.rect = pygame.Rect(0, 0, self.settings.laser_width, self.settings.laser_height)
		self.rect.midright = falco_game.falco.rect.midright

		# Store the laser's position as a decimal value. 
		self.x = float(self.rect.x)

	def update(self):
		"""Move the laser across the screen."""
		# Update the decimal position of the laser.
		self.x += self.settings.laser_speed
		# Update the rect position. 
		self.rect.x = self.x

	def draw_laser(self):
		"""Draw the laser to the screen."""
		pygame.draw.rect(self.screen, self.color, self.rect)