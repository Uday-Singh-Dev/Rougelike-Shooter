import pygame
import math
from assets import *
from settings import *
from camera import *
from weapon_creation import *
from effects import *
from enemy import *
from UI import *

recoil_stats = [0, 0]

class Player:
    def __init__(self, pos, speed, health):
        self.pos = pygame.Vector2(pos)

        self.speed = speed
        self.max_health = health
        self.health = health
        self.previous_health = health

        # Scale & sprite data
        self.image_size = 108  # 24 * 4.5
        self.sprite_width = 63  # 14 * 4.5
        self.sprite_height = 72  # 16 * 4.5
        self.hitbox_offset_x = (self.image_size - self.sprite_width) // 2  # 22
        self.hitbox_offset_y = (self.image_size - self.sprite_height) // 2  # 18

        self.rect = pygame.Rect(
            int(self.pos.x),
            int(self.pos.y),
            self.sprite_width,
            self.sprite_height
        )

        self.facing_right = True
        self.reloading = False
        self.reload_start_time = 0

        # Dash
        self.dash = False
        self.dash_start = 0
        self.dash_cooldown = 1300
        self.dash_duration = 150

        # Animations
        self.idle_anim = player_["player1"]["idle"]
        self.run_anim = player_["player1"]["run"]

        self.gun = current_gun.gun_image
        self.current_anim = self.idle_anim
        self.recoil_dir = pygame.Vector2(-1, 0)
        self.angle = 0
        self.gun_pos = [0, 0]

        # Damage cooldown
        self.damage_cooldown = 1900
        self.last_damage_time = 0
        self.invunrable = False

        # Sounds
        self.footsteps = player_footstep
        self.footstep_channel = pygame.mixer.Channel(31)
        self.footstep_channel.set_volume(0.3)
        self.reload_channel = pygame.mixer.Channel(30)
        self.damage_channel = pygame.mixer.Channel(28)
        self.dash_channel = pygame.mixer.Channel(27)
        self.heartbeat_channel = pygame.mixer.Channel(25)

    def update_rect(self):
        #updates the rect
        self.rect.topleft = (
            int(self.pos.x) + self.hitbox_offset_x,
            int(self.pos.y) + self.hitbox_offset_y
        )

    def handle_input(self, wall_group):
        #gets current time
        now = pygame.time.get_ticks()
        #gets keys pressed
        keys = pygame.key.get_pressed()

        #checks if key pressed are (W)(A)(S)(D)
        move = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w]
        )
        #checks if key is SHIFT . if is shift and the dash duration is finished
        if keys[pygame.K_LSHIFT] and not self.dash and (now - self.dash_start > self.dash_cooldown):
            self.dash = True
            self.dash_start = now
            self.dash_channel.play(dash_S)
        #if dash finished sets dash to false
        if self.dash and (now - self.dash_start > self.dash_duration):
            self.dash = False
        #plays movement sound if statement is true. loops when finished
        if move.length_squared() > 0:
            if not self.footstep_channel.get_busy():
                self.footstep_channel.play(self.footsteps, loops=-1)
            #normalises and adds the speed
            move = move.normalize() * self.speed
            #if dash is true increases the speed to add dash effect
            if self.dash:
                move *= 5
        else:
            # Not moving
            if self.footstep_channel.get_busy():
                self.footstep_channel.stop()

        # Move and collide on X axis
        self.pos.x += move.x
        self.update_rect()
        temp_rect = self.rect.copy()

        for wall in wall_group:
            if temp_rect.colliderect(wall.rect):
                if move.x > 0:
                    self.pos.x = wall.rect.left - self.rect.width - self.hitbox_offset_x
                elif move.x < 0:
                    self.pos.x = wall.rect.right - self.hitbox_offset_x
                self.update_rect()
                temp_rect = self.rect.copy()  # Update temp_rect for Y movement after collision fix

        # Move and collide on Y axis                     
        self.pos.y += move.y
        self.update_rect()
        temp_rect = self.rect.copy()

        for wall in wall_group:
            if temp_rect.colliderect(wall.rect):
                if move.y > 0:
                    self.pos.y = wall.rect.top - self.rect.height - self.hitbox_offset_y
                elif move.y < 0:
                    self.pos.y = wall.rect.bottom - self.hitbox_offset_y
                self.update_rect()

        # Set animation based on movement
        if move.length_squared() > 0:
            self.current_anim = self.run_anim
        else:
            self.current_anim = self.idle_anim

    def update_facing(self):
        #based on mouse pos updates the direction of player
        mx, my = pygame.mouse.get_pos()
        mx, my = camera.reverse((mx, my))
        if mx > self.rect.centerx + 30:
            self.facing_right = True
        elif mx < self.rect.centerx - 30:
            self.facing_right = False

    def get_frame(self):
        #gets the current _frame eg running idle or facing direction and hurt
        frame = self.current_anim.update().copy()

        if self.invunrable and (pygame.time.get_ticks() // 100) % 2 == 0:
            overlay = pygame.Surface(frame.get_size(), flags=pygame.SRCALPHA)
            overlay.fill((255, 255, 255))
            frame.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        return frame

    def draw_gun(self, screen, camera, current_gun,offset_x,offset_y):
        #draws the gun
        self.gun = current_gun.gun_image
        #offset from player
        offx, offy = 25+offset_x, 15+offset_y
        hx = self.rect.centerx + (offx if self.facing_right else -offx)
        hy = self.rect.centery + offy
        self.gun_pos = (hx, hy)
        #gets the mouse pos
        mx, my = pygame.mouse.get_pos()
        #adds camera to mouse pos
        world_mouse = pygame.Vector2(camera.reverse((mx, my)))
        gun_world = pygame.Vector2(hx, hy)
        
        self.recoil_dir = (gun_world - world_mouse).normalize()
        dx, dy = world_mouse.x - hx, world_mouse.y - hy
        #add the angle the mouse is facing 
        self.angle = math.degrees(math.atan2(-dy, dx))
        #rotate the image
        gun_image = pygame.transform.rotate(self.gun, self.angle if self.facing_right else -self.angle)
        #if not facing right flips the image
        if not self.facing_right:
            gun_image = pygame.transform.flip(gun_image, False, True)
        
        gun_rect = gun_image.get_rect(center=(hx, hy))
        screen.blit(gun_image, camera.apply(gun_rect))

    def recoil_update(self, wall_group):
        global recoil_stats
        #adds recoil if recoil is set to higher than 0
        if recoil_stats[0] > 0.1:
            recoil_stats[0] *= recoil_stats[1]

            rad = math.radians(self.angle)
            recoil_vec = pygame.Vector2(
                -math.cos(rad) * recoil_stats[0],
                math.sin(rad) * recoil_stats[0]
            )

            self.pos.x += recoil_vec.x
            temp_rect = self.rect.copy()
            temp_rect.x = int(self.pos.x) + self.hitbox_offset_x
            #same wall collision in movmeent except to track when recoil happens as a teleporting error kept appeaaring
            for wall in wall_group:
                if temp_rect.colliderect(wall.rect):
                    if recoil_vec.x > 0:
                        temp_rect.right = wall.rect.left
                    elif recoil_vec.x < 0:
                        temp_rect.left = wall.rect.right
                    self.pos.x = temp_rect.x - self.hitbox_offset_x

            self.pos.y += recoil_vec.y
            temp_rect = self.rect.copy()
            temp_rect.y = int(self.pos.y) + self.hitbox_offset_y
            for wall in wall_group:
                if temp_rect.colliderect(wall.rect):
                    if recoil_vec.y > 0:
                        temp_rect.bottom = wall.rect.top
                    elif recoil_vec.y < 0:
                        temp_rect.top = wall.rect.bottom
                    self.pos.y = temp_rect.y - self.hitbox_offset_y
                    
            #updates the pos
            self.update_rect()

    def reload(self, current_gun):
        #checks for key presses
        keys = pygame.key.get_pressed()
        #if key is r and is not already reloading
        if keys[pygame.K_r] and not self.reloading:
            #reload is now true
            self.reloading = True
            self.reload_start_time = pygame.time.get_ticks()
            spawn_clip(self.rect.x + 50, self.rect.y + 50, effects["clip"], self.facing_right)
            self.reload_channel.play(current_gun.reload_sound)

        if self.reloading and pygame.time.get_ticks() - self.reload_start_time >= current_gun.reload_time:
            #checks if the reload is finished
            current_gun.current_reload = current_gun.reload_size
            self.reloading = False
            
    def collision_check(self, enemy_group, player, blood_alpha, game_state,player_score, camera=None):
        now = pygame.time.get_ticks()
        collided_enemy = None
        max_check_distance = 200  # Adjust based on enemy size/speed

        if player.health <= 0:
            game_state = "game over"
        
        for enemy in enemy_group:
            enemy.player_invunrable = False  # Reset flag

            # Optional: Skip if enemy too far from player
            if self.pos.distance_to(enemy.pos) > max_check_distance:
                continue

            # Optional: Skip if enemy is off-camera (requires camera object)
            if camera and not is_on_camera(enemy, camera, buffer=50):
                continue

            if self.rect.colliderect(enemy.rect):
                collided_enemy = enemy
                break  # Stop at first collision

        # If collision and cooldown is over
        if collided_enemy and (now - self.last_damage_time >= self.damage_cooldown):
            trigger_screenshake(150, 3, 0)
                #reduce score on hit
            player_score //= 2

            # Start heartbeat loop only once
            if self.heartbeat_channel and not self.heartbeat_channel.get_busy():
                self.heartbeat_channel.play(heartbeat_S, loops=-1)

            blood_alpha = 255  # Reset blood vignette when hit

            # Play damage sound
            if self.damage_channel:
                self.damage_channel.play(HitHurt_S)

            self.health -= collided_enemy.damage

            # Blood effect
            spawn_blood(self.rect.centerx, self.rect.centery, effects["blood"])

            # Start cooldown
            self.last_damage_time = now

        # Update invulnerability state
        inv_active = (now - self.last_damage_time) < self.damage_cooldown
        self.invunrable = inv_active

        if collided_enemy and not inv_active:
            inv_active = True
            if inv_active:
                collided_enemy.player_invunrable = True
                blood_alpha = 255  
                
            else:
                collided_enemy.player_invunrable = False

        # Stop heartbeat if no longer needed
        if not inv_active and self.heartbeat_channel.get_busy():
            self.heartbeat_channel.stop()

        return blood_alpha, game_state,player_score
            
    def update(self, current_gun, wall_group):
        self.handle_input(wall_group)
        self.update_facing()
        self.recoil_update(wall_group)
        self.reload(current_gun)
