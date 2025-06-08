import pygame
from sys import exit

# metodo da pontuação do jogo
def display_score():
    currentTime = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {currentTime}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(500, 50))
    screen.blit(score_surf, score_rect)

pygame.init()

# Inicializa a tela
screen = pygame.display.set_mode((800, 600))

# Carrega as sprites
backgroudOriginal_image = pygame.image.load('sprites\\NES - Castlevania 2 Simons Quest.png').convert_alpha()
heroOriginal_surface = pygame.image.load('sprites\\warrior - idle.png').convert_alpha()
batOriginal_surface = pygame.image.load('sprites\\bat.png').convert_alpha()

# pega as escalas das imagens
backgroudOriginal_width, backgroudOriginal_height = backgroudOriginal_image.get_size()
heroOriginal_width, heroOriginal_height = heroOriginal_surface.get_size()
batOriginal_width, batOriginal_height = batOriginal_surface.get_size()

scale_factor = 1.5
scaleHero_factor = 2
scaleBat_factor = 2

new_size = (int(backgroudOriginal_width * scale_factor), int(backgroudOriginal_height * scale_factor))
newHero_size = (int(heroOriginal_width * scaleHero_factor), int(heroOriginal_height * scaleHero_factor))
newbat_size = (int(batOriginal_width * scaleBat_factor), int(batOriginal_height * scaleBat_factor))

backgroud_surface = pygame.transform.scale(backgroudOriginal_image, new_size)
hero_surface = pygame.transform.scale(heroOriginal_surface, newHero_size)
bat_surface = pygame.transform.scale(batOriginal_surface, newbat_size)

# Atualiza tamanho da janela para bater com o fundo
screen = pygame.display.set_mode(new_size)
pygame.display.set_caption('BloodLost')
clock = pygame.time.Clock()
test_font = pygame.font.Font('fonts\\Pixeltype.ttf', 50)

# pega as rects dos objetos
bat_rect = bat_surface.get_rect(topleft=(700, 255))
player_rect = hero_surface.get_rect(topleft=(300, 245))
player_gravity = 0

# Variáveis do jogo
game_active = True #variavel importante para o jogo estiver ou não
start_time = 0
bg_x_pos = 0  # posição do fundo

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 310:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -15
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 310:
                    player_gravity = -15
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                bat_rect.left = 1100
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # Movimento do fundo
        bg_x_pos -= 2  # velocidade do scroll
        if bg_x_pos <= -backgroud_surface.get_width():
            bg_x_pos = 0

        # Desenha duas cópias lado a lado
        screen.blit(backgroud_surface, (bg_x_pos, 0))
        screen.blit(backgroud_surface, (bg_x_pos + backgroud_surface.get_width(), 0))

        display_score()

        # Inimigo bat
        bat_rect.x -= 4
        if bat_rect.right <= 0:
            bat_rect.left = 1100
        screen.blit(bat_surface, bat_rect)

        # Jogador
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 310:
            player_rect.bottom = 310
        screen.blit(hero_surface, player_rect)

        # Colisão
        if bat_rect.colliderect(player_rect):
            game_active = False
    else:
        print('parou')

    pygame.display.update()
    clock.tick(60)
