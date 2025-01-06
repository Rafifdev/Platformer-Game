# Mengimpor modul pygame untuk membuat game
import pygame
from pygame.locals import *

# Inisialisasi pygame
pygame.init()

# Membuat objek clock untuk mengontrol frame rate
clock = pygame.time.Clock()
fps = 60

# Menentukan ukuran layar
screen_width = 1000
screen_height = 1000

# Membuat layar game dengan ukuran yang ditentukan
screen = pygame.display.set_mode((screen_width, screen_height))

# Memberi judul pada jendela game
pygame.display.set_caption("Platformer Game by Andi, Bagus & Rafif")

# Menyiapkan font untuk teks
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

# Variabel global
tile_size = 50
game_over = 0
main_menu = True
level = 0
max_levels = 7
score = 0

# Inisialisasi warna
white = (255, 255, 255)
blue = (0, 0, 255)

# Memuat gambar latar belakang dan tombol
bg_img = pygame.image.load('img/sky.png')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')

# Fungsi untuk menggambar teks di layar
def draw_text(text, font, text_col, x, y):
    # Render teks ke permukaan gambar
	img = font.render(text, True, text_col)

    # Menampilkan gambar teks pada layar
	screen.blit(img, (x, y))

# Kelas untuk tombol
class Button():
	def __init__(self, x, y, image):
        # Menyimpan gambar dan menentukan area tombol
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
        # Inisialisasi aksi tombol
		action = False

		# Mengambil posisi mouse
		pos = pygame.mouse.get_pos()

		# Mengecek apakah mouse berada di atas tombol dan diklik
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

        # Reset klik jika tombol mouse dilepas
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

        # Menampilkan tombol di layar
		screen.blit(self.image, self.rect)
		return action

# Kelas untuk pemain
class Player():
	def __init__(self, x, y):
        # Memanggil fungsi reset untuk inisialisasi awal
		self.reset(x, y)
	def update(self, game_over):

        # Inisialisasi pergerakan horizontal dan vertikal
		mx = 0
		my = 0
		walk_cooldown = 5
		if game_over == 0:

			# Sistem gerak player
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_a]:
				mx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_d]:
				mx += 5
				self.counter += 1
				self.direction = 1
			if key[pygame.K_a] == False and key[pygame.K_d] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]

            # Animasi berjalan
			if self.counter > walk_cooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]

            # Menambahkan gravitasi
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			my += self.vel_y

            # Menentukan apakah pemain berada di udara
			self.in_air = True
			for tile in world.tile_list:

				# Periksa mentok horizontal
				if tile[1].colliderect(self.rect.x + mx, self.rect.y, self.width, self.height):
					mx = 0

				# Periksa mentok vertikal
				if tile[1].colliderect(self.rect.x, self.rect.y + my, self.width, self.height):
					if self.vel_y < 0:
						my = tile[1].bottom - self.rect.top
						self.vel_y = 0
					elif self.vel_y >= 0:
						my = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False

            # Periksa nabrak dengan musuh atau rintangan
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over = -1
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1

            # Perbarui posisi pemain
			self.rect.x += mx
			self.rect.y += my

		elif game_over == -1:
            # Tampilkan gambar pemain mati dan teks GAME OVER
			self.image = self.dead_image
			draw_text('GAME OVER!', font, blue, (screen_width // 2) - 150, screen_height // 2)
			if self.rect.y > 200:
				self.rect.y -= 5

        # Tampilkan gambar pemain di layar
		screen.blit(self.image, self.rect)
		return game_over


	def reset(self, x, y):
        # Animasi player
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(1, 13):
			img_right = pygame.image.load(f'img/player{num}.png')
			img_right = pygame.transform.scale(img_right, (40, 80))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('img/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True

# Kelas untuk map
class World():
	def __init__(self, data):
		self.tile_list = []

        # Memuat gambar untuk tile map
		tileup1_img = pygame.image.load('img/tileup1.png')
		tileup2_img = pygame.image.load('img/tileup2.png')
		tileup3_img = pygame.image.load('img/tileup3.png')
		tileup4_img = pygame.image.load('img/tileup4.png')
		tileup5_img = pygame.image.load('img/tileup5.png')
		tileup6_img = pygame.image.load('img/tileup6.png')
		tiledown1_img = pygame.image.load('img/tiledown1.png')
		tiledown2_img = pygame.image.load('img/tiledown2.png')
		tiledown3_img = pygame.image.load('img/tiledown3.png')
		tiledown4_img = pygame.image.load('img/tiledown4.png')
		tiledown5_img = pygame.image.load('img/tiledown5.png')
		borderup1_img = pygame.image.load('img/borderup1.png')
		borderup2_img = pygame.image.load('img/borderup2.png')
		borderup3_img = pygame.image.load('img/borderup3.png')
		borderup4_img = pygame.image.load('img/borderup4.png')
		borderup5_img = pygame.image.load('img/borderup5.png')
		borderup6_img = pygame.image.load('img/borderup6.png')
		borderleft1_img = pygame.image.load('img/borderleft1.png')
		borderleft2_img = pygame.image.load('img/borderleft2.png')
		borderleft3_img = pygame.image.load('img/borderleft3.png')
		borderright1_img = pygame.image.load('img/borderright1.png')
		borderright2_img = pygame.image.load('img/borderright2.png')
		barrel_img = pygame.image.load('img/barrel.png')
		box_img = pygame.image.load('img/box.png')
		vase_img = pygame.image.load('img/vase.png')

        # Membuat daftar tile dari data
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(tileup1_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(tileup2_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					img = pygame.transform.scale(tileup3_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 4:
					img = pygame.transform.scale(tileup4_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 5:
					img = pygame.transform.scale(tileup5_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 6:
					img = pygame.transform.scale(tileup6_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 7:
					img = pygame.transform.scale(tiledown1_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 8:
					img = pygame.transform.scale(tiledown2_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 9:
					img = pygame.transform.scale(tiledown3_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 10:
					img = pygame.transform.scale(tiledown4_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 11:
					img = pygame.transform.scale(tiledown5_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 12:
					img = pygame.transform.scale(borderup1_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 13:
					img = pygame.transform.scale(borderup2_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 14:
					img = pygame.transform.scale(borderup3_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 15:
					img = pygame.transform.scale(borderup4_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 16:
					img = pygame.transform.scale(borderup5_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 17:
					img = pygame.transform.scale(borderup6_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 18:
					img = pygame.transform.scale(borderleft1_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 19:
					img = pygame.transform.scale(borderleft2_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 20:
					img = pygame.transform.scale(borderleft3_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 21:
					img = pygame.transform.scale(borderright1_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 22:
					img = pygame.transform.scale(borderright2_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 23:
					img = pygame.transform.scale(barrel_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 24:
					img = pygame.transform.scale(box_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 25:
					img = pygame.transform.scale(vase_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 26:
					blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
					blob_group.add(blob)
				if tile == 27:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)
				if tile == 28:
					barrel = Barrel(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					barrel_group.add(barrel)
				if tile == 29:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					exit_group.add(exit)
				col_count += 1
			row_count += 1

    # Kelas untuk memunculkan semua tile di map
	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
# Kelas untuk musuh
class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

        # Membuat gambar musuh
		self.image = pygame.image.load('img/blob.png')
		self.rect = self.image.get_rect()

        # Mengambil koordinat
		self.rect.x = x
		self.rect.y = y

        # Pergerakan object musuh
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
        # Menggerakan mush
		self.rect.x += self.move_direction
		self.move_counter += 1
        # Membalik arah pergerakan setelah bergerak sejauh 50 piksel
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1

# Kelas untuk lava sebagai rintangan
class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

# Kelas untuk item barrel
class Barrel(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/barrel.png')
		self.image = pygame.transform.scale(img, (tile_size // 1, tile_size // 1))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

# Fungsi untuk mereset level
def reset_level():
    global world, barrel_group, blob_group, score  
    print("Resetting level...")  
    blob_group.empty()  
    world = World(world_data) 
    score = 0  

# Kelas untuk pintu keluar level
class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/exit.png')
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

world_data = [
    [12, 13, 14, 13, 12, 14, 15, 16, 17, 12, 12, 13, 14, 12, 13, 14, 12, 12, 12, 15], 
    [18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21], 
    [18, 0, 0, 0, 0, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 29, 22], 
    [19, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 0, 2, 2, 22], 
    [20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 5, 0, 0, 0, 21], 
    [18, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 21], 
    [19, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22], 
    [18, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21], 
    [20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21], 
    [19, 0, 2, 0, 0, 0, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22], 
    [18, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 26, 28, 0, 26, 0, 0, 0, 0, 21], 
    [20, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 22], 
    [20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 0, 22], 
    [19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 21], 
    [18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 0, 0, 0, 0, 0, 0, 22], 
    [18, 0, 0, 0, 0, 0, 0, 28, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 21], 
    [19, 0, 0, 0, 0, 0, 2, 2, 2, 27, 27, 27, 27, 27, 7, 7, 7, 7, 7, 22], 
    [19, 0, 0, 0, 0, 2, 7, 7, 9, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7, 22], 
    [18, 0, 0, 0, 2, 7, 8, 9, 7, 7, 10, 11, 7, 7, 7, 9, 7, 11, 7, 21], 
    [20, 3, 2, 2, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 10, 7, 7, 22]
]

# Inisialisasi permain
player = Player(100, screen_height - 130)

# Membuat grup sprite untuk elemen permainan
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
barrel_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# Menambahkan barrel untuk skor
score_barrel = Barrel(tile_size // 2, tile_size // 2)
barrel_group.add(score_barrel)

# inisialisasi map
world = World(world_data)

# Membuat tombol untuk memulai, me-restart, dan keluar
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

# Variabel untuk menjalankan loop game
run = True
while run:
	clock.tick(fps)
	screen.blit(bg_img, (0, 0))

	if main_menu == True:
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
	else:
		world.draw()
		if game_over == 0:
            # Memperbarui gerakan musuh
			blob_group.update()

            # Memeriksa pemain menyentuh dengan barrel (skor bertambah)
			if pygame.sprite.spritecollide(player, barrel_group, True):
				score += 1
    
            # Menampilkan skor di layar
			draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)

        # Menampilkan grup sprite di layar
		blob_group.draw(screen)
		lava_group.draw(screen)
		barrel_group.draw(screen)
		exit_group.draw(screen)

		game_over = player.update(game_over)

		if game_over == -1:
            # Menampilkan tombol restart jika permainan selesai
			if restart_button.draw():
				reset_level()
				player.reset(100, screen_height - 130)
				game_over = 0
				score = 0

		if game_over == 1:
            # Menampilkan teks jika pemain menang
			draw_text('YOU WIN!', font, blue, (screen_width // 2) - 115, screen_height // 2 - 100)
			draw_text(f'barrels Collected: {score}', font_score, white, (screen_width // 2) - 90, screen_height // 2 - 50)

            # Menentukan posisi tombol
			button_x = (screen_width // 2) - (exit_button.rect.width // 2)
			button_y = (screen_height // 2) + 20 
			exit_button.rect.topleft = (button_x, button_y)
			if exit_button.draw():
				run = False

    # Jika pencet x maka game akan keluar
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

    # Memperbarui tampilan layar
	pygame.display.update()

# Keluar dari game
pygame.quit()
