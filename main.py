import pygame
from sys import exit
from random import randint, choice
import json
import os
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

JUMP_FORCE = -9
GRAVITY_ASCEND = 0.4
GRAVITY_DESCEND = 0.8
GROUND_Y = 310

MAX_LIVES = 3
HEART_SIZE = 32
HEART_SPACING = 40
HEARTS_START_X = SCREEN_WIDTH - 150
HEARTS_Y = 30

SCALE_FACTOR = 1.5
HERO_SCALE = 2
ENEMY_SCALE = 2

# NOVO: Tipos de daltonismo disponíveis
COLORBLIND_TYPES = {
    "normal": {"en": "Normal Vision", "pt": "Visão Normal"},
    "protanomalia": {"en": "Protanomalia", "pt": "Protanomalia"},
    "deuteranomalia": {"en": "Deuteranomalia", "pt": "Deuteranomalia"},
    "tritanomalia": {"en": "Tritanomalia", "pt": "Tritanomalia"},
}

COLORBLIND_ORDER = ["normal", "protanomalia", "deuteranomalia", "tritanomalia"]

PHASE_THRESHOLDS = [0, 500, 1500, 3000, 5000]
PHASE_NAMES = {
    "en": [
        "Castle Entrance",
        "Dark Corridors",
        "Ancient Library",
        "Vampire's Chamber",
        "Dracula's Lair",
    ],
    "pt": [
        "Entrada do Castelo",
        "Corredores Sombrios",
        "Biblioteca Antiga",
        "Câmara do Vampiro",
        "Covil do Drácula",
    ],
}

BOSS_TRIGGER = 50

POINTS_JUMP_ENEMY = 50
POINTS_KILL_ENEMY = 20
POINTS_BOSS_DEFEAT = 1000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
YELLOW = (255, 255, 100)
GOLD = (255, 215, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)

TEXTS = {
    "en": {
        "title": "BloodLost",
        "colorblind_mode": "Color Mode: {}",
        "best_score": "Best Score: {}",
        "start": "START",
        "instructions": "INSTRUCTIONS",  # NOVO
        "highscores": "HIGHSCORES",
        "settings": "SETTINGS",
        "language": "LANGUAGE",
        "quit": "QUIT",
        "navigate": "Use ARROWS to navigate, ENTER to select",
        "shoot_info": "NEW: Press X to SHOOT magic projectiles, Z for WHIP attacks!",
        "whip_info": "Whip has long range and destroys enemies instantly!",
        "hall_of_fame": "HALL OF FAME",
        "best_score_display": "BEST SCORE: {} seconds",
        "boss_defeated": "Boss Defeated: {}",
        "enemies_whipped": "Enemies Whipped: {}",
        "dracula_boss": "Dracula - DEFEATED",
        "dracula_boss_not": "Dracula - Not faced",
        "rank": "Rank: {}",
        "no_records": "No records yet!",
        "press_back": "Press ESC or ENTER to return",
        "configurations": "CONFIGURATIONS",
        "volume": "Volume: {}%",
        "difficulty": "Difficulty: Normal",
        "reset_highscore": "Reset Highscore",
        "reset_boss": "Reset Boss Progress",
        "back": "Back",
        "volume_instruction": "Use A/D or LEFT/RIGHT ARROWS to adjust volume",
        "enter_instruction": "ENTER to select, ESC to go back",
        "reset_record_warning": "ENTER to reset record (cannot be undone!)",
        "reset_boss_warning": "ENTER to reset boss progress",
        "back_menu": "ENTER to return to main menu",
        "your_score": "Your Score: {}",
        "best": "Best: {}",
        "boss_defeated_run": "Boss Defeated: {}",
        "enemies_whipped_run": "Enemies Whipped This Run: {}",
        "max_phase": "Max Phase Reached: {}",
        "play_again": "Press SPACE to play again",
        "return_menu": "Press ESC to return to menu",
        "new_record": "NEW RECORD!",
        "score": "Score: {}",
        "phase": "Phase {}: {}",
        "boss_approaching": "DRACULA APPROACHES!",
        "next_phase": "Next phase in: {}s",
        "invulnerable": "INVULNERABLE",
        "reload": "Reload: {}",
        "ready_shoot": "Ready to Shoot!",
        "whip_cooldown": "Whip Cooldown: {}",
        "whip_ready": "Whip Ready! [Z]",
        "enemies_defeated": "Enemies Defeated: {}",
        "combo": "Combo x{}!",
        "boss_defeated": "DRACULA DEFEATED!",
        "boss_hp": "{}/{} HP",
        "dracula_boss_name": "Count Dracula",
        "ranks": {
            "vampire_slayer": "VAMPIRE SLAYER",
            "dark_knight": "DARK KNIGHT",
            "castle_explorer": "CASTLE EXPLORER",
            "brave_warrior": "BRAVE WARRIOR",
            "novice_hunter": "NOVICE HUNTER",
        },
        "game_instructions": "GAME INSTRUCTIONS",
        "basic_controls": "BASIC CONTROLS:",
        "movement": "Movement:",
        "movement_keys": "A/LEFT ARROW - Move Left",
        "movement_keys_right": "D/RIGHT ARROW - Move Right",
        "jump": "Jump:",
        "jump_keys": "SPACE/UP ARROW/W - Jump",
        "combat": "COMBAT SYSTEM:",
        "shooting": "Magic Projectiles:",
        "shooting_keys": "X/E - Shoot magic knives",
        "whip_attack": "Whip Attack:",
        "whip_keys": "Z/Q - Whip attack (high damage, long range)",
        "gameplay": "GAMEPLAY:",
        "objective": "Survive as long as possible in Dracula's castle",
        "enemies": "Jump over enemies or destroy them with attacks",
        "scoring": "Scoring System:",
        "score_jump": "Jump over enemy: +50 points",
        "score_kill": "Destroy enemy: +20 points",
        "score_boss": "Defeat Dracula: +1000 points",
        "boss_info": "BOSS BATTLE:",
        "boss_trigger": "Dracula appears after reaching 50 points",
        "boss_movement": "During boss battle, use A/D to move left/right",
        "boss_strategy": "Hit Dracula with projectiles to damage him",
        "boss_avoid": "Avoid his fireballs and cape attacks",
        "phases_info": "CASTLE PHASES:",
        "phase_progression": "Progress through 5 castle phases as you score higher",
        "tips": "TIPS:",
        "tip_combo": "Chain attacks for combo multipliers",
        "tip_whip": "Whip attack destroys enemies instantly",
        "tip_invulnerable": "You're briefly invulnerable after taking damage",
    },
    "pt": {
        "title": "BloodLost",
        "colorblind_mode": "Modo de Cor: {}",
        "best_score": "Melhor Pontuacao: {}",
        "start": "INICIAR",
        "instructions": "INSTRUCOES",  # NOVO
        "highscores": "RECORDES",
        "settings": "CONFIGURACOES",
        "language": "IDIOMA",
        "quit": "SAIR",
        "navigate": "Use SETAS para navegar, ENTER para selecionar",
        "shoot_info": "NOVO: Aperte X para ATIRAR projéteis mágicos, Z para atacar com CHICOTE!",
        "whip_info": "O chicote tem longo alcance e destrói inimigos instantaneamente!",
        "hall_of_fame": "HALL DA FAMA",
        "best_score_display": "MELHOR PONTUAÇÃO: {} segundos",
        "boss_defeated": "Chefe Derrotado: {}",
        "enemies_whipped": "Inimigos Chicoteados: {}",
        "dracula_boss": "Drácula - DERROTADO",
        "dracula_boss_not": "Drácula - Não enfrentado",
        "rank": "Rank: {}",
        "no_records": "Ainda não há recordes!",
        "press_back": "Aperte ESC ou ENTER para voltar",
        "configurations": "CONFIGURACOES",
        "volume": "Volume: {}%",
        "difficulty": "Dificuldade: Normal",
        "reset_highscore": "Resetar Recorde",
        "reset_boss": "Resetar Progresso do Chefe",
        "back": "Voltar",
        "volume_instruction": "Use A/D ou SETAS ESQUERDA/DIREITA para ajustar volume",
        "enter_instruction": "ENTER para selecionar, ESC para voltar",
        "reset_record_warning": "ENTER para resetar o recorde (não pode ser desfeito!)",
        "reset_boss_warning": "ENTER para resetar progresso do chefe",
        "back_menu": "ENTER para voltar ao menu principal",
        "your_score": "Sua Pontuação: {}",
        "best": "Melhor: {}",
        "boss_defeated_run": "Chefe Derrotado: {}",
        "enemies_whipped_run": "Inimigos Chicoteados Esta Partida: {}",
        "max_phase": "Fase Máxima Alcançada: {}",
        "play_again": "Aperte ESPAÇO para jogar novamente",
        "return_menu": "Aperte ESC para voltar ao menu",
        "new_record": "NOVO RECORDE!",
        "score": "Pontuação: {}",
        "phase": "Fase {}: {}",
        "boss_approaching": "DRÁCULA SE APROXIMA!",
        "next_phase": "Próxima fase em: {}s",
        "invulnerable": "INVULNERÁVEL",
        "reload": "Recarregando: {}",
        "ready_shoot": "Pronto para Atirar!",
        "whip_cooldown": "Recarga do Chicote: {}",
        "whip_ready": "Chicote Pronto! [Z]",
        "enemies_defeated": "Inimigos Derrotados: {}",
        "combo": "Combo x{}!",
        "boss_defeated": "DRÁCULA DERROTADO!",
        "boss_hp": "{}/{} HP",
        "dracula_boss_name": "Conde Drácula",
        "ranks": {
            "vampire_slayer": "CAÇADOR DE VAMPIROS",
            "dark_knight": "CAVALEIRO SOMBRIO",
            "castle_explorer": "EXPLORADOR DO CASTELO",
            "brave_warrior": "GUERREIRO CORAJOSO",
            "novice_hunter": "CAÇADOR NOVATO",
        },
        "game_instructions": "INSTRUCOES DO JOGO",
        "basic_controls": "CONTROLES BASICOS:",
        "movement": "Movimento:",
        "movement_keys": "A/SETA ESQUERDA - Mover para Esquerda",
        "movement_keys_right": "D/SETA DIREITA - Mover para Direita",
        "jump": "Pular:",
        "jump_keys": "ESPACO/SETA CIMA/W - Pular",
        "combat": "SISTEMA DE COMBATE:",
        "shooting": "Projéteis Mágicos:",
        "shooting_keys": "X/E - Atirar facas mágicas",
        "whip_attack": "Ataque de Chicote:",
        "whip_keys": "Z/Q - Ataque de chicote (alto dano, longo alcance)",
        "gameplay": "JOGABILIDADE:",
        "objective": "Sobreviva o máximo possível no castelo do Drácula",
        "enemies": "Pule sobre inimigos ou os destrua com ataques",
        "scoring": "Sistema de Pontuação:",
        "score_jump": "Pular sobre inimigo: +50 pontos",
        "score_kill": "Destruir inimigo: +20 pontos",
        "score_boss": "Derrotar Drácula: +1000 pontos",
        "boss_info": "BATALHA DO CHEFE:",
        "boss_trigger": "Drácula aparece após alcançar 50 pontos",
        "boss_movement": "Durante batalha do chefe, use A/D para mover esquerda/direita",
        "boss_strategy": "Atinja o Drácula com projéteis para causar dano",
        "boss_avoid": "Evite suas bolas de fogo e ataques do manto",
        "phases_info": "FASES DO CASTELO:",
        "phase_progression": "Progrida através de 5 fases do castelo conforme sua pontuação aumenta",
        "tips": "DICAS:",
        "tip_combo": "Encadeie ataques para multiplicadores de combo",
        "tip_whip": "Ataque de chicote destrói inimigos instantaneamente",
        "tip_invulnerable": "Você fica brevemente invulnerável após receber dano",
    },
}

PLAYER_START_X = 300
PLAYER_START_Y = 245


class LifeManager:
    def __init__(
        self, resource_manager, language_manager
    ):  # CORRIGIDO: adicionar language_manager
        self.current_lives = MAX_LIVES
        self.max_lives = MAX_LIVES
        self.resource_manager = resource_manager
        self.language_manager = language_manager  # NOVO
        self.heart_sprite = None
        self.empty_heart_sprite = None
        self.load_heart_sprites()

    def load_heart_sprites(self):
        """Carrega sprites do coração baseado no modo de daltonismo"""
        colorblind_mode = self.language_manager.colorblind_mode
        heart_sprite_name = f"heart_{colorblind_mode}"

        # Tentar carregar sprite do coração para o modo atual
        if heart_sprite_name in self.resource_manager.sprites:
            self.heart_sprite = self.resource_manager.sprites[heart_sprite_name]
        else:
            # Fallback para criar sprite pixel art
            self.heart_sprite = self.create_heart_sprite(True)

        # Coração vazio sempre usa o mesmo sprite (cinza)
        try:
            empty_heart_name = "empty_heart"
            if empty_heart_name in self.resource_manager.sprites:
                self.empty_heart_sprite = self.resource_manager.sprites[empty_heart_name]
            else:
                self.empty_heart_sprite = self.resource_manager.load_sprite(
                    "empty_heart", "sprites\\Item\\empity.png", 2.0
                )
        except:
            self.empty_heart_sprite = self.create_heart_sprite(False)

    def update_colorblind_mode(self):
        """Atualiza os sprites quando o modo de daltonismo muda"""
        self.load_heart_sprites()

    def create_heart_sprite(self, filled=True):
        """Cria um sprite de coração pixel art"""
        sprite = pygame.Surface((16, 16), pygame.SRCALPHA)

        if filled:
            # Coração vermelho preenchido
            heart_color = (220, 20, 60)  # Vermelho escuro
            outline_color = (139, 0, 0)  # Vermelho muito escuro para contorno
        else:
            # Coração vazio/cinza
            heart_color = (100, 100, 100)  # Cinza
            outline_color = (60, 60, 60)  # Cinza escuro para contorno

        # Pixel art do coração (16x16)
        heart_pixels = [
            "  ####  ####  ",
            " ########### ",
            "##############",
            "##############",
            " ############ ",
            "  ##########  ",
            "   ########   ",
            "    ######    ",
            "     ####     ",
            "      ##      ",
            "              ",
        ]

        for y, row in enumerate(heart_pixels):
            for x, pixel in enumerate(row):
                if pixel == "#":
                    sprite.set_at((x, y), heart_color)
                elif pixel == ".":
                    sprite.set_at((x, y), outline_color)

        # Escalar para ficar maior
        return pygame.transform.scale(sprite, (HEART_SIZE, HEART_SIZE))

    def take_damage(self):
        """Remove uma vida e retorna True se ainda há vidas, False se game over"""
        if self.current_lives > 0:
            self.current_lives -= 1
        return self.current_lives > 0

    def is_alive(self):
        """Retorna se o jogador ainda tem vidas"""
        return self.current_lives > 0

    def reset_lives(self):
        """Restaura todas as vidas"""
        self.current_lives = self.max_lives

    def add_life(self):
        """Adiciona uma vida (máximo 3)"""
        if self.current_lives < self.max_lives:
            self.current_lives += 1

    def draw(self, screen):
        """Desenha os corações na tela"""
        for i in range(self.max_lives):
            heart_x = HEARTS_START_X + (i * HEART_SPACING)
            heart_y = HEARTS_Y

            if i < self.current_lives:
                # Coração preenchido
                screen.blit(self.heart_sprite, (heart_x, heart_y))
            else:
                # Coração vazio
                screen.blit(self.empty_heart_sprite, (heart_x, heart_y))


class PlayerAnimationState:
    def __init__(self):
        self.current_state = "walking"
        self.state_timer = 0
        self.frame_counter = 0
        self.victory_timer = 0
        self.victory_auto_return = 480

    def update_state(self, is_attacking, is_jumping):
        self.state_timer += 1
        self.frame_counter += 1

        if is_attacking:
            if self.current_state != "attacking":
                self.state_timer = 0
                self.frame_counter = 0
            self.current_state = "attacking"
        elif is_jumping:
            if self.current_state != "jumping":
                self.state_timer = 0
                self.frame_counter = 0
            self.current_state = "jumping"
        else:
            if self.current_state != "walking":
                self.state_timer = 0
                self.frame_counter = 0
            self.current_state = "walking"

    def get_current_state(self):
        return self.current_state

    def get_state_timer(self):
        return self.state_timer

    def get_frame_counter(self):
        return self.frame_counter


class WhipAttack:
    def __init__(self, x, y, direction="right"):
        self.x = x
        self.y = y
        self.direction = direction
        self.active = True

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8

        self.hitboxes = self.setup_hitboxes()

        self.damage_dealt = []
        self.screen_shake = 0

    def setup_hitboxes(self):
        if self.direction == "right":
            return [
                pygame.Rect(self.x + 40, self.y - 10, 60, 30),
                pygame.Rect(self.x + 40, self.y - 15, 120, 40),
                pygame.Rect(self.x + 40, self.y - 20, 180, 50),
            ]
        else:
            return [
                pygame.Rect(self.x - 100, self.y - 10, 60, 30),
                pygame.Rect(self.x - 160, self.y - 15, 120, 40),
                pygame.Rect(self.x - 220, self.y - 20, 180, 50),
            ]

    def update(self):
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.current_frame += 1
            self.animation_timer = 0

            if self.current_frame >= 3:
                self.active = False
                return False

        if self.screen_shake > 0:
            self.screen_shake -= 1

        return True

    def get_current_hitbox(self):
        if self.current_frame < len(self.hitboxes):
            return self.hitboxes[self.current_frame]
        return None

    def check_enemy_collision(self, obstacles):
        if not self.active:
            return []

        current_hitbox = self.get_current_hitbox()
        if not current_hitbox:
            return []

        hit_enemies = []
        for obstacle in obstacles:
            obstacle_id = id(obstacle)
            if obstacle_id not in self.damage_dealt:
                if current_hitbox.colliderect(obstacle["rect"]):
                    hit_enemies.append(obstacle)
                    self.damage_dealt.append(obstacle_id)
                    self.screen_shake = 10

        return hit_enemies

    def draw(self, screen, whip_sprites=None):
        if not self.active:
            return

        shake_x = (
            randint(-self.screen_shake // 2, self.screen_shake // 2)
            if self.screen_shake > 0
            else 0
        )
        shake_y = (
            randint(-self.screen_shake // 2, self.screen_shake // 2)
            if self.screen_shake > 0
            else 0
        )

        current_hitbox = self.get_current_hitbox()
        if current_hitbox:
            if whip_sprites and len(whip_sprites) > self.current_frame:
                sprite = whip_sprites[self.current_frame]
                if self.direction == "left":
                    sprite = pygame.transform.flip(sprite, True, False)
                screen.blit(
                    sprite, (current_hitbox.x + shake_x, current_hitbox.y + shake_y)
                )
            else:
                if self.current_frame == 2:
                    end_x = (
                        current_hitbox.right
                        if self.direction == "right"
                        else current_hitbox.left
                    )
                    end_pos = (end_x + shake_x, self.y + shake_y)

                    pygame.draw.circle(screen, (255, 215, 0), end_pos, 3)
                    pygame.draw.circle(screen, (255, 255, 255), end_pos, 2)


class PlayerAttackSystem:
    def __init__(self, language_manager):
        self.current_whip_attack = None
        self.attack_cooldown = 0
        self.attack_cooldown_max = 30

        self.whip_sprites = []

        self.enemies_defeated = 0
        self.combo_counter = 0
        self.combo_timer = 0

        self.language_manager = language_manager

    def load_whip_sprites(self, resource_manager):
        sprite_paths = []

        for i, path in enumerate(sprite_paths):
            try:
                sprite = resource_manager.load_sprite(f"whip_{i}", path, 2.0)
                self.whip_sprites.append(sprite)
            except:
                self.whip_sprites.append(None)

    def can_attack(self):
        return self.attack_cooldown <= 0 and (
            self.current_whip_attack is None or not self.current_whip_attack.active
        )

    def start_whip_attack(self, player_rect, direction="right"):
        if not self.can_attack():
            return False

        self.current_whip_attack = WhipAttack(
            player_rect.centerx,
            player_rect.centery - 10,
            direction,
        )

        self.attack_cooldown = self.attack_cooldown_max

        return True

    def is_attacking(self):
        return self.current_whip_attack and self.current_whip_attack.active

    def get_attack_frame(self):
        if self.current_whip_attack and self.current_whip_attack.active:
            return self.current_whip_attack.current_frame
        return 0

    def update(self, obstacles, boss_manager=None, sounds=None):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_counter = 0

        if self.current_whip_attack and self.current_whip_attack.active:
            still_active = self.current_whip_attack.update()

            if still_active:
                hit_enemies = self.current_whip_attack.check_enemy_collision(obstacles)

                if hit_enemies:
                    for enemy in hit_enemies:
                        if enemy in obstacles:
                            obstacles.remove(enemy)

                    killed_count = len(hit_enemies)
                    self.enemies_defeated += killed_count
                    self.combo_counter += killed_count
                    self.combo_timer = 120

                    if sounds and "whip_hit" in sounds:
                        sounds["whip_hit"].play()

                    return killed_count

                if boss_manager and boss_manager.is_boss_active():
                    if self.check_boss_collision(boss_manager):
                        # Boss foi atingido!
                        if sounds and "whip_hit" in sounds:
                            sounds["whip_hit"].play()

                        self.combo_counter += 1
                        self.combo_timer = 120
            else:
                self.current_whip_attack = None

    def check_boss_collision(self, boss_manager):
        """Verifica se o chicote atingiu o boss"""
        if not self.current_whip_attack or not self.current_whip_attack.active:
            return False

        current_hitbox = self.current_whip_attack.get_current_hitbox()
        if not current_hitbox:
            return False

        # Verificar se já causou dano neste frame
        boss_id = "boss_dracula"
        if boss_id in self.current_whip_attack.damage_dealt:
            return False

        # Verificar colisão com o boss
        boss = boss_manager.current_boss
        if boss and boss.active and boss.phase == "fighting":
            if current_hitbox.colliderect(boss.boss_rect):
                # Usar o método take_whip_damage do boss
                if boss.take_whip_damage(2):  # Chicote causa 2 de dano
                    # Marcar que já causou dano
                    self.current_whip_attack.damage_dealt.append(boss_id)
                    self.current_whip_attack.screen_shake = 15
                    return True

        return False

    def draw(self, screen):
        if self.current_whip_attack and self.current_whip_attack.active:
            self.current_whip_attack.draw(screen, self.whip_sprites)

    def draw_ui(self, screen, fonts):
        if self.combo_counter > 1:
            combo_color = (
                (255, 100, 100) if self.combo_counter >= 5 else (255, 200, 100)
            )
            combo_text = self.language_manager.get_text("combo").format(
                self.combo_counter
            )
            combo_surf = fonts["medium"].render(combo_text, False, combo_color)
            combo_rect = combo_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))

            shadow_surf = fonts["medium"].render(combo_text, False, (0, 0, 0))
            shadow_rect = shadow_surf.get_rect(center=(SCREEN_WIDTH // 2 + 2, 102))

            screen.blit(shadow_surf, shadow_rect)
            screen.blit(combo_surf, combo_rect)


class KnifeProjectile:
    def __init__(self, x, y, knife_sprite=None):
        self.x = x
        self.y = y
        self.speed = 10
        self.width = 25
        self.height = 8
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.active = True
        self.rotation = 0
        self.rotation_speed = 15
        self.knife_sprite = knife_sprite
        self.original_sprite = knife_sprite

    def update(self):
        self.x += self.speed
        self.rect.x = self.x

        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation = 0

        if self.x > SCREEN_WIDTH + 50:
            self.active = False

    def draw(self, screen):
        if self.knife_sprite and self.original_sprite:
            sprite_rect = self.original_sprite.get_rect(
                center=(self.x + self.width // 2, self.y + self.height // 2)
            )
            screen.blit(self.original_sprite, sprite_rect)


class DraculaBattle:
    def __init__(
        self,
        screen_width,
        screen_height,
        language_manager,
        fireball_sprite=None,
        resource_manager=None,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = True
        self.scroll_locked = True
        self.language_manager = language_manager

        if resource_manager and "fireball" in resource_manager.sprites:
            self.fireball_sprite = resource_manager.sprites["fireball"]
        else:
            self.fireball_sprite = None

        # Battle phases
        self.phase = "entrance"
        self.entrance_timer = 0
        self.defeat_timer = 0

        self.fireball_sprite = fireball_sprite

        # Boss stats
        self.max_hp = 25
        self.boss_hp = self.max_hp
        self.boss_rect = pygame.Rect(600, 130, 90, 200)

        # Animation states
        self.current_sprite = "idle"  # "idle" or "attack"
        self.attack_animation_timer = 0
        self.sprite_timer = 0

        # Combat system
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.attack_interval = 90
        self.fireballs = []

        # Effects
        self.invulnerable_timer = 0
        self.screen_shake = 0
        self.flash_timer = 0

        # Position for entrance
        self.boss_rect.x = self.screen_width + 100
        self.target_x = 580

    def update(self, player_rect, player_projectiles):
        if not self.active:
            return False

        # Update timers
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
        if self.screen_shake > 0:
            self.screen_shake -= 1
        if self.flash_timer > 0:
            self.flash_timer -= 1

        # Update sprite animation
        self.update_sprite_animation()

        # Phase management
        if self.phase == "entrance":
            self.update_entrance()
        elif self.phase == "fighting":
            self.update_fighting(player_rect, player_projectiles)
        elif self.phase == "defeat":
            self.update_defeat()

        # Update fireballs
        self.update_fireballs()

        return self.active

    def update_sprite_animation(self):
        self.sprite_timer += 1

        # Handle attack animation
        if self.current_sprite == "attack":
            self.attack_animation_timer += 1
            if self.attack_animation_timer >= 60:  # Attack animation lasts 1 second
                self.current_sprite = "idle"
                self.attack_animation_timer = 0

    def update_entrance(self):
        if self.boss_rect.x > self.target_x:
            self.boss_rect.x -= 3
        else:
            self.boss_rect.x = self.target_x
            self.entrance_timer += 1

        if self.entrance_timer > 60:
            self.phase = "fighting"
            self.screen_shake = 20

    def take_whip_damage(self, damage=2):
        if self.invulnerable_timer > 0:
            return False

        self.boss_hp -= damage
        self.invulnerable_timer = 30  # Invulnerabilidade mais longa para chicote
        self.flash_timer = 20  # Flash mais longo
        self.screen_shake = 25  # Shake mais intenso

        # Efeito especial para chicote
        if self.boss_hp <= self.max_hp // 2:
            self.attack_interval = max(40, self.attack_interval - 3)

        return True

    def update_fighting(self, player_rect, player_projectiles):
        self.attack_timer += 1

        # Attack pattern
        if self.attack_cooldown <= 0:
            self.start_fireball_attack()
            self.attack_cooldown = self.attack_interval

        # Check for damage from player projectiles
        self.check_projectile_damage(player_projectiles)

        # Check if defeated
        if self.boss_hp <= 0:
            self.phase = "defeat"
            self.defeat_timer = 0

    def start_fireball_attack(self):
        # Change to attack sprite
        self.current_sprite = "attack"
        self.attack_animation_timer = 0

        # Create fireball after short delay
        fireball = {
            "x": self.boss_rect.x - 20,
            "y": self.boss_rect.centery,
            "speed_x": -5,
            "speed_y": randint(-2, 2),
            "lifetime": 120,
        }
        self.fireballs.append(fireball)

    def check_projectile_damage(self, player_projectiles):
        if self.invulnerable_timer > 0:
            return

        for projectile in player_projectiles:
            if projectile.active and self.boss_rect.colliderect(projectile.rect):
                self.boss_hp -= 1
                self.invulnerable_timer = 20
                self.flash_timer = 15
                self.screen_shake = 15

                projectile.active = False

                # Increase attack speed as HP decreases
                if self.boss_hp <= self.max_hp // 2:
                    self.attack_interval = max(50, self.attack_interval - 5)

                break

    def update_fireballs(self):
        active_fireballs = []
        for fireball in self.fireballs:
            fireball["x"] += fireball["speed_x"]
            fireball["y"] += fireball["speed_y"]
            fireball["lifetime"] -= 1

            if fireball["lifetime"] > 0 and fireball["x"] > -50:
                active_fireballs.append(fireball)

        self.fireballs = active_fireballs

    def update_defeat(self):
        self.defeat_timer += 1

        if self.defeat_timer % 10 == 0:
            self.flash_timer = 8
            self.screen_shake = 10

        if self.defeat_timer >= 90:
            self.active = False
            return False

    def check_player_damage(self, player_rect):
        if self.phase != "fighting":
            return False

        # Check fireball collision
        for fireball in self.fireballs:
            fireball_rect = pygame.Rect(fireball["x"] - 15, fireball["y"] - 15, 30, 30)
            if player_rect.colliderect(fireball_rect):
                return True

        return False

    def draw(self, screen, dracula_sprites=None):

        shake_x = (
            randint(-self.screen_shake // 2, self.screen_shake // 2)
            if self.screen_shake > 0
            else 0
        )
        shake_y = (
            randint(-self.screen_shake // 2, self.screen_shake // 2)
            if self.screen_shake > 0
            else 0
        )

        # Draw fireballs
        for fireball in self.fireballs:
            fireball_x = int(fireball["x"] + shake_x)
            fireball_y = int(fireball["y"] + shake_y)
            if self.fireball_sprite:
                # Use o sprite da bola de fogo
                fireball_rect = self.fireball_sprite.get_rect(
                    center=(fireball_x, fireball_y)
                )
                screen.blit(self.fireball_sprite, fireball_rect)
            else:
                # Fallback para os círculos antigos
                pygame.draw.circle(screen, (255, 100, 0), (fireball_x, fireball_y), 12)
                pygame.draw.circle(screen, (255, 200, 100), (fireball_x, fireball_y), 6)

        # Draw Dracula
        boss_color = (220, 0, 100)  # Dark purple for Dracula
        if self.flash_timer > 0:
            boss_color = (255, 255, 255)

        # Use sprite if available, otherwise draw rectangle
        if dracula_sprites and self.current_sprite in dracula_sprites:
            boss_surface = dracula_sprites[self.current_sprite]
            if self.flash_timer > 0:
                flash_surface = boss_surface.copy()
                flash_surface.fill((255, 255, 255), special_flags=pygame.BLEND_ADD)
                screen.blit(
                    flash_surface,
                    (self.boss_rect.x + shake_x, self.boss_rect.y + shake_y),
                )
            else:
                screen.blit(
                    boss_surface,
                    (self.boss_rect.x + shake_x, self.boss_rect.y + shake_y),
                )
        else:
            pygame.draw.rect(
                screen,
                boss_color,
                (
                    self.boss_rect.x + shake_x,
                    self.boss_rect.y + shake_y,
                    self.boss_rect.width,
                    self.boss_rect.height,
                ),
            )

        # Draw health bar
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 300
        bar_height = 25
        bar_x = (self.screen_width - bar_width) // 2
        bar_y = 40

        pygame.draw.rect(
            screen, (50, 50, 50), (bar_x - 3, bar_y - 3, bar_width + 6, bar_height + 6)
        )

        current_width = int((self.boss_hp / self.max_hp) * bar_width)

        if self.boss_hp > self.max_hp * 0.6:
            health_color = (200, 0, 0)
        elif self.boss_hp > self.max_hp * 0.3:
            health_color = (255, 150, 0)
        else:
            health_color = (255, 50, 50)

        pygame.draw.rect(
            screen, health_color, (bar_x, bar_y, current_width, bar_height)
        )

        font = pygame.font.Font(None, 24)
        hp_text = self.language_manager.get_text("boss_hp").format(
            self.boss_hp, self.max_hp
        )
        hp_surface = font.render(hp_text, True, WHITE)
        hp_rect = hp_surface.get_rect(
            center=(self.screen_width // 2, bar_y + bar_height // 2)
        )
        screen.blit(hp_surface, hp_rect)

        font_title = pygame.font.Font(None, 32)
        boss_name = self.language_manager.get_text("dracula_boss_name")
        text = font_title.render(boss_name, True, WHITE)
        text_rect = text.get_rect(center=(self.screen_width // 2, bar_y - 20))
        screen.blit(text, text_rect)


class BossManager:
    def __init__(self, language_manager):
        self.current_boss = None
        self.boss_defeated = False
        self.boss_victory_timer = 0
        self.boss_reward_given = False
        self.language_manager = language_manager
        self.fireball_sprite = None

    def reset_boss_state(self):
        """Reset completo do estado do boss"""
        self.current_boss = None
        self.boss_victory_timer = 0
        self.boss_reward_given = False

    def set_fireball_sprite(self, sprite):
        self.fireball_sprite = sprite

    def should_trigger_boss(self, current_score):
        return (
            current_score >= BOSS_TRIGGER
            and not self.boss_defeated
            and self.current_boss is None
        )

    def start_boss_battle(self):
        self.current_boss = DraculaBattle(
            SCREEN_WIDTH, SCREEN_HEIGHT, self.language_manager, self.fireball_sprite
        )
        self.boss_reward_given = False
        return True

    def update(self, player_rect, player_projectiles):
        if self.current_boss and self.current_boss.active:
            still_active = self.current_boss.update(player_rect, player_projectiles)

            if not still_active and not self.boss_reward_given:
                self.boss_defeated = True
                self.boss_victory_timer = 300  # 5 segundos
                self.boss_reward_given = True
                return "boss_defeated"

        # Se o boss foi derrotado, contar o timer de vitória
        if self.boss_victory_timer > 0:
            self.boss_victory_timer -= 1
            if self.boss_victory_timer <= 0:
                # Boss completamente derrotado - limpar tudo
                self.current_boss = None
                return "boss_complete"
            # Ainda no timer de vitória
            return "boss_victory_timer"

        return "active" if self.current_boss else "none"

    def check_player_damage(self, player_rect):
        if (
            self.current_boss
            and self.current_boss.active
            and self.current_boss.phase == "fighting"
        ):
            return self.current_boss.check_player_damage(player_rect)
        return False

    def is_boss_active(self):
        return (
            self.current_boss is not None
            and self.current_boss.active
            and self.current_boss.phase in ["entrance", "fighting"]
        )

    def draw(self, screen, boss_sprites=None):
        if self.current_boss and self.current_boss.active:
            self.current_boss.draw(screen, boss_sprites)

        if self.boss_victory_timer > 0:
            font = pygame.font.Font(None, 48)
            victory_text = font.render(
                self.language_manager.get_text("boss_defeated"), True, GOLD
            )
            victory_rect = victory_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )

            shadow_text = font.render(
                self.language_manager.get_text("boss_defeated"), True, BLACK
            )
            shadow_rect = shadow_text.get_rect(
                center=(SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT // 2 + 2)
            )

            screen.blit(shadow_text, shadow_rect)
            screen.blit(victory_text, victory_rect)

    def reset_for_new_game(self):
        """Reset completo para nova partida"""
        self.current_boss = None
        self.boss_defeated = False
        self.boss_victory_timer = 0
        self.boss_reward_given = False


class LanguageManager:
    def __init__(self):
        self.current_language = "pt"
        self.colorblind_mode = "normal"  # NOVO
        self.load_settings()

    def load_settings(self):
        try:
            if os.path.exists("language_settings.json"):
                with open("language_settings.json", "r") as f:
                    data = json.load(f)
                    self.current_language = data.get("language", "pt")
                    self.colorblind_mode = data.get("colorblind_mode", "normal")  # NOVO
        except:
            pass

    def save_settings(self):
        try:
            data = {
                "language": self.current_language,
                "colorblind_mode": self.colorblind_mode,  # NOVO
            }
            with open("language_settings.json", "w") as f:
                json.dump(data, f)
        except:
            pass

    def set_language(self, language):
        if language in TEXTS:
            self.current_language = language
            self.save_settings()

    # NOVO: Método para mudar modo de daltonismo
    def set_colorblind_mode(self, mode):
        if mode in COLORBLIND_TYPES:
            self.colorblind_mode = mode
            self.save_settings()

    # NOVO: Método para obter nome do modo atual
    def get_colorblind_mode_name(self):
        return COLORBLIND_TYPES[self.colorblind_mode][self.current_language]

    def get_text(self, key):
        return TEXTS.get(self.current_language, TEXTS["pt"]).get(key, key)

    def get_phase_name(self, phase_index):
        if 0 <= phase_index < len(PHASE_NAMES[self.current_language]):
            return PHASE_NAMES[self.current_language][phase_index]
        return "Unknown Phase"


class HighscoreManager:
    def __init__(self, filename="highscore.json"):
        self.filename = filename
        self.highscore = self.load()

    def load(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    return data.get("highscore", 0)
        except:
            pass
        return 0

    def save(self, score):
        try:
            data = {"highscore": score}
            with open(self.filename, "w") as f:
                json.dump(data, f)
            self.highscore = score
        except:
            pass

    def is_new_record(self, score):
        return score > self.highscore

    def update_if_record(self, score):
        if self.is_new_record(score):
            self.save(score)
            return True
        return False

    def reset(self):
        self.save(0)


class ResourceManager:
    def __init__(self):
        self.sprites = {}
        self.sounds = {}
        self.fonts = {}

    def load_sprite(self, name, path, scale=1.0):
        try:
            sprite = pygame.image.load(path).convert_alpha()
            if scale != 1.0:
                new_size = (
                    int(sprite.get_width() * scale),
                    int(sprite.get_height() * scale),
                )
                sprite = pygame.transform.scale(sprite, new_size)
            self.sprites[name] = sprite
            return sprite
        except:
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((255, 0, 255))
            self.sprites[name] = placeholder
            return placeholder

    def load_sound(self, name, path, volume=1.0):
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            self.sounds[name] = sound
            return sound
        except:
            return None

    def load_font(self, name, path, size):
        try:
            font = pygame.font.Font(path, size)
            self.fonts[name] = font
            return font
        except:
            return pygame.font.Font(None, size)


class AnimationManager:
    def __init__(self):
        self.animations = {}
        self.current_frames = {}

    def add_animation(self, name, frames):
        self.animations[name] = frames
        self.current_frames[name] = 0

    def update(self, name, speed=0.1):
        if name in self.animations:
            self.current_frames[name] += speed
            if self.current_frames[name] >= len(self.animations[name]):
                self.current_frames[name] = 0
            return self.animations[name][int(self.current_frames[name])]
        return None

    def get_current_frame(self, name):
        if name in self.animations:
            return self.animations[name][int(self.current_frames[name])]
        return None


class PhaseManager:
    def __init__(self, language_manager):
        self.current_phase = 0
        self.previous_phase = -1
        self.phase_change_timer = 0
        self.show_phase_notification = False
        self.language_manager = language_manager

    def get_current_phase(self, score):
        for i in range(len(PHASE_THRESHOLDS) - 1, -1, -1):
            if score >= PHASE_THRESHOLDS[i]:
                return i
        return 0

    def update_phase(self, score):
        new_phase = self.get_current_phase(score)
        if new_phase != self.current_phase:
            self.previous_phase = self.current_phase
            self.current_phase = new_phase
            self.show_phase_notification = True
            self.phase_change_timer = 0
            return True
        return False

    def update_notification_timer(self):
        if self.show_phase_notification:
            self.phase_change_timer += 1
            if self.phase_change_timer > 180:
                self.show_phase_notification = False

    def get_phase_name(self, phase_index=None):
        if phase_index is None:
            phase_index = self.current_phase
        return self.language_manager.get_phase_name(phase_index)

    def get_background_name(self, phase_index=None):
        if phase_index is None:
            phase_index = self.current_phase
        return f"background_phase_{phase_index}"


class BloodLostGame:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("BloodLost - Dracula Boss Battle")
        self.clock = pygame.time.Clock()

        self.language_manager = LanguageManager()
        self.resource_manager = ResourceManager()
        self.animation_manager = AnimationManager()
        self.highscore_manager = HighscoreManager()
        self.phase_manager = PhaseManager(self.language_manager)
        self.boss_manager = BossManager(self.language_manager)
        # CORREÇÃO: LifeManager será criado DEPOIS de carregar os recursos
        self.life_manager = None

        self.player_animation_state = PlayerAnimationState()
        self.player_animation_state.victory_auto_return = 300

        self.game_state = "menu"
        self.game_active = False
        self.victory_triggered = False

        self.score = 0
        self.score_boss = 0
        self.start_time = 0
        self.bg_x_pos = 0
        self.new_record_timer = 0

        self.loading_screen_active = False
        self.loading_timer = 0
        self.loading_duration = 1800

        self.player_gravity = 0
        self.enemies_jumped = 0
        self.enemies_killed = 0

        self.last_move_direction = "right"

        self.player_projectiles = []
        self.shoot_cooldown = 0

        self.attack_system = PlayerAttackSystem(self.language_manager)

        self.player_invulnerable_timer = 0
        self.player_damaged = False

        self.selected_option = 0
        self.selected_setting = 0
        self.volume = 0.7

        self.obstacle_list = []

        self.music_playing = False
        self.game_over_music_playing = False
        self.main_menu_playing = True
        self.boss_music_playing = False

        self.load_resources()
        
        # CORREÇÃO: Criar LifeManager APÓS carregar os recursos
        self.life_manager = LifeManager(self.resource_manager, self.language_manager)
        
        self.setup_timers()
        self.setup_player()

    def load_resources(self):
        rm = self.resource_manager

        # NOVO: Mapeamento de backgrounds por tipo de daltonismo
        self.background_mappings = {
            "normal": [
                "sprites\\Background\\Cenario 1.png",
                "sprites\\Background\\Cenario 2.png",
                "sprites\\Background\\Cenario 3.png",
                "sprites\\Background\\Cenario 4.png",
                "sprites\\Background\\Cenario 5.png",
            ],
            "protanomalia": [
                "sprites\\Background\\protanomalia.png",
                "sprites\\Background\\protanomalia2.png",
                "sprites\\Background\\protanomalia3.png",
                "sprites\\Background\\protanomalia4.png",
                "sprites\\Background\\protanomalia5.png",
            ],
            "deuteranomalia": [
                "sprites\\Background\\deuteranomalia.png",
                "sprites\\Background\\deuteranomalia2.png",
                "sprites\\Background\\deuteranomalia3.png",
                "sprites\\Background\\deuteranomalia4.png",
                "sprites\\Background\\deuteranomalia5.png",
            ],
            "tritanomalia": [
                "sprites\\Background\\tritanomalia.png",
                "sprites\\Background\\tritanomalia2.png",
                "sprites\\Background\\tritanomalia3.png",
                "sprites\\Background\\tritanomalia4.png",
                "sprites\\Background\\tritanomalia5.png",
            ],
        }

        # Carregar todos os backgrounds de todos os tipos
        for colorblind_type, paths in self.background_mappings.items():
            for i, path in enumerate(paths):
                background_name = f"background_{colorblind_type}_phase_{i}"
                try:
                    sprite = pygame.image.load(path).convert_alpha()
                    sprite = pygame.transform.scale(
                        sprite,
                        (
                            int(sprite.get_width() * SCALE_FACTOR),
                            int(sprite.get_height() * SCALE_FACTOR),
                        ),
                    )
                    rm.sprites[background_name] = sprite
                except Exception as e:
                    print(f"✗ Erro ao carregar {path}: {e}")
                    fallback_normal = f"background_normal_phase_{i}"
                    if fallback_normal in rm.sprites:
                        rm.sprites[background_name] = rm.sprites[fallback_normal]
                        print(f"  → Usando fallback: {fallback_normal}")
                    elif i > 0:
                        fallback_phase0 = f"background_{colorblind_type}_phase_0"
                        if fallback_phase0 in rm.sprites:
                            rm.sprites[background_name] = rm.sprites[fallback_phase0]
                            print(f"  → Usando fallback: {fallback_phase0}")

        # Carregar menu e game over backgrounds
        rm.load_sprite("menu_bg", "sprites\\Background\\loading.webp", SCALE_FACTOR)

        try:
            gameover_img = pygame.image.load(
                "sprites\\Background\\gameover.png"
            ).convert_alpha()
            gameover_img = pygame.transform.scale(
                gameover_img, (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            rm.sprites["gameover_bg"] = gameover_img
        except:
            fallback_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fallback_surface.fill((50, 20, 50))
            rm.sprites["gameover_bg"] = fallback_surface

        # Carregar sprites do player (não mudam com daltonismo)
        rm.load_sprite("player_idle", "sprites\\Player\\walk1.png", HERO_SCALE)
        rm.load_sprite("player_walk1", "sprites\\Player\\walk1.png", HERO_SCALE)
        rm.load_sprite("player_walk2", "sprites\\Player\\wal2.png", HERO_SCALE)
        rm.load_sprite("player_walk3", "sprites\\Player\\walk3.png", HERO_SCALE)
        rm.load_sprite("player_jump", "sprites\\Player\\jump.png", HERO_SCALE)
        rm.load_sprite("player_attack1", "sprites\\Player\\attack1.png", HERO_SCALE)
        rm.load_sprite("player_attack2", "sprites\\Player\\attack2.png", HERO_SCALE)
        rm.load_sprite("player_attack3", "sprites\\Player\\attack3.png", HERO_SCALE)

        # NOVO: Mapeamento de sprites do Drácula por tipo de daltonismo
        self.dracula_mappings = {
            "normal": {
                "idle": "sprites\\Dracula\\draculaIdle.png",
                "attack": "sprites\\Dracula\\draculaAttack.png",
                "fireball": "sprites\\Dracula\\foguinho.png",
            },
            "protanomalia": {
                "idle": "sprites\\Dracula\\draculaIdleProtanomaly.png",
                "attack": "sprites\\Dracula\\draculaAttackProtanomaly.png",
                "fireball": "sprites\\Dracula\\foguinho.png",
            },
            "deuteranomalia": {
                "idle": "sprites\\Dracula\\draculaIdleProtanomaly.png",
                "attack": "sprites\\Dracula\\draculaAttackProtanomaly.png",
                "fireball": "sprites\\Dracula\\foguinho.png",
            },
            "tritanomalia": {
                "idle": "sprites\\Dracula\\draculaIdle.png",
                "attack": "sprites\\Dracula\\draculaAttack.png",
                "fireball": "sprites\\Dracula\\foguinho.png",
            },
        }

        # Carregar sprites do Drácula para todos os modos
        self.dracula_sprites_all = {}
        for colorblind_type, sprites in self.dracula_mappings.items():
            self.dracula_sprites_all[colorblind_type] = {}

            for sprite_type, path in sprites.items():
                sprite_name = f"dracula_{sprite_type}_{colorblind_type}"
                try:
                    if sprite_type == "fireball":
                        sprite = rm.load_sprite(sprite_name, path, 1.5)
                    else:
                        sprite = rm.load_sprite(sprite_name, path, 3.0)
                    self.dracula_sprites_all[colorblind_type][sprite_type] = sprite
                except Exception as e:
                    print(f"✗ Erro ao carregar sprite do Drácula {path}: {e}")
                    # Fallback para o sprite normal
                    fallback_name = f"dracula_{sprite_type}_normal"
                    if fallback_name in rm.sprites:
                        self.dracula_sprites_all[colorblind_type][sprite_type] = (
                            rm.sprites[fallback_name]
                        )
                    else:
                        # Criar placeholder
                        if sprite_type == "fireball":
                            placeholder = pygame.Surface((30, 30))
                            placeholder.fill((255, 100, 0))
                        else:
                            placeholder = pygame.Surface((90, 120))
                            placeholder.fill((150, 0, 100))
                        self.dracula_sprites_all[colorblind_type][
                            sprite_type
                        ] = placeholder

        # Inicializar sprites do Drácula com o modo atual
        self.update_dracula_sprites()

        self.attack_system.load_whip_sprites(rm)

        # NOVO: Mapeamento de inimigos por tipo de daltonismo
        self.enemy_mappings = {
            "normal": {
                "bat": [
                    "sprites\\Bat\\bat.png",
                    "sprites\\Bat\\batWalk.png",
                    "sprites\\Bat\\batWalk1.png",
                ],
                "zombie": [
                    "sprites\\Zombie\\Enemie3Idle.png",
                    "sprites\\Zombie\\Enemie3Walk.png",
                ],
                "knight": [
                    "sprites\\Knight\\Enemie1Idle.png",
                    "sprites\\Knight\\Enemie1Walk1.png",
                    "sprites\\Knight\\Enemie1Walk2.png",
                ],
                "owl": [
                    "sprites\\Owl\\Enemie2Idle.png",
                    "sprites\\Owl\\Enemie2Walk.png",
                ],
                "bat1": [
                    "sprites\\Bat2\\Enemie6Idle.png",
                    "sprites\\Bat2\\Enemie6Walk.png",
                    "sprites\\Bat2\\Enemie6Walk2.png",
                ],
                "panther": [
                    "sprites\\Panther\\Enemie4Idle.png",
                    "sprites\\Panther\\Enemie4Walk.png",
                    "sprites\\Panther\\Enemie4Walk1.png",
                    "sprites\\Panther\\Enemie4Walk2.png",
                ],
            },
            "protanomalia": {
                "bat": [
                    "sprites\\Bat\\batDeuteranomaly.png",
                    "sprites\\Bat\\batWalkDeuteranomaly.png",
                    "sprites\\Bat\\batWalk1Deuteranomaly.png",
                ],
                "zombie": [
                    "sprites\\Zombie\\Enemie3Idle.png",
                    "sprites\\Zombie\\Enemie3Walk.png",
                ],
                "knight": [
                    "sprites\\Knight\\Enemie1Idle.png",
                    "sprites\\Knight\\Enemie1Walk1.png",
                    "sprites\\Knight\\Enemie1Walk2.png",
                ],
                "owl": [
                    "sprites\\Owl\\Enemie2Idle.png",
                    "sprites\\Owl\\Enemie2Walk.png",
                ],
                "bat1": [
                    "sprites\\Bat2\\Enemie6Idle.png",
                    "sprites\\Bat2\\Enemie6Walk.png",
                    "sprites\\Bat2\\Enemie6Walk2.png",
                ],
                "panther": [
                    "sprites\\Panther\\Enemie4IdleProtanomaly.png",
                    "sprites\\Panther\\Enemie4WalkProtanomaly.png",
                    "sprites\\Panther\\Enemie4Walk1Protanomaly.png",
                    "sprites\\Panther\\Enemie4Walk2Protanomaly.png",
                ],
            },
            "deuteranomalia": {
                "bat": [
                    "sprites\\Bat\\batDeuteranomaly.png",
                    "sprites\\Bat\\batWalkDeuteranomaly.png",
                    "sprites\\Bat\\batWalk1Deuteranomaly.png",
                ],
                "zombie": [
                    "sprites\\Zombie\\Enemie3Idle.png",
                    "sprites\\Zombie\\Enemie3Walk.png",
                ],
                "knight": [
                    "sprites\\Knight\\Enemie1Idle.png",
                    "sprites\\Knight\\Enemie1Walk1.png",
                    "sprites\\Knight\\Enemie1Walk2.png",
                ],
                "owl": [
                    "sprites\\Owl\\Enemie2Idle.png",
                    "sprites\\Owl\\Enemie2Walk.png",
                ],
                "bat1": [
                    "sprites\\Bat2\\Enemie6Idle.png",
                    "sprites\\Bat2\\Enemie6Walk.png",
                    "sprites\\Bat2\\Enemie6Walk2.png",
                ],
                "panther": [
                    "sprites\\Panther\\Enemie4IdleProtanomaly.png",
                    "sprites\\Panther\\Enemie4WalkProtanomaly.png",
                    "sprites\\Panther\\Enemie4Walk1Protanomaly.png",
                    "sprites\\Panther\\Enemie4Walk2Protanomaly.png",
                ],
            },
            "tritanomalia": {
                "bat": [
                    "sprites\\Bat\\bat.png",
                    "sprites\\Bat\\batWalk.png",
                    "sprites\\Bat\\batWalk1.png",
                ],
                "zombie": [
                    "sprites\\Zombie\\Enemie3IdleTritanopia.png",
                    "sprites\\Zombie\\Enemie3WalkTritanopia.png",
                ],
                "knight": [
                    "sprites\\Knight\\Enemie1IdleTritanopia.png",
                    "sprites\\Knight\\Enemie1Walk1Tritanopia.png",
                    "sprites\\Knight\\Enemie1Walk2Tritanopia.png",
                ],
                "owl": [
                    "sprites\\Owl\\Enemie2IdleTritanopia.png",
                    "sprites\\Owl\\Enemie2WalkTritanopia.png",
                ],
                "bat1": [
                    "sprites\\Bat2\\Enemie6IdleTritanomaly.png",
                    "sprites\\Bat2\\Enemie6WalkTritanomaly.png",
                    "sprites\\Bat2\\Enemie6Walk2Tritanomaly.png",
                ],
                "panther": [
                    "sprites\\Panther\\Enemie4Idle.png",
                    "sprites\\Panther\\Enemie4Walk.png",
                    "sprites\\Panther\\Enemie4Walk1.png",
                    "sprites\\Panther\\Enemie4Walk2.png",
                ],
            },
        }

        # Carregar todos os sprites de inimigos para todos os modos
        for colorblind_type, enemies in self.enemy_mappings.items():
            for enemy_name, sprite_paths in enemies.items():
                frames = []
                for i, path in enumerate(sprite_paths):
                    sprite_name = f"{enemy_name}_{colorblind_type}_{i}"
                    try:
                        sprite = rm.load_sprite(sprite_name, path, ENEMY_SCALE)
                        frames.append(sprite)
                    except Exception as e:
                        # Fallback para o sprite normal
                        fallback_name = f"{enemy_name}_normal_{i}"
                        if fallback_name in rm.sprites:
                            frames.append(rm.sprites[fallback_name])
                        else:
                            # Criar placeholder
                            placeholder = pygame.Surface((50, 50))
                            placeholder.fill((255, 0, 255))
                            frames.append(placeholder)

                # Adicionar animação
                animation_name = f"{enemy_name}_{colorblind_type}"
                self.animation_manager.add_animation(animation_name, frames)

        # Player animations
        player_walk_frames = [
            rm.sprites["player_walk1"],
            rm.sprites["player_walk2"],
            rm.sprites["player_walk3"],
            rm.sprites["player_walk2"],
        ]
        self.animation_manager.add_animation("player_walk", player_walk_frames)

        player_attack_frames = [
            rm.sprites["player_attack1"],
            rm.sprites["player_attack2"],
            rm.sprites["player_attack3"],
        ]
        self.animation_manager.add_animation("player_attack", player_attack_frames)

        # NOVO: Mapeamento do item de vida por tipo de daltonismo
        self.life_item_mappings = {
            "normal": "sprites\\Item\\life.png",
            "protanomalia": "sprites\\Item\\lifeDeuteranomaly.png",
            "deuteranomalia": "sprites\\Item\\lifeDeuteranomaly.png",
            "tritanomalia": "sprites\\Item\\life.png",
        }

        # Carregar sprites de vida para todos os modos
        for colorblind_type, path in self.life_item_mappings.items():
            sprite_name = f"heart_{colorblind_type}"
            try:
                rm.load_sprite(sprite_name, path, 2.0)
            except:
                # Fallback para o sprite normal
                if "heart_normal" in rm.sprites:
                    rm.sprites[sprite_name] = rm.sprites["heart_normal"]

        # Load sounds
        rm.load_sound("bg_music", "music\\Marble Gallery.mp3", self.volume)
        rm.load_sound(
            "game_over", "music\\game-over-deep-male-voice-clip-352695.mp3", self.volume
        )
        rm.load_sound("menu_music", "music\\main-menu.mp3", self.volume)
        rm.load_sound("boss_music", "music\\Prologue.mp3", self.volume)
        rm.load_sound("loading_music", "music\\Loading.mp3", self.volume)

        rm.load_sound("whip_attack", "music\\whip.mp3", self.volume * 0.7)
        rm.load_sound("whip_hit", "music\\whipHit.mp3", self.volume * 0.6)

        # Load fonts
        rm.load_font("title", "fonts\\Pixeltype.ttf", 80)
        rm.load_font("large", "fonts\\Pixeltype.ttf", 50)
        rm.load_font("medium", "fonts\\Pixeltype.ttf", 40)
        rm.load_font("small", "fonts\\Pixeltype.ttf", 25)

        # Load knife sprite
        rm.load_sprite("knife", "sprites\\Item\\faquinha2.png", 1.5)
        rm.load_sound("shoot", "music\\knife.mp3", self.volume * 0.5)

    def setup_timers(self):
        self.obstacle_timer = pygame.USEREVENT + 1
        self.enemy_animation_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.obstacle_timer, 1500)
        pygame.time.set_timer(self.enemy_animation_timer, 150)

    def setup_player(self):
        self.player_rect = self.resource_manager.sprites["player_idle"].get_rect(
            topleft=(PLAYER_START_X, PLAYER_START_Y)
        )
        self.current_player_surface = self.resource_manager.sprites["player_idle"]

    def update_volume(self):
        for sound in self.resource_manager.sounds.values():
            if sound:
                sound.set_volume(self.volume)

    def get_enemy_animation_name(self, enemy_type):
        colorblind_mode = self.language_manager.colorblind_mode
        return f"{enemy_type}_{colorblind_mode}"

    def update_dracula_sprites(self):
        """Atualiza os sprites do Drácula baseado no modo de daltonismo atual"""
        colorblind_mode = self.language_manager.colorblind_mode

        if colorblind_mode in self.dracula_sprites_all:
            self.dracula_sprites = self.dracula_sprites_all[colorblind_mode]

            # Atualizar sprite da bola de fogo no boss manager
            if "fireball" in self.dracula_sprites:
                self.boss_manager.set_fireball_sprite(self.dracula_sprites["fireball"])
        else:
            # Fallback para normal
            self.dracula_sprites = self.dracula_sprites_all.get("normal", {})
            if "fireball" in self.dracula_sprites:
                self.boss_manager.set_fireball_sprite(self.dracula_sprites["fireball"])

    def create_obstacle(self):
        if self.boss_manager.is_boss_active():
            return

        enemy_types = [
            {"type": "bat", "y": 255},
            {"type": "zombie", "y": 248},
            {"type": "knight", "y": 250},
            {"type": "owl", "y": 150},
            {"type": "bat1", "y": 255},
            {"type": "panther", "y": 270},
        ]

        chosen_enemy = choice(enemy_types)

        # MODIFICADO: Usar animação baseada no modo de daltonismo
        animation_name = self.get_enemy_animation_name(chosen_enemy["type"])
        current_frame = self.animation_manager.get_current_frame(animation_name)

        if current_frame:
            obstacle_rect = current_frame.get_rect(
                topleft=(randint(700, 1100), chosen_enemy["y"])
            )
            obstacle_data = {
                "rect": obstacle_rect,
                "type": chosen_enemy["type"],  # Manter o tipo base
                "animation_name": animation_name,  # NOVO: Nome da animação específica
                "surface": current_frame,
            }
            self.obstacle_list.append(obstacle_data)

    def update_obstacles(self):
        if self.boss_manager.is_boss_active():
            self.obstacle_list.clear()
            return

        updated_obstacles = []
        for obstacle in self.obstacle_list:
            obstacle["rect"].x -= 5

            # MODIFICADO: Usar o animation_name específico
            animation_name = obstacle.get(
                "animation_name", self.get_enemy_animation_name(obstacle["type"])
            )
            obstacle["surface"] = self.animation_manager.get_current_frame(
                animation_name
            )

            self.screen.blit(obstacle["surface"], obstacle["rect"])

            if obstacle["rect"].x > -100:
                updated_obstacles.append(obstacle)

        self.obstacle_list = updated_obstacles

    def check_collisions(self):
        """Método modificado para usar o sistema de vidas"""
        if self.boss_manager.is_boss_active():
            return True, 0

        jumped_enemies = 0
        enemies_to_remove = []

        for i, obstacle in enumerate(self.obstacle_list):
            if self.player_rect.colliderect(obstacle["rect"]):
                if (
                    self.player_gravity > 0
                    and self.player_rect.bottom <= obstacle["rect"].centery + 10
                    and self.player_rect.centery < obstacle["rect"].centery
                ):
                    jumped_enemies += 1
                    enemies_to_remove.append(i)
                    self.player_gravity = min(self.player_gravity, -2)
                else:
                    # Colisão lateral - verificar se pode tomar dano
                    if self.player_invulnerable_timer <= 0:
                        # Remove o inimigo que causou dano
                        enemies_to_remove.append(i)

                        # Tomar dano
                        still_alive = self.life_manager.take_damage()
                        self.player_invulnerable_timer = (
                            120  # 2 segundos de invulnerabilidade
                        )

                        if not still_alive:
                            # Game Over
                            return False, jumped_enemies
                        # Se ainda tem vidas, continua o jogo mas com invulnerabilidade

        # Remover inimigos pulados ou que causaram dano
        for i in reversed(enemies_to_remove):
            if i < len(self.obstacle_list):
                self.obstacle_list.pop(i)

        return True, jumped_enemies

    def update_player_animation(self):
        is_attacking = self.attack_system.is_attacking()
        is_jumping = self.player_rect.bottom < GROUND_Y

        self.player_animation_state.update_state(is_attacking, is_jumping)

        current_state = self.player_animation_state.get_current_state()

        if current_state == "attacking" and is_attacking:
            attack_frame = self.attack_system.get_attack_frame()
            if attack_frame == 0:
                self.current_player_surface = self.resource_manager.sprites[
                    "player_attack1"
                ]
            elif attack_frame == 1:
                self.current_player_surface = self.resource_manager.sprites[
                    "player_attack2"
                ]
            else:
                self.current_player_surface = self.resource_manager.sprites[
                    "player_attack3"
                ]

        elif current_state == "jumping":
            self.current_player_surface = self.resource_manager.sprites["player_jump"]

        else:
            walk_sprite = self.animation_manager.update("player_walk", 0.05)
            if walk_sprite:
                self.current_player_surface = walk_sprite
            else:
                self.current_player_surface = self.resource_manager.sprites[
                    "player_walk1"
                ]

    def throw_knife(self):
        if self.shoot_cooldown <= 0:
            projectile_x = self.player_rect.centerx + 20
            projectile_y = self.player_rect.centery - 4

            knife_sprite = self.resource_manager.sprites.get("knife")

            new_projectile = KnifeProjectile(projectile_x, projectile_y, knife_sprite)
            self.player_projectiles.append(new_projectile)

            self.shoot_cooldown = 20

            if "shoot" in self.resource_manager.sounds:
                self.resource_manager.sounds["shoot"].play()

    def update_projectiles(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        killed_enemies = 0
        active_projectiles = []
        for projectile in self.player_projectiles:
            projectile.update()

            if projectile.active:
                hit_enemy = False
                for obstacle in self.obstacle_list[:]:
                    if projectile.rect.colliderect(obstacle["rect"]):
                        projectile.active = False
                        self.obstacle_list.remove(obstacle)
                        hit_enemy = True
                        killed_enemies += 1

                        if "whip_hit" in self.resource_manager.sounds:
                            self.resource_manager.sounds["whip_hit"].play()
                        break

                if not hit_enemy:
                    active_projectiles.append(projectile)

        self.player_projectiles = active_projectiles
        return killed_enemies

    def draw_projectiles(self):
        for projectile in self.player_projectiles:
            if projectile.active:
                projectile.draw(self.screen)

    def handle_whip_attack(self):
        keys = pygame.key.get_pressed()
        direction = self.last_move_direction

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction = "right"

        if self.attack_system.start_whip_attack(self.player_rect, direction):
            if "whip_attack" in self.resource_manager.sounds:
                self.resource_manager.sounds["whip_attack"].play()

    def display_score(self):
        score_surf = self.resource_manager.fonts["large"].render(
            self.language_manager.get_text("score").format(self.score), False, WHITE
        )
        self.screen.blit(score_surf, (20, 20))

        # Boss warning
        if (
            self.score >= BOSS_TRIGGER - 200
            and not self.boss_manager.boss_defeated
            and not self.boss_manager.is_boss_active()
        ):
            warning_color = (
                (255, 100, 100)
                if (pygame.time.get_ticks() // 500) % 2
                else (255, 200, 200)
            )
            # warning_text = self.language_manager.get_text("boss_approaching")
            # warning_surf = self.resource_manager.fonts["medium"].render(
            #     warning_text, False, warning_color
            # )
            # warning_rect = warning_surf.get_rect(center=(400, 150))
            # self.screen.blit(warning_surf, warning_rect)

        if self.highscore_manager.is_new_record(self.score) and self.score > 0:
            if (self.new_record_timer // 30) % 2:
                record_surf = self.resource_manager.fonts["medium"].render(
                    self.language_manager.get_text("new_record"), False, (255, 50, 50)
                )
                record_rect = record_surf.get_rect(center=(400, 180))
                self.screen.blit(record_surf, record_rect)

        if self.player_invulnerable_timer > 0:
            if (self.player_invulnerable_timer // 10) % 2:
                invul_surf = self.resource_manager.fonts["small"].render(
                    self.language_manager.get_text("invulnerable"),
                    False,
                    (100, 255, 100),
                )
                invul_rect = invul_surf.get_rect(center=(400, 200))
                self.screen.blit(invul_surf, invul_rect)

        return self.score

    def display_score_boss(self):
        """Display score specifically for boss battles"""
        current_time = int(pygame.time.get_ticks() / 1000) - self.start_time

        # Update score_boss to match current game time
        self.score_boss = current_time

        # Return the current time for use in other methods
        return current_time

    def draw_phase_notification(self):
        if self.phase_manager.show_phase_notification:
            notification_surface = pygame.Surface((400, 100))
            notification_surface.set_alpha(200)
            notification_surface.fill((0, 0, 0))
            notification_rect = notification_surface.get_rect(center=(400, 200))
            self.screen.blit(notification_surface, notification_rect)

            phase_text = self.language_manager.get_text("phase").format(
                self.phase_manager.current_phase + 1, ""
            )
            phase_surf = self.resource_manager.fonts["large"].render(
                phase_text, False, GOLD
            )
            phase_rect = phase_surf.get_rect(center=(400, 180))
            self.screen.blit(phase_surf, phase_rect)

            name_text = self.phase_manager.get_phase_name()
            name_surf = self.resource_manager.fonts["medium"].render(
                name_text, False, WHITE
            )
            name_rect = name_surf.get_rect(center=(400, 220))
            self.screen.blit(name_surf, name_rect)

    def draw_menu(self):
        self.screen.blit(self.resource_manager.sprites["menu_bg"], (0, 0))

        title_surf = self.resource_manager.fonts["title"].render(
            self.language_manager.get_text("title"), False, RED
        )
        title_rect = title_surf.get_rect(center=(400, 80))
        self.screen.blit(title_surf, title_rect)

        highscore_surf = self.resource_manager.fonts["medium"].render(
            self.language_manager.get_text("best_score").format(
                self.highscore_manager.highscore
            ),
            False,
            GOLD,
        )
        highscore_rect = highscore_surf.get_rect(center=(400, 160))
        self.screen.blit(highscore_surf, highscore_rect)

        # ALTERAÇÃO: Adicionar "INSTRUÇÕES" na lista de opções do menu
        menu_options = [
            self.language_manager.get_text("start"),
            self.language_manager.get_text("instructions"),  # NOVO
            self.language_manager.get_text("highscores"),
            self.language_manager.get_text("settings"),
        ]

        for i, option in enumerate(menu_options):
            color = YELLOW if i == self.selected_option else GRAY

            if i == self.selected_option:
                # Sombra do texto
                shadow_surf = self.resource_manager.fonts["medium"].render(
                    option, False, BLACK
                )
                shadow_rect = shadow_surf.get_rect(
                    center=(402, 212 + i * 40)
                )  # Espaçamento reduzido
                self.screen.blit(shadow_surf, shadow_rect)

            option_surf = self.resource_manager.fonts["medium"].render(
                option, False, color
            )
            option_rect = option_surf.get_rect(
                center=(400, 210 + i * 40)
            )  # Espaçamento reduzido
            self.screen.blit(option_surf, option_rect)

    def draw_instructions(self):
        self.screen.blit(self.resource_manager.sprites["menu_bg"], (0, 0))

        # Overlay escuro para melhor legibilidade
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Título
        title_surf = self.resource_manager.fonts["large"].render(
            self.language_manager.get_text("game_instructions"), False, RED
        )
        title_rect = title_surf.get_rect(center=(400, 30))
        self.screen.blit(title_surf, title_rect)

        # Organizar instruções em colunas
        left_column_x = 180
        right_column_x = 620
        start_y = 80
        line_height = 25

        # Coluna Esquerda - Controles Básicos
        instructions_left = [
            self.language_manager.get_text("basic_controls"),
            "",
            self.language_manager.get_text("movement"),
            self.language_manager.get_text("movement_keys"),
            self.language_manager.get_text("movement_keys_right"),
            "",
            self.language_manager.get_text("jump"),
            self.language_manager.get_text("jump_keys"),
            "",
            self.language_manager.get_text("combat"),
            "",
            self.language_manager.get_text("shooting"),
            self.language_manager.get_text("shooting_keys"),
            "",
            self.language_manager.get_text("whip_attack"),
            self.language_manager.get_text("whip_keys"),
        ]

        # Coluna Direita - Gameplay e Dicas
        instructions_right = [
            self.language_manager.get_text("gameplay"),
            "",
            self.language_manager.get_text("objective"),
            self.language_manager.get_text("enemies"),
            "",
            self.language_manager.get_text("scoring"),
            self.language_manager.get_text("score_jump"),
            self.language_manager.get_text("score_kill"),
            self.language_manager.get_text("score_boss"),
            "",
            self.language_manager.get_text("boss_info"),
            self.language_manager.get_text("boss_trigger"),
            self.language_manager.get_text("boss_movement"),
            self.language_manager.get_text("boss_strategy"),
            self.language_manager.get_text("boss_avoid"),
        ]

        # Desenhar coluna esquerda
        for i, instruction in enumerate(instructions_left):
            if instruction == "":
                continue

            y_pos = start_y + i * line_height
            if y_pos > SCREEN_HEIGHT - 100:  # Evitar sair da tela
                break

            # Cores diferentes para diferentes tipos de texto
            if instruction == self.language_manager.get_text("basic_controls"):
                color = YELLOW
                font = self.resource_manager.fonts["medium"]
            elif instruction == self.language_manager.get_text("combat"):
                color = YELLOW
                font = self.resource_manager.fonts["medium"]
            elif ":" in instruction and not any(
                key in instruction for key in ["A/", "D/", "SPACE", "X/", "Z/"]
            ):
                color = (150, 150, 255)  # Azul claro para títulos de seção
                font = self.resource_manager.fonts["small"]
            elif any(key in instruction for key in ["A/", "D/", "SPACE", "X/", "Z/"]):
                color = (100, 255, 100)  # Verde para teclas
                font = self.resource_manager.fonts["small"]
            else:
                color = WHITE
                font = self.resource_manager.fonts["small"]

            text_surf = font.render(instruction, False, color)
            text_rect = text_surf.get_rect()
            text_rect.centerx = left_column_x
            text_rect.y = y_pos
            self.screen.blit(text_surf, text_rect)

        # Desenhar coluna direita
        for i, instruction in enumerate(instructions_right):
            if instruction == "":
                continue

            y_pos = start_y + i * line_height
            if y_pos > SCREEN_HEIGHT - 100:  # Evitar sair da tela
                break

            # Cores diferentes para diferentes tipos de texto
            if instruction == self.language_manager.get_text("gameplay"):
                color = YELLOW
                font = self.resource_manager.fonts["medium"]
            elif instruction == self.language_manager.get_text("boss_info"):
                color = YELLOW
                font = self.resource_manager.fonts["medium"]
            elif ":" in instruction and not any(
                key in instruction for key in ["+", "50", "20", "1000"]
            ):
                color = (255, 150, 100)  # Laranja claro para títulos de seção
                font = self.resource_manager.fonts["small"]
            elif any(key in instruction for key in ["+50", "+20", "+1000"]):
                color = GOLD  # Dourado para pontuação
                font = self.resource_manager.fonts["small"]
            else:
                color = WHITE
                font = self.resource_manager.fonts["small"]

            text_surf = font.render(instruction, False, color)
            text_rect = text_surf.get_rect()
            text_rect.centerx = right_column_x
            text_rect.y = y_pos
            self.screen.blit(text_surf, text_rect)

        # Instruções na parte inferior
        bottom_instructions = [
            self.language_manager.get_text("phases_info"),
            self.language_manager.get_text("phase_progression"),
            "",
            self.language_manager.get_text("tips"),
            self.language_manager.get_text("tip_combo"),
            self.language_manager.get_text("tip_whip"),
            self.language_manager.get_text("tip_invulnerable"),
        ]

        bottom_y = 420
        for i, instruction in enumerate(bottom_instructions):
            if instruction == "":
                continue

            y_pos = bottom_y + i * 20
            if y_pos > SCREEN_HEIGHT - 50:
                break

            if instruction == self.language_manager.get_text("phases_info"):
                color = YELLOW
                font = self.resource_manager.fonts["medium"]
            elif instruction == self.language_manager.get_text("tips"):
                color = YELLOW
                font = self.resource_manager.fonts["medium"]
            else:
                color = LIGHT_GRAY
                font = self.resource_manager.fonts["small"]

            text_surf = font.render(instruction, False, color)
            text_rect = text_surf.get_rect(center=(400, y_pos))
            self.screen.blit(text_surf, text_rect)

        # Instruções para voltar
        back_surf = self.resource_manager.fonts["small"].render(
            self.language_manager.get_text("press_back"), False, DARK_GRAY
        )
        back_rect = back_surf.get_rect(center=(400, SCREEN_HEIGHT - 20))
        self.screen.blit(back_surf, back_rect)

    def draw_highscores(self):
        self.screen.blit(self.resource_manager.sprites["menu_bg"], (0, 0))

        title_surf = self.resource_manager.fonts["medium"].render(
            self.language_manager.get_text("hall_of_fame"), False, RED
        )
        title_rect = title_surf.get_rect(center=(400, 80))
        self.screen.blit(title_surf, title_rect)

        if self.highscore_manager.highscore > 0:
            trophy_surf = self.resource_manager.fonts["large"].render("🏆", False, GOLD)
            trophy_rect = trophy_surf.get_rect(center=(300, 200))
            self.screen.blit(trophy_surf, trophy_rect)

            record_surf = self.resource_manager.fonts["medium"].render(
                self.language_manager.get_text("best_score_display").format(
                    self.highscore_manager.highscore
                ),
                False,
                GOLD,
            )
            record_rect = record_surf.get_rect(center=(400, 200))
            self.screen.blit(record_surf, record_rect)

            # Show boss defeat status
            if self.boss_manager.boss_defeated:
                boss_text = self.language_manager.get_text("dracula_boss")
                color = LIGHT_GRAY
            else:
                boss_text = self.language_manager.get_text("dracula_boss_not")
                color = DARK_GRAY

            boss_surf = self.resource_manager.fonts["small"].render(
                boss_text, False, color
            )
            boss_rect = boss_surf.get_rect(center=(400, 240))
            self.screen.blit(boss_surf, boss_rect)

            # Show whip kills if any
            if (
                hasattr(self, "attack_system")
                and self.attack_system.enemies_defeated > 0
            ):
                whip_kills_text = self.language_manager.get_text(
                    "enemies_whipped"
                ).format(self.attack_system.enemies_defeated)
                whip_surf = self.resource_manager.fonts["small"].render(
                    whip_kills_text, False, (255, 150, 100)
                )
                whip_rect = whip_surf.get_rect(center=(400, 270))
                self.screen.blit(whip_surf, whip_rect)

            # Show rank
            rank_data = self.get_rank_info(self.highscore_manager.highscore)
            rank_surf = self.resource_manager.fonts["small"].render(
                self.language_manager.get_text("rank").format(rank_data["title"]),
                False,
                rank_data["color"],
            )
            rank_rect = rank_surf.get_rect(center=(400, 320))
            self.screen.blit(rank_surf, rank_rect)
        else:
            no_record_surf = self.resource_manager.fonts["medium"].render(
                self.language_manager.get_text("no_records"), False, LIGHT_GRAY
            )
            no_record_rect = no_record_surf.get_rect(center=(400, 200))
            self.screen.blit(no_record_surf, no_record_rect)

        back_surf = self.resource_manager.fonts["small"].render(
            self.language_manager.get_text("press_back"), False, DARK_GRAY
        )
        back_rect = back_surf.get_rect(center=(400, 520))
        self.screen.blit(back_surf, back_rect)

    def get_rank_info(self, score):
        if score >= 50 and self.boss_manager.boss_defeated:
            return {
                "title": self.language_manager.get_text("ranks")["vampire_slayer"],
                "color": (255, 50, 50),
            }
        elif score >= 40:
            return {
                "title": self.language_manager.get_text("ranks")["dark_knight"],
                "color": (150, 50, 150),
            }
        elif score >= 30:
            return {
                "title": self.language_manager.get_text("ranks")["castle_explorer"],
                "color": (100, 100, 255),
            }
        elif score >= 15:
            return {
                "title": self.language_manager.get_text("ranks")["brave_warrior"],
                "color": (255, 150, 50),
            }
        else:
            return {
                "title": self.language_manager.get_text("ranks")["novice_hunter"],
                "color": LIGHT_GRAY,
            }

    def draw_settings(self):
        self.screen.blit(self.resource_manager.sprites["menu_bg"], (0, 0))

        title_surf = self.resource_manager.fonts["medium"].render(
            self.language_manager.get_text("configurations"), False, RED
        )
        title_rect = title_surf.get_rect(center=(400, 100))
        self.screen.blit(title_surf, title_rect)

        current_lang_text = (
            "English" if self.language_manager.current_language == "en" else "Portugues"
        )

        # NOVO: Obter nome do modo de daltonismo atual
        current_colorblind_text = self.language_manager.get_colorblind_mode_name()

        settings_options = [
            self.language_manager.get_text("volume").format(int(self.volume * 100)),
            f"{self.language_manager.get_text('language')}: {current_lang_text}",
            self.language_manager.get_text("colorblind_mode").format(
                current_colorblind_text
            ),  # NOVO
            self.language_manager.get_text("back"),
        ]

        for i, option in enumerate(settings_options):
            if i == self.selected_setting:
                color = YELLOW
                shadow_surf = self.resource_manager.fonts["medium"].render(
                    option, False, BLACK
                )
                shadow_rect = shadow_surf.get_rect(center=(402, 162 + i * 40))
                self.screen.blit(shadow_surf, shadow_rect)

                # Setas direcionais
                if i == 0:  # Volume
                    if self.volume > 0:
                        left_arrow = self.resource_manager.fonts["medium"].render(
                            " < ", False, YELLOW
                        )
                        left_arrow_rect = left_arrow.get_rect(
                            center=(280, 160 + i * 40)
                        )
                        self.screen.blit(left_arrow, left_arrow_rect)

                    if self.volume < 1.0:
                        right_arrow = self.resource_manager.fonts["medium"].render(
                            " > ", False, YELLOW
                        )
                        right_arrow_rect = right_arrow.get_rect(
                            center=(520, 160 + i * 40)
                        )
                        self.screen.blit(right_arrow, right_arrow_rect)

                elif i == 1:  # Idioma
                    if self.language_manager.current_language == "en":
                        left_arrow = self.resource_manager.fonts["medium"].render(
                            " < ", False, YELLOW
                        )
                        left_arrow_rect = left_arrow.get_rect(
                            center=(240, 160 + i * 40)
                        )
                        self.screen.blit(left_arrow, left_arrow_rect)

                    if self.language_manager.current_language == "pt":
                        right_arrow = self.resource_manager.fonts["medium"].render(
                            " > ", False, YELLOW
                        )
                        right_arrow_rect = right_arrow.get_rect(
                            center=(560, 160 + i * 40)
                        )
                        self.screen.blit(right_arrow, right_arrow_rect)

                elif i == 2:  # NOVO: Modo Daltonismo
                    # Sempre mostrar setas para ciclar entre os modos
                    left_arrow = self.resource_manager.fonts["medium"].render(
                        " < ", False, YELLOW
                    )
                    left_arrow_rect = left_arrow.get_rect(center=(180, 160 + i * 40))
                    self.screen.blit(left_arrow, left_arrow_rect)

                    right_arrow = self.resource_manager.fonts["medium"].render(
                        " > ", False, YELLOW
                    )
                    right_arrow_rect = right_arrow.get_rect(center=(620, 160 + i * 40))
                    self.screen.blit(right_arrow, right_arrow_rect)

            else:
                color = GRAY

            option_surf = self.resource_manager.fonts["medium"].render(
                option, False, color
            )
            option_rect = option_surf.get_rect(center=(400, 160 + i * 40))
            self.screen.blit(option_surf, option_rect)

    def draw_game_over(self):
        self.screen.blit(self.resource_manager.sprites["gameover_bg"], (0, 0))

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        is_new_record = (
            self.highscore_manager.is_new_record(self.score) and self.score > 0
        )

        if is_new_record:
            if (pygame.time.get_ticks() // 500) % 2:
                record_surf = self.resource_manager.fonts["medium"].render(
                    self.language_manager.get_text("new_record"), False, GOLD
                )
                record_rect = record_surf.get_rect(center=(400, 200))

                shadow_surf = self.resource_manager.fonts["medium"].render(
                    self.language_manager.get_text("new_record"), False, BLACK
                )
                shadow_rect = shadow_surf.get_rect(center=(402, 202))
                self.screen.blit(shadow_surf, shadow_rect)
                self.screen.blit(record_surf, record_rect)

        score_text = self.language_manager.get_text("your_score").format(self.score)
        shadow_surf = self.resource_manager.fonts["large"].render(
            score_text, False, BLACK
        )
        shadow_rect = shadow_surf.get_rect(center=(402, 242))
        self.screen.blit(shadow_surf, shadow_rect)

        score_surf = self.resource_manager.fonts["large"].render(
            score_text, False, (255, 50, 50)
        )
        score_rect = score_surf.get_rect(center=(400, 240))
        self.screen.blit(score_surf, score_rect)

        best_text = self.language_manager.get_text("best").format(
            self.highscore_manager.highscore
        )
        best_surf = self.resource_manager.fonts["small"].render(best_text, False, GOLD)
        best_rect = best_surf.get_rect(center=(400, 280))
        self.screen.blit(best_surf, best_rect)

        # Show if Dracula was defeated
        if self.boss_manager.boss_defeated:
            boss_text = self.language_manager.get_text("boss_defeated_run").format(
                self.language_manager.get_text("dracula_boss_name")
            )
            boss_surf = self.resource_manager.fonts["small"].render(
                boss_text, False, (200, 100, 200)
            )
            boss_rect = boss_surf.get_rect(center=(400, 310))
            self.screen.blit(boss_surf, boss_rect)

        # Show whip kills
        if hasattr(self, "attack_system") and self.attack_system.enemies_defeated > 0:
            whip_text = self.language_manager.get_text("enemies_whipped_run").format(
                self.attack_system.enemies_defeated
            )
            whip_surf = self.resource_manager.fonts["small"].render(
                whip_text, False, (255, 150, 100)
            )
            whip_rect = whip_surf.get_rect(center=(400, 330))
            self.screen.blit(whip_surf, whip_rect)

        # Show max phase reached
        max_phase = self.phase_manager.current_phase
        phase_text = self.language_manager.get_text("max_phase").format(max_phase + 1)
        phase_surf = self.resource_manager.fonts["small"].render(
            phase_text, False, LIGHT_GRAY
        )
        phase_rect = phase_surf.get_rect(center=(400, 360))
        self.screen.blit(phase_surf, phase_rect)

        restart_text = self.language_manager.get_text("play_again")
        restart_surf = self.resource_manager.fonts["medium"].render(
            restart_text, False, GRAY
        )
        restart_rect = restart_surf.get_rect(center=(400, 420))
        self.screen.blit(restart_surf, restart_rect)

        menu_text = self.language_manager.get_text("return_menu")
        menu_surf = self.resource_manager.fonts["small"].render(
            menu_text, False, LIGHT_GRAY
        )
        menu_rect = menu_surf.get_rect(center=(400, 450))
        self.screen.blit(menu_surf, menu_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Durante o loading, apenas permitir quit (opcionalmente pular com SPACE)
            if self.loading_screen_active:
                if event.type == pygame.KEYDOWN:
                    # OPCIONAL: Permitir pular o loading com SPACE
                    if event.key == pygame.K_SPACE:
                        if "loading_music" in self.resource_manager.sounds:
                            self.resource_manager.sounds["loading_music"].stop()
                        self.loading_screen_active = False
                        self.loading_timer = 0
                        self.initialize_game_after_loading()
                continue

            if self.game_state == "menu":
                self.handle_menu_events(event)
            elif self.game_state == "instructions":  # NOVO
                self.handle_instructions_events(event)
            elif self.game_state == "highscores":
                self.handle_highscore_events(event)
            elif self.game_state == "settings":
                self.handle_settings_events(event)
            elif self.game_state == "playing":
                self.handle_game_events(event)
            elif self.game_state == "game_over":
                self.handle_game_over_events(event)
            elif self.game_state == "victory":
                self.handle_victory_events(event)

        return True

    def handle_victory_events(self, event):
        pass

    def handle_instructions_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                self.game_state = "menu"

    def handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.selected_option = (
                    self.selected_option - 1
                ) % 4  # ALTERADO: 4 opções agora
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.selected_option = (
                    self.selected_option + 1
                ) % 4  # ALTERADO: 4 opções agora
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:  # START
                    self.start_game()
                elif self.selected_option == 1:  # INSTRUÇÕES - NOVO
                    self.game_state = "instructions"
                elif self.selected_option == 2:  # HIGHSCORES
                    self.game_state = "highscores"
                elif self.selected_option == 3:  # SETTINGS
                    self.game_state = "settings"

    def handle_highscore_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                self.game_state = "menu"

    def handle_settings_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.selected_setting = (self.selected_setting - 1) % 4
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.selected_setting = (self.selected_setting + 1) % 4
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"
            elif event.key == pygame.K_RETURN:
                if self.selected_setting == 3:  # Voltar
                    self.game_state = "menu"
            elif event.key in [pygame.K_LEFT, pygame.K_a]:
                if self.selected_setting == 0:  # Volume
                    self.volume = max(0.0, self.volume - 0.1)
                    self.update_volume()
                elif self.selected_setting == 1:  # Idioma
                    new_lang = (
                        "pt" if self.language_manager.current_language == "en" else "en"
                    )
                    self.language_manager.set_language(new_lang)
                elif self.selected_setting == 2:  # Modo Daltonismo
                    current_index = COLORBLIND_ORDER.index(
                        self.language_manager.colorblind_mode
                    )
                    new_index = (current_index - 1) % len(COLORBLIND_ORDER)
                    self.language_manager.set_colorblind_mode(
                        COLORBLIND_ORDER[new_index]
                    )
                    self.life_manager.update_colorblind_mode()  # Atualizar sprites de vida
                    self.update_dracula_sprites()  # NOVO: Atualizar sprites do Drácula

            elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                if self.selected_setting == 0:  # Volume
                    self.volume = min(1.0, self.volume + 0.1)
                    self.update_volume()
                elif self.selected_setting == 1:  # Idioma
                    new_lang = (
                        "en" if self.language_manager.current_language == "pt" else "pt"
                    )
                    self.language_manager.set_language(new_lang)
                elif self.selected_setting == 2:  # Modo Daltonismo
                    current_index = COLORBLIND_ORDER.index(
                        self.language_manager.colorblind_mode
                    )
                    new_index = (current_index + 1) % len(COLORBLIND_ORDER)
                    self.language_manager.set_colorblind_mode(
                        COLORBLIND_ORDER[new_index]
                    )
                    self.life_manager.update_colorblind_mode()  # Atualizar sprites de vida
                    self.update_dracula_sprites()  # NOVO: Atualizar sprites do Drácula

    def handle_game_events(self, event):
        if event.type == self.obstacle_timer:
            self.create_obstacle()
        elif event.type == self.enemy_animation_timer:
            # MODIFICADO: Atualizar animações de todos os modos
            colorblind_mode = self.language_manager.colorblind_mode
            for enemy_type in ["bat", "zombie", "knight", "owl", "bat1", "panther"]:
                animation_name = f"{enemy_type}_{colorblind_mode}"
                self.animation_manager.update(animation_name, 1)
        elif event.type == pygame.KEYDOWN:
            if (
                event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]
                and self.player_rect.bottom >= GROUND_Y
            ):
                self.player_gravity = JUMP_FORCE
            elif event.key == pygame.K_e:
                self.throw_knife()
            elif event.key == pygame.K_q:
                self.handle_whip_attack()
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"
                self.reset_game_state()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (
                self.player_rect.collidepoint(event.pos)
                and self.player_rect.bottom >= GROUND_Y
            ):
                self.player_gravity = JUMP_FORCE

    def handle_game_over_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"
                self.reset_game_state()

    def start_game(self):
        # Ativar tela de loading PRIMEIRO
        self.loading_screen_active = True
        self.loading_timer = 0
        self.game_state = "loading"  # Novo estado

        # Parar música do menu
        if "menu_music" in self.resource_manager.sounds:
            self.resource_manager.sounds["menu_music"].stop()
        self.main_menu_playing = False

        if "loading_music" in self.resource_manager.sounds:
            self.resource_manager.sounds["loading_music"].play(loops=-1)

        # Limpeza básica inicial
        self.obstacle_list.clear()
        self.player_projectiles.clear()

    def initialize_game_after_loading(self):
        """Inicializa o jogo após a tela de loading"""
        self.game_state = "playing"
        self.victory_timer = 0
        self.victory_triggered = False

        self.shoot_cooldown = 0
        self.enemies_jumped = 0
        self.enemies_killed = 0
        self.life_manager.reset_lives()

        # RESET DO SCORE
        self.score = 0
        self.score_boss = 0

        self.attack_system = PlayerAttackSystem(self.language_manager)
        self.attack_system.load_whip_sprites(self.resource_manager)

        self.player_animation_state = PlayerAnimationState()
        self.last_move_direction = "right"

        self.start_time = int(pygame.time.get_ticks() / 1000)
        self.new_record_timer = 0
        self.player_rect.x = PLAYER_START_X
        self.player_rect.y = PLAYER_START_Y
        self.player_rect.bottom = GROUND_Y
        self.player_gravity = 0

        self.player_invulnerable_timer = 0
        self.player_damaged = False

        self.phase_manager = PhaseManager(self.language_manager)

        # Reset completo do boss manager
        if hasattr(self.boss_manager, "reset_for_new_game"):
            self.boss_manager.reset_for_new_game()
        else:
            self.boss_manager = BossManager(self.language_manager)
            self.boss_manager.boss_defeated = False

        if "fireball" in self.resource_manager.sprites:
            self.boss_manager.set_fireball_sprite(
                self.resource_manager.sprites["fireball"]
            )

        if "loading_music" in self.resource_manager.sounds:
            self.resource_manager.sounds["loading_music"].stop()

        # Iniciar música do jogo
        if "bg_music" in self.resource_manager.sounds:
            self.resource_manager.sounds["bg_music"].play(loops=-1)
        self.music_playing = True

    def draw_loading_screen(self):
        """Desenha a tela de loading com texto do Drácula subindo"""
        # Tela completamente preta
        self.screen.fill((0, 0, 0))

        # Definir os textos por idioma
        dracula_texts = {
            "pt": [
                "O Conde Drácula retornou...",
                "As trevas se espalham pelo castelo...",
                "Sua sede de sangue é insaciável...",
                "Prepare-se para enfrentar o mal ancestral...",
                "A batalha final se aproxima...",
            ],
            "en": [
                "Count Dracula has returned...",
                "Darkness spreads through the castle...",
                "His thirst for blood is insatiable...",
                "Prepare to face the ancient evil...",
                "The final battle approaches...",
            ],
        }

        current_texts = dracula_texts[self.language_manager.current_language]

        # Calcular posições dos textos baseado no timer
        # Cada texto aparece em intervalos diferentes e sobe com velocidades ligeiramente diferentes
        text_intervals = [0, 300, 600, 900, 1200]  # Quando cada texto começa a aparecer
        text_speeds = [2.5, 2.8, 2.3, 2.6, 2.4]  # Velocidade de subida de cada texto

        # Desenhar cada texto
        for i, text in enumerate(current_texts):
            # Verificar se é hora deste texto aparecer
            if self.loading_timer > text_intervals[i]:
                # Calcular quanto tempo este texto específico está na tela
                text_age = self.loading_timer - text_intervals[i]

                # Posição Y inicial (começa na parte inferior da tela)
                start_y = SCREEN_HEIGHT + 50

                # Calcular posição atual (subindo)
                current_y = start_y - (text_age * text_speeds[i])

                # Só desenhar se o texto ainda estiver visível (não saiu completamente da tela)
                if (
                    current_y > -100
                ):  # -100 para dar uma margem antes de parar de renderizar
                    # Efeito de fade baseado na posição
                    # Texto fica mais opaco quando está no centro da tela
                    center_distance = abs(current_y - SCREEN_HEIGHT // 2)
                    max_distance = SCREEN_HEIGHT // 2 + 100
                    alpha = max(50, 255 - int((center_distance / max_distance) * 205))

                    # Escolher fonte baseada na importância do texto
                    if (
                        i == 0 or i == len(current_texts) - 1
                    ):  # Primeiro e último texto maiores
                        font = self.resource_manager.fonts["large"]
                        color = (220, 50, 50)  # Vermelho sangue
                    else:
                        font = self.resource_manager.fonts["medium"]
                        color = (200, 200, 200)  # Cinza claro

                    # Renderizar o texto
                    text_surf = font.render(text, False, color)
                    text_surf.set_alpha(alpha)

                    # Centralizar horizontalmente
                    text_rect = text_surf.get_rect(
                        center=(SCREEN_WIDTH // 2, int(current_y))
                    )

                    # Desenhar sombra para melhor legibilidade
                    shadow_surf = font.render(text, False, (0, 0, 0))
                    shadow_surf.set_alpha(alpha // 2)
                    shadow_rect = shadow_surf.get_rect(
                        center=(SCREEN_WIDTH // 2 + 2, int(current_y) + 2)
                    )

                    self.screen.blit(shadow_surf, shadow_rect)
                    self.screen.blit(text_surf, text_rect)

        # Efeito adicional: partículas ou névoa (opcional)
        if self.loading_timer > 60:
            # Desenhar algumas "partículas" flutuantes para ambiente sombrio
            import random

            for _ in range(5):
                particle_x = random.randint(0, SCREEN_WIDTH)
                particle_y = random.randint(0, SCREEN_HEIGHT)
                particle_alpha = random.randint(20, 80)
                particle_size = random.randint(1, 3)

                particle_surface = pygame.Surface(
                    (particle_size * 2, particle_size * 2)
                )
                particle_surface.set_alpha(particle_alpha)
                particle_surface.fill((100, 100, 120))  # Azul acinzentado

                self.screen.blit(particle_surface, (particle_x, particle_y))

        # Indicador sutil de progresso no canto (opcional)
        if self.loading_timer > 1500:  # Aparece próximo do final
            progress = (self.loading_timer - 1500) / (self.loading_duration - 1500)
            progress = min(1.0, progress)

            if progress < 1.0:
                loading_indicator = "." * int((progress * 3) + 1)
                indicator_text = f"Preparando{loading_indicator}"

                indicator_surf = self.resource_manager.fonts["small"].render(
                    indicator_text, False, (100, 100, 100)
                )

                # Posicionar no canto inferior direito
                indicator_rect = indicator_surf.get_rect()
                indicator_rect.bottomright = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20)

                self.screen.blit(indicator_surf, indicator_rect)

    def reset_game_state(self):
        # Garantir que loading screen está desativado
        self.loading_screen_active = False
        self.loading_timer = 0
        self.life_manager.reset_lives()

        if "loading_music" in self.resource_manager.sounds:
            self.resource_manager.sounds["loading_music"].stop()

        self.obstacle_list.clear()
        self.player_projectiles.clear()
        self.shoot_cooldown = 0
        self.enemies_jumped = 0
        self.enemies_killed = 0
        self.victory_triggered = False

        # RESET DOS SCORES
        self.score = 0
        self.score_boss = 0

        self.player_rect.x = PLAYER_START_X
        self.player_rect.y = PLAYER_START_Y
        self.player_rect.bottom = GROUND_Y
        self.player_gravity = 0

        self.player_invulnerable_timer = 0
        self.player_damaged = False

        self.player_animation_state = PlayerAnimationState()
        self.last_move_direction = "right"

        self.phase_manager = PhaseManager(self.language_manager)

        # Reset completo do boss manager
        if hasattr(self.boss_manager, "reset_for_new_game"):
            self.boss_manager.reset_for_new_game()
        else:
            self.boss_manager = BossManager(self.language_manager)
            self.boss_manager.boss_defeated = False

        if "fireball" in self.resource_manager.sprites:
            self.boss_manager.set_fireball_sprite(
                self.resource_manager.sprites["fireball"]
            )

        if "bg_music" in self.resource_manager.sounds:
            self.resource_manager.sounds["bg_music"].stop()
        if "boss_music" in self.resource_manager.sounds:
            self.resource_manager.sounds["boss_music"].stop()
        self.music_playing = False
        self.boss_music_playing = False

        if "menu_music" in self.resource_manager.sounds:
            self.resource_manager.sounds["menu_music"].play(loops=-1)
        self.main_menu_playing = True

    def get_current_background(self):
        # Obter o modo de daltonismo atual
        colorblind_mode = self.language_manager.colorblind_mode

        # Durante a batalha do boss, usar sempre o background da fase 4
        if (
            self.boss_manager.is_boss_active()
            or self.boss_manager.boss_victory_timer > 0
        ):
            background_name = f"background_{colorblind_mode}_phase_4"
        else:
            current_phase = self.phase_manager.current_phase
            background_name = f"background_{colorblind_mode}_phase_{current_phase}"

        if background_name in self.resource_manager.sprites:
            return self.resource_manager.sprites[background_name]
        else:
            # Fallback para o background normal da fase 0
            fallback = f"background_{colorblind_mode}_phase_0"
            if fallback in self.resource_manager.sprites:
                return self.resource_manager.sprites[fallback]
            else:
                return self.resource_manager.sprites.get("background_normal_phase_0")

    def update_game(self):
        # Se estiver na tela de loading
        if self.loading_screen_active:
            self.loading_timer += 1

            if self.loading_timer >= self.loading_duration:
                # Loading concluído, inicializar o jogo
                self.loading_screen_active = False
                self.loading_timer = 0
                self.initialize_game_after_loading()

            return  # Não fazer mais nada durante o loading

        if self.victory_triggered or self.game_state == "victory":
            if not self.victory_triggered:
                self.victory_timer = 0
                self.victory_triggered = True

            self.victory_timer += 1
            if self.victory_timer >= 300:
                self.game_state = "menu"
                self.victory_triggered = False
                self.reset_game_state()
            return

        if self.game_state != "playing":
            return

        if self.game_state == "playing":
            if self.player_invulnerable_timer > 0:
                self.player_invulnerable_timer -= 1

            # Check for Dracula boss trigger
            if self.boss_manager.should_trigger_boss(self.score):
                self.boss_manager.start_boss_battle()
                if "bg_music" in self.resource_manager.sounds:
                    self.resource_manager.sounds["bg_music"].stop()
                if "boss_music" in self.resource_manager.sounds:
                    self.resource_manager.sounds["boss_music"].play(loops=-1)
                self.music_playing = False
                self.boss_music_playing = True

            # Update boss status FIRST
            boss_status = self.boss_manager.update(
                self.player_rect, self.player_projectiles
            )

            # Check for boss completion IMMEDIATELY
            if boss_status == "boss_complete":
                self.game_state = "victory"
                self.victory_triggered = True
                self.boss_manager.current_boss = None
                self.boss_manager.boss_victory_timer = 0
                self.obstacle_list.clear()
                self.player_projectiles.clear()
                self.shoot_cooldown = 0
                self.player_invulnerable_timer = 0
                if "boss_music" in self.resource_manager.sounds:
                    self.resource_manager.sounds["boss_music"].stop()

                if self.highscore_manager.update_if_record(self.score):
                    pass

                self.game_state = "victory"
                self.victory_timer = 0
                self.stop_all_music()
                return

            if boss_status == "boss_defeated":
                self.score += POINTS_BOSS_DEFEAT
                self.game_state = "victory"
                self.stop_all_music()

            # Controles do jogador
            keys = pygame.key.get_pressed()
            if self.boss_manager.is_boss_active():
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.player_rect.x -= 5
                    self.last_move_direction = "left"

                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.player_rect.x += 5
                    self.last_move_direction = "right"

            if keys[pygame.K_q]:
                self.handle_whip_attack()

            if self.player_rect.x < 0:
                self.player_rect.x = 0
            elif self.player_rect.x > SCREEN_WIDTH - self.player_rect.width:
                self.player_rect.x = SCREEN_WIDTH - self.player_rect.width

            # Atualizar projecteis e contar inimigos mortos por faca
            killed_by_projectiles = self.update_projectiles()
            if killed_by_projectiles > 0:
                self.score += POINTS_KILL_ENEMY * killed_by_projectiles
                self.enemies_killed += killed_by_projectiles

            # Atualizar sistema de chicote e contar inimigos mortos por chicote
            killed_by_whip = self.attack_system.update(
                self.obstacle_list, self.boss_manager, self.resource_manager.sounds
            )
            if killed_by_whip and killed_by_whip > 0:
                self.score += POINTS_KILL_ENEMY * killed_by_whip
                self.enemies_killed += killed_by_whip

            # Renderização - Sistema modificado com sistema de vidas
            if (
                not self.boss_manager.is_boss_active()
                and self.boss_manager.boss_victory_timer <= 0
            ):
                # Lógica normal do jogo com scroll do background
                self.bg_x_pos -= 2
                current_bg = self.get_current_background()
                if self.bg_x_pos <= -current_bg.get_width():
                    self.bg_x_pos = 0

                self.screen.blit(current_bg, (self.bg_x_pos, 0))
                self.screen.blit(
                    current_bg, (self.bg_x_pos + current_bg.get_width(), 0)
                )

                self.update_obstacles()

                # Sistema de colisão modificado
                collision_result, jumped_enemies = self.check_collisions()
                if jumped_enemies > 0:
                    self.score += POINTS_JUMP_ENEMY * jumped_enemies
                    self.enemies_jumped += jumped_enemies

                # Se collision_result é False, significa game over (sem vidas)
                if not collision_result:
                    if self.highscore_manager.update_if_record(self.score):
                        pass
                    self.game_state = "game_over"
                    self.score_boss = 0
                    self.stop_all_music()
                    if "game_over" in self.resource_manager.sounds:
                        self.resource_manager.sounds["game_over"].play()
                    return

            else:
                # Durante boss battle, usar background fixo do Dracula's Lair
                current_bg = self.get_current_background()
                # Limpar a tela completamente antes de desenhar o background fixo
                self.screen.fill((0, 0, 0))  # Tela preta primeiro
                self.screen.blit(current_bg, (0, 0))  # Background estático sem scroll
                self.obstacle_list.clear()

                # Reset da posição do background para evitar problemas quando sair do boss
                self.bg_x_pos = 0

                # Verificar dano do boss (modificado)
                if (
                    self.player_invulnerable_timer <= 0
                    and self.boss_manager.check_player_damage(self.player_rect)
                ):
                    self.player_invulnerable_timer = (
                        120  # 2 segundos de invulnerabilidade
                    )

                    # Tomar dano do boss
                    still_alive = self.life_manager.take_damage()
                    if not still_alive:
                        # Game Over
                        if self.highscore_manager.update_if_record(self.score):
                            pass
                        self.game_state = "game_over"
                        self.score_boss = 0
                        self.stop_all_music()
                        if "game_over" in self.resource_manager.sounds:
                            self.resource_manager.sounds["game_over"].play()
                        return

            # Resto da lógica do jogo
            self.draw_projectiles()

            # Sistema de pontuação atualizado - apenas mostra o score atual
            self.display_score()  # Não mais atualiza o score por tempo
            self.score_boss = self.display_score_boss()

            # Só atualizar fase se não estiver no boss
            if (
                not self.boss_manager.is_boss_active()
                and self.boss_manager.boss_victory_timer <= 0
            ):
                phase_changed = self.phase_manager.update_phase(self.score)
                self.phase_manager.update_notification_timer()

            # Física do jogador
            if self.player_gravity < 0:
                self.player_gravity += GRAVITY_ASCEND
            else:
                self.player_gravity += GRAVITY_DESCEND

            self.player_rect.y += self.player_gravity

            if self.player_rect.bottom >= GROUND_Y:
                self.player_rect.bottom = GROUND_Y

            self.update_player_animation()
            self.render_player_and_effects()
            self.boss_manager.draw(self.screen, self.dracula_sprites)
            self.attack_system.draw_ui(self.screen, self.resource_manager.fonts)

            # Desenhar os corações (sistema de vidas)
            self.life_manager.draw(self.screen)

            # Só mostrar notificação de fase se não estiver no boss
            if (
                not self.boss_manager.is_boss_active()
                and self.boss_manager.boss_victory_timer <= 0
            ):
                self.draw_phase_notification()

    def render_player_and_effects(self):
        self.draw_player()
        self.attack_system.draw(self.screen)

    def draw_player(self):
        if self.player_invulnerable_timer > 0:
            if (self.player_invulnerable_timer // 5) % 2:
                temp_surface = self.current_player_surface.copy()
                temp_surface.set_alpha(128)
                self.screen.blit(temp_surface, self.player_rect)
            else:
                self.screen.blit(self.current_player_surface, self.player_rect)
        else:
            self.screen.blit(self.current_player_surface, self.player_rect)

    def stop_all_music(self):
        sounds_to_stop = ["bg_music", "boss_music", "menu_music", "loading_music"]
        for sound_name in sounds_to_stop:
            if sound_name in self.resource_manager.sounds:
                self.resource_manager.sounds[sound_name].stop()

        self.music_playing = False
        self.boss_music_playing = False
        self.main_menu_playing = False

    def update_audio(self):
        if self.game_state in ["menu", "instructions", "highscores", "settings"]:
            if self.music_playing or self.boss_music_playing:
                self.stop_all_music()

            if (
                not self.main_menu_playing
                and "menu_music" in self.resource_manager.sounds
            ):
                self.resource_manager.sounds["menu_music"].play(loops=-1)
                self.main_menu_playing = True

        elif self.game_state == "playing":
            if self.main_menu_playing and "menu_music" in self.resource_manager.sounds:
                self.resource_manager.sounds["menu_music"].stop()
                self.main_menu_playing = False

        elif self.game_state == "game_over":
            if self.music_playing or self.boss_music_playing or self.main_menu_playing:
                self.stop_all_music()

    def render(self):
        if self.loading_screen_active:
            self.draw_loading_screen()
        elif self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "instructions":
            self.draw_instructions()
        elif self.game_state == "highscores":
            self.draw_highscores()
        elif self.game_state == "settings":
            self.draw_settings()
        elif self.game_state == "game_over":
            self.draw_game_over()
        elif self.game_state == "victory":
            self.draw_victory()

    def run(self):
        if "menu_music" in self.resource_manager.sounds:
            self.resource_manager.sounds["menu_music"].play(loops=-1)

        running = True
        while running:
            running = self.handle_events()
            if not running:
                break

            self.update_audio()
            if self.victory_triggered and self.game_state != "victory":
                self.game_state = "victory"
            self.update_game()
            self.render()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
        exit()

    def draw_victory(self):
        # Usar background da fase atual
        current_bg = self.get_current_background()
        self.screen.blit(current_bg, (0, 0))

        # Overlay escuro
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Título de vitória
        victory_text = (
            "DRÁCULA DERROTADO!"
            if self.language_manager.current_language == "pt"
            else "DRACULA DEFEATED!"
        )
        victory_surf = self.resource_manager.fonts["title"].render(
            victory_text, False, GOLD
        )
        victory_rect = victory_surf.get_rect(center=(400, 150))

        # Sombra do título
        shadow_surf = self.resource_manager.fonts["title"].render(
            victory_text, False, BLACK
        )
        shadow_rect = shadow_surf.get_rect(center=(402, 152))
        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(victory_surf, victory_rect)

        # Mostrar pontuação final
        score_text = self.language_manager.get_text("your_score").format(self.score)
        score_surf = self.resource_manager.fonts["large"].render(
            score_text, False, WHITE
        )
        score_rect = score_surf.get_rect(center=(400, 250))
        self.screen.blit(score_surf, score_rect)

        # Mostrar se é novo recorde
        if self.highscore_manager.is_new_record(self.score):
            if (pygame.time.get_ticks() // 500) % 2:
                record_surf = self.resource_manager.fonts["medium"].render(
                    self.language_manager.get_text("new_record"), False, (255, 50, 50)
                )
                record_rect = record_surf.get_rect(center=(400, 300))
                self.screen.blit(record_surf, record_rect)

        # Instruções
        instruction_text = (
            "Retornando ao menu principal..."
            if self.language_manager.current_language == "pt"
            else "Returning to main menu..."
        )
        instruction_surf = self.resource_manager.fonts["small"].render(
            instruction_text, False, GRAY
        )
        instruction_rect = instruction_surf.get_rect(center=(400, 400))
        self.screen.blit(instruction_surf, instruction_rect)

        # Timer automático
        time_left = (300 - self.victory_timer) // 60
        if time_left > 0:
            auto_text = (
                f"Retorno automático em: {time_left}s"
                if self.language_manager.current_language == "pt"
                else f"Auto return in: {time_left}s"
            )
            auto_surf = self.resource_manager.fonts["small"].render(
                auto_text, False, DARK_GRAY
            )
            auto_rect = auto_surf.get_rect(center=(400, 450))
            self.screen.blit(auto_surf, auto_rect)


def main():
    try:
        game = BloodLostGame()
        game.run()
    except Exception as e:
        print(f"Erro ao iniciar o jogo: {e}")
        import traceback

        traceback.print_exc()
        pygame.quit()
        exit()


if __name__ == "__main__":
    main()
