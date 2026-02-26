import pygame
import math
import random
from assets import *
from player import *
from effects import *
from weapon_creation import *
from UI import *




BLACK = (0, 0, 0)
bullet_group = pygame.sprite.Group()

mouse_was_down_shooting = False
mouse_was_down = False
ammo_total = 0

shooting = False

last_shot_time = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, facing_right, screen, current_gun, offset=40):
        super().__init__()
        self.original_image = current_gun.bullet_image
        self.speed = current_gun.speed
        self.facing_right = facing_right
        self.screen = screen
        self.angle = angle
        self.bullet_health = current_gun.damage
        self.bounce = current_gun.bounce
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image.set_colorkey((0, 0, 0))

        rad_angle = math.radians(angle)
        offset_x = math.cos(rad_angle) * offset
        offset_y = -math.sin(rad_angle) * offset

        self.explosion_channels = [pygame.mixer.Channel(i) for i in range(6, 11)]
        self.current_channel = 0

        self.spawn_x = pos[0] + offset_x
        self.spawn_y = pos[1] + offset_y

        self.rect = self.image.get_rect(center=(self.spawn_x, self.spawn_y))
        self.prev_x = self.rect.centerx
        self.prev_y = self.rect.centery

        self.vel_x = math.cos(rad_angle) * self.speed
        self.vel_y = -math.sin(rad_angle) * self.speed

        self.total_distance_traveled = 0
        self.max_range = current_gun.distance  

    def update(self, screen, current_gun, enemy_group, wall_group, player, score_container):
        self.prev_x = self.rect.centerx
        self.prev_y = self.rect.centery

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        #only track distance when bounce finshed
        if self.bounce <= 0:
            self.total_distance_traveled += math.hypot(self.vel_x, self.vel_y)

        # --- Check max range ---
        if self.total_distance_traveled >= self.max_range:
            explosion = Explosion(self.rect.centerx, self.rect.centery, self.angle, current_gun)
            explosion_group.add(explosion)
            self.kill()
            return

        # --- Collision with walls (acts as boundaries too) ---
        for wall in wall_group:
            if self.rect.colliderect(wall.rect):
                self.bounce -= 1
                if self.bounce <= 0:
                    explosion = Explosion(self.rect.centerx, self.rect.centery, self.angle, current_gun)
                    explosion_group.add(explosion)
                    self.kill()
                    return

                # Determine bounce axis based on wall orientation
                overlap_x = min(self.rect.right - wall.rect.left, wall.rect.right - self.rect.left)
                overlap_y = min(self.rect.bottom - wall.rect.top, wall.rect.bottom - self.rect.top)

                if overlap_x < overlap_y:
                    # Horizontal hit → reverse X velocity
                    if self.vel_x > 0:
                        self.rect.right = wall.rect.left
                    else:
                        self.rect.left = wall.rect.right
                    self.vel_x *= -1
                else:
                    # Vertical hit → reverse Y velocity
                    if self.vel_y > 0:
                        self.rect.bottom = wall.rect.top
                    else:
                        self.rect.top = wall.rect.bottom
                    self.vel_y *= -1

                # Update angle + rotated image
                self.angle = -math.degrees(math.atan2(self.vel_y, self.vel_x))
                self.image = pygame.transform.rotate(self.original_image, self.angle)
                self.image.set_colorkey((0, 0, 0))
                self.rect = self.image.get_rect(center=self.rect.center)
                return

        # --- Collision with enemies ---
        for enemy in enemy_group:
            if self.rect.colliderect(enemy.rect) and enemy.health > 0:
                for i in range(3):
                    spawn_smoke(self.prev_x, self.prev_y, effects["smoke"])
                spawn_blood(enemy.rect.centerx, enemy.rect.centery, effects["blood"])

                damage_dealt = min(self.bullet_health, enemy.health)
                enemy.take_damage(damage_dealt, player.rect)
                trigger_screenshake(200, 4, 0)

                base_gain = damage_dealt * 8
                multiplier = 1 + (score_container["score"] / 100)
                gained_score = int(base_gain * multiplier)
                score_container["score"] += gained_score

                self.bullet_health -= damage_dealt
                
                if self.bullet_health <= 0:
                    self.kill()
                return

        # --- Bullet trail effect ---
        spawn_smoke(self.prev_x, self.prev_y, effects["smoke"])


    
def handle_shooting(screen, player_rect, facing_right, gun_tip_position, reloading, recoil_stats, current_gun):
    global mouse_was_down_shooting, last_shot_time

    # Get mouse input
    mouse_down = pygame.mouse.get_pressed()[0]
    now = pygame.time.get_ticks()
    shoot_delay = current_gun.firerate
    just_pressed = mouse_down and not mouse_was_down_shooting

    # Handle auto vs semi
    if current_gun.type == "automatic":
        trigger = mouse_down
    else:
        trigger = just_pressed

    # True if player tried to shoot this frame (even if reloading)
    shot_attempted = trigger and not reloading

    # Only allow shooting if there's ammo
    has_enough_ammo = current_gun.current_reload > current_gun.number_of_bullets
    shooting = shot_attempted and has_enough_ammo and (now - last_shot_time >= shoot_delay)

    if shooting:
        last_shot_time = now

        # Play shooting sound
        shoot_channels = [pygame.mixer.Channel(i) for i in range(5)]
        current_channel = 0
        shoot_channels[current_channel].play(current_gun.shoot_sound)
        current_channel = (current_channel + 1) % len(shoot_channels)

        # Effects
        trigger_screenshake(250, 4, 0)
        trigger_screenshake(100, 2, 1)
        spawn_shell(gun_tip_position[0], gun_tip_position[1], current_gun.bullet_shell_image, facing_right, current_gun)
        recoil_stats[0] = current_gun.recoil
        recoil_stats[1] = current_gun.recoil_decay

        # Fractional ammo deduction for UI
        current_gun.current_reload -= current_gun.number_of_bullets
        
        # Aim and shoot bullets
        mx, my = pygame.mouse.get_pos()
        mx, my = camera.reverse((mx, my))
        hx, hy = gun_tip_position
        dx, dy = mx - hx, my - hy
        angle = math.degrees(math.atan2(-dy, dx))

        for i in range(current_gun.number_of_bullets):
            if current_gun.number_of_bullets == 1:
                ang = angle
            else:
                offset = current_gun.spread * (i / (current_gun.number_of_bullets - 1) - 0.5)
                ang = angle + offset

            bullet = Bullet(gun_tip_position, ang, facing_right, screen, current_gun)
            bullet_group.add(bullet)

    mouse_was_down_shooting = mouse_down

    return shooting, shot_attempted, has_enough_ammo
