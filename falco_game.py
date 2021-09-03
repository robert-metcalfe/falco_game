import sys, pygame
from time import sleep
from pygame import mixer

from fg_settings import Settings 
from fg_stats import GameStats
from falco_vector import Falco
from falco_laser import FalcoLaser
from marth import Marth 
from fg_button import Button
from fg_scoreboard import Scoreboard

class FalcoGame:
	"""Overall class to manage game assets and behavior."""

	def __init__(self):
		"""initialize the game, and create game resources.""" 
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		self.screen_rect = self.screen.get_rect()
		pygame.display.set_caption("Laser Go BRRRRRR")
 
		self.bg_color = self.settings.bg_color  

		# Create an instance to store game stats,
		# and create a scoreboard.
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.falco = Falco(self)
		self.lasers = pygame.sprite.Group()
		self.marths = pygame.sprite.Group()

		self._create_gaggle()

		# Make the Play button.
		self.play_button = Button(self, "Go!")

	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.falco.update()
				self._update_lasers()
				self._update_marths()
				
			self._update_screen()
			
	def _check_events(self):
		"""Respond to keypresses and mouse events."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self._save_high_score()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""Start a new game when the player clicks 'Go!'"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			# Reset the game settings.
			self.settings.initialize_dynamic_settings()

			# Reset the game statistics.
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_icons()

			# Get rid of any remaining lasers and Marths.
			self.marths.empty()
			self.lasers.empty()

			# Create a new gaggle and center Falco.
			self._create_gaggle()
			self.falco.center_falco()

			# Hide the mouse cursor.
			pygame.mouse.set_visible(False)

			# Play background music.
			self._play_background_music()

	def _check_keydown_events(self, event):
		"""Respond to key presses."""
		if event.key == pygame.K_UP:
			self.falco.moving_up = True
		elif event.key == pygame.K_DOWN:
			self.falco.moving_down = True
		elif event.key == pygame.K_q:
			self._save_high_score()
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._shoot_laser()

	def _check_keyup_events(self, event):
		"""Respond to key releases.""" 
		if event.key == pygame.K_UP:
			self.falco.moving_up = False
		elif event.key == pygame.K_DOWN:
			self.falco.moving_down = False

	def _shoot_laser(self):
		"""Create a new laser and add it to the lasers group"""
		new_laser = FalcoLaser(self)
		self.lasers.add(new_laser)

		# Play a sound when bullet is fired.
		laser_sound = mixer.Sound('laser.wav')
		laser_sound.play()

	def _update_lasers(self):
		"""Update positions for lasers and delete old lasers."""
		self.lasers.update()

		# Get rid of lasers that have disappeared. 
		for laser in self.lasers.copy():
			if laser.rect.left > self.screen_rect.right:
				self.lasers.remove(laser)

		self._check_laser_marth_collisions()

	def _check_laser_marth_collisions(self):
		"""
		Check for any lasers that have hit Marths,
		and get rid of the laser and the Marth.
		"""
		collisions = pygame.sprite.groupcollide(
			self.lasers, self.marths, True, True)

		if collisions:
			for marths in collisions.values():
				self.stats.score += self.settings.marth_points * len(marths)
			self.sb.prep_score()
			self.sb.check_high_score()

			# Play explosion sound when collision occurs.
			hit_sound = mixer.Sound('marth_hit.wav')
			hit_sound.play()

		if not self.marths:
			# Destroy existing lasers and create new gaggle. 
			self.lasers.empty()
			self._create_gaggle()
			self.settings.increase_speed()

			# Increase level.
			self.stats.level += 1
			self.sb.prep_level()

	def _create_gaggle(self):
		"""Create the gaggle of Marths."""
		# Create a Marth and find the number of Marths in a column.
		marth = Marth(self)
		marth_width, marth_height = marth.rect.size
		number_marths_y = self.screen_rect.height // marth_height

		number_columns = 4

		# Create the full gaggle of Marths.
		for column_number in range(number_columns):
			for marth_number in range(number_marths_y):
				self._create_marth(marth_number, column_number)
			
	def _create_marth(self, marth_number, column_number):
		"""Create a Marth and place it in a column."""
		marth = Marth(self)
		marth_width, marth_height = marth.rect.size
		marth.y = marth_height * marth_number
		marth.rect.y = marth.y
		marth.rect.x = self.screen_rect.right - marth.rect.width - (marth.rect.width * column_number) 
		self.marths.add(marth)

	def _update_marths(self):
		"""
		Check if Marths are at an edge/
		Then update the positions of the Marths in the gaggle.
		"""
		self._check_gaggle_edges()
		self.marths.update()

		# Look for Marth-Falco collisions. 
		if pygame.sprite.spritecollideany(self.falco, self.marths):
			self._bird_down()

		# Look for Marths hitting the left of the screen.
		self._check_marths_left()

	def _check_gaggle_edges(self):
		"""Respond appropriately if Marths have reached an edge."""
		for marth in self.marths.sprites():
			if marth.check_edges():
				self._change_gaggle_direction()
				break

	def _change_gaggle_direction(self):
		"""Move the entire gaggle left and change the gaggle's direction."""
		for marth in self.marths.sprites():
			marth.rect.x -= self.settings.gaggle_drop_speed
		self.settings.gaggle_direction *= -1

	def _bird_down(self):
		"""Respond to Falco being grabbed by Marth."""

		if self.stats.falcos_left > 0:
			# Decrement Falcos left, and update scoreboard.
			self.stats.falcos_left -= 1 
			self.sb.prep_icons()

			# Get rid of any remaining Marths and Lasers.
			self.lasers.empty()
			self.marths.empty()

			# Create a new gaggle and center the Falco.
			self._create_gaggle()
			self.falco.center_falco()

			# Play explosion sound when collision occurs.
			falco_sound = mixer.Sound('falco_hit.wav')
			falco_sound.play()

			# Pause.
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

			# Play explosion sound when collision occurs.
			falco_sound = mixer.Sound('falco_hit.wav')
			falco_sound.play()

	def _check_marths_left(self):
		"""Check if any Marths have reached the left of the screen."""
		screen_rect = self.screen.get_rect()
		for marth in self.marths.sprites():
			if marth.rect.left <= screen_rect.left:
				# Treat this the same as if the Falco got grabbed.
				self._bird_down()
				break

	def _save_high_score(self):
		"""Write the high score to a text file."""
		filename = "fg_highscore.txt"
		high_score = round(self.stats.high_score, -1)
		high_score_str = str(high_score)

		with open(filename, 'w') as file_object:
			file_object.write(high_score_str)

	def _play_background_music(self):
		"""Play backround music on a loop."""
		if self.stats.game_active:
			mixer.music.load('fd.wav')
			mixer.music.play(-1)

	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen."""
		self.screen.fill(self.bg_color)

		"""# Load background image (image takes up too much memory).
		background = pygame.image.load('images/fd.bmp')
		self.screen.blit(background, (0,0))"""

		self.falco.blitme()
		for laser in self.lasers.sprites():
			laser.draw_laser()
		self.marths.draw(self.screen)

		# Draw the score information.
		self.sb.show_score()

		# Draw the play button to the screen when the game is inactive.
		if not self.stats.game_active:
			self.play_button.draw_button()

		# Make the most recently drawn screen visible.
		pygame.display.flip()

if __name__ == '__main__':
	fg = FalcoGame()
	fg.run_game()