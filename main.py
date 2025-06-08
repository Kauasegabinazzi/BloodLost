import pygame
from sys import exit

pygame.init() #permite iniciar a biblioteca e usar seus recursos

screen = pygame.display.set_mode((800, 600))

backgroudOriginal_image = pygame.image.load('sprites\\NES - Castlevania 2 Simons Quest.png').convert_alpha() #carrega as imagens numa variavel
heroOriginal_surface = pygame.image.load('sprites\\warrior - idle.png').convert_alpha() # convert_alpha ajuda o pygame a trabalhar melhor com as sprites
batOriginal_surface = pygame.image.load('sprites\\bat.png').convert_alpha() 

backgroudOriginal_width, backgroudOriginal_height = backgroudOriginal_image.get_size()
heroOriginal_width, heroOriginal_height = heroOriginal_surface.get_size()
batOriginal_width, batOriginal_height = batOriginal_surface.get_size()

scale_factor = 1.5
scaleHero_factor = 2
scaleBat_factor = 2

new_size = (backgroudOriginal_width * scale_factor, backgroudOriginal_height * scale_factor)
newHero_size = (heroOriginal_width * scaleHero_factor, heroOriginal_height * scaleHero_factor)
newbat_size = (batOriginal_width * scaleBat_factor, batOriginal_height * scaleBat_factor)

backgroud_surface = pygame.transform.scale(backgroudOriginal_image, new_size)

screen = pygame.display.set_mode(new_size) #cria uma janela do tamanho e largura desejaveis
pygame.display.set_caption('BloodLost')
clock = pygame.time.Clock()
test_font = pygame.font.Font('fonts\\Pixeltype.ttf', 50)

score_surf = test_font.render('My Game', False, (255, 255, 255))
score_rect = score_surf.get_rect(center = (500, 50))

bat_surface = pygame.transform.scale(batOriginal_surface, newbat_size)
bat_rect = bat_surface.get_rect(topleft = (700,255))

hero_surface = pygame.transform.scale(heroOriginal_surface, newHero_size)
player_rect = hero_surface.get_rect(topleft = (300,245))
player_gravity = 0



while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() # finaliza o pygame

        if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 310:
            if player_rect.collidepoint(event.pos) : 
                 player_gravity = -15

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= 310 :
                player_gravity = -15

    screen.blit(backgroud_surface,(0,0))
    
    pygame.draw.rect(screen,(148, 0, 211), score_rect, border_radius=5)
    pygame.draw.rect(screen, (255, 20, 147), score_rect, width=2, border_radius=5)
    
    screen.blit(score_surf,score_rect)

    bat_rect.x -= 4
    if bat_rect.right <= 0 : bat_rect.left = 1100

    screen.blit(bat_surface,bat_rect)

    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 310: player_rect.bottom = 310
    screen.blit(hero_surface, player_rect)
    
    pygame.display.update()
    clock.tick(60) #diz para não rodar acima de 60 fps
