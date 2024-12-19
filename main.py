import pygame
pygame.init()

screen_height = 800
screen_width = 800
tile_size = 40

screen = pygame.display.set_mode((screen_height,screen_width))
pygame.display.set_caption("Platformer Game by Andi, Bagus & Rafif")
bg_img = pygame.image.load('img/sky.jpg') 
sun_img = pygame.image.load('img/sun.png')

def white_grid():
  for line in range(0, 21):
    pygame.draw.line(screen, (255,255,255), (0, line * tile_size), (screen_width, line * tile_size))
    pygame.draw.line(screen, (255,255,255), (line * tile_size, 0), (line * tile_size, screen_height))

class Player():
  def __init__(self, x, y):
    img = pygame.image.load('img/player1.png')
    self.image = pygame.transform.scale(img, (40, 80))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.graf_y = 0
    self.jumped = False
    
  def update(self):
    mx = 0
    my = 0
    
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE] and self.jumped == False:
      self.graf_y = -5
      self.jumped = True
    if key[pygame.K_SPACE] == False:
      self.jumped = False
    if key[pygame.K_LEFT]:
      mx -= 0.8
    if key[pygame.K_RIGHT]:
      mx += 0.8
      
    if key[pygame.K_1]:
      my -= 1.5
    if key[pygame.K_2]:
      my += 1.5
      
    # Gravitasi
    self.graf_y += 0.1
    if self.graf_y >= 1:
      self.graf_y = 0.1
    my += self.graf_y
    
    self.rect.x += mx
    self.rect.y += my

    if self.rect.bottom > screen_height:
      self.rect.bottom = screen_height
    
    if self.rect.right > screen_width:
        self.rect.right = screen_width

    if self.rect.left < 0:
        self.rect.left = 0
        
    if self.rect.top < 0:
        self.rect.top = 0

    
    screen.blit(self.image, self.rect)

class World():
  def __init__(self, data):
    self.tile_list = [] 
    
    dirt_img = pygame.image.load('img/dirt.png')
    grass_img = pygame.image.load('img/grass.png')
    fire_img = pygame.image.load('img/fire.png')
    slime_img = pygame.image.load('img/slime.png')
    
    row_count = 0 
    for row in data:
      col_count = 0 
      for tile in row:
        
        if tile == 1:
          img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          tile = (img, img_rect)
          self.tile_list.append(tile)
          
        if tile == 2:
          img = pygame.transform.scale(grass_img, (tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          tile = (img, img_rect)
          self.tile_list.append(tile)
          
        if tile == 3:
          img = pygame.transform.scale(slime_img,(tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          tile = (img, img_rect)
          self.tile_list.append(tile)
        
        if tile == 6:
          img = pygame.transform.scale(fire_img, (tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          tile = (img, img_rect)
          self.tile_list.append(tile)
        col_count += 1 
      row_count += 1 

  def draw(self):
    for tile in self.tile_list:
        screen.blit(tile[0], tile[1])

world_map = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
  [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
  [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
  [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
  [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
  [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
  [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
  [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
  [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
  [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
  [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
  [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(world_map)
player = Player(80, 680)

start = True
while start:
  screen.blit(bg_img, (0, 0)) 
  screen.blit(sun_img, (350, 60))

  world.draw()
  player.update()
  # white_grid() 

  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          start = False
          
  pygame.display.update()
pygame.quit()