class GameStats:
	"""Track statistics for Laser Go Brrr"""

	def __init__(self, fg_game):
		"""Initialize statistics."""
		self.settings = fg_game.settings
		self.reset_stats()

		# Start Lasers Go Brr in an inactive state.
		self.game_active = False

		# High score should never be reset.
		self.high_score = 0
		self.load_high_score()

	def load_high_score(self):
		"""Read text file to load high score at the start of the game."""
		try:
			with open("fg_highscore.txt") as file_object:
				contents = file_object.read()
				self.high_score = int(contents)
		except FileNotFoundError:
			with open("fg_highscore.txt", 'w') as file_object:
				file_object.write("0")

	def reset_stats(self):
		"""Initialize statistics that can change during the game."""
		self.falcos_left = self.settings.falco_limit
		self.score = 0
		self.level = 1