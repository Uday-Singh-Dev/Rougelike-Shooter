#enemy spawning.
import pygame
import random
from enemy import *
from UI import *

_round_anim_active = False
_round_anim_start = 0
_round_anim_duration = 4  # seconds
_round_anim_round = 0




spawn_delay = 4000  # ms delay before spawning enemies
spawn_timer = 0
spawn_enemies = False
completed = False
round_complete_animation_started = False
round_start_animation_started = False


_round_complete_anim_active = False
_round_complete_anim_start = 0
_round_complete_anim_duration = 4  # seconds


def start_round_animation(current_round):
    global _round_anim_round, _round_anim_start, _round_anim_active
    #each time round animation called increases the round
    current_round += 1
    _round_anim_round = current_round
    _round_anim_start = time.time()
    _round_anim_active = True
    return current_round


def update_round_animation(screen):
    global _round_anim_start, _round_anim_duration, _round_anim_active, _round_anim_round
    #plays the round animation
    if not _round_anim_active:
        return False  # Animation not active, so not running

    now = time.time()
    elapsed = now - _round_anim_start
    #checks if animation is finished
    if elapsed > _round_anim_duration:
        _round_anim_active = False
        return False  # Animation ended

    progress = elapsed / _round_anim_duration
    
    scale = 3
    alpha = int(255 * (1 - progress))
    
    text = f"ROUND {_round_anim_round}"
    color = (255, 255, 255)  # white

    text_surf = font.render(text, True, color)
    text_surf.set_alpha(alpha)
    text_surf = pygame.transform.rotozoom(text_surf, 0, scale)

    start_x = -text_surf.get_width()
    end_x = screen.get_width() + text_surf.get_width()
    center_x = int(start_x + (end_x - start_x) * progress)
    center_y = screen.get_height() // 3

    
    rect = text_surf.get_rect(center=(center_x, center_y))
    screen.blit(text_surf, rect)

    return True  # Animation is still running



def start_round_complete_animation():
    #the round complete animation (copy of round start animation
    global _round_complete_anim_active, _round_complete_anim_start
    _round_complete_anim_active = True
    _round_complete_anim_start = time.time()


def update_round_complete_animation(screen):
    global _round_complete_anim_active, _round_complete_anim_start, _round_complete_anim_duration

    if not _round_complete_anim_active:
        return False  # Animation not active

    now = time.time()
    elapsed = now - _round_complete_anim_start
    if elapsed > _round_complete_anim_duration:
        _round_complete_anim_active = False
        return False  # Animation finished

    progress = elapsed / _round_complete_anim_duration

    scale = 3
    alpha = int(255 * (1 - progress))  # fade out

    text = "ROUND COMPLETE!"
    color = (255, 215, 0)  # gold/yellow color

    text_surf = font.render(text, True, color)
    text_surf.set_alpha(alpha)
    text_surf = pygame.transform.rotozoom(text_surf, 0, scale)

    start_x = screen.get_width()  # start from right side
    end_x = -text_surf.get_width()  # move to left side
    center_x = int(start_x + (end_x - start_x) * progress)
    center_y = screen.get_height() // 3

    rect = text_surf.get_rect(center=(center_x, center_y))
    screen.blit(text_surf, rect)

    return True  # Animation still running














def enemy_spawning(player, enemy_group, wall_group, level, round_):
    spawn_area = pygame.Rect(
        1200,                   # left (x) inside left wall
        1200,                   # top (y) inside top wall
        6000 - 1200*2,          # width (right wall - left wall)
        6000 - 1200*2           # height (bottom wall - top wall)
    )
    min_distance = 500  # Minimum distance from player

    # Scaling multipliers for stats
    speed_multiplier = 1 + (level * 0.05) + (round_ * 0.02)
    health_multiplier = 1 + (level * 0.1) + (round_ * 0.05)
    damage_multiplier = 1 + (level * 0.05) + (round_ * 0.03)

    for _ in range(level * 3):
        for attempt in range(100):  # Limit spawn attempts
            spawn_x = random.randint(spawn_area.left, spawn_area.right)
            spawn_y = random.randint(spawn_area.top, spawn_area.bottom)
            spawn_pos = pygame.Vector2(spawn_x, spawn_y)

            # Too close to player
            if spawn_pos.distance_to(player.pos) < min_distance:
                continue

            # Base stats
            base_speed = 6
            base_health = 6
            base_damage = 1

            # Scale stats with level and round
            scaled_speed = base_speed * speed_multiplier
            scaled_health = int(base_health * health_multiplier)
            scaled_damage = int(base_damage * damage_multiplier)

            # Create a temporary enemy for collision test
            temp_enemy = Runner(
                (spawn_x, spawn_y),
                speed=scaled_speed,
                health=scaled_health,
                damage=scaled_damage
            )

            # Check if the enemy is spawning in a wall
            if pygame.sprite.spritecollide(temp_enemy, wall_group, False):
                continue

            enemy_group.add(temp_enemy)
            break
        
def round_completed(screen, enemy_group, current_round, round_anim_active, completed, spawn_ready):
    if spawn_ready and len(enemy_group) == 0:
        if not round_anim_active:
            completed = True
            return current_round, round_anim_active, completed  # 3 values
    return current_round, round_anim_active, completed  # 3 values

