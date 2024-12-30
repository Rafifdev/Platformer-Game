# Import dan Inisialisasi
import pygame
pygame.init()

# Ukuran layar
screen_height = 800
screen_width = 800

# Ukuran tiap kotak
tile_size = 40

# Membuat layar
screen = pygame.display.set_mode((screen_height,screen_width))
pygame.display.set_caption("Platformer Game by Andi, Bagus & Rafif")

# Initialisasi gambar
bg_img = pygame.image.load('img/sky.jpg') 
sun_img = pygame.image.load('img/sun.png')

# Membuat Grid Pada Layar
def white_grid():
  for line in range(0, 21):
    pygame.draw.line(screen, (255,255,255), (0, line * tile_size), (screen_width, line * tile_size))
    pygame.draw.line(screen, (255,255,255), (line * tile_size, 0), (line * tile_size, screen_height))

# Membuat player
class Player():
  def __init__(self, x, y):
    img = pygame.image.load('img/player1.png')
    
    # Menyimpan animasi untuk gerakan ke kanan.
    self.images_right = []
    
    # Menyimpan animasi untuk gerakan ke kanan.
    self.images_left = []
    
    self.index = 0
    self.counter = 0
    
    # Animasi
    for num in range(1, 5):
      
      # inisialisasi gambar
      img_right = pygame.image.load(f'img/player{num}.png')
      
      # Mengatur ukuran gambar player
      img_right = pygame.transform.scale(img_right, (40, 80))
      
      # Membalik gambar horizontal untuk animasi ke kiri.
      img_left = pygame.transform.flip(img_right, True, False)
      
      # Memasukan ke array
      self.images_right.append(img_right)
      self.images_left.append(img_left)
    
    # Gambar awal pemain (player 1)
    self.image = self.images_right[self.index]
    
    # Mengatur ukuran gambar player
    self.image = pygame.transform.scale(img, (40, 80))
    
    # Mengambil posisi gambar plaeyr
    self.rect = self.image.get_rect()
    
    # Mengatur ukuran gambar player X dan Y
    self.rect.x = x
    self.rect.y = y
    
    self.width = self.image.get_width()
    self.height = self.image.get_height()
    
    self.graf_y = 0
    self.jumped = False
    self.direction = 0
    
  # function untuk pergerakan
  def update(self):
    mx = 0
    my = 0
    walk_cooldown = 40
    
    # Memeriksa tombol yang di pencet
    key = pygame.key.get_pressed()
    
    # Tombol untuk melompat ( W )
    if key[pygame.K_w] and self.jumped == False:
      self.graf_y = -5
      
      # Saat di pencet menjadi true
      self.jumped = True

    # Saat tidak di pencet menjadi False
    if key[pygame.K_w] == False:
      self.jumped = False
    
    # Tombol untuk jalan ke kiri ( A )
    if key[pygame.K_a]:
      mx -= 0.8
      self.counter += 1
      self.direction = -1
    
    # Tombol untuk jalan ke kanan ( D )
    if key[pygame.K_d]:
      mx += 0.8
      self.counter += 1
      self.direction = 1
    
    # Kalau tombol tidak di pencet = false
    if key[pygame.K_a] == False and key[pygame.K_d] == False:
      self.counter = 0
      self.index = 0
      
      if self.direction == 1:
        self.image = self.images_right[self.index]
      if self.direction == -1:
        self.image = self.images_left[self.index]

    # Membuat Animasi
    if self.counter > walk_cooldown:
      self.counter = 0	
      self.index += 1
      if self.index >= len(self.images_right):
        self.index = 0
      if self.direction == 1:
        self.image = self.images_right[self.index]
      if self.direction == -1:
        self.image = self.images_left[self.index]
    
    # Secret button
    if key[pygame.K_1]:
      my -= 1.5
      
    # Gravitasi
    self.graf_y += 0.1
    if self.graf_y >= 1:
      self.graf_y = 0.1
    my += self.graf_y
    
    for tile in world.tile_list:
      if tile[1].colliderect(self.rect.x + mx, self.rect.y, self.width, self.height):
        mx = 0
      if tile[1].colliderect(self.rect.x, self.rect.y + my, self.width, self.height):
        if self.graf_y < 0:
          my = tile[1].bottom - self.rect.top
          self.graf_y = 0
        elif self.graf_y >= 0:
          my = tile[1].top - self.rect.bottom
          self.graf_y = 0
          
    # Membatasi gerakan player dalam layar.
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

    # Menampilkan gambar player        
    screen.blit(self.image, self.rect)
    
    # Untuk membuat border di sekitar player
    #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

# Class world
class World():
  def __init__(self, data):
    self.tile_list = [] 
    
    # Inisialisasi gambar ke variabel
    dirt_img = pygame.image.load('img/dirt.png')
    grass_img = pygame.image.load('img/grass.png')
    fire_img = pygame.image.load('img/fire.png')
    slime_img = pygame.image.load('img/slime.png')
    
    row_count = 0 
    for row in data:
      col_count = 0 
      for tile in row:
        
        # Jika tile bernilai 1, gambar tanah (dirt).
        if tile == 1:
          img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          tile = (img, img_rect)
          self.tile_list.append(tile)
        
        # Jika tile bernilai 2, gambar rumput (grass).
        if tile == 2:
          img = pygame.transform.scale(grass_img, (tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          tile = (img, img_rect)
          self.tile_list.append(tile)
        
        # Jika tile bernilai 3, gambar slime.
        if tile == 3:
          img = pygame.transform.scale(slime_img,(tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          tile = (img, img_rect)
          self.tile_list.append(tile)
          
        # Jika tile bernilai 6, gambar api (fire).
        if tile == 6:
          img = pygame.transform.scale(fire_img, (tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          tile = (img, img_rect)
          self.tile_list.append(tile)
        col_count += 1 
      row_count += 1 

  # Fungsi untuk menggambar tile pada layar.
  def draw(self):
    for tile in self.tile_list:
        screen.blit(tile[0], tile[1])
        # Untuk membuat border di sekitar tile
        #pygame.draw.rect(screen, (255, 255, 255), tile[1], 1)

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

# Inisialisasi class
world = World(world_map)
player = Player(80, 680)

# Kondisi awal start = true
start = True
while start:
  screen.blit(bg_img, (0, 0)) 
  screen.blit(sun_img, (350, 60))

  # Menjalankan class world
  world.draw()
  
  # Menjalanlan class player
  player.update()
  # white_grid() 

  # Jika quit start menjadi False
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          start = False
          
  pygame.display.update()
pygame.quit()