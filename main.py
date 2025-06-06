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
hero_surface = pygame.transform.scale(heroOriginal_surface, newHero_size)
bat_surface = pygame.transform.scale(batOriginal_surface, newbat_size)

screen = pygame.display.set_mode(new_size) #cria uma janela do tamanho e largura desejaveis
pygame.display.set_caption('BloodLost')
clock = pygame.time.Clock()
test_font = pygame.font.Font('fonts\\Pixeltype.ttf', 50)
text_surface = test_font.render('Game Over', False, 'White')


player_rect = hero_surface.get_rect(topleft = (300,245))
bat_rect = bat_surface.get_rect(topleft = (700,255))

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() # finaliza o pygame
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos) : print('teste')

    screen.blit(backgroud_surface,(0,0))
    screen.blit(text_surface,(400,70))
    bat_rect.x -= 4
    if bat_rect.right <= 0 : bat_rect.left = 1100
    screen.blit(bat_surface,bat_rect)
    screen.blit(hero_surface, player_rect)
    
    # if player_rect.colliderect(bat_rect):
    #     print('collision')

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())


    pygame.display.update()
    clock.tick(60) #diz para não rodar acima de 60 fps
