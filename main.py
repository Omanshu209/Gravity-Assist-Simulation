'''
Formulae used :
	
	1) Pythagoras theorem - Hypotenuse² = Perpendicular² + Base²
	2) Newton's second law of motion - Force = mass x acceleration
	3) Newton's law of gravitation - Force = (G x mass1 x mass2) / distance²
	4) Trigonometric functions - atan2(y, x) : arc tangent, sin(radians) : sine, cos(radians) : cosine
'''

# importing required modules
import pygame
from math import atan2, sin, cos, sqrt

pygame.init()# initialising pygame

# declaring constants
WIDTH : int = 800
HEIGHT : int = 600

WHITE_RGB : tuple = (255, 255, 255)
ORANGE_RGB : tuple = (255, 165, 0)
BLUE_RGB : tuple = (0, 0, 200)
BLACK_RGB : tuple = (0, 0, 0)

# creating the window and setting its caption
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect")

# declaring constants
PLANET_MASS : int = 100
PLANET_RADIUS : int = 50
OBJ_MASS : int = 5
OBJ_RADIUS : int = 5
G : int = 5
FPS : int = 60
VELOCITY_SCALE : int = 100

# loading and scaling the images
BG = pygame.transform.scale(pygame.image.load("assets/background.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("assets/jupiter.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))

class Planet:
	
	def __init__(self, x : int, y : int, mass : float):
		self.x : int = x
		self.y : int = y
		self.mass : float = mass
	
	def draw(self):
		window.blit(PLANET, (self.x - PLANET_RADIUS, self.y - PLANET_RADIUS))

class Object:
	
	def __init__(self, x : int, y : int, velocity_x : float, velocity_y : float, mass : float):
		self.x : int = x
		self.y : int = y
		self.velocity_x : float = velocity_x
		self.velocity_y : float = velocity_y
		self.mass : float = mass
	
	def draw(self):
		pygame.draw.circle(window, ORANGE_RGB, (round(self.x), round(self.y)), OBJ_RADIUS)
	
	def move(self, planet = None):
		distance : float = sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)# using pythagoras theorem
		force : float = (G * self.mass * planet.mass) / (distance ** 2)# using Newton's law of gravitation
		
		acceleration : float = force / self.mass# using Newton's second law of motion
		angle : float = atan2(planet.y - self.y, planet.x - self.x)
		
		# finding the vertical and horizontal components of the acceleration
		acceleration_x : float = acceleration * cos(angle)
		acceleration_y : float = acceleration * sin(angle)
		
		# updating the velocity
		self.velocity_x += acceleration_x
		self.velocity_y += acceleration_y
		
		# updating the position
		self.x += self.velocity_x
		self.y += self.velocity_y

# a function to create an object of the class 'Object'
def create_object(location, mouse):
	t_x, t_y = location
	m_x, m_y = mouse
	velocity_x : float = (m_x - t_x) / VELOCITY_SCALE
	velocity_y : float = (m_y - t_y) / VELOCITY_SCALE
	obj : Object = Object(t_x, t_y, velocity_x, velocity_y, OBJ_MASS)
	return obj

def main():
	running : bool = True
	clock = pygame.time.Clock()
	
	planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
	objects : list = []
	temp_obj_pos = None
	
	while running:
		window.fill(BLACK_RGB)
		clock.tick(FPS)
		
		mouse_pos = pygame.mouse.get_pos()
		
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				running : bool = False
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				if temp_obj_pos:
					obj = create_object(temp_obj_pos, mouse_pos)
					objects.append(obj)
					temp_obj_pos = None
				else:
					temp_obj_pos = mouse_pos
		
		window.blit(BG, (0, 0))
		
		if temp_obj_pos:
			pygame.draw.line(window, WHITE_RGB, temp_obj_pos, mouse_pos, 2)
			pygame.draw.circle(window, ORANGE_RGB, temp_obj_pos, OBJ_RADIUS)
		
		# updating the position of objects
		for obj in objects[:]:
			obj.draw()
			obj.move(planet)
			off_screen = obj.x < 0 or obj.y < 0 or obj.x > WIDTH or obj.y > HEIGHT
			collided = sqrt((obj.x - planet.x) ** 2 + (obj.y - planet.y) ** 2) <= PLANET_RADIUS
			
			if off_screen or collided:
				objects.remove(obj)
		
		planet.draw()
		
		pygame.display.update()# updating the window

if __name__ == "__main__":
	main()

pygame.quit()