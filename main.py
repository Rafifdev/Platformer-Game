import pygame

# Installasi
pygame.init()

# Screen size
screen_height = 800
screen_width = 800

screen = pygame.display.set_mode((screen_height,screen_width))
pygame.display.set_caption("Platformer Game by Rafif, Andi, & Bagus")

# Load image
bg_img = pygame.image.load('img/sky.jpg')
sun_img = pygame.image.load('img/sun.png')

# variabel game
tile_size = 160

running = True
while running:
  screen.blit(bg_img, (0,0))
  screen.blit(sun_img, (350,60))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

  pygame.display.update()
pygame.quit()