import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

# Background colour 
background = (234, 218, 184)

# Block colours
block_red = (245, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)

# Paddle colours
paddle_colour = (142, 135, 123)
paddle_outline = (100, 100, 100)  

# Define the font 
font = pygame.font.SysFont('Constantia', 30)

# Game variables
columns = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False # To check if the ball has gone out of the game window
game_over = 0

# Text Colour
text_colour = (78, 81, 139)

# Define the text font 
font = pygame.font.SysFont('Constantia', 30)

def draw_text(text, font, text_colour, x, y):
	image = font.render(text, True, text_colour)
	screen.blit(image, (x, y))


# Brick wall class
class Wall():
	def __init__(self):
		self.width = screen_width // columns
		self.height = 50

	def create_wall(self):
		self.blocks = []

		# Define an empty list for an individual block 
		block_individual = []
		for row in range(rows):
			# Reset the block row list
			block_row = []

			# Iterate through each column in that row
			for column in range(columns):
				# Generate x and y positions from each block to create the rectangle
				block_x = column * self.width 
				block_y = row * self.height
				rect = pygame.Rect(block_x, block_y, self.width, self.height)

				# Assign block strength based on row
				if row < 2:
					strength = 3
				elif row < 4:
					strength = 2
				elif row < 6:
					strength = 1

				# Create a list to store the rectangle and colour the data
				block_individual = [rect, strength]

				# Append that individual block to the block row
				block_row.append(block_individual)

			# Append the row to the full list of blocks
			self.blocks.append(block_row)


	def draw_wall(self):
		for row in self.blocks:
			for block in row:
				# Assign a colour based on block strength
				if block[1] == 3:
					block_colour = block_blue  
				elif block[1] == 2:
					block_colour = block_green
				elif block[1] == 1:
					block_colour = block_red


				pygame.draw.rect(screen, block_colour, block[0])
				pygame.draw.rect(screen, background, block[0], 2)


class Paddle:
	def __init__(self):
		self.reset()
		
	def move(self):
		# Reset movement direction
		self.direction = 0
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x -= self.speed
			self.direction = 1
		elif key[pygame.K_RIGHT] and self.rect.right < screen_width:
			self.rect.x += self.speed
			self.direction = 0

	def draw(self):
		pygame.draw.rect(screen, paddle_colour, self.rect)
		pygame.draw.rect(screen, paddle_outline, self.rect, 3)

	def reset(self):
		# Define paddle variables
		self.height = 20
		self.width = int(screen_width / columns)
		self.x = int((screen_width / 2) - (self.width / 2))
		self.y = screen_height - (self.height * 2)
		self.speed = 10
		self.rect = Rect(self.x, self.y, self.width, self.height)
		self.direction = 0 # Track the direction the paddle is moving in



# The Ball Class
class Ball:
	def __init__(self, x, y):
		self.reset(x, y)

	def move(self):

		collision_threshold = 5

		# Start off with the assumption that the wall has been destroyed completely
		wall_destroyed = 1
		row_counter = 0
		for row in wall.blocks:
			item_counter = 0
			for item in row:
				# Check for collision with each block in the wall
				if self.rect.colliderect(item[0]):
					# Check if collision is from above
					if abs(self.rect.bottom - item[0].top) < collision_threshold and self.velocity_y > 0:
						self.velocity_y *= -1
					# Check if collision is from below
					if abs(self.rect.top - item[0].bottom) < collision_threshold and self.velocity_y < 0:
						self.velocity_y *= -1
					# Check if collision is from left
					if abs(self.rect.right - item[0].left) < collision_threshold and self.velocity_x > 0:
						self.velocity_x *= -1
					# Check if collision is from right
					if abs(self.rect.left - item[0].right) < collision_threshold and self.velocity_x < 0:
						self.velocity_x *= -1
					# We also reduce the block strength by colliding with it
					if wall.blocks[row_counter][item_counter][1] > 1:
						wall.blocks[row_counter][item_counter][1] -= 1
					else:
						wall.blocks[row_counter][item_counter][0] = (0, 0, 0, 0)

				# Check if block still exists, in which case the wall is not destroyed 
				if wall.blocks[row_counter][item_counter][0] != (0, 0, 0, 0):
					wall_destroyed = 0
				# increase the item counter
				item_counter += 1

			# increase the row counter, having completed the entire row
			row_counter += 1

		# After iterating through all the blocks, check if the wall is destroyed
		if wall_destroyed == 1:
			self.game_over = 1 # The player has won, rather than lost  

		# Check for collision with the walls
		if self.rect.left < 0 or self.rect.right > screen_width:
			self.velocity_x *= -1

		# Check for the collision with the top and bottom
		if self.rect.top < 0:
			self.velocity_y *= -1

		# If the paddle misses the ball, the game should end
		if self.rect.bottom > screen_height:
			self.game_over = -1		

		# Check for collision with the player paddle
		if self.rect.colliderect(player_paddle):
			# Check for collision from the top of the paddle
			if abs(self.rect.bottom - player_paddle.rect.top) < collision_threshold and self.velocity_y > 0:
				self.velocity_y *= -1 
				self.velocity_x += player_paddle.direction
				if self.velocity_x > self.maximum_speed:
					self.velocity_x = self.maximum_speed
				elif self.velocity_x < 0 and self.velocity_x < -self.maximum_speed:
					self.velocity_x = -self.maximum_speed
			else:
				self.velocity_x *= -1


		self.rect.x += self.velocity_x
		self.rect.y += self.velocity_y

		return self.game_over

	def draw(self):
		pygame.draw.circle(screen, paddle_colour, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)
		pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius, 3)

	def reset(self, x, y):
		self.radius = 10
		self.x = x - self.radius
		self.y = y
		self.rect = Rect(self.x, self.y, self.radius * 2, self.radius * 2)
		self.velocity_x = 4
		self.velocity_y = -4
		self.maximum_speed = 5
		self.game_over = 0

# Create the wall
wall = Wall()
wall.create_wall()

# Create the paddle
player_paddle = Paddle()

# Create the ball
ball = Ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)


run = True
while run:

	clock.tick(fps) # Add a limit to how fast the screen updates

	screen.fill(background)

	# Draw all objects
	wall.draw_wall()
	player_paddle.draw()
	ball.draw()

	if live_ball:
		# Move the objects
		player_paddle.move()
		game_over = ball.move()
		if game_over != 0:
			live_ball = False

	# Print player instructions/state
	if not live_ball:
		if game_over == 0:
			draw_text('CLICK ANYWHERE TO START', font, text_colour, 100, screen_height // 2 + 100)
		elif game_over == 1:
			draw_text('YOU WON!', font, text_colour, 240, screen_height // 2 + 50)
			draw_text('CLICK ANYWHERE TO START', font, text_colour, 100, screen_height // 2 + 100)
		elif game_over == -1:
			draw_text('YOU LOST!', font, text_colour, 240, screen_height // 2 + 50)
			draw_text('CLICK ANYWHERE TO START', font, text_colour, 100, screen_height // 2 + 100)

	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
			live_ball = True
			ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
			player_paddle.reset()
			wall.create_wall()

	pygame.display.update()

pygame.quit()