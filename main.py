import pygame
from sys import exit
from random import randint, choice
import json
import os

# ==================== CONSTANTES ====================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Física do jogo
JUMP_FORCE = -9
GRAVITY_ASCEND = 0.4
GRAVITY_DESCEND = 0.8
GROUND_Y = 310

# Fatores de escala
SCALE_FACTOR = 1.5
HERO_SCALE = 2
ENEMY_SCALE = 2

# Sistema de fases - pontuações para mudança de fase
PHASE_THRESHOLDS = [0, 10, 20, 30, 40]  # Pontuações para mudar de fase
PHASE_NAMES = ["Castle Entrance", "Dark Corridors", "Ancient Library", "Vampire's Chamber", "Final Battle"]

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
YELLOW = (255, 255, 100)
GOLD = (255, 215, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)

# ==================== CLASSE PARA GERENCIAR HIGHSCORE ====================
class HighscoreManager:
    def __init__(self, filename='highscore.json'):
        self.filename = filename
        self.highscore = self.load()
    
    def load(self):
        """Carrega o highscore do arquivo"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    return data.get('highscore', 0)
        except:
            pass
        return 0
    
    def save(self, score):
        """Salva novo highscore"""
        try:
            data = {'highscore': score}
            with open(self.filename, 'w') as f:
                json.dump(data, f)
            self.highscore = score
        except:
            pass
    
    def is_new_record(self, score):
        """Verifica se é novo recorde"""
        return score > self.highscore
    
    def update_if_record(self, score):
        """Atualiza se for novo recorde"""
        if self.is_new_record(score):
            self.save(score)
            return True
        return False
    
    def reset(self):
        """Reseta o highscore"""
        self.save(0)

# ==================== CLASSE PARA GERENCIAR RECURSOS ====================
class ResourceManager:
    def __init__(self):
        self.sprites = {}
        self.sounds = {}
        self.fonts = {}
        
    def load_sprite(self, name, path, scale=1.0):
        """Carrega e escala um sprite"""
        try:
            sprite = pygame.image.load(path).convert_alpha()
            if scale != 1.0:
                new_size = (int(sprite.get_width() * scale), int(sprite.get_height() * scale))
                sprite = pygame.transform.scale(sprite, new_size)
            self.sprites[name] = sprite
            return sprite
        except:
            print(f"Erro ao carregar sprite: {path}")
            return None
    
    def load_sound(self, name, path, volume=1.0):
        """Carrega um som"""
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            self.sounds[name] = sound
            return sound
        except:
            print(f"Erro ao carregar som: {path}")
            return None
    
    def load_font(self, name, path, size):
        """Carrega uma fonte"""
        try:
            font = pygame.font.Font(path, size)
            self.fonts[name] = font
            return font
        except:
            print(f"Erro ao carregar fonte: {path}")
            return pygame.font.Font(None, size)

# ==================== CLASSE PARA ANIMAÇÕES ====================
class AnimationManager:
    def __init__(self):
        self.animations = {}
        self.current_frames = {}
    
    def add_animation(self, name, frames):
        """Adiciona uma animação"""
        self.animations[name] = frames
        self.current_frames[name] = 0
    
    def update(self, name, speed=0.1):
        """Atualiza uma animação"""
        if name in self.animations:
            self.current_frames[name] += speed
            if self.current_frames[name] >= len(self.animations[name]):
                self.current_frames[name] = 0
            return self.animations[name][int(self.current_frames[name])]
        return None
    
    def get_current_frame(self, name):
        """Retorna o frame atual"""
        if name in self.animations:
            return self.animations[name][int(self.current_frames[name])]
        return None

# ==================== CLASSE PARA GERENCIAR FASES ====================
class PhaseManager:
    def __init__(self):
        self.current_phase = 0
        self.previous_phase = -1
        self.phase_change_timer = 0
        self.show_phase_notification = False
        
    def get_current_phase(self, score):
        """Determina a fase atual baseada na pontuação"""
        for i in range(len(PHASE_THRESHOLDS) - 1, -1, -1):
            if score >= PHASE_THRESHOLDS[i]:
                return i
        return 0
    
    def update_phase(self, score):
        """Atualiza a fase e detecta mudanças"""
        new_phase = self.get_current_phase(score)
        if new_phase != self.current_phase:
            self.previous_phase = self.current_phase
            self.current_phase = new_phase
            self.show_phase_notification = True
            self.phase_change_timer = 0
            return True
        return False
    
    def update_notification_timer(self):
        """Atualiza o timer da notificação de mudança de fase"""
        if self.show_phase_notification:
            self.phase_change_timer += 1
            if self.phase_change_timer > 180:  # 3 segundos a 60 FPS
                self.show_phase_notification = False
    
    def get_phase_name(self, phase_index=None):
        """Retorna o nome da fase"""
        if phase_index is None:
            phase_index = self.current_phase
        if 0 <= phase_index < len(PHASE_NAMES):
            return PHASE_NAMES[phase_index]
        return "Unknown Phase"
    
    def get_background_name(self, phase_index=None):
        """Retorna o nome do background da fase"""
        if phase_index is None:
            phase_index = self.current_phase
        return f'background_phase_{phase_index}'

# ==================== CLASSE PRINCIPAL DO JOGO ====================
class BloodLostGame:
    def __init__(self):
        pygame.init()
        
        # Inicialização básica
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('BloodLost')
        self.clock = pygame.time.Clock()
        
        # Managers
        self.resource_manager = ResourceManager()
        self.animation_manager = AnimationManager()
        self.highscore_manager = HighscoreManager()
        self.phase_manager = PhaseManager()
        
        # Estados do jogo
        self.game_state = "menu"
        self.game_active = False
        
        # Variáveis do jogo
        self.score = 0
        self.start_time = 0
        self.bg_x_pos = 0
        self.new_record_timer = 0
        
        # Variáveis do jogador
        self.player_gravity = 0
        
        # Variáveis de menu
        self.selected_option = 0
        self.selected_setting = 0
        self.volume = 0.7
        
        # Obstáculos
        self.obstacle_list = []
        
        # Controle de áudio
        self.music_playing = False
        self.game_over_music_playing = False
        self.main_menu_playing = True
        
        # Carrega recursos
        self.load_resources()
        
        # Configura timers
        self.setup_timers()
        
        # Inicializa player
        self.setup_player()
        
    def load_resources(self):
        """Carrega todos os recursos do jogo"""
        rm = self.resource_manager
        
        # Carrega sprites de background para cada fase
        background_paths = [
            'sprites\\NES - Castlevania 2 Simons Quest.png', 
            'sprites\\teste8.png', 
            'sprites\\teste3.png',  
            'sprites\\teste5.png', 
            'sprites\\teste2.png', 
        ]
        
        # Carrega cada background de fase
        for i, path in enumerate(background_paths):
            background_name = f'background_phase_{i}'
            loaded_sprite = rm.load_sprite(background_name, path, SCALE_FACTOR)
            
            # Se não conseguir carregar, usa o background padrão
            if loaded_sprite is None and i > 0:
                print(f"Usando background padrão para fase {i}")
                rm.sprites[background_name] = rm.sprites['background_phase_0']
        
        # Background do menu
        rm.load_sprite('menu_bg', 'sprites\\loading.webp', SCALE_FACTOR)
        
        # CORREÇÃO: Carrega a imagem de game over
        try:
            gameover_img = pygame.image.load('sprites\\gameover.png').convert_alpha()
            gameover_img = pygame.transform.scale(gameover_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            rm.sprites['gameover_bg'] = gameover_img
        except:
            print("Erro ao carregar imagem de game over")
            fallback_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fallback_surface.fill((50, 20, 50))
            rm.sprites['gameover_bg'] = fallback_surface
        
        # Player sprites
        rm.load_sprite('player_idle', 'sprites\\warrior - idle.png', HERO_SCALE)
        rm.load_sprite('player_walk1', 'sprites\\warrior-walk1.png', HERO_SCALE)
        rm.load_sprite('player_walk2', 'sprites\\warrior-walk2.png', HERO_SCALE)
        rm.load_sprite('player_walk3', 'sprites\\warrior-walk3.png', HERO_SCALE)
        rm.load_sprite('player_jump', 'sprites\\warrior-jump.png', HERO_SCALE)
        
        # Enemy sprites
        enemies_data = [
            ('bat', ['sprites\\bat.png', 'sprites\\bat-walk.png', 'sprites\\bat-walk1.png']),
            ('zombie', ['sprites\\Enemie3 - idle.png', 'sprites\\Enemie3-walk.png']),
            ('knight', ['sprites\\Enemie1 - idle.png', 'sprites\\Enemie1-walk1.png', 'sprites\\Enemie1-walk2.png']),
            ('owl', ['sprites\\Enemie2 - idle.png', 'sprites\\Enemie2-walk.png']),
            ('bat1', ['sprites\\Enemie6 - idle.png', 'sprites\\Enemie6-walk.png', 'sprites\\Enemie6-walk2.png']),
            ('panther', ['sprites\\Enemie4 - idle.png', 'sprites\\Enemie4-walk.png', 'sprites\\Enemie4-walk1.png', 'sprites\\Enemie4-walk2.png'])
        ]
        
        for enemy_name, sprite_paths in enemies_data:
            frames = []
            for i, path in enumerate(sprite_paths):
                sprite_name = f'{enemy_name}_{i}'
                frames.append(rm.load_sprite(sprite_name, path, ENEMY_SCALE))
            self.animation_manager.add_animation(enemy_name, frames)
        
        # Player animation
        player_walk_frames = [
            rm.sprites['player_idle'],
            rm.sprites['player_walk1'],
            rm.sprites['player_walk2'],
            rm.sprites['player_walk3']
        ]
        self.animation_manager.add_animation('player_walk', player_walk_frames)
        
        # Carrega sons
        rm.load_sound('bg_music', 'music\\Marble Gallery.mp3', self.volume)
        rm.load_sound('game_over', 'music\\game-over-deep-male-voice-clip-352695.mp3', self.volume)
        rm.load_sound('menu_music', 'music\\main-menu.mp3', self.volume)
        
        # Carrega fontes
        rm.load_font('title', 'fonts\\Pixeltype.ttf', 80)
        rm.load_font('large', 'fonts\\Pixeltype.ttf', 50)
        rm.load_font('medium', 'fonts\\Pixeltype.ttf', 40)
        rm.load_font('small', 'fonts\\Pixeltype.ttf', 25)
    
    def setup_timers(self):
        """Configura os timers do jogo"""
        self.obstacle_timer = pygame.USEREVENT + 1
        self.enemy_animation_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.obstacle_timer, 1500)
        pygame.time.set_timer(self.enemy_animation_timer, 150)
    
    def setup_player(self):
        """Inicializa o jogador"""
        self.player_rect = self.resource_manager.sprites['player_idle'].get_rect(topleft=(300, 245))
        self.current_player_surface = self.resource_manager.sprites['player_idle']
    
    def update_volume(self):
        """Atualiza o volume de todos os sons"""
        for sound in self.resource_manager.sounds.values():
            sound.set_volume(self.volume)
    
    def create_obstacle(self):
        """Cria um novo obstáculo"""
        enemy_types = [
            {'type': 'bat', 'y': 255},
            {'type': 'zombie', 'y': 248},
            {'type': 'knight', 'y': 250},
            {'type': 'owl', 'y': 150},
            {'type': 'bat1', 'y': 255},
            {'type': 'panther', 'y': 270}
        ]
        
        chosen_enemy = choice(enemy_types)
        current_frame = self.animation_manager.get_current_frame(chosen_enemy['type'])
        
        if current_frame:
            obstacle_rect = current_frame.get_rect(topleft=(randint(700, 1100), chosen_enemy['y']))
            obstacle_data = {
                'rect': obstacle_rect,
                'type': chosen_enemy['type'],
                'surface': current_frame
            }
            self.obstacle_list.append(obstacle_data)
    
    def update_obstacles(self):
        """Atualiza posição dos obstáculos"""
        updated_obstacles = []
        for obstacle in self.obstacle_list:
            obstacle['rect'].x -= 5
            obstacle['surface'] = self.animation_manager.get_current_frame(obstacle['type'])
            self.screen.blit(obstacle['surface'], obstacle['rect'])
            
            if obstacle['rect'].x > -100:
                updated_obstacles.append(obstacle)
        
        self.obstacle_list = updated_obstacles
    
    def check_collisions(self):
        """Verifica colisões"""
        for obstacle in self.obstacle_list:
            if self.player_rect.colliderect(obstacle['rect']):
                return False
        return True
    
    def update_player_animation(self):
        """Atualiza animação do jogador"""
        if self.player_rect.bottom < GROUND_Y:
            self.current_player_surface = self.resource_manager.sprites['player_jump']
        else:
            self.current_player_surface = self.animation_manager.update('player_walk', 0.1)
    
    def display_score(self):
        """Exibe pontuação, highscore e informações de fase"""
        current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        
        # Score atual
        score_surf = self.resource_manager.fonts['large'].render(f'Score: {current_time}', False, WHITE)
        self.screen.blit(score_surf, (20, 20))
        
        # Highscore com efeitos
        highscore_color = GOLD
        if self.highscore_manager.is_new_record(current_time):
            self.new_record_timer += 1
            if (self.new_record_timer // 20) % 2:
                highscore_color = (255, 50, 50)
            else:
                highscore_color = YELLOW
        
        highscore_surf = self.resource_manager.fonts['small'].render(f'Best: {self.highscore_manager.highscore}', False, highscore_color)
        self.screen.blit(highscore_surf, (20, 70))
        
        # Informações da fase atual
        phase_name = self.phase_manager.get_phase_name()
        phase_surf = self.resource_manager.fonts['small'].render(f'Phase {self.phase_manager.current_phase + 1}: {phase_name}', False, LIGHT_GRAY)
        self.screen.blit(phase_surf, (20, 100))
        
        # Próxima fase
        if self.phase_manager.current_phase < len(PHASE_THRESHOLDS) - 1:
            next_threshold = PHASE_THRESHOLDS[self.phase_manager.current_phase + 1]
            remaining = next_threshold - current_time
            if remaining > 0:
                next_phase_surf = self.resource_manager.fonts['small'].render(f'Next phase in: {remaining}s', False, YELLOW)
                self.screen.blit(next_phase_surf, (20, 120))
        
        # Mensagem de novo recorde
        if self.highscore_manager.is_new_record(current_time) and current_time > 0:
            if (self.new_record_timer // 30) % 2:
                record_surf = self.resource_manager.fonts['medium'].render('NEW RECORD!', False, (255, 50, 50))
                record_rect = record_surf.get_rect(center=(400, 150))
                self.screen.blit(record_surf, record_rect)
        
        return current_time
    
    def draw_phase_notification(self):
        """Desenha notificação de mudança de fase"""
        if self.phase_manager.show_phase_notification:
            # Fundo semi-transparente
            notification_surface = pygame.Surface((400, 100))
            notification_surface.set_alpha(200)
            notification_surface.fill((0, 0, 0))
            notification_rect = notification_surface.get_rect(center=(400, 200))
            self.screen.blit(notification_surface, notification_rect)
            
            # Texto de mudança de fase
            phase_text = f"PHASE {self.phase_manager.current_phase + 1}"
            phase_surf = self.resource_manager.fonts['large'].render(phase_text, False, GOLD)
            phase_rect = phase_surf.get_rect(center=(400, 180))
            self.screen.blit(phase_surf, phase_rect)
            
            # Nome da fase
            name_text = self.phase_manager.get_phase_name()
            name_surf = self.resource_manager.fonts['medium'].render(name_text, False, WHITE)
            name_rect = name_surf.get_rect(center=(400, 220))
            self.screen.blit(name_surf, name_rect)
    
    def draw_menu(self):
        """Desenha o menu principal"""
        self.screen.blit(self.resource_manager.sprites['menu_bg'], (0, 0))
        
        # Título
        title_surf = self.resource_manager.fonts['title'].render('BloodLost', False, RED)
        title_rect = title_surf.get_rect(center=(400, 80))
        self.screen.blit(title_surf, title_rect)
        
        # Subtítulo
        subtitle_surf = self.resource_manager.fonts['medium'].render('Castlevania Runner', False, LIGHT_GRAY)
        subtitle_rect = subtitle_surf.get_rect(center=(400, 120))
        self.screen.blit(subtitle_surf, subtitle_rect)
        
        # Highscore
        highscore_surf = self.resource_manager.fonts['medium'].render(f'Best Score: {self.highscore_manager.highscore}', False, GOLD)
        highscore_rect = highscore_surf.get_rect(center=(400, 160))
        self.screen.blit(highscore_surf, highscore_rect)
        
        # Opções do menu
        menu_options = ['START', 'HIGHSCORES', 'SETTINGS', 'QUIT']
        for i, option in enumerate(menu_options):
            color = YELLOW if i == self.selected_option else GRAY
            
            if i == self.selected_option:
                # Sombra para opção selecionada
                shadow_surf = self.resource_manager.fonts['medium'].render(option, False, BLACK)
                shadow_rect = shadow_surf.get_rect(center=(402, 232 + i * 50))
                self.screen.blit(shadow_surf, shadow_rect)
                
                # Indicador
                indicator_surf = self.resource_manager.fonts['medium'].render('>', False, YELLOW)
                indicator_rect = indicator_surf.get_rect(center=(300, 230 + i * 50))
                self.screen.blit(indicator_surf, indicator_rect)
            
            option_surf = self.resource_manager.fonts['medium'].render(option, False, color)
            option_rect = option_surf.get_rect(center=(400, 230 + i * 50))
            self.screen.blit(option_surf, option_rect)
        
        # Instruções
        instruction_surf = self.resource_manager.fonts['small'].render('Use SETAS para navegar, ENTER para selecionar', False, DARK_GRAY)
        instruction_rect = instruction_surf.get_rect(center=(400, 470))
        self.screen.blit(instruction_surf, instruction_rect)
    
    def draw_highscores(self):
        """Desenha tela de highscores"""
        self.screen.blit(self.resource_manager.sprites['menu_bg'], (0, 0))
        
        # Título
        title_surf = self.resource_manager.fonts['medium'].render('HALL OF FAME', False, RED)
        title_rect = title_surf.get_rect(center=(400, 80))
        self.screen.blit(title_surf, title_rect)
        
        if self.highscore_manager.highscore > 0:
            # Troféu
            trophy_surf = self.resource_manager.fonts['large'].render('🏆', False, GOLD)
            trophy_rect = trophy_surf.get_rect(center=(300, 200))
            self.screen.blit(trophy_surf, trophy_rect)
            
            # Record
            record_surf = self.resource_manager.fonts['medium'].render(f'BEST SCORE: {self.highscore_manager.highscore} seconds', False, GOLD)
            record_rect = record_surf.get_rect(center=(400, 200))
            self.screen.blit(record_surf, record_rect)
            
            # Maior fase alcançada
            max_phase = self.phase_manager.get_current_phase(self.highscore_manager.highscore)
            phase_text = f'Max Phase: {max_phase + 1} - {PHASE_NAMES[max_phase]}'
            phase_surf = self.resource_manager.fonts['small'].render(phase_text, False, LIGHT_GRAY)
            phase_rect = phase_surf.get_rect(center=(400, 230))
            self.screen.blit(phase_surf, phase_rect)
            
            # Rank
            rank_data = self.get_rank_info(self.highscore_manager.highscore)
            rank_surf = self.resource_manager.fonts['small'].render(f'Rank: {rank_data["title"]}', False, rank_data["color"])
            rank_rect = rank_surf.get_rect(center=(400, 260))
            self.screen.blit(rank_surf, rank_rect)
            
            # Mensagem
            message_surf = self.resource_manager.fonts['small'].render(rank_data["message"], False, GRAY)
            message_rect = message_surf.get_rect(center=(400, 290))
            self.screen.blit(message_surf, message_rect)
        else:
            no_record_surf = self.resource_manager.fonts['medium'].render('No records yet!', False, LIGHT_GRAY)
            no_record_rect = no_record_surf.get_rect(center=(400, 200))
            self.screen.blit(no_record_surf, no_record_rect)
        
        # Instruções
        back_surf = self.resource_manager.fonts['small'].render('Press ESC or ENTER to return', False, DARK_GRAY)
        back_rect = back_surf.get_rect(center=(400, 450))
        self.screen.blit(back_surf, back_rect)
    
    def get_rank_info(self, score):
        """Retorna informações do rank baseado na pontuação"""
        if score >= 100:
            return {"title": "VAMPIRE SLAYER", "color": (255, 50, 50), "message": "You are the ultimate vampire hunter!"}
        elif score >= 60:
            return {"title": "DARK KNIGHT", "color": (150, 50, 150), "message": "The castle trembles before you!"}
        elif score >= 30:
            return {"title": "CASTLE EXPLORER", "color": (100, 100, 255), "message": "You're getting stronger, warrior!"}
        elif score >= 15:
            return {"title": "BRAVE WARRIOR", "color": (255, 150, 50), "message": "Keep training to become legendary!"}
        else:
            return {"title": "NOVICE HUNTER", "color": LIGHT_GRAY, "message": "Keep training to become legendary!"}
    
    def draw_settings(self):
        """Desenha tela de configurações"""
        self.screen.blit(self.resource_manager.sprites['menu_bg'], (0, 0))
        
        # Título
        title_surf = self.resource_manager.fonts['medium'].render('CONFIGURAÇÕES', False, RED)
        title_rect = title_surf.get_rect(center=(400, 100))
        self.screen.blit(title_surf, title_rect)
        
        # Opções
        settings_options = [
            f'Volume: {int(self.volume * 100)}%',
            'Dificuldade: Normal',
            'Reset Highscore',
            'Voltar'
        ]
        
        for i, option in enumerate(settings_options):
            if i == self.selected_setting:
                color = YELLOW
                # Sombra
                shadow_surf = self.resource_manager.fonts['medium'].render(option, False, BLACK)
                shadow_rect = shadow_surf.get_rect(center=(402, 182 + i * 50))
                self.screen.blit(shadow_surf, shadow_rect)
                
                # Indicador
                indicator_surf = self.resource_manager.fonts['medium'].render('>', False, YELLOW)
                indicator_rect = indicator_surf.get_rect(center=(200, 180 + i * 50))
                self.screen.blit(indicator_surf, indicator_rect)
            else:
                color = (255, 100, 100) if i == 2 else GRAY  # Vermelho para reset
            
            option_surf = self.resource_manager.fonts['medium'].render(option, False, color)
            option_rect = option_surf.get_rect(center=(400, 180 + i * 50))
            self.screen.blit(option_surf, option_rect)
        
        # Instruções
        instructions = [
            'Use A/D ou SETAS ESQUERDA/DIREITA para ajustar volume',
            'ENTER para selecionar, ESC para voltar',
            'ENTER para resetar o recorde (não pode ser desfeito!)',
            'ENTER para selecionar, ESC para voltar'
        ]
        
        instruction_surf = self.resource_manager.fonts['small'].render(instructions[self.selected_setting], False, DARK_GRAY)
        instruction_rect = instruction_surf.get_rect(center=(400, 400))
        self.screen.blit(instruction_surf, instruction_rect)
    
    def draw_game_over(self):
        """Desenha tela de game over"""
        self.screen.blit(self.resource_manager.sprites['gameover_bg'], (0, 0))
        
        # Adiciona um overlay semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Novo recorde?
        is_new_record = self.highscore_manager.is_new_record(self.score) and self.score > 0
        
        if is_new_record:
            # Efeito piscante para novo recorde
            if (pygame.time.get_ticks() // 500) % 2:
                record_surf = self.resource_manager.fonts['medium'].render('NEW RECORD!', False, GOLD)
                record_rect = record_surf.get_rect(center=(400, 240))
                
                # Sombra do texto
                shadow_surf = self.resource_manager.fonts['medium'].render('NEW RECORD!', False, BLACK)
                shadow_rect = shadow_surf.get_rect(center=(402, 242))
                self.screen.blit(shadow_surf, shadow_rect)
                self.screen.blit(record_surf, record_rect)
        
        # Pontuação com sombra
        score_text = f'Your Score: {self.score}'
        shadow_surf = self.resource_manager.fonts['large'].render(score_text, False, BLACK)
        shadow_rect = shadow_surf.get_rect(center=(402, 282))
        self.screen.blit(shadow_surf, shadow_rect)
        
        score_surf = self.resource_manager.fonts['large'].render(score_text, False, (255, 50, 50))
        score_rect = score_surf.get_rect(center=(400, 280))
        self.screen.blit(score_surf, score_rect)
        
        # Melhor pontuação com sombra
        best_text = f'Best: {self.highscore_manager.highscore}'
        shadow_surf = self.resource_manager.fonts['small'].render(best_text, False, BLACK)
        shadow_rect = shadow_surf.get_rect(center=(402, 322))
        self.screen.blit(shadow_surf, shadow_rect)
        
        best_surf = self.resource_manager.fonts['small'].render(best_text, False, GOLD)
        best_rect = best_surf.get_rect(center=(400, 320))
        self.screen.blit(best_surf, best_rect)
        
        # Fase máxima alcançada
        max_phase = self.phase_manager.get_current_phase(self.score)
        phase_text = f'Max Phase Reached: {max_phase + 1}'
        phase_surf = self.resource_manager.fonts['small'].render(phase_text, False, LIGHT_GRAY)
        phase_rect = phase_surf.get_rect(center=(400, 350))
        self.screen.blit(phase_surf, phase_rect)
        
        # Instruções com sombra
        restart_text = 'Press SPACE to play again'
        shadow_surf = self.resource_manager.fonts['medium'].render(restart_text, False, BLACK)
        shadow_rect = shadow_surf.get_rect(center=(402, 392))
        self.screen.blit(shadow_surf, shadow_rect)
        
        restart_surf = self.resource_manager.fonts['medium'].render(restart_text, False, GRAY)
        restart_rect = restart_surf.get_rect(center=(400, 390))
        self.screen.blit(restart_surf, restart_rect)
        
        menu_text = 'Press ESC to return to menu'
        shadow_surf = self.resource_manager.fonts['small'].render(menu_text, False, BLACK)
        shadow_rect = shadow_surf.get_rect(center=(402, 432))
        self.screen.blit(shadow_surf, shadow_rect)
        
        menu_surf = self.resource_manager.fonts['small'].render(menu_text, False, LIGHT_GRAY)
        menu_rect = menu_surf.get_rect(center=(400, 430))
        self.screen.blit(menu_surf, menu_rect)
    
    def handle_events(self):
        """Gerencia todos os eventos"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Eventos baseados no estado
            if self.game_state == "menu":
                self.handle_menu_events(event)
            elif self.game_state == "highscores":
                self.handle_highscore_events(event)
            elif self.game_state == "settings":
                self.handle_settings_events(event)
            elif self.game_state == "playing":
                self.handle_game_events(event)
            elif self.game_state == "game_over":
                self.handle_game_over_events(event)
        
        return True
    
    def handle_menu_events(self, event):
        """Gerencia eventos do menu"""
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.selected_option = (self.selected_option - 1) % 4
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.selected_option = (self.selected_option + 1) % 4
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:  # START
                    self.start_game()
                elif self.selected_option == 1:  # HIGHSCORES
                    self.game_state = "highscores"
                elif self.selected_option == 2:  # SETTINGS
                    self.game_state = "settings"
                elif self.selected_option == 3:  # QUIT
                    return False
    
    def handle_highscore_events(self, event):
        """Gerencia eventos da tela de highscores"""
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                self.game_state = "menu"
    
    def handle_settings_events(self, event):
        """Gerencia eventos das configurações"""
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.selected_setting = (self.selected_setting - 1) % 4
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.selected_setting = (self.selected_setting + 1) % 4
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"
            elif event.key == pygame.K_RETURN:
                if self.selected_setting == 2:  # Reset Highscore
                    self.highscore_manager.reset()
                elif self.selected_setting == 3:  # Voltar
                    self.game_state = "menu"
            elif event.key in [pygame.K_LEFT, pygame.K_a]:
                if self.selected_setting == 0:  # Volume
                    self.volume = max(0.0, self.volume - 0.1)
                    self.update_volume()
            elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                if self.selected_setting == 0:  # Volume
                    self.volume = min(1.0, self.volume + 0.1)
                    self.update_volume()
    
    def handle_game_events(self, event):
        """Gerencia eventos durante o jogo"""
        if event.type == self.obstacle_timer:
            self.create_obstacle()
        elif event.type == self.enemy_animation_timer:
            # Atualiza animações dos inimigos
            for enemy_type in ['bat', 'zombie', 'knight', 'owl', 'bat1', 'panther']:
                self.animation_manager.update(enemy_type, 1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.player_rect.bottom >= GROUND_Y:
                self.player_gravity = JUMP_FORCE
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"
                self.reset_game_state()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.player_rect.collidepoint(event.pos) and self.player_rect.bottom >= GROUND_Y:
                self.player_gravity = JUMP_FORCE
    
    def handle_game_over_events(self, event):
        """Gerencia eventos do game over"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"
                self.reset_game_state()
    
    def start_game(self):
        """Inicia uma nova partida"""
        self.game_state = "playing"
        self.obstacle_list.clear()
        self.start_time = int(pygame.time.get_ticks() / 1000)
        self.new_record_timer = 0
        self.player_rect.bottom = GROUND_Y
        self.player_gravity = 0
        
        # Reseta o gerenciador de fases
        self.phase_manager = PhaseManager()
        
        # Música
        if 'menu_music' in self.resource_manager.sounds:
            self.resource_manager.sounds['menu_music'].stop()
        self.main_menu_playing = False
        
        if 'bg_music' in self.resource_manager.sounds:
            self.resource_manager.sounds['bg_music'].play(loops=-1)
        self.music_playing = True
    
    def reset_game_state(self):
        """Reseta estado do jogo"""
        self.obstacle_list.clear()
        self.player_rect.bottom = GROUND_Y
        self.player_gravity = 0
        
        # Reseta o gerenciador de fases
        self.phase_manager = PhaseManager()
        
        # Para música do jogo
        if 'bg_music' in self.resource_manager.sounds:
            self.resource_manager.sounds['bg_music'].stop()
        self.music_playing = False
        
        # Inicia música do menu
        if 'menu_music' in self.resource_manager.sounds:
            self.resource_manager.sounds['menu_music'].play(loops=-1)
        self.main_menu_playing = True
    
    def get_current_background(self):
        """Retorna o background da fase atual"""
        background_name = self.phase_manager.get_background_name()
        if background_name in self.resource_manager.sprites:
            return self.resource_manager.sprites[background_name]
        else:
            return self.resource_manager.sprites['background_phase_0']  # Fallback
    
    def update_game(self):
        """Atualiza lógica do jogo"""
        if self.game_state == "playing":
            # Scroll do background
            self.bg_x_pos -= 2
            current_bg = self.get_current_background()
            if self.bg_x_pos <= -current_bg.get_width():
                self.bg_x_pos = 0
            
            # Desenha background com scroll (usando o background da fase atual)
            self.screen.blit(current_bg, (self.bg_x_pos, 0))
            self.screen.blit(current_bg, (self.bg_x_pos + current_bg.get_width(), 0))
            
            # Atualiza score
            self.score = self.display_score()
            
            # Atualiza fase baseada no score
            phase_changed = self.phase_manager.update_phase(self.score)
            
            # Atualiza timer de notificação de mudança de fase
            self.phase_manager.update_notification_timer()
            
            # Atualiza obstáculos
            self.update_obstacles()
            
            # Física do jogador
            if self.player_gravity < 0:
                self.player_gravity += GRAVITY_ASCEND
            else:
                self.player_gravity += GRAVITY_DESCEND
            
            self.player_rect.y += self.player_gravity
            
            # Limita no chão
            if self.player_rect.bottom >= GROUND_Y:
                self.player_rect.bottom = GROUND_Y
            
            # Atualiza animação do jogador
            self.update_player_animation()
            self.screen.blit(self.current_player_surface, self.player_rect)
            
            # Desenha notificação de mudança de fase (por cima de tudo)
            self.draw_phase_notification()
            
            # Verifica colisões
            if not self.check_collisions():
                # Game over
                if self.highscore_manager.update_if_record(self.score):
                    pass  # Novo recorde salvo automaticamente
                
                self.game_state = "game_over"
                
                # Para música e toca game over
                if 'bg_music' in self.resource_manager.sounds:
                    self.resource_manager.sounds['bg_music'].stop()
                self.music_playing = False
                
                if 'game_over' in self.resource_manager.sounds:
                    self.resource_manager.sounds['game_over'].play()
                self.game_over_music_playing = True
    
    def update_audio(self):
        """Gerencia estados de áudio"""
        if self.game_state in ["menu", "highscores", "settings"]:
            if self.music_playing and 'bg_music' in self.resource_manager.sounds:
                self.resource_manager.sounds['bg_music'].stop()
                self.music_playing = False
            
            if not self.main_menu_playing and 'menu_music' in self.resource_manager.sounds:
                self.resource_manager.sounds['menu_music'].play(loops=-1)
                self.main_menu_playing = True
                
        elif self.game_state == "playing":
            if self.main_menu_playing and 'menu_music' in self.resource_manager.sounds:
                self.resource_manager.sounds['menu_music'].stop()
                self.main_menu_playing = False
            
            if not self.music_playing and 'bg_music' in self.resource_manager.sounds:
                self.resource_manager.sounds['bg_music'].play(loops=-1)
                self.music_playing = True
                
        elif self.game_state == "game_over":
            if self.music_playing and 'bg_music' in self.resource_manager.sounds:
                self.resource_manager.sounds['bg_music'].stop()
                self.music_playing = False
            
            if self.main_menu_playing and 'menu_music' in self.resource_manager.sounds:
                self.resource_manager.sounds['menu_music'].stop()
                self.main_menu_playing = False
    
    def render(self):
        """Renderiza a tela baseada no estado atual"""
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "highscores":
            self.draw_highscores()
        elif self.game_state == "settings":
            self.draw_settings()
        elif self.game_state == "game_over":
            self.draw_game_over()
        # Estado "playing" é renderizado em update_game()
    
    def run(self):
        """Loop principal do jogo"""
        # Inicia música do menu
        if 'menu_music' in self.resource_manager.sounds:
            self.resource_manager.sounds['menu_music'].play(loops=-1)
        
        running = True
        while running:
            # Eventos
            running = self.handle_events()
            if not running:
                break
            
            # Atualiza áudio
            self.update_audio()
            
            # Atualiza jogo
            self.update_game()
            
            # Renderização
            self.render()
            
            # Atualiza tela
            pygame.display.update()
            self.clock.tick(FPS)
        
        pygame.quit()
        exit()

# ==================== FUNÇÃO PRINCIPAL ====================
def main():
    """Função principal"""
    try:
        game = BloodLostGame()
        game.run()
    except Exception as e:
        print(f"Erro ao iniciar o jogo: {e}")
        pygame.quit()
        exit()

# ==================== EXECUÇÃO ====================
if __name__ == "__main__":
    main()