import pygame
import time
import pygame_menu
from pygame_menu import Theme

WIDTH = 800
pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("SkySearch Game")

RED = (0, 255, 100)
GREEN = (0, 155, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (25, 25, 25)
BLACK = (128,128,128)
PURPLE = (0, 0, 100)
ORANGE = (215, 55 ,55)
GREY = (0,0,0)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		# check if you are in the grid             check if not barrier
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()
	


visited = set()

def dfs_I(draw,grid,start,end):
	# pilha 
	stack, visited = [], []
	stack.append(start)
	print("\nDFS : ")
	came_from = {}

	while len(stack)>0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		cube = stack.pop()

		if cube == end:
			reconstruct_path(came_from,end,draw)
			print("Achei o Planeta Gama, vou colonizá-lo!!")
			start.make_start()
			end.make_end()
			break
		
		#print(f"Estou em ({cube.get_pos()[0]},{cube.get_pos()[1]})")

		if cube not in visited:
			visited.append(cube)
			print(cube.get_pos())
		for neighbor in cube.neighbors:
			if neighbor not in visited:
				stack.append(neighbor)
				neighbor.make_open()
				came_from[neighbor] = cube

		if cube != start:
			cube.make_closed()

		draw()    

visited_bfs = [] # List for visited nodes.
queue = []     #Initialize a queue	

def bfs(draw,grid, start,end): #function for BFS
	visited_bfs.append(start)
	queue.append(start)
	came_from = {}

	while queue:          # Creating loop to visit each node
		m = queue.pop(0) 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		if m == end:
			print("Spaceship achou o Planeta Gama\nSe divirta com seu Planeta, crie uma civilização nele!!")
			reconstruct_path(came_from,end,draw)
			end.make_end()
			start.make_start()
			return True

		#print(f"Estou em ({m.get_pos()[0]},{m.get_pos()[1]})")
		for neighbor in m.neighbors:

			if neighbor not in visited_bfs:
				visited_bfs.append(neighbor)
				queue.append(neighbor)
				came_from[neighbor] = m
				neighbor.make_open()


		if m != start:
			m.make_closed()
		draw()


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def set_difficulty(value, difficulty):
	# Do the job here !

	global box

	box = 25

	#print(f"valor = {value}\nDificuldade = {difficulty}")

	if difficulty == 3:
		box = 10
		#print(f"box = {box}")
		return  
	elif difficulty == 2:
		box = 25
		#print(f"box = {box}")

		return 
	else:
		box = 50
		#print(f"box = {box}")
		return 

search = 1

# entrega criar um repositório
	# link pro repo dentro da organização
	# e o vídeo de 3 a 5 min mostrando o trabalho rodando explicando o que é
	# mostrar no código os pontos principais
	# de preferência com os 2 membros :/

def set_search(value, busca):
	global search

	search = 1

	if busca == 1: # dfs
		search = 1
		#print(f"search = {search}")

	else: # bfs
		search = 2
		#print(f"search = {search}")

def start_the_game():
	# Do the job here !

	win,width = WIN,WIDTH 
	ROWS = box
	grid = make_grid(ROWS, width)

	start = None
	end = None
	run = True

	while run:
		draw(win, grid, ROWS, width)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		
			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]

				# verifica se já começou ou não e se não é o final
				if not start and spot != end:
					start = spot
					start.make_start()

				# verifica se já colocou o final e se não é o começo
				elif not end and spot != start:
					end = spot
					end.make_end()

				# se não for começo e nem final é barreira
				elif spot != end and spot != start:
					spot.make_barrier()

			# clique com a direita do mouse significa não seleciona mais
			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None
		
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					if search == 1:
						dfs_I(lambda: draw(win, grid, ROWS, width),grid,start,end)
					else:
						bfs(lambda: draw(win, grid, ROWS, width),grid,start,end)
						
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

				if event.key == pygame.K_m:
					start = None
					end = None
					#grid = make_grid(ROWS, width)
					main(win,width)

		
	pygame.quit()

def main(win, width):
	font = pygame_menu.font.FONT_FIRACODE

	mytheme = Theme(background_color=(0,0,0,0), # transparent background
                title_background_color=(4, 47, 126),
                title_font_shadow=True,
                widget_padding=25,
				widget_font = font,
				widget_font_color = (255,255,255),
				widget_font_size = 15
                )

	#pygame_menu.themes.THEME_DARK
	menu = pygame_menu.Menu('Welcome To The SkySearch Game', WIDTH, WIDTH,
		theme=mytheme)

	about_theme = pygame_menu.themes.THEME_DARK.copy()
	about_theme.widget_margin = (0, 0)
	about_theme.font = font

	about_menu = pygame_menu.Menu(
		'About', WIDTH, WIDTH,
		theme=mytheme
	)

	text = ["""Your objective is first :\n1 - Place the Spaceship\n2 - Place the Planet Gama \n 
	then place the barriers in order to make it difficult\n (and not impossible)\n
	for the Spaceship to reach the Planeta Gama.\n'"""]

	for m in text:
		about_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=15)
		about_menu.add.vertical_margin(30)
		about_menu.add.button('Return to menu', pygame_menu.events.BACK)

	menu.add.selector('Difficulty :', [('Easy 10 rows',3),('Medium 25 rows', 2),('Hard 50 rows', 1)],default = 1 ,onchange=set_difficulty)
	menu.add.selector('Busca :', [('DFS', 1), ('BFS', 2)],default = 1 ,onchange=set_search)
	menu.add.button('Play', start_the_game)
	menu.add.button('Objective', about_menu)
	menu.add.button('Quit', pygame_menu.events.EXIT)

	# gambiarra, adicionei um botão para adicionar um texto, pardon
	menu.add.button('Press C to clear the screen', )
	menu.add.button('Press M to return to the menu', )
	menu.add.button('Press Space to launch the algorithm', )

	menu.mainloop(WIN)

main(WIN,WIDTH)