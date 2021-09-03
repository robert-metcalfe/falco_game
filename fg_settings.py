class Settings:
	"""A class to store all setting for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's static settings."""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (60, 10, 100)

		# Falco settings
		self.falco_limit = 3

		# Laser settings
		self.laser_width = 75
		self.laser_height = 3
		self.laser_color = (255, 0, 0)

		# Alien settings
		self.gaggle_drop_speed = 15

		# How quickly the game speeds up. 
		self.speedup_scale = 1.1

		# How quickly the Marth point value increases.
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""initialize settings that change throughout the game."""
		self.falco_speed = 1.0
		self.laser_speed = 1.5
		self.marth_speed = 0.75

		# Gaggle direction of 1 represents down; -1 represents up.
		self.gaggle_direction = 1

		# Scoring
		self.marth_points = 50

	def increase_speed(self):
		"""increase speed settings and Marth point values."""
		self.falco_speed *= self.speedup_scale
		self.laser_speed *= self.speedup_scale
		self.marth_speed *= self.speedup_scale

		self.marth_points = int(self.marth_points * self.score_scale)