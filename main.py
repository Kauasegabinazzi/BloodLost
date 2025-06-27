import pygame
from sys import exit
from random import randint
from random import choice



def display_score():
    """
    Exibe a pontuação atual na tela com base no tempo de jogo em segundos.
    
    Returns:
        int: tempo (em segundos) desde o início do jogo.
    """
    currentTime = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {currentTime}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(500, 50))
    screen.blit(score_surf, score_rect)
    return currentTime

def obstacle_movement(obstacle_list):
    """
    Move os obstáculos para a esquerda e os mantém na tela enquanto visíveis.

    Args:
        obstacle_list (list): Lista de dicionários contendo dados dos obstáculos.
    
    Returns:
        list: Lista atualizada com obstáculos ainda visíveis na tela.
    """
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
    """
    Verifica se houve colisão entre o jogador e algum obstáculo.
    
    Args:
        player (pygame.Rect): Retângulo do jogador.
        obstacles (list): Lista de obstáculos (com retângulos).

    Returns:
        bool: False se houve colisão, True caso contrário.
    """
    if obstacles:
        for obstacle_data in obstacles:
            obstacle_rect = obstacle_data["rect"]
            if player.colliderect(obstacle_rect):
                return False
    return True

def playerAnimation():
    """
    Atualiza a imagem do jogador com base em sua posição:
    - Se está pulando, mostra o sprite de pulo.
    - Se está no chão, anima a caminhada.
    """
    global hero_surface, playerIndex

    if player_rect.bottom < 310:
        hero_surface = playerJump
    else:
        playerIndex += 0.1
        if playerIndex >= len(playerWalk): playerIndex = 0
        hero_surface = playerWalk[int(playerIndex)]

def update_enemy_animations():
    """
    Atualiza o índice de animação de cada tipo de inimigo e define o sprite atual
    de cada obstáculo com base no seu tipo.
    """
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

# Inicializa todos os módulos do pygame (som, vídeo, teclado, etc.)
pygame.init()

# Cria a janela principal do jogo com tamanho 800x600 pixels
screen = pygame.display.set_mode((800, 600))

# region SPRITES

# Carrega a imagem de fundo do jogo e preserva a transparência
backgroudOriginal_image = pygame.image.load('sprites\\NES - Castlevania 2 Simons Quest.png').convert_alpha()

# Sprites do personagem principal (guerreiro) em diferentes estados
heroOriginal_surface = pygame.image.load('sprites\\warrior - idle.png').convert_alpha()
heroOriginalwalk1_surface = pygame.image.load('sprites\\warrior-walk1.png').convert_alpha()
heroOriginalwalk2_surface = pygame.image.load('sprites\\warrior-walk2.png').convert_alpha()
heroOriginalwalk3_surface = pygame.image.load('sprites\\warrior-walk3.png').convert_alpha()
heroOriginaljump_surface = pygame.image.load('sprites\\warrior-jump.png').convert_alpha()

# Sprites de um tipo de morcego com animação de voo
batOriginal_surface = pygame.image.load('sprites\\bat.png').convert_alpha()
batOriginalWalk_surface = pygame.image.load('sprites\\bat-walk.png').convert_alpha()
batOriginalWalk2_surface = pygame.image.load('sprites\\bat-walk1.png').convert_alpha()

# Sprites do zumbi, incluindo idle e caminhada
zombieOriginal_surface = pygame.image.load('sprites\\Enemie3 - idle.png').convert_alpha()
zombieOriginalWalk_surface = pygame.image.load('sprites\\Enemie3-walk.png').convert_alpha()

# Sprites do cavaleiro inimigo em idle e duas poses de caminhada
knightOriginal_surface = pygame.image.load('sprites\\Enemie1 - idle.png').convert_alpha()
knightOriginalWalk_surface = pygame.image.load('sprites\\Enemie1-walk1.png').convert_alpha()
knightOriginalWalk1_surface = pygame.image.load('sprites\\Enemie1-walk2.png').convert_alpha()

# Sprites do inimigo tipo coruja parado e em voo
owlOriginal_surface = pygame.image.load('sprites\\Enemie2 - idle.png').convert_alpha()
owlOriginalWalk_surface = pygame.image.load('sprites\\Enemie2-walk.png').convert_alpha()

# Outro tipo de morcego com estilo e animação diferentes
bat1Original_surface = pygame.image.load('sprites\\Enemie6 - idle.png').convert_alpha()
bat1OriginalWalk_surface = pygame.image.load('sprites\\Enemie6-walk.png').convert_alpha()
bat1OriginalWalk2_surface = pygame.image.load('sprites\\Enemie6-walk2.png').convert_alpha()

# Sprites da pantera com animações de idle e três fases de caminhada
pantherOriginal_surface = pygame.image.load('sprites\\Enemie4-walk.png').convert_alpha()
pantherOriginalWalk_surface = pygame.image.load('sprites\\Enemie4 - idle.png').convert_alpha()
pantherOriginalWalk2_surface = pygame.image.load('sprites\\Enemie4-walk1.png').convert_alpha()
pantherOriginalWalk3_surface = pygame.image.load('sprites\\Enemie4-walk2.png').convert_alpha()

# endregion SPRITES

# Escala das imagens
scale_factor = 1.5
scaleHero_factor = 2
scaleBat_factor = 2

# region REDIMENSIONANDO AS SPRITES

# Redimensiona o plano de fundo com o fator de escala geral
new_size = (int(backgroudOriginal_image.get_width() * scale_factor), int(backgroudOriginal_image.get_height() * scale_factor))

# Redimensiona sprites do zumbi (idle e walk)
newzombie_size = (int(zombieOriginal_surface.get_width() * scaleBat_factor), int(zombieOriginal_surface.get_height() * scaleBat_factor))
newzombieWalk_size = (int(zombieOriginalWalk_surface.get_width() * scaleBat_factor), int(zombieOriginalWalk_surface.get_height() * scaleBat_factor))

# Redimensiona sprites do cavaleiro (idle e dois estágios de walk)
newknight_size = (int(knightOriginal_surface.get_width() * scaleBat_factor), int(knightOriginal_surface.get_height() * scaleBat_factor))
newknightWalk_size = (int(knightOriginalWalk_surface.get_width() * scaleBat_factor), int(knightOriginalWalk_surface.get_height() * scaleBat_factor))
newknightWalk1_size = (int(knightOriginalWalk1_surface.get_width() * scaleBat_factor), int(knightOriginalWalk1_surface.get_height() * scaleBat_factor))

# Redimensiona sprites da coruja (idle e walk)
newOwl_size = (int(owlOriginal_surface.get_width() * scaleBat_factor), int(owlOriginal_surface.get_height() * scaleBat_factor))
newOwlWalk_size = (int(owlOriginalWalk_surface.get_width() * scaleBat_factor), int(owlOriginalWalk_surface.get_height() * scaleBat_factor))

# Redimensiona sprites da pantera (idle e 3 estágios de caminhada)
newPanther_size = (int(pantherOriginal_surface.get_width() * scaleBat_factor), int(pantherOriginal_surface.get_height() * scaleBat_factor))
newPantherWalk_size = (int(pantherOriginalWalk_surface.get_width() * scaleBat_factor), int(pantherOriginalWalk_surface.get_height() * scaleBat_factor))
newPantherWalk2_size = (int(pantherOriginalWalk2_surface.get_width() * scaleBat_factor), int(pantherOriginalWalk2_surface.get_height() * scaleBat_factor))
newPantherWalk3_size = (int(pantherOriginalWalk3_surface.get_width() * scaleBat_factor), int(pantherOriginalWalk3_surface.get_height() * scaleBat_factor))

# Redimensiona sprites do herói (idle, 3 walk e jump)
newHero_size = (int(heroOriginal_surface.get_width() * scaleHero_factor), int(heroOriginal_surface.get_height() * scaleHero_factor))
newHeroWalk1_size = (int(heroOriginalwalk1_surface.get_width() * scaleHero_factor), int(heroOriginalwalk1_surface.get_height() * scaleHero_factor))
newHeroWalk2_size = (int(heroOriginalwalk2_surface.get_width() * scaleHero_factor), int(heroOriginalwalk2_surface.get_height() * scaleHero_factor))
newHeroWalk3_size = (int(heroOriginalwalk3_surface.get_width() * scaleHero_factor), int(heroOriginalwalk3_surface.get_height() * scaleHero_factor))
newHeroJump_size = (int(heroOriginaljump_surface.get_width() * scaleHero_factor), int(heroOriginaljump_surface.get_height() * scaleHero_factor))

# Redimensiona sprites do primeiro tipo de morcego (idle e 2 voos)
newbat_size = (int(batOriginal_surface.get_width() * scaleBat_factor), int(batOriginal_surface.get_height() * scaleBat_factor))
newbatWalk_size = (int(batOriginalWalk_surface.get_width() * scaleBat_factor), int(batOriginalWalk_surface.get_height() * scaleBat_factor))
newbatWalk2_size = (int(batOriginalWalk2_surface.get_width() * scaleBat_factor), int(batOriginalWalk2_surface.get_height() * scaleBat_factor))

# Redimensiona sprites do segundo tipo de morcego (idle e 2 voos)
newbat1_size = (int(bat1Original_surface.get_width() * scaleBat_factor), int(bat1Original_surface.get_height() * scaleBat_factor))
newbat1Walk_size = (int(bat1OriginalWalk_surface.get_width() * scaleBat_factor), int(bat1OriginalWalk_surface.get_height() * scaleBat_factor))
newbat1Walk2_size = (int(bat1OriginalWalk2_surface.get_width() * scaleBat_factor), int(bat1OriginalWalk2_surface.get_height() * scaleBat_factor))

# endregion REDIMENSIONANDO AS SPRITES

# region AJUSTE DE ESCALA DAS SPRITES

# Ajuste de escala do plano de fundo
backgroud_surface = pygame.transform.scale(backgroudOriginal_image, new_size)

# Ajuste de escala do zumbi
zombie_surface = pygame.transform.scale(zombieOriginal_surface, newzombie_size)
zombieWalk_surface = pygame.transform.scale(zombieOriginalWalk_surface, newzombieWalk_size)

# Ajuste de escala do cavaleiro
knight_surface = pygame.transform.scale(knightOriginal_surface, newknight_size)
knightWalk_surface = pygame.transform.scale(knightOriginalWalk_surface, newknightWalk_size)
knightWalk1_surface = pygame.transform.scale(knightOriginalWalk1_surface, newknightWalk1_size)

# Ajuste de escala da coruja
owl_surface = pygame.transform.scale(owlOriginal_surface, newOwl_size)
owlWalk_surface = pygame.transform.scale(owlOriginalWalk_surface, newOwlWalk_size)

# Ajuste de escala da pantera
panther_surface = pygame.transform.scale(pantherOriginal_surface, newPanther_size)
pantherWalk_surface = pygame.transform.scale(pantherOriginalWalk_surface, newPantherWalk_size)
pantherWalk2_surface = pygame.transform.scale(pantherOriginalWalk2_surface, newPantherWalk2_size)
pantherWalk3_surface = pygame.transform.scale(pantherOriginalWalk3_surface, newPantherWalk3_size)

# Ajuste de escala do personagem principal (herói)
hero_surface = pygame.transform.scale(heroOriginal_surface, newHero_size)
hero_surfaceWalk1 = pygame.transform.scale(heroOriginalwalk1_surface, newHeroWalk1_size)
hero_surfaceWalk2 = pygame.transform.scale(heroOriginalwalk2_surface, newHeroWalk2_size)
hero_surfaceWalk3 = pygame.transform.scale(heroOriginalwalk3_surface, newHeroWalk3_size)
hero_surfaceJump = pygame.transform.scale(heroOriginaljump_surface, newHeroJump_size)

# Ajuste de escala do morcego
bat_surface = pygame.transform.scale(batOriginal_surface, newbat_size)
batWalk_surface = pygame.transform.scale(batOriginalWalk_surface, newbatWalk_size)
batWalk2_surface = pygame.transform.scale(batOriginalWalk2_surface, newbatWalk2_size)

# Ajuste de escala do segundo morcego
bat1_surface = pygame.transform.scale(bat1Original_surface, newbat1_size)
bat1Walk_surface = pygame.transform.scale(bat1OriginalWalk_surface, newbat1Walk_size)
bat1Walk2_surface = pygame.transform.scale(bat1OriginalWalk2_surface, newbat1Walk2_size)

# endregion AJUSTE DE ESCALA DAS SPRITES

# region FRAMES PARA ANIMAÇÃO

playerWalk = [hero_surface, hero_surfaceWalk1, hero_surfaceWalk2, hero_surfaceWalk3]
playerJump = hero_surfaceJump
batFrames = [bat_surface, batWalk_surface, batWalk2_surface]
bat1Frames = [bat1_surface, bat1Walk_surface, bat1Walk2_surface]
zombieFrames = [zombie_surface, zombieWalk_surface]
knightFrames = [knight_surface, knightWalk_surface, knightWalk1_surface]
owlFrames = [owl_surface, owlWalk_surface]
pantherFrames = [pantherWalk_surface, pantherWalk2_surface, pantherWalk3_surface]

# endregion FRAMES PARA ANIMAÇÃO

# region ÍNDICES PARA CONTROLE DE ANIMAÇÃO

playerIndex = 0
batFramesIndex = 0
bat1FramesIndex = 0
zombieFramesIndex = 0
knightFramesIndex = 0
owlFramesIndex = 0
pantherFramesIndex = 0

# endregion ÍNDICES PARA CONTROLE DE ANIMAÇÃO

# Cria a janela do jogo com o tamanho do background redimensionado
screen = pygame.display.set_mode(new_size)

# Define o título da janela
pygame.display.set_caption('BloodLost')

# Inicializa o relógio para controlar o FPS
clock = pygame.time.Clock()

# Define a fonte que será usada para exibir textos no jogo
test_font = pygame.font.Font('fonts\\Pixeltype.ttf', 50)

# Define a posição inicial do jogador na tela
player_rect = hero_surface.get_rect(topleft=(300, 245))

# Define a gravidade inicial (sem queda)
player_gravity = 0

# Estado do jogo (ativo ou em tela de início/fim)
game_active = False

# Armazena o tempo de início do jogo (usado para calcular pontuação)
start_time = 0

# Posição horizontal do plano de fundo (para efeito de scroll)
bg_x_pos = 0

# Pontuação do jogador
score = 0

# region ELEMENTOS VISUAIS DA TELA INICIAL E GAME OVER

# Imagem de fundo para a tela inicial (com o personagem em pé)
player_stand = pygame.image.load('sprites\\loading.webp').convert_alpha()
player_stand = pygame.transform.scale(player_stand, new_size)
player_stand_rect = player_stand.get_rect(topleft=(0, 0))

# Título do jogo na tela inicial
game_name = test_font.render('BloodLost', False, (255, 255, 255))
game_name_rect = game_name.get_rect(center=(560, 60))

# Tela de fundo para o game over
gameover_stand = pygame.image.load('sprites\\gameover.png').convert_alpha()
gameover_stand = pygame.transform.scale(gameover_stand, new_size)
gameover_stand_rect = gameover_stand.get_rect(topleft=(0, 0))

# Mensagem de instrução na tela inicial
game_message = test_font.render('Press space to run', False, (255, 255, 255))
game_message_rect = game_message.get_rect(center=(560, 300))

# endregion ELEMENTOS VISUAIS DA TELA INICIAL E GAME OVER

# region TIMERS DO JOGO

# Timer para gerar obstáculos a cada 1500ms (1,5s)
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Timer para atualizar animações dos inimigos a cada 150ms
enemy_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer, 150)  # 150ms para animação mais suave

# endregion TIMERS DO JOGO

# Armazena os obstáculos atuais que estão na tela
obstacle_rect_list = []

# region LISTA DE INIMIGOS DISPONÍVEIS

# Cada inimigo possui:
# - 'surface': o sprite base
# - 'y': a posição vertical de onde ele será desenhado
# - 'type': uma string que identifica o tipo (usada para animações e lógica)
enemies = [
    {"surface": bat_surface, "y": 255, "type": "bat"},
    {"surface": zombie_surface, "y": 248, "type": "zombie"},
    {"surface": bat1_surface, "y": 255, "type": "bat1"},
    {"surface": knight_surface, "y": 250, "type": "knight"},
    {"surface": owl_surface, "y": 150, "type": "owl"},
    {"surface": panther_surface, "y": 270, "type": "panther"},
]

# endregion LISTA DE INIMIGOS DISPONÍVEIS

# region SONS DO JOGO

# Música de fundo durante o gameplay
bgMusic = pygame.mixer.Sound('music\\Marble Gallery.mp3')

# Som reproduzido quando o jogador perde
bgGameOver = pygame.mixer.Sound('music\\game-over-deep-male-voice-clip-352695.mp3')

# Som reproduzido na tela inicial do jogo
bgMainMenu = pygame.mixer.Sound('music\\main-menu.mp3')

# Controla se a música de fundo está tocando
music_playing = False

# Controla se o som de game over já foi tocado
game_over_music_playing = False

# Controla se a música na tela inicial está tocando
main_menu_playing = True

# endregion SONS DO JOGO

# region CONSTS
JUMP_FORCE = -9
GRAVITY_ASCEND = 0.4  # Gravidade enquanto sobe
GRAVITY_DESCEND = 0.8 # Gravidade enquanto desce
# endregion CONSTS

# Se o jogo estiver ativo e a música ainda não estiver tocando,
# inicia a reprodução da música de fundo.
if game_active and not music_playing:
    bgMusic.play(loops=-1) # Toca a música indefinidamente (loop infinito)
    music_playing = True # Marca que a música já está tocando para evitar repetição

while True:
    # Captura todos os eventos do Pygame (teclado, mouse, fechar janela, timers etc)
    for event in pygame.event.get():
        # Se o evento for fechar a janela, encerra o jogo
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Se o jogo estiver ativo (rodando)
        if game_active: 
            # Evento do timer para criar obstáculos periodicamente
            if event.type == obstacle_timer:
                # Escolhe um inimigo aleatório para criar o obstáculo
                chosen_enemy = choice(enemies)
                # Cria um retângulo para o obstáculo na posição X aleatória à direita e Y fixa
                obstacle_rect = chosen_enemy["surface"].get_rect(topleft=(randint(700, 1100), chosen_enemy["y"]))
                
                # Cria o dicionário com informações do obstáculo para controle e desenho
                obstacle_data = {
                    "rect": obstacle_rect,
                    "type": chosen_enemy["type"],
                    "current_surface": chosen_enemy["surface"]
                }
                # Adiciona o obstáculo na lista de obstáculos ativos
                obstacle_rect_list.append(obstacle_data)
                
            # Evento do timer para atualizar animações dos inimigos
            if event.type == enemy_animation_timer:
                update_enemy_animations()

        # Controle de input quando o jogo está ativo
        if game_active:
            # Se o jogador clicar com o mouse e estiver no chão (posição Y)
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 310:
                # Verifica se clicou no personagem
                if player_rect.collidepoint(event.pos):
                    player_gravity = JUMP_FORCE  # Aplica pulo (gravidade negativa)
            
            # Se pressionar a tecla espaço e estiver no chão
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 310:
                    player_gravity = JUMP_FORCE  # Pula

        # Controle de input quando o jogo NÃO está ativo (tela inicial ou game over)
        else:
            bgMainMenu.play(loops=-1)
            main_menu_playing = True

            # Pressionar espaço para iniciar ou reiniciar o jogo
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True               # Ativa o jogo
                obstacle_rect_list.clear()      # Limpa obstáculos antigos
                start_time = int(pygame.time.get_ticks() / 1000)  # Reseta o timer do jogo

                # Se a música do menu principal estiver tocando, ela para
                if main_menu_playing:
                    bgMainMenu.stop()
                    main_menu_playing = False
                
                # Se a música de game over estiver tocando, para ela
                if game_over_music_playing:
                    bgGameOver.stop()
                    game_over_music_playing = False
                
                # Inicia a música de fundo se ainda não estiver tocando
                if not music_playing:
                    bgMusic.play(loops=-1)
                    music_playing = True

    # Se o jogo está ativo, executa a lógica principal de gameplay
    if game_active:
        # Garante que a música de fundo está tocando
        if not music_playing:
            bgMusic.play(loops=-1)
            music_playing = True
        
        # Para a música de game over se estiver tocando
        if game_over_music_playing:
            bgGameOver.stop()
            game_over_music_playing = False

        # Movimento de scroll do fundo (desloca para esquerda)
        bg_x_pos -= 2
        # Quando o fundo sair da tela, reseta posição para loop infinito
        if bg_x_pos <= -backgroud_surface.get_width():
            bg_x_pos = 0

        # Desenha o fundo duas vezes para dar efeito de scroll contínuo
        screen.blit(backgroud_surface, (bg_x_pos, 0))
        screen.blit(backgroud_surface, (bg_x_pos + backgroud_surface.get_width(), 0))

        # Atualiza e exibe o placar
        score = display_score()

        # Atualiza a posição e exibe os obstáculos
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Aplica gravidade no jogador e movimenta verticalmente
        if player_gravity < 0:  # Enquanto está subindo
            player_gravity += GRAVITY_ASCEND
        else:  # Quando começa a cair
            player_gravity += GRAVITY_DESCEND

        player_rect.y += player_gravity

        # Evita que o jogador caia abaixo do chão (posição Y=310)
        if player_rect.bottom >= 310:
            player_rect.bottom = 310
        
        # Atualiza animação do jogador (corrida ou pulo)
        playerAnimation()
        # Desenha o jogador na tela
        screen.blit(hero_surface, player_rect)

        # Verifica colisão entre jogador e obstáculos
        previous_game_active = game_active
        game_active = collisions(player_rect, obstacle_rect_list)
        
        # Se o jogo acabou de terminar (estado mudou de True para False)
        if previous_game_active and not game_active:
            # Para a música de fundo e inicia som de game over
            if music_playing:
                bgMusic.stop()
                music_playing = False
            
            if not game_over_music_playing:
                bgGameOver.play(loops=0)  # Toca som de game over uma vez
                game_over_music_playing = True

    # Se o jogo não estiver ativo (tela inicial ou game over)
    else:
        # Se o jogador já fez algum ponto e música de game over não está tocando, toca som
        if score > 0 and not game_over_music_playing:
            bgGameOver.play(loops=0)
            game_over_music_playing = True
        
        # Para a música de fundo se estiver tocando
        if music_playing:
            bgMusic.stop()
            music_playing = False

        # Prepara mensagem com o placar para exibir na tela
        score_message = test_font.render(f'Your Score: {score}', False, 'Red')
        score_message_rect = score_message.get_rect(center=(530, 300))

        # Limpa obstáculos da tela
        obstacle_rect_list.clear() 
        # Reseta jogador para posição inicial e gravidade zerada
        player_rect.bottom = 310
        player_gravity = 0

        # Se o jogador nunca começou (score 0), exibe tela inicial
        if score == 0:
            screen.blit(player_stand, player_stand_rect)
            screen.blit(game_name, game_name_rect)
            screen.blit(game_message, game_message_rect)
        else:
            # Caso contrário, exibe tela de game over com o placar final
            screen.blit(gameover_stand, gameover_stand_rect)
            screen.blit(score_message, score_message_rect)

    # Atualiza a tela com tudo que foi desenhado
    pygame.display.update()
    # Controla o FPS para rodar a 60 frames por segundo
    clock.tick(60)