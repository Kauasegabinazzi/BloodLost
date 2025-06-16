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
    for obstacle_data in obstacle_list:
        obstacle_surface = obstacle_data["current_surface"]
        obstacle_rect = obstacle_data["rect"]
        
        obstacle_rect.x -= 5
        screen.blit(obstacle_surface, obstacle_rect)
        if obstacle_rect.x > -100:
            new_obstacle_list.append(obstacle_data)
    return new_obstacle_list

def collisions(player, obstacles):
    if obstacles:
        for obstacle_data in obstacles:
            obstacle_rect = obstacle_data["rect"]
            if player.colliderect(obstacle_rect):
                return False
    return True

def playerAnimation():
    global hero_surface, playerIndex

    if player_rect.bottom < 310:
        hero_surface = playerJump
    else:
        playerIndex += 0.1
        if playerIndex >= len(playerWalk): playerIndex = 0
        hero_surface = playerWalk[int(playerIndex)]

def update_enemy_animations():
    global batFramesIndex, bat1FramesIndex, zombieFramesIndex, knightFramesIndex, owlFramesIndex, pantherFramesIndex
    
    # Atualiza animação do bat normal
    batFramesIndex += 1
    if batFramesIndex >= len(batFrames):
        batFramesIndex = 0
    
    # Atualiza animação do bat1
    bat1FramesIndex += 1
    if bat1FramesIndex >= len(bat1Frames):
        bat1FramesIndex = 0
    
    # Atualiza animação do zombie
    zombieFramesIndex += 1
    if zombieFramesIndex >= len(zombieFrames):
        zombieFramesIndex = 0
    
    # Atualiza animação do knight
    knightFramesIndex += 1
    if knightFramesIndex >= len(knightFrames):
        knightFramesIndex = 0
    
    # Atualiza animação do owl
    owlFramesIndex += 1
    if owlFramesIndex >= len(owlFrames):
        owlFramesIndex = 0
    
    # Atualiza animação do panther
    pantherFramesIndex += 1
    if pantherFramesIndex >= len(pantherFrames):
        pantherFramesIndex = 0
    
    # Atualiza os obstáculos com suas respectivas animações
    for obstacle_data in obstacle_rect_list:
        if obstacle_data["type"] == "bat":
            obstacle_data["current_surface"] = batFrames[batFramesIndex]
        elif obstacle_data["type"] == "bat1":
            obstacle_data["current_surface"] = bat1Frames[bat1FramesIndex]
        elif obstacle_data["type"] == "zombie":
            obstacle_data["current_surface"] = zombieFrames[zombieFramesIndex]
        elif obstacle_data["type"] == "knight":
            obstacle_data["current_surface"] = knightFrames[knightFramesIndex]
        elif obstacle_data["type"] == "owl":
            obstacle_data["current_surface"] = owlFrames[owlFramesIndex]
        elif obstacle_data["type"] == "panther":
            obstacle_data["current_surface"] = pantherFrames[pantherFramesIndex]

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Carregando sprites
backgroudOriginal_image = pygame.image.load('sprites\\NES - Castlevania 2 Simons Quest.png').convert_alpha()

heroOriginal_surface = pygame.image.load('sprites\\warrior - idle.png').convert_alpha()
heroOriginalwalk1_surface = pygame.image.load('sprites\\warrior-walk1.png').convert_alpha()
heroOriginalwalk2_surface = pygame.image.load('sprites\\warrior-walk2.png').convert_alpha()
heroOriginalwalk3_surface = pygame.image.load('sprites\\warrior-walk3.png').convert_alpha()
heroOriginaljump_surface = pygame.image.load('sprites\\warrior-jump.png').convert_alpha()

batOriginal_surface = pygame.image.load('sprites\\bat.png').convert_alpha()
batOriginalWalk_surface = pygame.image.load('sprites\\bat-walk.png').convert_alpha()
batOriginalWalk2_surface = pygame.image.load('sprites\\bat-walk1.png').convert_alpha()

zombieOriginal_surface = pygame.image.load('sprites\\Enemie3 - idle.png').convert_alpha()
zombieOriginalWalk_surface = pygame.image.load('sprites\\Enemie3-walk.png').convert_alpha()

knightOriginal_surface = pygame.image.load('sprites\\Enemie1 - idle.png').convert_alpha()
knightOriginalWalk_surface = pygame.image.load('sprites\\Enemie1-walk1.png').convert_alpha()
knightOriginalWalk1_surface = pygame.image.load('sprites\\Enemie1-walk2.png').convert_alpha()

owlOriginal_surface = pygame.image.load('sprites\\Enemie2 - idle.png').convert_alpha()
owlOriginalWalk_surface = pygame.image.load('sprites\\Enemie2-walk.png').convert_alpha()

bat1Original_surface = pygame.image.load('sprites\\Enemie6 - idle.png').convert_alpha()
bat1OriginalWalk_surface = pygame.image.load('sprites\\Enemie6-walk.png').convert_alpha()
bat1OriginalWalk2_surface = pygame.image.load('sprites\\Enemie6-walk2.png').convert_alpha()

pantherOriginal_surface = pygame.image.load('sprites\\Enemie4-walk.png').convert_alpha()
pantherOriginalWalk_surface = pygame.image.load('sprites\\Enemie4 - idle.png').convert_alpha()
pantherOriginalWalk2_surface = pygame.image.load('sprites\\Enemie4-walk1.png').convert_alpha()
pantherOriginalWalk3_surface = pygame.image.load('sprites\\Enemie4-walk2.png').convert_alpha()

# Escala das imagens
scale_factor = 1.5
scaleHero_factor = 2
scaleBat_factor = 2

new_size = (int(backgroudOriginal_image.get_width() * scale_factor), int(backgroudOriginal_image.get_height() * scale_factor))

newzombie_size = (int(zombieOriginal_surface.get_width() * scaleBat_factor), int(zombieOriginal_surface.get_height() * scaleBat_factor))
newzombieWalk_size = (int(zombieOriginalWalk_surface.get_width() * scaleBat_factor), int(zombieOriginalWalk_surface.get_height() * scaleBat_factor))
newknight_size = (int(knightOriginal_surface.get_width() * scaleBat_factor), int(knightOriginal_surface.get_height() * scaleBat_factor))
newknightWalk_size = (int(knightOriginalWalk_surface.get_width() * scaleBat_factor), int(knightOriginalWalk_surface.get_height() * scaleBat_factor))
newknightWalk1_size = (int(knightOriginalWalk1_surface.get_width() * scaleBat_factor), int(knightOriginalWalk1_surface.get_height() * scaleBat_factor))
newOwl_size = (int(owlOriginal_surface.get_width() * scaleBat_factor), int(owlOriginal_surface.get_height() * scaleBat_factor))
newOwlWalk_size = (int(owlOriginalWalk_surface.get_width() * scaleBat_factor), int(owlOriginalWalk_surface.get_height() * scaleBat_factor))
newPanther_size = (int(pantherOriginal_surface.get_width() * scaleBat_factor), int(pantherOriginal_surface.get_height() * scaleBat_factor))
newPantherWalk_size = (int(pantherOriginalWalk_surface.get_width() * scaleBat_factor), int(pantherOriginalWalk_surface.get_height() * scaleBat_factor))
newPantherWalk2_size = (int(pantherOriginalWalk2_surface.get_width() * scaleBat_factor), int(pantherOriginalWalk2_surface.get_height() * scaleBat_factor))
newPantherWalk3_size = (int(pantherOriginalWalk3_surface.get_width() * scaleBat_factor), int(pantherOriginalWalk3_surface.get_height() * scaleBat_factor))

newHero_size = (int(heroOriginal_surface.get_width() * scaleHero_factor), int(heroOriginal_surface.get_height() * scaleHero_factor))
newHeroWalk1_size = (int(heroOriginalwalk1_surface.get_width() * scaleHero_factor), int(heroOriginalwalk1_surface.get_height() * scaleHero_factor))
newHeroWalk2_size = (int(heroOriginalwalk2_surface.get_width() * scaleHero_factor), int(heroOriginalwalk2_surface.get_height() * scaleHero_factor))
newHeroWalk3_size = (int(heroOriginalwalk3_surface.get_width() * scaleHero_factor), int(heroOriginalwalk3_surface.get_height() * scaleHero_factor))
newHeroJump_size = (int(heroOriginaljump_surface.get_width() * scaleHero_factor), int(heroOriginaljump_surface.get_height() * scaleHero_factor))

newbat_size = (int(batOriginal_surface.get_width() * scaleBat_factor), int(batOriginal_surface.get_height() * scaleBat_factor))
newbatWalk_size = (int(batOriginalWalk_surface.get_width() * scaleBat_factor), int(batOriginalWalk_surface.get_height() * scaleBat_factor))
newbatWalk2_size = (int(batOriginalWalk2_surface.get_width() * scaleBat_factor), int(batOriginalWalk2_surface.get_height() * scaleBat_factor))

newbat1_size = (int(bat1Original_surface.get_width() * scaleBat_factor), int(bat1Original_surface.get_height() * scaleBat_factor))
newbat1Walk_size = (int(bat1OriginalWalk_surface.get_width() * scaleBat_factor), int(bat1OriginalWalk_surface.get_height() * scaleBat_factor))
newbat1Walk2_size = (int(bat1OriginalWalk2_surface.get_width() * scaleBat_factor), int(bat1OriginalWalk2_surface.get_height() * scaleBat_factor))

backgroud_surface = pygame.transform.scale(backgroudOriginal_image, new_size)

# Escalando sprites dos inimigos
zombie_surface = pygame.transform.scale(zombieOriginal_surface, newzombie_size)
zombieWalk_surface = pygame.transform.scale(zombieOriginalWalk_surface, newzombieWalk_size)

knight_surface = pygame.transform.scale(knightOriginal_surface, newknight_size)
knightWalk_surface = pygame.transform.scale(knightOriginalWalk_surface, newknightWalk_size)
knightWalk1_surface = pygame.transform.scale(knightOriginalWalk1_surface, newknightWalk1_size)

owl_surface = pygame.transform.scale(owlOriginal_surface, newOwl_size)
owlWalk_surface = pygame.transform.scale(owlOriginalWalk_surface, newOwlWalk_size)

panther_surface = pygame.transform.scale(pantherOriginal_surface, newPanther_size)
pantherWalk_surface = pygame.transform.scale(pantherOriginalWalk_surface, newPantherWalk_size)
pantherWalk2_surface = pygame.transform.scale(pantherOriginalWalk2_surface, newPantherWalk2_size)
pantherWalk3_surface = pygame.transform.scale(pantherOriginalWalk3_surface, newPantherWalk3_size)

hero_surface = pygame.transform.scale(heroOriginal_surface, newHero_size)
hero_surfaceWalk1 = pygame.transform.scale(heroOriginalwalk1_surface, newHeroWalk1_size)
hero_surfaceWalk2 = pygame.transform.scale(heroOriginalwalk2_surface, newHeroWalk2_size)
hero_surfaceWalk3 = pygame.transform.scale(heroOriginalwalk3_surface, newHeroWalk3_size)
hero_surfaceJump = pygame.transform.scale(heroOriginaljump_surface, newHeroJump_size)

playerWalk = [hero_surface, hero_surfaceWalk1, hero_surfaceWalk2, hero_surfaceWalk3]
playerJump = hero_surfaceJump
playerIndex = 0

bat_surface = pygame.transform.scale(batOriginal_surface, newbat_size)
batWalk_surface = pygame.transform.scale(batOriginalWalk_surface, newbatWalk_size)
batWalk2_surface = pygame.transform.scale(batOriginalWalk2_surface, newbatWalk2_size)

batFrames = [bat_surface, batWalk_surface, batWalk2_surface]
batFramesIndex = 0

bat1_surface = pygame.transform.scale(bat1Original_surface, newbat1_size)
bat1Walk_surface = pygame.transform.scale(bat1OriginalWalk_surface, newbat1Walk_size)
bat1Walk2_surface = pygame.transform.scale(bat1OriginalWalk2_surface, newbat1Walk2_size)

bat1Frames = [bat1_surface, bat1Walk_surface, bat1Walk2_surface]
bat1FramesIndex = 0

# Criando arrays de frames para animação dos inimigos
zombieFrames = [zombie_surface, zombieWalk_surface]
zombieFramesIndex = 0

knightFrames = [knight_surface, knightWalk_surface, knightWalk1_surface]
knightFramesIndex = 0

owlFrames = [owl_surface, owlWalk_surface]
owlFramesIndex = 0

pantherFrames = [pantherWalk_surface, pantherWalk2_surface, pantherWalk3_surface]
pantherFramesIndex = 0

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

# Timer para animação dos inimigos
enemy_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer, 150)  # 150ms para animação mais suave

obstacle_rect_list = []

# Definindo os inimigos com tipo para identificação
enemies = [
    {"surface": bat_surface, "y": 255, "type": "bat"},
    {"surface": zombie_surface, "y": 248, "type": "zombie"},
    {"surface": bat1_surface, "y": 255, "type": "bat1"},
    {"surface": knight_surface, "y": 250, "type": "knight"},
    {"surface": owl_surface, "y": 150, "type": "owl"},
    {"surface": panther_surface, "y": 270, "type": "panther"},
]

bgMusic = pygame.mixer.Sound('music\\Marble Gallery.mp3')
bgGameOver = pygame.mixer.Sound('music\\game-over-deep-male-voice-clip-352695.mp3')
bgMusic.play(loops= -1)
bgGameOver.play(loops= 1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active: 
            if event.type == obstacle_timer:
                chosen_enemy = choice(enemies)  # pega um inimigo aleatório
                obstacle_rect = chosen_enemy["surface"].get_rect(topleft=(randint(700, 1100), chosen_enemy["y"]))
                
                # Criando um dicionário com informações completas do obstáculo
                obstacle_data = {
                    "rect": obstacle_rect,
                    "type": chosen_enemy["type"],
                    "current_surface": chosen_enemy["surface"]
                }
                obstacle_rect_list.append(obstacle_data)
                
            if event.type == enemy_animation_timer:
                update_enemy_animations()

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
        
        playerAnimation()
        screen.blit(hero_surface, player_rect)

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