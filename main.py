import pygame
from sys import exit
from random import randint
from random import choice

def display_score():
    currentTime = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {currentTime}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(500, 50))
    screen.blit(score_surf, score_rect)
    return currentTime

def obstacle_movement(obstacle_list):
    new_obstacle_list = []
    for obstacle_surface, obstacle_rect in obstacle_list:
        obstacle_rect.x -= 5
        screen.blit(obstacle_surface, obstacle_rect)
        if obstacle_rect.x > -100:
            new_obstacle_list.append((obstacle_surface, obstacle_rect))
    return new_obstacle_list

def collisions(player, obstacles):
    if obstacles:
        for surface, obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


pygame.init()
screen = pygame.display.set_mode((800, 600))

# Carregando sprites
backgroudOriginal_image = pygame.image.load('sprites\\NES - Castlevania 2 Simons Quest.png').convert_alpha()
heroOriginal_surface = pygame.image.load('sprites\\warrior - idle.png').convert_alpha()
batOriginal_surface = pygame.image.load('sprites\\bat.png').convert_alpha()
zombieOriginal_surface = pygame.image.load('sprites\\Enemie3 - idle.png').convert_alpha()
knightOriginal_surface = pygame.image.load('sprites\\Enemie1 - idle.png').convert_alpha()
owlOriginal_surface = pygame.image.load('sprites\\Enemie2 - idle.png').convert_alpha()
pantherOriginal_surface = pygame.image.load('sprites\\Enemie4 - idle.png').convert_alpha()
bat1Original_surface = pygame.image.load('sprites\\Enemie6 - idle.png').convert_alpha()

# Escala das imagens
scale_factor = 1.5
scaleHero_factor = 2
scaleBat_factor = 2

new_size = (int(backgroudOriginal_image.get_width() * scale_factor), int(backgroudOriginal_image.get_height() * scale_factor))
newHero_size = (int(heroOriginal_surface.get_width() * scaleHero_factor), int(heroOriginal_surface.get_height() * scaleHero_factor))
newbat_size = (int(batOriginal_surface.get_width() * scaleBat_factor), int(batOriginal_surface.get_height() * scaleBat_factor))
newzombie_size = (int(zombieOriginal_surface.get_width() * scaleBat_factor), int(zombieOriginal_surface.get_height() * scaleBat_factor))
newknight_size = (int(knightOriginal_surface.get_width() * scaleBat_factor), int(knightOriginal_surface.get_height() * scaleBat_factor))
newOwl_size = (int(owlOriginal_surface.get_width() * scaleBat_factor), int(owlOriginal_surface.get_height() * scaleBat_factor))
newPanther_size = (int(pantherOriginal_surface.get_width() * scaleBat_factor), int(pantherOriginal_surface.get_height() * scaleBat_factor))
newbat1_size = (int(bat1Original_surface.get_width() * scaleBat_factor), int(bat1Original_surface.get_height() * scaleBat_factor))

backgroud_surface = pygame.transform.scale(backgroudOriginal_image, new_size)
hero_surface = pygame.transform.scale(heroOriginal_surface, newHero_size)
bat_surface = pygame.transform.scale(batOriginal_surface, newbat_size)
zombie_surface = pygame.transform.scale(zombieOriginal_surface, newzombie_size)
knight_surface = pygame.transform.scale(knightOriginal_surface, newknight_size)
owl_surface = pygame.transform.scale(owlOriginal_surface, newOwl_size)
panther_surface = pygame.transform.scale(pantherOriginal_surface, newPanther_size)
bat1_surface = pygame.transform.scale(bat1Original_surface, newbat1_size)

screen = pygame.display.set_mode(new_size)
pygame.display.set_caption('BloodLost')
clock = pygame.time.Clock()
test_font = pygame.font.Font('fonts\\Pixeltype.ttf', 50)

player_rect = hero_surface.get_rect(topleft=(300, 245))
player_gravity = 0
game_active = False
start_time = 0
bg_x_pos = 0
score = 0

# Intro
player_stand = pygame.image.load('sprites\\loading.webp').convert_alpha()
player_stand = pygame.transform.scale(player_stand, new_size)
player_stand_rect = player_stand.get_rect(topleft=(0, 0))

game_name = test_font.render('BloodLost', False, (255, 255, 255))
game_name_rect = game_name.get_rect(center=(560, 60))

gameover_stand = pygame.image.load('sprites\\gameover.png').convert_alpha()
gameover_stand = pygame.transform.scale(gameover_stand, new_size)
gameover_stand_rect = gameover_stand.get_rect(topleft=(0, 0))

game_message = test_font.render('Press space to run', False, (255, 255, 255))
game_message_rect = game_message.get_rect(center=(560, 300))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

obstacle_rect_list = []
enemies = [
    {"surface": bat_surface, "y": 255},
    {"surface": zombie_surface, "y": 248},
    {"surface": bat1_surface, "y": 255},
    {"surface": knight_surface, "y": 250},
    {"surface": owl_surface, "y": 110},
    {"surface": panther_surface, "y": 270},
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == obstacle_timer and game_active:
                chosen_enemy = choice(enemies)  # pega um inimigo aleatório
                obstacle_rect = chosen_enemy["surface"].get_rect(topleft=(randint(700, 1100), chosen_enemy["y"]))
                obstacle_rect_list.append((chosen_enemy["surface"], obstacle_rect))

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
                obstacle_rect_list.clear()
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # Scroll do fundo
        bg_x_pos -= 2
        if bg_x_pos <= -backgroud_surface.get_width():
            bg_x_pos = 0

        screen.blit(backgroud_surface, (bg_x_pos, 0))
        screen.blit(backgroud_surface, (bg_x_pos + backgroud_surface.get_width(), 0))

        score = display_score()

        # Obstáculos
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Jogador
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 310:
            player_rect.bottom = 310
        screen.blit(hero_surface, player_rect)

        # Colisão (opcional)
        # for obstacle_surface, obstacle_rect in obstacle_rect_list:
        #     if player_rect.colliderect(obstacle_rect):
        #         game_active = False

        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        score_message = test_font.render(f'Your Score: {score}', False, 'Red')
        score_message_rect = score_message.get_rect(center=(530, 300))

        obstacle_rect_list.clear() 
        player_rect.bottom = 310
        player_gravity = 0

        if score == 0:
            screen.blit(player_stand, player_stand_rect)
            screen.blit(game_name, game_name_rect)
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(gameover_stand, gameover_stand_rect)
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
