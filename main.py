import pygame
from sys import exit

# metodo da pontuação do jogo
def display_score():
    currentTime = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {currentTime}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(500, 50))
    screen.blit(score_surf, score_rect)
    return currentTime

pygame.init()

# Inicializa a tela
screen = pygame.display.set_mode((800, 600))

# Carrega as sprites
backgroudOriginal_image = pygame.image.load('sprites\\NES - Castlevania 2 Simons Quest.png').convert_alpha()
heroOriginal_surface = pygame.image.load('sprites\\warrior - idle.png').convert_alpha()
batOriginal_surface = pygame.image.load('sprites\\bat.png').convert_alpha()
knightOriginal_surface = pygame.image.load('sprites\\Enemie1 - idle.png').convert_alpha()
owlOriginal_surface = pygame.image.load('sprites\\Enemie2 - idle.png').convert_alpha()
zombieOriginal_surface = pygame.image.load('sprites\\Enemie3 - idle.png').convert_alpha()
catOriginal_surface = pygame.image.load('sprites\\Enemie4 - idle.png').convert_alpha()
bat2Original_surface = pygame.image.load('sprites\\Enemie6 - idle.png').convert_alpha()

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
game_active = False #variavel importante para o jogo estiver ou não
start_time = 0
bg_x_pos = 0  # posição do fundo
score = 0

#intro
player_stand = pygame.image.load('sprites\\loading.webp').convert_alpha()
player_stand = pygame.transform.scale(player_stand, new_size)  # redimensiona para ocupar a tela
player_stand_rect = player_stand.get_rect(topleft=(0, 0))  # posiciona no canto superior esquerdo

game_name = test_font.render('BloodLost', False, (255, 255, 255))
game_name_rect = game_name.get_rect(center = (560, 60))

gameover_stand = pygame.image.load('sprites\\gameover.png').convert_alpha()
gameover_stand = pygame.transform.scale(gameover_stand, new_size)  # redimensiona para ocupar a tela
gameover_stand_rect = gameover_stand.get_rect(topleft=(0, 0))  # posiciona no canto superior esquerdo

game_name = test_font.render('BloodLost', False, (255, 255, 255))
game_name_rect = game_name.get_rect(center = (560, 60))

game_message = test_font.render('Press space to run', False, (255, 255, 255))
game_message_rect = game_message.get_rect(center = (560, 300))

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

        score = display_score()

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
        # screen.fill((255, 20, 147))
        # screen.fill('Black')

        score_message = test_font.render(f'Your Score: {score}', False, 'Red')
        score_message_rect = score_message.get_rect(center = (530, 300))

        if score == 0:
            screen.blit(player_stand, player_stand_rect)
            screen.blit(game_name, game_name_rect)
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(gameover_stand, gameover_stand_rect)
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
