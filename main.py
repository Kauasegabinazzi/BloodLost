import pygame
from sys import exit
from random import randint, choice
import json
import os
import math

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
PHASE_THRESHOLDS = [0, 10, 20, 30, 40]
PHASE_NAMES = ["Castle Entrance", "Dark Corridors", "Ancient Library", "Vampire's Chamber", "Final Battle"]

# Boss triggers - em quais fases aparecem bosses
BOSS_TRIGGERS = {2: "vampire", 4: "demon"}  # Fase 3 e 5 têm boss battles

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
YELLOW = (255, 255, 100)
GOLD = (255, 215, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)

# ==================== CLASSE DE ESTADOS DO JOGADOR ====================
class PlayerAnimationState:
    def __init__(self):
        self.current_state = "idle"  # idle, walking, jumping, attacking
        self.state_timer = 0
        self.attack_priority = True  # Ataque tem prioridade sobre movimento
        
    def update_state(self, player_rect, is_attacking, is_jumping, is_moving):
        """Atualiza o estado da animação baseado nas ações do jogador"""
        self.state_timer += 1
        
        # Prioridade: ataque > pulo > movimento > idle
        if is_attacking:
            if self.current_state != "attacking":
                self.state_timer = 0
            self.current_state = "attacking"
        elif is_jumping:
            if self.current_state not in ["attacking"]:
                if self.current_state != "jumping":
                    self.state_timer = 0
                self.current_state = "jumping"
        elif is_moving:
            if self.current_state not in ["attacking", "jumping"]:
                if self.current_state != "walking":
                    self.state_timer = 0
                self.current_state = "walking"
        else:
            if self.current_state not in ["attacking", "jumping"]:
                if self.current_state != "idle":
                    self.state_timer = 0
                self.current_state = "idle"
    
    def get_current_state(self):
        return self.current_state
    
    def get_state_timer(self):
        return self.state_timer

# ==================== CLASSE DE ATAQUE COM CHICOTE ====================
class WhipAttack:
    def __init__(self, x, y, direction="right"):
        self.x = x
        self.y = y
        self.direction = direction  # "right" ou "left"
        self.active = True
        
        # Animação do chicote (3 frames)
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8  # Frames por estágio da animação
        
        # NOVO: Controle de sprite do jogador durante ataque
        self.player_sprite_frame = 0
        
        # Hitboxes para cada frame da animação
        self.hitboxes = self.setup_hitboxes()
        
        # Dano e efeitos
        self.damage_dealt = []  # Lista de inimigos já atingidos neste ataque
        self.screen_shake = 0
        
    def setup_hitboxes(self):
        """Define as hitboxes para cada frame da animação"""
        if self.direction == "right":
            return [
                # Frame 0: Chicote começando (pequeno alcance)
                pygame.Rect(self.x + 40, self.y - 10, 60, 30),
                # Frame 1: Chicote estendendo (médio alcance) 
                pygame.Rect(self.x + 40, self.y - 15, 120, 40),
                # Frame 2: Chicote totalmente estendido (longo alcance)
                pygame.Rect(self.x + 40, self.y - 20, 180, 50)
            ]
        else:  # direction == "left"
            return [
                # Frame 0: Chicote começando (pequeno alcance)
                pygame.Rect(self.x - 100, self.y - 10, 60, 30),
                # Frame 1: Chicote estendendo (médio alcance)
                pygame.Rect(self.x - 160, self.y - 15, 120, 40),
                # Frame 2: Chicote totalmente estendido (longo alcance)
                pygame.Rect(self.x - 220, self.y - 20, 180, 50)
            ]
    
    def update(self):
        """Atualiza a animação do chicote - VERSÃO MELHORADA"""
        self.animation_timer += 1
        
        # Muda para próximo frame
        if self.animation_timer >= self.animation_speed:
            self.current_frame += 1
            self.player_sprite_frame = self.current_frame  # Sincroniza com sprite do player
            self.animation_timer = 0
            
            # Ataque termina após 3 frames
            if self.current_frame >= 3:
                self.active = False
                return False
        
        # Reduz screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
            
        return True
    
    def get_current_hitbox(self):
        """Retorna a hitbox atual baseada no frame da animação"""
        if self.current_frame < len(self.hitboxes):
            return self.hitboxes[self.current_frame]
        return None
    
    def check_enemy_collision(self, obstacles):
        """Verifica colisão com inimigos e aplica dano"""
        if not self.active:
            return []
        
        current_hitbox = self.get_current_hitbox()
        if not current_hitbox:
            return []
        
        hit_enemies = []
        for obstacle in obstacles:
            # Verifica se ainda não foi atingido neste ataque
            obstacle_id = id(obstacle)
            if obstacle_id not in self.damage_dealt:
                if current_hitbox.colliderect(obstacle['rect']):
                    hit_enemies.append(obstacle)
                    self.damage_dealt.append(obstacle_id)
                    self.screen_shake = 10
        
        return hit_enemies
    
    def draw(self, screen, whip_sprites=None):
        """Desenha o chicote e efeitos visuais"""
        if not self.active:
            return
            
        # Offset para screen shake
        shake_x = randint(-self.screen_shake//2, self.screen_shake//2) if self.screen_shake > 0 else 0
        shake_y = randint(-self.screen_shake//2, self.screen_shake//2) if self.screen_shake > 0 else 0
        
        current_hitbox = self.get_current_hitbox()
        if current_hitbox:
            # Se tiver sprites customizados do chicote
            if whip_sprites and len(whip_sprites) > self.current_frame:
                sprite = whip_sprites[self.current_frame]
                if self.direction == "left":
                    sprite = pygame.transform.flip(sprite, True, False)
                screen.blit(sprite, (current_hitbox.x + shake_x, current_hitbox.y + shake_y))
            else:
                # Desenho placeholder - linha que simula o chicote
                start_pos = (self.x + shake_x, self.y + shake_y)
                
                if self.direction == "right":
                    end_x = current_hitbox.right
                else:
                    end_x = current_hitbox.left
                    
                end_pos = (end_x + shake_x, self.y + shake_y)
                
                # Cor baseada no frame (mais brilhante no pico)
                colors = [(200, 150, 100), (255, 200, 150), (255, 255, 200)]
                color = colors[min(self.current_frame, len(colors)-1)]
                
                # Desenha linha do chicote
                pygame.draw.line(screen, color, start_pos, end_pos, 4)
                
                # Efeito de brilho na ponta
                if self.current_frame == 2:  # Frame de máxima extensão
                    pygame.draw.circle(screen, (255, 255, 255), end_pos, 8)
                    pygame.draw.circle(screen, color, end_pos, 6)


class PlayerAttackSystem:
    def __init__(self):
        self.current_whip_attack = None
        self.attack_cooldown = 0
        self.attack_cooldown_max = 30  # 0.5 segundos a 60 FPS
        
        # Sprites do chicote (opcional)
        self.whip_sprites = []
        
        # Estatísticas de combate
        self.enemies_defeated = 0
        self.combo_counter = 0
        self.combo_timer = 0
        
    def load_whip_sprites(self, resource_manager):
        """Carrega sprites do chicote"""
        sprite_paths = [
            'sprites\\attack1.png',
            'sprites\\attack2.png', 
            'sprites\\attack3.png'
        ]
        
        for i, path in enumerate(sprite_paths):
            try:
                sprite = resource_manager.load_sprite(f'whip_{i}', path, 2.0)
                self.whip_sprites.append(sprite)
            except:
                print(f"Sprite do chicote {i} não encontrado: {path}")
                self.whip_sprites.append(None)
    
    def can_attack(self):
        """Verifica se pode atacar"""
        return self.attack_cooldown <= 0 and (self.current_whip_attack is None or not self.current_whip_attack.active)
    
    def start_whip_attack(self, player_rect, direction="right"):
        """Inicia ataque com chicote"""
        if not self.can_attack():
            return False
            
        # Cria novo ataque
        self.current_whip_attack = WhipAttack(
            player_rect.centerx, 
            player_rect.centery - 10,  # Ligeiramente acima do centro
            direction
        )
        
        # Define cooldown
        self.attack_cooldown = self.attack_cooldown_max
        
        return True
    
    def update(self, obstacles, sounds=None):
        """Atualiza sistema de ataque"""
        # Reduz cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Reduz timer do combo
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_counter = 0
        
        # Atualiza ataque atual
        if self.current_whip_attack and self.current_whip_attack.active:
            still_active = self.current_whip_attack.update()
            
            if still_active:
                # Verifica colisões com inimigos
                hit_enemies = self.current_whip_attack.check_enemy_collision(obstacles)
                
                if hit_enemies:
                    # Remove inimigos atingidos
                    for enemy in hit_enemies:
                        if enemy in obstacles:
                            obstacles.remove(enemy)
                    
                    # Atualiza estatísticas
                    self.enemies_defeated += len(hit_enemies)
                    self.combo_counter += len(hit_enemies)
                    self.combo_timer = 120  # 2 segundos para manter combo
                    
                    # Toca som de hit
                    if sounds and 'whip_hit' in sounds:
                        sounds['whip_hit'].play()
            else:
                # Ataque terminou
                self.current_whip_attack = None
    
    def draw(self, screen):
        """Desenha ataque atual"""
        if self.current_whip_attack and self.current_whip_attack.active:
            self.current_whip_attack.draw(screen, self.whip_sprites)
    
    def draw_ui(self, screen, fonts):
        """Desenha interface do sistema de ataque"""
        # Cooldown indicator
        if self.attack_cooldown > 0:
            cooldown_text = f"Whip Cooldown: {self.attack_cooldown}"
            cooldown_surf = fonts['small'].render(cooldown_text, False, (255, 200, 100))
            screen.blit(cooldown_surf, (SCREEN_WIDTH - 200, 50))
        else:
            ready_text = "Whip Ready! [Z]"
            ready_surf = fonts['small'].render(ready_text, False, (100, 255, 100))
            screen.blit(ready_surf, (SCREEN_WIDTH - 200, 50))
        
        # Estatísticas de combate
        if self.enemies_defeated > 0:
            kills_text = f"Enemies Defeated: {self.enemies_defeated}"
            kills_surf = fonts['small'].render(kills_text, False, (200, 200, 200))
            screen.blit(kills_surf, (SCREEN_WIDTH - 200, 80))
        
        # Combo counter
        if self.combo_counter > 1:
            combo_color = (255, 100, 100) if self.combo_counter >= 5 else (255, 200, 100)
            combo_text = f"Combo x{self.combo_counter}!"
            combo_surf = fonts['medium'].render(combo_text, False, combo_color)
            combo_rect = combo_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
            
            # Sombra para destaque
            shadow_surf = fonts['medium'].render(combo_text, False, (0, 0, 0))
            shadow_rect = shadow_surf.get_rect(center=(SCREEN_WIDTH // 2 + 2, 102))
            
            screen.blit(shadow_surf, shadow_rect)
            screen.blit(combo_surf, combo_rect)

# ==================== CLASSE DE PROJÉTIL DO JOGADOR ====================
class PlayerProjectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 8
        self.width = 12
        self.height = 6
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.active = True
    
    def update(self):
        """Atualiza posição do projétil"""
        self.x += self.speed
        self.rect.x = self.x
        
        # Remove projétil se sair da tela
        if self.x > SCREEN_WIDTH + 50:
            self.active = False
    
    def draw(self, screen):
        """Desenha o projétil"""
        # Projétil azul brilhante
        pygame.draw.ellipse(screen, (100, 150, 255), self.rect)
        # Núcleo branco para brilho
        core_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 1, self.width - 4, self.height - 2)
        pygame.draw.ellipse(screen, (200, 220, 255), core_rect)

# ==================== CLASSES DE BOSS BATTLE ====================
class BossBattle:
    def __init__(self, boss_type, screen_width, screen_height):
        self.boss_type = boss_type
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = True
        self.scroll_locked = True
        
        # Estado do boss
        self.phase = "entrance"  # entrance, fighting, defeat, victory
        self.entrance_timer = 0
        self.defeat_timer = 0
        
        # Configurações específicas do boss
        self.setup_boss_stats()
        
        # Sistema de ataques
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.current_attack = None
        self.projectiles = []
        
        # Sistema de dano ao boss
        self.damage_zones = []
        self.invulnerable_timer = 0
        
        # Efeitos visuais
        self.screen_shake = 0
        self.flash_timer = 0
        
    def setup_boss_stats(self):
        """Configura estatísticas baseadas no tipo de boss"""
        boss_configs = {
            "vampire": {
                "hp": 15,  # AUMENTADO: 15 tiros para derrotar
                "size": (80, 100),
                "pos": (600, 210),
                "attacks": ["bat_swarm", "teleport_strike"],
                "attack_interval": 120,
                "speed": 2
            },
            "demon": {
                "hp": 20,  # AUMENTADO: 20 tiros para derrotar
                "size": (90, 110),
                "pos": (580, 200),
                "attacks": ["fire_breath", "charge"],
                "attack_interval": 100,
                "speed": 2.5
            }
        }
        
        config = boss_configs.get(self.boss_type, boss_configs["vampire"])
        self.max_hp = config["hp"]
        self.boss_hp = self.max_hp
        self.boss_rect = pygame.Rect(config["pos"][0], config["pos"][1], 
                                   config["size"][0], config["size"][1])
        self.attacks = config["attacks"]
        self.attack_interval = config["attack_interval"]
        self.boss_speed = config["speed"]
        
        # Posição inicial (fora da tela)
        self.boss_rect.x = self.screen_width + 100
        self.target_x = config["pos"][0]
        
    def update(self, player_rect, player_projectiles):
        """Atualiza lógica do boss battle"""
        if not self.active:
            return False
            
        # Reduz timers
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
        if self.screen_shake > 0:
            self.screen_shake -= 1
        if self.flash_timer > 0:
            self.flash_timer -= 1
            
        # Máquina de estados
        if self.phase == "entrance":
            self.update_entrance()
        elif self.phase == "fighting":
            self.update_fighting(player_rect, player_projectiles)
        elif self.phase == "defeat":
            self.update_defeat()
            
        # Atualiza projéteis
        self.update_projectiles()
        
        return self.active
    
    def update_entrance(self):
        """Boss entrando em cena"""
        # Move boss para posição inicial
        if self.boss_rect.x > self.target_x:
            self.boss_rect.x -= self.boss_speed * 2
        else:
            self.boss_rect.x = self.target_x
            self.entrance_timer += 1
            
        # Após 60 frames, inicia o combate
        if self.entrance_timer > 60:
            self.phase = "fighting"
            self.screen_shake = 20
    
    def update_fighting(self, player_rect, player_projectiles):
        """Lógica principal do combate"""
        self.attack_timer += 1
        
        # Sistema de ataques
        if self.attack_cooldown <= 0 and self.current_attack is None:
            self.start_random_attack()
            
        # Executa ataque atual
        if self.current_attack:
            self.execute_current_attack()
            
        # NOVO: Verifica dano dos projéteis do jogador
        self.check_projectile_damage(player_projectiles)
        
        # Verifica se boss foi derrotado
        if self.boss_hp <= 0:
            self.phase = "defeat"
            self.defeat_timer = 0
    
    def check_projectile_damage(self, player_projectiles):
        """Verifica se projéteis do jogador atingiram o boss"""
        if self.invulnerable_timer > 0:
            return
            
        for projectile in player_projectiles:
            if projectile.active and self.boss_rect.colliderect(projectile.rect):
                # Boss levou dano
                self.boss_hp -= 1
                self.invulnerable_timer = 20  # Menor invulnerabilidade para projéteis
                self.flash_timer = 15
                self.screen_shake = 15
                
                # Remove o projétil
                projectile.active = False
                
                # Boss fica mais agressivo quando ferido
                if self.boss_hp <= self.max_hp // 2:
                    self.attack_interval = max(60, self.attack_interval - 15)
                
                # Só processa um projétil por frame
                break
    
    def start_random_attack(self):
        """Inicia um ataque aleatório"""
        self.current_attack = choice(self.attacks)
        self.attack_timer = 0
        self.attack_cooldown = self.attack_interval
        
    def execute_current_attack(self):
        """Executa o ataque atual baseado no tipo de boss"""
        if self.boss_type == "vampire":
            self.execute_vampire_attacks()
        elif self.boss_type == "demon":
            self.execute_demon_attacks()
    
    def execute_vampire_attacks(self):
        """Ataques do vampiro"""
        if self.current_attack == "teleport_strike":
            if self.attack_timer == 30:
                # Teleporta perto do player
                self.boss_rect.x = 250
                self.flash_timer = 10
                self.create_danger_zone(200, 250, 150, 80, 60)
            elif self.attack_timer >= 90:
                self.current_attack = None
                self.boss_rect.x = self.target_x
                
        elif self.current_attack == "bat_swarm":
            if self.attack_timer == 20:
                # Cria morcegos
                for i in range(5):
                    angle = (i * 36) * math.pi / 180
                    self.projectiles.append({
                        'type': 'bat',
                        'x': self.boss_rect.centerx,
                        'y': self.boss_rect.centery,
                        'speed_x': math.cos(angle) * 3,
                        'speed_y': math.sin(angle) * 2,
                        'lifetime': 120
                    })
            elif self.attack_timer >= 100:
                self.current_attack = None
    
    def execute_demon_attacks(self):
        """Ataques do demônio"""
        if self.current_attack == "fire_breath":
            if self.attack_timer % 15 == 0 and self.attack_timer < 75:
                # Cria bolas de fogo
                self.projectiles.append({
                    'type': 'fire',
                    'x': self.boss_rect.x - 20,
                    'y': self.boss_rect.centery,
                    'speed_x': -4,
                    'speed_y': randint(-1, 1),
                    'lifetime': 80
                })
            elif self.attack_timer >= 100:
                self.current_attack = None
                
        elif self.current_attack == "charge":
            if self.attack_timer < 60:
                # Boss se move rapidamente
                self.boss_rect.x -= 4
                if self.attack_timer % 10 == 0:
                    self.screen_shake = 5
            elif self.attack_timer < 120:
                # Retorna à posição
                if self.boss_rect.x < self.target_x:
                    self.boss_rect.x += 3
            else:
                self.boss_rect.x = self.target_x
                self.current_attack = None
    
    def create_danger_zone(self, x, y, w, h, duration):
        """Cria zona de perigo"""
        self.damage_zones.append({
            'rect': pygame.Rect(x, y, w, h),
            'duration': duration,
            'warning_time': 20,
            'active': False
        })
    
    def update_projectiles(self):
        """Atualiza projéteis e zonas de dano"""
        # Atualiza projéteis
        active_projectiles = []
        for proj in self.projectiles:
            proj['x'] += proj['speed_x']
            proj['y'] += proj['speed_y']
            proj['lifetime'] -= 1
            
            if proj['lifetime'] > 0 and -50 < proj['x'] < self.screen_width + 50:
                active_projectiles.append(proj)
        
        self.projectiles = active_projectiles
        
        # Atualiza zonas de dano
        active_zones = []
        for zone in self.damage_zones:
            zone['duration'] -= 1
            if zone['duration'] > zone['warning_time']:
                zone['active'] = False  # Ainda em warning
            else:
                zone['active'] = True   # Agora causa dano
                
            if zone['duration'] > 0:
                active_zones.append(zone)
        
        self.damage_zones = active_zones
    
    def check_player_damage(self, player_rect):
        """Verifica se player levou dano - VERSÃO CORRIGIDA"""
        # NÃO verifica dano durante entrada do boss
        if self.phase != "fighting":
            return False
            
        # Colisão com projéteis
        for proj in self.projectiles:
            proj_rect = pygame.Rect(proj['x'] - 15, proj['y'] - 15, 30, 30)
            if player_rect.colliderect(proj_rect):
                return True
                
        # Colisão com zonas de dano ativas
        for zone in self.damage_zones:
            if zone['active'] and player_rect.colliderect(zone['rect']):
                return True
                
        # Colisão direta com boss durante certos ataques E se boss está próximo
        if (self.current_attack in ["teleport_strike", "charge"] and 
            self.boss_rect.x < 500 and  # Boss deve estar próximo
            player_rect.colliderect(self.boss_rect)):
            return True
            
        return False
    
    def update_defeat(self):
        """Animação de derrota do boss"""
        self.defeat_timer += 1
        
        # Efeitos visuais de derrota
        if self.defeat_timer % 10 == 0:
            self.flash_timer = 8
            self.screen_shake = 10
            
        # Boss defeated após 90 frames
        if self.defeat_timer >= 90:
            self.active = False
            return False
    
    def draw(self, screen, boss_sprites=None):
        """Desenha boss e efeitos"""
        # Screen shake offset
        shake_x = randint(-self.screen_shake//2, self.screen_shake//2) if self.screen_shake > 0 else 0
        shake_y = randint(-self.screen_shake//2, self.screen_shake//2) if self.screen_shake > 0 else 0
        
        # Desenha zonas de perigo
        for zone in self.damage_zones:
            if not zone['active']:
                # Zona de aviso (amarelo piscante)
                alpha = 100 + (zone['duration'] % 20) * 3
                warning_surface = pygame.Surface((zone['rect'].width, zone['rect'].height))
                warning_surface.set_alpha(alpha)
                warning_surface.fill((255, 255, 0))
                screen.blit(warning_surface, (zone['rect'].x + shake_x, zone['rect'].y + shake_y))
            else:
                # Zona ativa (vermelho)
                danger_surface = pygame.Surface((zone['rect'].width, zone['rect'].height))
                danger_surface.set_alpha(150)
                danger_surface.fill((255, 0, 0))
                screen.blit(danger_surface, (zone['rect'].x + shake_x, zone['rect'].y + shake_y))
        
        # Desenha projéteis
        for proj in self.projectiles:
            color = (255, 100, 0) if proj['type'] == 'fire' else (100, 50, 150)
            size = 12 if proj['type'] == 'fire' else 8
            pygame.draw.circle(screen, color, 
                             (int(proj['x'] + shake_x), int(proj['y'] + shake_y)), size)
        
        # Desenha boss
        boss_color = (150, 50, 150) if self.boss_type == "vampire" else (200, 100, 50)
        if self.flash_timer > 0:
            boss_color = (255, 255, 255)
        
        # Se tiver sprites customizados
        if boss_sprites and self.boss_type in boss_sprites:
            boss_surface = boss_sprites[self.boss_type]
            if self.flash_timer > 0:
                flash_surface = boss_surface.copy()
                flash_surface.fill((255, 255, 255), special_flags=pygame.BLEND_ADD)
                screen.blit(flash_surface, (self.boss_rect.x + shake_x, self.boss_rect.y + shake_y))
            else:
                screen.blit(boss_surface, (self.boss_rect.x + shake_x, self.boss_rect.y + shake_y))
        else:
            pygame.draw.rect(screen, boss_color, 
                           (self.boss_rect.x + shake_x, self.boss_rect.y + shake_y, 
                            self.boss_rect.width, self.boss_rect.height))
        
        # Barra de vida do boss
        self.draw_health_bar(screen)
        
        # Instruções de combate melhoradas
        if self.phase == "fighting":
            self.draw_boss_battle_instructions(screen)
    
    def draw_health_bar(self, screen):
        """Desenha barra de vida do boss"""
        bar_width = 300
        bar_height = 25
        bar_x = (self.screen_width - bar_width) // 2
        bar_y = 40
        
        # Fundo da barra
        pygame.draw.rect(screen, (50, 50, 50), (bar_x - 3, bar_y - 3, bar_width + 6, bar_height + 6))
        
        # Barra de vida
        current_width = int((self.boss_hp / self.max_hp) * bar_width)
        
        # Cor da barra baseada na vida
        if self.boss_hp > self.max_hp * 0.6:
            health_color = (200, 0, 0)  # Vermelho quando vida alta
        elif self.boss_hp > self.max_hp * 0.3:
            health_color = (255, 150, 0)  # Laranja quando vida média
        else:
            health_color = (255, 50, 50)  # Vermelho claro quando vida baixa
            
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, current_width, bar_height))
        
        # Texto da vida
        font = pygame.font.Font(None, 24)
        hp_text = f"{self.boss_hp}/{self.max_hp} HP"
        hp_surface = font.render(hp_text, True, WHITE)
        hp_rect = hp_surface.get_rect(center=(self.screen_width // 2, bar_y + bar_height // 2))
        screen.blit(hp_surface, hp_rect)
        
        # Nome do boss
        font_title = pygame.font.Font(None, 32)
        boss_name = f"{self.boss_type.capitalize()} Boss"
        text = font_title.render(boss_name, True, WHITE)
        text_rect = text.get_rect(center=(self.screen_width // 2, bar_y - 20))
        screen.blit(text, text_rect)
    
    def draw_boss_battle_instructions(self, screen):
        """Desenha instruções melhoradas para boss battle"""
        font_medium = pygame.font.Font(None, 28)
        font_small = pygame.font.Font(None, 20)
        
        # Instruções de movimento
        instructions = [
            "BOSS BATTLE CONTROLS:",
            "SPACE/UP/W - Jump",
            "A/LEFT - Move Left", 
            "D/RIGHT - Move Right",
            "X - SHOOT (Magic Projectiles)!",
            "Z - WHIP ATTACK (Melee)!",
            "",
            "Hit boss with projectiles to damage!",
            "Avoid red zones and enemy attacks!"
        ]
        
        # Desenha fundo semi-transparente
        instruction_bg = pygame.Surface((350, len(instructions) * 22 + 10))
        instruction_bg.set_alpha(180)
        instruction_bg.fill((0, 0, 0))
        screen.blit(instruction_bg, (10, SCREEN_HEIGHT - len(instructions) * 22 - 20))
        
        # Desenha cada instrução
        for i, instruction in enumerate(instructions):
            if instruction == "BOSS BATTLE CONTROLS:":
                color = (255, 255, 100)  # Amarelo para título
                text = font_medium.render(instruction, True, color)
            elif instruction == "X - SHOOT (Magic Projectiles)!":
                color = (100, 255, 100)  # Verde para ataque
                text = font_small.render(instruction, True, color)
            elif instruction == "Z - WHIP ATTACK (Melee)!":
                color = (255, 150, 100)  # Laranja para chicote
                text = font_small.render(instruction, True, color)
            elif "Hit boss with projectiles" in instruction:
                color = (255, 150, 150)  # Rosa para dica importante
                text = font_small.render(instruction, True, color)
            elif instruction == "":
                continue  # Pula linhas vazias
            else:
                color = (200, 200, 200)  # Cinza claro para controles normais
                text = font_small.render(instruction, True, color)
            
            screen.blit(text, (20, SCREEN_HEIGHT - len(instructions) * 22 + i * 22))


class BossManager:
    def __init__(self):
        self.current_boss = None
        self.defeated_bosses = set()
        self.boss_victory_timer = 0
        self.boss_reward_given = False
    
    def should_trigger_boss(self, current_phase):
        """Verifica se deve ativar boss nesta fase"""
        return (current_phase in BOSS_TRIGGERS and 
                current_phase not in self.defeated_bosses and
                self.current_boss is None)
    
    def start_boss_battle(self, phase):
        """Inicia battle contra boss"""
        boss_type = BOSS_TRIGGERS.get(phase, "vampire")
        self.current_boss = BossBattle(boss_type, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.boss_reward_given = False
        return True
    
    def update(self, player_rect, player_projectiles):
        """Atualiza boss battle"""
        if self.current_boss and self.current_boss.active:
            still_active = self.current_boss.update(player_rect, player_projectiles)
            
            if not still_active and not self.boss_reward_given:
                # Boss foi derrotado
                defeated_phase = None
                for phase, boss_type in BOSS_TRIGGERS.items():
                    if boss_type == self.current_boss.boss_type:
                        defeated_phase = phase
                        break
                
                if defeated_phase is not None:
                    self.defeated_bosses.add(defeated_phase)
                
                self.boss_victory_timer = 120  # 2 segundos de celebração
                self.boss_reward_given = True
                return "boss_defeated"
        
        # Countdown da vitória
        if self.boss_victory_timer > 0:
            self.boss_victory_timer -= 1
            if self.boss_victory_timer <= 0:
                self.current_boss = None
                return "boss_complete"
        
        return "active" if self.current_boss else "none"
    
    def check_player_damage(self, player_rect):
        """Verifica dano do boss no player"""
        if self.current_boss and self.current_boss.active and self.current_boss.phase == "fighting":
            return self.current_boss.check_player_damage(player_rect)
        return False
    
    def is_boss_active(self):
        """Verifica se há boss ativo"""
        return self.current_boss is not None and self.current_boss.active
    
    def draw(self, screen, boss_sprites=None):
        """Desenha boss atual"""
        if self.current_boss and self.current_boss.active:
            self.current_boss.draw(screen, boss_sprites)
        
        # Mensagem de vitória
        if self.boss_victory_timer > 0:
            font = pygame.font.Font(None, 48)
            victory_text = font.render("BOSS DEFEATED!", True, GOLD)
            victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            # Sombra
            shadow_text = font.render("BOSS DEFEATED!", True, BLACK)
            shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT // 2 + 2))
            
            screen.blit(shadow_text, shadow_rect)
            screen.blit(victory_text, victory_rect)


# ==================== CLASSES ORIGINAIS ATUALIZADAS ====================
class HighscoreManager:
    def __init__(self, filename='highscore.json'):
        self.filename = filename
        self.highscore = self.load()
    
    def load(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    return data.get('highscore', 0)
        except:
            pass
        return 0
    
    def save(self, score):
        try:
            data = {'highscore': score}
            with open(self.filename, 'w') as f:
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
                new_size = (int(sprite.get_width() * scale), int(sprite.get_height() * scale))
                sprite = pygame.transform.scale(sprite, new_size)
            self.sprites[name] = sprite
            return sprite
        except:
            print(f"Erro ao carregar sprite: {path}")
            # Cria sprite placeholder
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((255, 0, 255))  # Rosa para indicar erro
            self.sprites[name] = placeholder
            return placeholder
    
    def load_sound(self, name, path, volume=1.0):
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            self.sounds[name] = sound
            return sound
        except:
            print(f"Erro ao carregar som: {path}")
            return None
    
    def load_font(self, name, path, size):
        try:
            font = pygame.font.Font(path, size)
            self.fonts[name] = font
            return font
        except:
            print(f"Erro ao carregar fonte: {path}")
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
    def __init__(self):
        self.current_phase = 0
        self.previous_phase = -1
        self.phase_change_timer = 0
        self.show_phase_notification = False
        
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
        if 0 <= phase_index < len(PHASE_NAMES):
            return PHASE_NAMES[phase_index]
        return "Unknown Phase"
    
    def get_background_name(self, phase_index=None):
        if phase_index is None:
            phase_index = self.current_phase
        return f'background_phase_{phase_index}'


# ==================== CLASSE PRINCIPAL ATUALIZADA COM SISTEMA DE ANIMAÇÃO ====================
class BloodLostGame:
    def __init__(self):
        pygame.init()
        
        # Inicialização básica
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('BloodLost - Shooting & Whip System Edition')
        self.clock = pygame.time.Clock()
        
        # Managers
        self.resource_manager = ResourceManager()
        self.animation_manager = AnimationManager()
        self.highscore_manager = HighscoreManager()
        self.phase_manager = PhaseManager()
        self.boss_manager = BossManager()
        
        # NOVO: Sistema de estados do jogador
        self.player_animation_state = PlayerAnimationState()
        
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
        
        # NOVO: Variáveis para controle de movimento
        self.player_is_moving = False
        
        # Sistema de projéteis do jogador
        self.player_projectiles = []
        self.shoot_cooldown = 0  # Cooldown entre tiros
        
        # NOVO: Sistema de ataque com chicote
        self.attack_system = PlayerAttackSystem()
        
        # Sistema de invulnerabilidade do player
        self.player_invulnerable_timer = 0
        self.player_damaged = False
        
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
        self.boss_music_playing = False
        
        # Carrega recursos
        self.load_resources()
        
        # Configura timers
        self.setup_timers()
        
        # Inicializa player
        self.setup_player()
        
    def load_resources(self):
        """Carrega todos os recursos do jogo - VERSÃO ATUALIZADA"""
        rm = self.resource_manager
        
        # Backgrounds para cada fase
        background_paths = [
            'sprites\\NES - Castlevania 2 Simons Quest.png', 
            'sprites\\teste8.png', 
            'sprites\\teste3.png',  
            'sprites\\teste5.png', 
            'sprites\\teste2.png', 
        ]
        
        for i, path in enumerate(background_paths):
            background_name = f'background_phase_{i}'
            loaded_sprite = rm.load_sprite(background_name, path, SCALE_FACTOR)
            if loaded_sprite is None and i > 0:
                print(f"Usando background padrão para fase {i}")
                rm.sprites[background_name] = rm.sprites['background_phase_0']
        
        # Menu e game over backgrounds
        rm.load_sprite('menu_bg', 'sprites\\loading.webp', SCALE_FACTOR)
        
        # Game over background
        try:
            gameover_img = pygame.image.load('sprites\\gameover.png').convert_alpha()
            gameover_img = pygame.transform.scale(gameover_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            rm.sprites['gameover_bg'] = gameover_img
        except:
            fallback_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fallback_surface.fill((50, 20, 50))
            rm.sprites['gameover_bg'] = fallback_surface
        
        # Player sprites - EXPANDIDO
        rm.load_sprite('player_idle', 'sprites\\walk1.png', HERO_SCALE)
        rm.load_sprite('player_walk1', 'sprites\\walk1.png', HERO_SCALE)
        rm.load_sprite('player_walk2', 'sprites\\wal2.png', HERO_SCALE)
        rm.load_sprite('player_walk3', 'sprites\\walk3.png', HERO_SCALE)
        rm.load_sprite('player_jump', 'sprites\\jump.png', HERO_SCALE)
        
        # NOVO: Sprites de ataque
        rm.load_sprite('player_attack1', 'sprites\\attack1.png', HERO_SCALE)
        rm.load_sprite('player_attack2', 'sprites\\attack2.png', HERO_SCALE) 
        rm.load_sprite('player_attack3', 'sprites\\attack3.png', HERO_SCALE)
        
        # Se os sprites de ataque não existirem, usa sprites alternativos
        try:
            # Tenta carregar sprites específicos de ataque
            pass
        except:
            # Fallback: usa sprites existentes com efeito visual
            rm.sprites['player_attack1'] = rm.sprites['player_walk1']
            rm.sprites['player_attack2'] = rm.sprites['player_walk2']
            rm.sprites['player_attack3'] = rm.sprites['player_walk3']
        
        # NOVO: Carrega sprites do chicote
        self.attack_system.load_whip_sprites(rm)
        
        # Boss sprites (usando inimigos existentes como placeholder)
        self.boss_sprites = {}
        try:
            # Tenta carregar sprites específicos de boss
            vampire_sprite = rm.load_sprite('boss_vampire', 'sprites\\Enemie6 - idle.png', 3.0)
            demon_sprite = rm.load_sprite('boss_demon', 'sprites\\Enemie4 - idle.png', 3.5)
            self.boss_sprites['vampire'] = vampire_sprite
            self.boss_sprites['demon'] = demon_sprite
        except:
            print("Usando sprites placeholder para bosses")
        
        # Enemy sprites para obstáculos normais
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
        
        # Player animations - EXPANDIDO
        player_walk_frames = [
            rm.sprites['player_idle'],
            rm.sprites['player_walk1'],
            rm.sprites['player_walk2'],
            rm.sprites['player_walk3']
        ]
        self.animation_manager.add_animation('player_walk', player_walk_frames)
        
        # NOVO: Animação de ataque
        player_attack_frames = [
            rm.sprites['player_attack1'],
            rm.sprites['player_attack2'],
            rm.sprites['player_attack3']
        ]
        self.animation_manager.add_animation('player_attack', player_attack_frames)
        
        # Carrega sons
        rm.load_sound('bg_music', 'music\\Marble Gallery.mp3', self.volume)
        rm.load_sound('game_over', 'music\\game-over-deep-male-voice-clip-352695.mp3', self.volume)
        rm.load_sound('menu_music', 'music\\main-menu.mp3', self.volume)
        rm.load_sound('boss_music', 'music\\Marble Gallery.mp3', self.volume)
        rm.load_sound('shoot', 'music\\knife.mp3', self.volume * 0.5)  # Som de tiro
        
        # NOVO: Sons do chicote
        rm.load_sound('whip_attack', 'music\\whip.mp3', self.volume * 0.7)
        rm.load_sound('whip_hit', 'music\\whipHit.mp3', self.volume * 0.6)
        
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
        """Cria um novo obstáculo (não durante boss battles)"""
        if self.boss_manager.is_boss_active():
            return  # Não cria obstáculos durante boss battle
            
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
        if self.boss_manager.is_boss_active():
            # Durante boss battle, remove todos os obstáculos
            self.obstacle_list.clear()
            return
            
        updated_obstacles = []
        for obstacle in self.obstacle_list:
            obstacle['rect'].x -= 5
            obstacle['surface'] = self.animation_manager.get_current_frame(obstacle['type'])
            self.screen.blit(obstacle['surface'], obstacle['rect'])
            
            if obstacle['rect'].x > -100:
                updated_obstacles.append(obstacle)
        
        self.obstacle_list = updated_obstacles
    
    def check_collisions(self):
        """Verifica colisões com obstáculos normais"""
        if self.boss_manager.is_boss_active():
            return True  # Boss manager cuida das colisões durante boss battle
            
        for obstacle in self.obstacle_list:
            if self.player_rect.colliderect(obstacle['rect']):
                return False
        return True
    
    def update_player_animation(self):
        """Atualiza animação do jogador - VERSÃO MELHORADA"""
        # Verifica estados do jogador
        is_attacking = (self.attack_system.current_whip_attack and 
                       self.attack_system.current_whip_attack.active)
        is_jumping = self.player_rect.bottom < GROUND_Y
        is_moving = self.player_is_moving
        
        # Atualiza estado da animação
        self.player_animation_state.update_state(
            self.player_rect, is_attacking, is_jumping, is_moving
        )
        
        current_state = self.player_animation_state.get_current_state()
        
        # Escolhe sprite baseado no estado
        if current_state == "attacking":
            # Durante ataque, usa animação de ataque sincronizada com o chicote
            if is_attacking:
                attack_frame = self.attack_system.current_whip_attack.current_frame
                attack_sprites = ['player_attack1', 'player_attack2', 'player_attack3']
                
                if attack_frame < len(attack_sprites):
                    sprite_name = attack_sprites[attack_frame]
                    self.current_player_surface = self.resource_manager.sprites[sprite_name]
                else:
                    self.current_player_surface = self.resource_manager.sprites['player_attack3']
            else:
                # Ataque terminou, volta ao estado normal
                self.current_player_surface = self.resource_manager.sprites['player_idle']
                
        elif current_state == "jumping":
            self.current_player_surface = self.resource_manager.sprites['player_jump']
            
        elif current_state == "walking":
            # Usa animação de caminhada
            self.current_player_surface = self.animation_manager.update('player_walk', 0.1)
            
        else:  # idle
            self.current_player_surface = self.resource_manager.sprites['player_idle']
    
    def shoot_projectile(self):
        """Cria um novo projétil do jogador"""
        if self.shoot_cooldown <= 0:
            # Cria projétil na posição do jogador
            projectile_x = self.player_rect.right
            projectile_y = self.player_rect.centery - 3
            
            new_projectile = PlayerProjectile(projectile_x, projectile_y)
            self.player_projectiles.append(new_projectile)
            
            # Define cooldown (15 frames = 0.25 segundos a 60 FPS)
            self.shoot_cooldown = 15
            
            # Toca som de tiro
            if 'shoot' in self.resource_manager.sounds:
                self.resource_manager.sounds['shoot'].play()
    
    def update_projectiles(self):
        """Atualiza projéteis do jogador"""
        # Reduz cooldown de tiro
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Atualiza projéteis ativos
        active_projectiles = []
        for projectile in self.player_projectiles:
            projectile.update()
            
            if projectile.active:
                active_projectiles.append(projectile)
                projectile.draw(self.screen)
        
        self.player_projectiles = active_projectiles
    
    def handle_whip_attack(self):
        """Gerencia ataque com chicote - VERSÃO ATUALIZADA"""
        # Determina direção baseada na última movimentação ou input atual
        keys = pygame.key.get_pressed()
        direction = "right"  # Padrão
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction = "right"
        
        # Inicia ataque
        if self.attack_system.start_whip_attack(self.player_rect, direction):
            # Força estado de ataque
            self.player_animation_state.current_state = "attacking"
            self.player_animation_state.state_timer = 0
            
            # Toca som de ataque
            if 'whip_attack' in self.resource_manager.sounds:
                self.resource_manager.sounds['whip_attack'].play()
    
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
        
        # Boss warning
        if self.phase_manager.current_phase in BOSS_TRIGGERS and self.phase_manager.current_phase not in self.boss_manager.defeated_bosses:
            warning_color = (255, 100, 100) if (pygame.time.get_ticks() // 500) % 2 else (255, 200, 200)
            boss_warning = self.resource_manager.fonts['small'].render('BOSS APPROACHING!', False, warning_color)
            self.screen.blit(boss_warning, (20, 130))
        
        # Próxima fase
        if self.phase_manager.current_phase < len(PHASE_THRESHOLDS) - 1:
            next_threshold = PHASE_THRESHOLDS[self.phase_manager.current_phase + 1]
            remaining = next_threshold - current_time
            if remaining > 0:
                next_phase_surf = self.resource_manager.fonts['small'].render(f'Next phase in: {remaining}s', False, YELLOW)
                self.screen.blit(next_phase_surf, (20, 150))
        
        # Mensagem de novo recorde
        if self.highscore_manager.is_new_record(current_time) and current_time > 0:
            if (self.new_record_timer // 30) % 2:
                record_surf = self.resource_manager.fonts['medium'].render('NEW RECORD!', False, (255, 50, 50))
                record_rect = record_surf.get_rect(center=(400, 180))
                self.screen.blit(record_surf, record_rect)
        
        # Indicador de invulnerabilidade
        if self.player_invulnerable_timer > 0:
            if (self.player_invulnerable_timer // 10) % 2:  # Pisca a cada 10 frames
                invul_surf = self.resource_manager.fonts['small'].render('INVULNERABLE', False, (100, 255, 100))
                invul_rect = invul_surf.get_rect(center=(400, 200))
                self.screen.blit(invul_surf, invul_rect)
        
        # Indicador de cooldown de tiro
        if self.shoot_cooldown > 0:
            cooldown_surf = self.resource_manager.fonts['small'].render(f'Reload: {self.shoot_cooldown}', False, (255, 200, 100))
            self.screen.blit(cooldown_surf, (SCREEN_WIDTH - 150, 20))
        else:
            ready_surf = self.resource_manager.fonts['small'].render('Ready to Shoot!', False, (100, 255, 100))
            self.screen.blit(ready_surf, (SCREEN_WIDTH - 150, 20))
        
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
        subtitle_surf = self.resource_manager.fonts['medium'].render('Shooting & Whip System Edition', False, LIGHT_GRAY)
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
        instruction_rect = instruction_surf.get_rect(center=(400, 450))
        self.screen.blit(instruction_surf, instruction_rect)
        
        # Nova instrução sobre sistemas de combate
        shoot_info = self.resource_manager.fonts['small'].render('NEW: Press X to SHOOT magic projectiles, Z for WHIP attacks!', False, (100, 150, 255))
        shoot_rect = shoot_info.get_rect(center=(400, 480))
        self.screen.blit(shoot_info, shoot_rect)
        
        whip_info = self.resource_manager.fonts['small'].render('Whip has long range and destroys enemies instantly!', False, (255, 150, 100))
        whip_rect = whip_info.get_rect(center=(400, 500))
        self.screen.blit(whip_info, whip_rect)
    
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
            
            # Bosses derrotados
            defeated_count = len(self.boss_manager.defeated_bosses)
            total_bosses = len(BOSS_TRIGGERS)
            boss_text = f'Bosses Defeated: {defeated_count}/{total_bosses}'
            boss_surf = self.resource_manager.fonts['small'].render(boss_text, False, (200, 100, 200))
            boss_rect = boss_surf.get_rect(center=(400, 230))
            self.screen.blit(boss_surf, boss_rect)
            
            # Inimigos derrotados com chicote
            if hasattr(self, 'attack_system') and self.attack_system.enemies_defeated > 0:
                whip_kills_text = f'Enemies Whipped: {self.attack_system.enemies_defeated}'
                whip_surf = self.resource_manager.fonts['small'].render(whip_kills_text, False, (255, 150, 100))
                whip_rect = whip_surf.get_rect(center=(400, 250))
                self.screen.blit(whip_surf, whip_rect)
            
            # Lista de bosses derrotados
            y_offset = 280
            for phase, boss_type in BOSS_TRIGGERS.items():
                if phase in self.boss_manager.defeated_bosses:
                    boss_name = f"{boss_type.capitalize()} Boss - DEFEATED"
                    color = LIGHT_GRAY
                else:
                    boss_name = f"{boss_type.capitalize()} Boss - Not faced"
                    color = DARK_GRAY
                
                boss_surf = self.resource_manager.fonts['small'].render(boss_name, False, color)
                boss_rect = boss_surf.get_rect(center=(400, y_offset))
                self.screen.blit(boss_surf, boss_rect)
                y_offset += 25
            
            # Rank
            rank_data = self.get_rank_info(self.highscore_manager.highscore)
            rank_surf = self.resource_manager.fonts['small'].render(f'Rank: {rank_data["title"]}', False, rank_data["color"])
            rank_rect = rank_surf.get_rect(center=(400, y_offset + 20))
            self.screen.blit(rank_surf, rank_rect)
        else:
            no_record_surf = self.resource_manager.fonts['medium'].render('No records yet!', False, LIGHT_GRAY)
            no_record_rect = no_record_surf.get_rect(center=(400, 200))
            self.screen.blit(no_record_surf, no_record_rect)
        
        # Instruções
        back_surf = self.resource_manager.fonts['small'].render('Press ESC or ENTER to return', False, DARK_GRAY)
        back_rect = back_surf.get_rect(center=(400, 520))
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
            'Reset Boss Progress',
            'Voltar'
        ]
        
        for i, option in enumerate(settings_options):
            if i == self.selected_setting:
                color = YELLOW
                # Sombra
                shadow_surf = self.resource_manager.fonts['medium'].render(option, False, BLACK)
                shadow_rect = shadow_surf.get_rect(center=(402, 182 + i * 40))
                self.screen.blit(shadow_surf, shadow_rect)
                
                # Indicador
                indicator_surf = self.resource_manager.fonts['medium'].render('>', False, YELLOW)
                indicator_rect = indicator_surf.get_rect(center=(200, 180 + i * 40))
                self.screen.blit(indicator_surf, indicator_rect)
            else:
                color = (255, 100, 100) if i in [2, 3] else GRAY  # Vermelho para resets
            
            option_surf = self.resource_manager.fonts['medium'].render(option, False, color)
            option_rect = option_surf.get_rect(center=(400, 180 + i * 40))
            self.screen.blit(option_surf, option_rect)
        
        # Instruções
        instructions = [
            'Use A/D ou SETAS ESQUERDA/DIREITA para ajustar volume',
            'ENTER para selecionar, ESC para voltar',
            'ENTER para resetar o recorde (não pode ser desfeito!)',
            'ENTER para resetar progresso dos bosses',
            'ENTER para voltar ao menu principal'
        ]
        
        if self.selected_setting < len(instructions):
            instruction_surf = self.resource_manager.fonts['small'].render(instructions[self.selected_setting], False, DARK_GRAY)
            instruction_rect = instruction_surf.get_rect(center=(400, 420))
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
                record_rect = record_surf.get_rect(center=(400, 200))
                
                # Sombra do texto
                shadow_surf = self.resource_manager.fonts['medium'].render('NEW RECORD!', False, BLACK)
                shadow_rect = shadow_surf.get_rect(center=(402, 202))
                self.screen.blit(shadow_surf, shadow_rect)
                self.screen.blit(record_surf, record_rect)
        
        # Pontuação com sombra
        score_text = f'Your Score: {self.score}'
        shadow_surf = self.resource_manager.fonts['large'].render(score_text, False, BLACK)
        shadow_rect = shadow_surf.get_rect(center=(402, 242))
        self.screen.blit(shadow_surf, shadow_rect)
        
        score_surf = self.resource_manager.fonts['large'].render(score_text, False, (255, 50, 50))
        score_rect = score_surf.get_rect(center=(400, 240))
        self.screen.blit(score_surf, score_rect)
        
        # Melhor pontuação
        best_text = f'Best: {self.highscore_manager.highscore}'
        best_surf = self.resource_manager.fonts['small'].render(best_text, False, GOLD)
        best_rect = best_surf.get_rect(center=(400, 280))
        self.screen.blit(best_surf, best_rect)
        
        # Bosses enfrentados nesta run
        bosses_fought = []
        for phase in BOSS_TRIGGERS:
            if phase <= self.phase_manager.current_phase and phase in self.boss_manager.defeated_bosses:
                bosses_fought.append(BOSS_TRIGGERS[phase])
        
        if bosses_fought:
            boss_text = f'Bosses Defeated: {", ".join([b.capitalize() for b in bosses_fought])}'
            boss_surf = self.resource_manager.fonts['small'].render(boss_text, False, (200, 100, 200))
            boss_rect = boss_surf.get_rect(center=(400, 310))
            self.screen.blit(boss_surf, boss_rect)
        
        # NOVO: Estatísticas de chicote
        if hasattr(self, 'attack_system') and self.attack_system.enemies_defeated > 0:
            whip_text = f'Enemies Whipped This Run: {self.attack_system.enemies_defeated}'
            whip_surf = self.resource_manager.fonts['small'].render(whip_text, False, (255, 150, 100))
            whip_rect = whip_surf.get_rect(center=(400, 330))
            self.screen.blit(whip_surf, whip_rect)
        
        # Fase máxima alcançada
        max_phase = self.phase_manager.current_phase
        phase_text = f'Max Phase Reached: {max_phase + 1}'
        phase_surf = self.resource_manager.fonts['small'].render(phase_text, False, LIGHT_GRAY)
        phase_rect = phase_surf.get_rect(center=(400, 360))
        self.screen.blit(phase_surf, phase_rect)
        
        # Instruções
        restart_text = 'Press SPACE to play again'
        restart_surf = self.resource_manager.fonts['medium'].render(restart_text, False, GRAY)
        restart_rect = restart_surf.get_rect(center=(400, 420))
        self.screen.blit(restart_surf, restart_rect)
        
        menu_text = 'Press ESC to return to menu'
        menu_surf = self.resource_manager.fonts['small'].render(menu_text, False, LIGHT_GRAY)
        menu_rect = menu_surf.get_rect(center=(400, 450))
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
                self.selected_setting = (self.selected_setting - 1) % 5
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.selected_setting = (self.selected_setting + 1) % 5
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"
            elif event.key == pygame.K_RETURN:
                if self.selected_setting == 2:  # Reset Highscore
                    self.highscore_manager.reset()
                elif self.selected_setting == 3:  # Reset Boss Progress
                    self.boss_manager.defeated_bosses.clear()
                elif self.selected_setting == 4:  # Voltar
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
            # Pulo
            if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w] and self.player_rect.bottom >= GROUND_Y:
                self.player_gravity = JUMP_FORCE
            # Tiro com X
            elif event.key == pygame.K_x:
                self.shoot_projectile()
            # NOVO: Ataque com chicote com Z
            elif event.key == pygame.K_z:
                self.handle_whip_attack()
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
        self.player_projectiles.clear()
        self.shoot_cooldown = 0
        
        # NOVO: Reseta sistema de ataque
        self.attack_system = PlayerAttackSystem()
        self.attack_system.load_whip_sprites(self.resource_manager)
        
        # NOVO: Reseta sistema de animação do jogador
        self.player_animation_state = PlayerAnimationState()
        self.player_is_moving = False
        
        self.start_time = int(pygame.time.get_ticks() / 1000)
        self.new_record_timer = 0
        self.player_rect.bottom = GROUND_Y
        self.player_gravity = 0
        
        # Reset do sistema de invulnerabilidade
        self.player_invulnerable_timer = 0
        self.player_damaged = False
        
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
        self.player_projectiles.clear()
        self.shoot_cooldown = 0
        self.player_rect.bottom = GROUND_Y
        self.player_gravity = 0
        
        # Reset do sistema de invulnerabilidade
        self.player_invulnerable_timer = 0
        self.player_damaged = False
        
        # NOVO: Reseta sistema de animação
        self.player_animation_state = PlayerAnimationState()
        self.player_is_moving = False
        
        # Reseta o gerenciador de fases
        self.phase_manager = PhaseManager()
        
        # Para música do jogo e boss
        if 'bg_music' in self.resource_manager.sounds:
            self.resource_manager.sounds['bg_music'].stop()
        if 'boss_music' in self.resource_manager.sounds:
            self.resource_manager.sounds['boss_music'].stop()
        self.music_playing = False
        self.boss_music_playing = False
        
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
        """Atualiza lógica do jogo - VERSÃO ATUALIZADA"""
        if self.game_state == "playing":
            # Reduz timer de invulnerabilidade do player
            if self.player_invulnerable_timer > 0:
                self.player_invulnerable_timer -= 1
            
            # Verifica se deve ativar boss
            if self.boss_manager.should_trigger_boss(self.phase_manager.current_phase):
                self.boss_manager.start_boss_battle(self.phase_manager.current_phase)
                
                # Muda música para boss battle
                if 'bg_music' in self.resource_manager.sounds:
                    self.resource_manager.sounds['bg_music'].stop()
                if 'boss_music' in self.resource_manager.sounds:
                    self.resource_manager.sounds['boss_music'].play(loops=-1)
                self.music_playing = False
                self.boss_music_playing = True
            
            # Processar input de movimento durante toda a gameplay
            keys = pygame.key.get_pressed()
            
            # NOVO: Rastreia se está se movendo
            self.player_is_moving = False
            
            # Movimento horizontal (sempre permitido, mas não durante ataque em certos casos)
            is_attacking = (self.attack_system.current_whip_attack and 
                           self.attack_system.current_whip_attack.active)
            
            # Permite movimento mesmo durante ataque (para maior fluidez)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player_rect.x -= 5
                self.player_is_moving = True
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player_rect.x += 5
                self.player_is_moving = True
            
            # Tiro contínuo com X pressionado
            if keys[pygame.K_x]:
                self.shoot_projectile()
            
            # NOVO: Ataque contínuo com Z pressionado
            if keys[pygame.K_z]:
                self.handle_whip_attack()
            
            # Limitar movimento horizontal na tela
            if self.player_rect.x < 0:
                self.player_rect.x = 0
            elif self.player_rect.x > SCREEN_WIDTH - self.player_rect.width:
                self.player_rect.x = SCREEN_WIDTH - self.player_rect.width
            
            # Atualiza projéteis do jogador
            self.update_projectiles()
            
            # NOVO: Atualiza sistema de ataque com chicote
            if not self.boss_manager.is_boss_active():
                self.attack_system.update(self.obstacle_list, self.resource_manager.sounds)
            
            # Atualiza boss manager
            boss_status = self.boss_manager.update(self.player_rect, self.player_projectiles)
            
            if boss_status == "boss_defeated":
                # Boss derrotado - adiciona pontos bonus
                self.score += 20  # Bonus por derrotar boss
                
            elif boss_status == "boss_complete":
                # Boss battle terminou, volta à música normal
                if 'boss_music' in self.resource_manager.sounds:
                    self.resource_manager.sounds['boss_music'].stop()
                if 'bg_music' in self.resource_manager.sounds:
                    self.resource_manager.sounds['bg_music'].play(loops=-1)
                self.boss_music_playing = False
                self.music_playing = True
            
            # Durante boss battle, comportamento diferente
            if self.boss_manager.is_boss_active():
                # Background estático durante boss
                current_bg = self.get_current_background()
                self.screen.blit(current_bg, (0, 0))
                
                # Não atualiza obstáculos normais
                self.obstacle_list.clear()
                
                # Só verifica dano se player não está invulnerável
                if (self.player_invulnerable_timer <= 0 and 
                    self.boss_manager.check_player_damage(self.player_rect)):
                    
                    # Aplica invulnerabilidade temporária
                    self.player_invulnerable_timer = 60  # 1 segundo a 60 FPS
                    self.player_damaged = True
                    
                    # Game over
                    if self.highscore_manager.update_if_record(self.score):
                        pass  # Novo recorde salvo
                    
                    self.game_state = "game_over"
                    self.stop_all_music()
                    if 'game_over' in self.resource_manager.sounds:
                        self.resource_manager.sounds['game_over'].play()
                    return
                    
            else:
                # Gameplay normal
                # Scroll do background
                self.bg_x_pos -= 2
                current_bg = self.get_current_background()
                if self.bg_x_pos <= -current_bg.get_width():
                    self.bg_x_pos = 0
                
                # Desenha background com scroll
                self.screen.blit(current_bg, (self.bg_x_pos, 0))
                self.screen.blit(current_bg, (self.bg_x_pos + current_bg.get_width(), 0))
                
                # Atualiza obstáculos normais
                self.update_obstacles()
                
                # Verifica colisões normais (só se não estiver invulnerável)
                if self.player_invulnerable_timer <= 0 and not self.check_collisions():
                    # Aplica invulnerabilidade temporária ao invés de game over imediato
                    self.player_invulnerable_timer = 60
                    self.player_damaged = True
                    
                    # Game over
                    if self.highscore_manager.update_if_record(self.score):
                        pass
                    
                    self.game_state = "game_over"
                    self.stop_all_music()
                    if 'game_over' in self.resource_manager.sounds:
                        self.resource_manager.sounds['game_over'].play()
                    return
            
            # Atualiza score
            self.score = self.display_score()
            
            # Atualiza fase baseada no score
            phase_changed = self.phase_manager.update_phase(self.score)
            
            # Atualiza timer de notificação de mudança de fase
            self.phase_manager.update_notification_timer()
            
            # Física do jogador
            if self.player_gravity < 0:
                self.player_gravity += GRAVITY_ASCEND
            else:
                self.player_gravity += GRAVITY_DESCEND
            
            self.player_rect.y += self.player_gravity
            
            # Limita no chão
            if self.player_rect.bottom >= GROUND_Y:
                self.player_rect.bottom = GROUND_Y
            
            # NOVO: Atualiza animação do jogador com sistema de estados
            self.update_player_animation()
            
            # Renderização do player com estados corretos
            if self.player_invulnerable_timer > 0:
                # Pisca o player durante invulnerabilidade
                if (self.player_invulnerable_timer // 5) % 2:
                    temp_surface = self.current_player_surface.copy()
                    temp_surface.set_alpha(128)
                    self.screen.blit(temp_surface, self.player_rect)
                else:
                    self.screen.blit(self.current_player_surface, self.player_rect)
            else:
                self.screen.blit(self.current_player_surface, self.player_rect)
            
            # NOVO: Desenha sistema de ataque com chicote
            self.attack_system.draw(self.screen)
            
            # Desenha boss (por cima de tudo)
            self.boss_manager.draw(self.screen, self.boss_sprites)
            
            # NOVO: Desenha UI do sistema de ataque
            self.attack_system.draw_ui(self.screen, self.resource_manager.fonts)
            
            # Desenha notificação de mudança de fase (por cima de tudo)
            self.draw_phase_notification()
    
    def stop_all_music(self):
        """Para toda a música"""
        sounds_to_stop = ['bg_music', 'boss_music', 'menu_music']
        for sound_name in sounds_to_stop:
            if sound_name in self.resource_manager.sounds:
                self.resource_manager.sounds[sound_name].stop()
        
        self.music_playing = False
        self.boss_music_playing = False
        self.main_menu_playing = False
    
    def update_audio(self):
        """Gerencia estados de áudio"""
        if self.game_state in ["menu", "highscores", "settings"]:
            if self.music_playing or self.boss_music_playing:
                self.stop_all_music()
            
            if not self.main_menu_playing and 'menu_music' in self.resource_manager.sounds:
                self.resource_manager.sounds['menu_music'].play(loops=-1)
                self.main_menu_playing = True
                
        elif self.game_state == "playing":
            if self.main_menu_playing and 'menu_music' in self.resource_manager.sounds:
                self.resource_manager.sounds['menu_music'].stop()
                self.main_menu_playing = False
            
            # A música durante o jogo é controlada pelo boss manager em update_game()
                
        elif self.game_state == "game_over":
            # Para todas as músicas
            if self.music_playing or self.boss_music_playing or self.main_menu_playing:
                self.stop_all_music()
    
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


# ==================== SISTEMA AVANÇADO DE ANIMAÇÃO ADICIONAL ====================
class PlayerAnimationSystem:
    """Sistema mais avançado para animações complexas"""
    def __init__(self):
        self.states = {
            "idle": {"priority": 0, "loop": True},
            "walking": {"priority": 1, "loop": True}, 
            "jumping": {"priority": 2, "loop": False},
            "attacking": {"priority": 3, "loop": False},
            "hurt": {"priority": 4, "loop": False}
        }
        self.current_state = "idle"
        self.previous_state = "idle"
        self.state_timer = 0
        self.animation_speed = {"idle": 0.05, "walking": 0.1, "attacking": 0.2, "jumping": 0.1}
    
    def request_state_change(self, new_state):
        """Solicita mudança de estado respeitando prioridades"""
        if new_state in self.states:
            current_priority = self.states[self.current_state]["priority"]
            new_priority = self.states[new_state]["priority"]
            
            # Muda estado se a prioridade for maior ou igual
            if new_priority >= current_priority:
                if self.current_state != new_state:
                    self.previous_state = self.current_state
                    self.current_state = new_state
                    self.state_timer = 0
                    return True
        return False
    
    def update(self, animation_manager):
        """Atualiza animação baseada no estado atual"""
        self.state_timer += 1
        
        # Se animação não loop terminou, volta ao estado anterior
        if not self.states[self.current_state]["loop"]:
            max_frames = len(animation_manager.animations.get(f'player_{self.current_state}', [1]))
            speed = self.animation_speed.get(self.current_state, 0.1)
            
            if self.state_timer * speed >= max_frames:
                self.request_state_change("idle")
        
        # Retorna sprite atual
        animation_name = f'player_{self.current_state}'
        return animation_manager.update(animation_name, self.animation_speed.get(self.current_state, 0.1))


# ==================== FUNÇÃO PRINCIPAL ====================
def main():
    """Função principal"""
    try:
        game = BloodLostGame()
        game.run()
    except Exception as e:
        print(f"Erro ao iniciar o jogo: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        exit()


# ==================== EXECUÇÃO ====================
if __name__ == "__main__":
    main()