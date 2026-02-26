import pygame
from assets import *
from effects import *
import random

enemy_group = pygame.sprite.Group()
enemy_dead_group = pygame.sprite.Group()

class Enemy_dead(pygame.sprite.Sprite):
    #adds the enemy dead sprite
    def __init__(self, x, y, facing_right):
        super().__init__()
        self.image = enemies["runner"]["dead"]
        self.facing_right = facing_right
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(topleft=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed, health, damage, idle_anim, run_anim, attack_anim, attack_anim_2, falling_frame):
        super().__init__()
        #stats the for the enemy
        self.pos = pygame.Vector2(pos)
        self.previous_pos = self.pos.copy()

        self.speed = speed
        self.wander_speed = speed * 0.3
        self.health = health
        self.max_health = health
        self.damage = damage

        self.full_image_size = 64  # original full image size
        self.scale_factor = 4.5

        # Sprite bounds inside the original image
        self.sprite_rect_orig = pygame.Rect(23, 21, 17, 21)

        # Scaled full image size
        self.image_size = int(self.full_image_size * self.scale_factor)  # 64 * 4.5 = 288

        # Scaled sprite hitbox
        self.sprite_rect_scaled = pygame.Rect(
            int(self.sprite_rect_orig.x * self.scale_factor),
            int(self.sprite_rect_orig.y * self.scale_factor),
            int(self.sprite_rect_orig.width * self.scale_factor),
            int(self.sprite_rect_orig.height * self.scale_factor)
        )

        # Hitbox offset relative to the full image
        self.hitbox_offset_x = self.sprite_rect_scaled.x
        self.hitbox_offset_y = self.sprite_rect_scaled.y
        self.sprite_width = self.sprite_rect_scaled.width
        self.sprite_height = self.sprite_rect_scaled.height

        # Initialize rect for collisions
        self.rect = pygame.Rect(
            int(self.pos.x) + self.hitbox_offset_x,
            int(self.pos.y) + self.hitbox_offset_y,
            self.sprite_width,
            self.sprite_height
        )

        # View rectangle
        self.view_rect = pygame.Rect(0, 0, 1920, 1080)
        self.view_rect.center = self.rect.center

        # Wander logic
        self.wander_timer = 0
        self.wander_direction = pygame.Vector2(0, 0)
        self.wander_cooldown = 1000
        self.wander_start = 0

        # Player alert logic
        self.alert_timer = 0
        self.alert_duration = 2000
        self.alert = False

        # Damage state
        self.damage_duration = 120
        self.last_damage_time = 0

        # Animation handling
        self.idle_anim = idle_anim
        self.run_anim = run_anim
        self.attack_anim = attack_anim
        self.attack_anim_2 = attack_anim_2
        self.falling_frame = falling_frame
        self.current_anim = self.idle_anim

        #booleans for checking
        self.facing_right = True
        self.recoil_velocity = pygame.Vector2(0, 0)
        self.recoil = False
        self.dying = False
        self.dead = False
        self.found = False
        self.hit = False
        self.attacking = False
        self.hit_pause = 0

        
        self.attack_start_time = 0  # Prevent uninitialized error

        # Sound handling
        self.enemy_death_channel = pygame.mixer.Channel(24)
        self.enemy_hit_channel = pygame.mixer.Channel(18)
        self.enemy_hit_channel.set_volume(0.5)

    def update_direction(self, direction):
        #updates direction if x is greater than 0
        if direction.length_squared() > 0:
            self.facing_right = direction.x > 0

    def update_pos(self):
        #updates the pos
        self.rect.topleft = (
            int(self.pos.x) + self.hitbox_offset_x,
            int(self.pos.y) + self.hitbox_offset_y
        )
        self.view_rect.center = self.rect.center

    def get_frame(self):
        #adds the correct frame depending on what state its in
        now = pygame.time.get_ticks()
        #makes the image falling if dying else updates animation 
        frame = self.falling_frame.copy() if self.dying else self.current_anim.update().copy()
        #makes the sprite white when damaged
        if (now - self.last_damage_time) <= self.damage_duration:
            white_overlay = pygame.Surface(frame.get_size(), flags=pygame.SRCALPHA)
            white_overlay.fill((255, 255, 255))
            frame.blit(white_overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        #flips the frame if needed
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        return frame

    def player_finding(self, player):
        #if the player is in the view rect set found to true
        self.found = self.view_rect.colliderect(player.rect)
        #however if not self. idle will be true
        if not self.found and not self.hit and self.wander_direction.length_squared() == 0:
            self.current_anim = self.idle_anim

    def wander_state(self):
        #wander state (not used so lag dosent appear)
        if not self.found and not self.hit and not getattr(self, 'player_invunrable', False):
            #makes the movement stop for a random time
            self.wander_cooldown = random.randint(100, 3000)
            now = pygame.time.get_ticks()

            #if the cooldown is finished start the next wander movement
            if self.wander_timer <= 0:
                if now - self.wander_start >= self.wander_cooldown:
                    #checks if enoughj time has passed for the wander_cooldown
                    self.wander_direction = pygame.Vector2(random.randint(-50, 50), random.randint(-50, 50))

                    #if the enemy has movement it normalises the movement to account for diaganol mvoement
                    if self.wander_direction.length_squared() != 0:
                        self.wander_direction = self.wander_direction.normalize()
                    else:
                        #sets it to 0
                        self.wander_direction = pygame.Vector2(0, 0)
                    #sets wander start to now to track when the last time wander state was active
                    self.wander_timer = 100
                    self.wander_start = now
            else:
                #sets the animation to run when wandering(walking)
                self.current_anim = self.run_anim
                #updates the pos based on the direction and then the speed of the enemy
                self.pos += self.wander_direction * self.wander_speed
                #updates the direction based on if x is greater than 0 or not
                self.update_direction(self.wander_direction)
                #updates the pos
                self.update_pos()
                #reduces a ms from the wander_timer ( based on fps)
                self.wander_timer -= 1

                if self.wander_timer <= 0:
                    self.wander_start = now
                    self.wander_direction = pygame.Vector2(0, 0)

    def take_damage(self, damage, player):
        global hit_pause_timer
        now = pygame.time.get_ticks()
        #if take damage called self.hit is true
        self.hit = True
        #reduces health from enemy
        self.health -= damage

        #if player passed through adds recoil on damage
        if player:
            self.recoil_on_damage(player)
        #plays hurt sfx 
        if not self.enemy_hit_channel.get_busy():
            self.enemy_hit_channel.play(enemy_hurt_S)

        #alert set to active
        self.alert_timer = now
        self.last_damage_time = now

        #if health <= 0 then dying is true
        if self.health <= 0 and not self.dying:
            self.dying = True
            self.hit = False
            if self.recoil_velocity.length_squared() < 0.01:
                direction = self.pos - pygame.Vector2(player.rect.center)
                if direction.length_squared() > 0:
                    self.recoil_velocity = direction.normalize() * 30
                else:
                    self.recoil_velocity = pygame.Vector2(0, 0)

    def check_wall_collision(self, wall_group):
        #checks for wall collision using clamping
        for wall in wall_group:
            if self.rect.colliderect(wall.rect):
                overlap_left = self.rect.right - wall.rect.left
                overlap_right = wall.rect.right - self.rect.left
                overlap_top = self.rect.bottom - wall.rect.top
                overlap_bottom = wall.rect.bottom - self.rect.top

                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                #using the direction of the objects adds collision based on the enemy hitbox offset
                if min_overlap == overlap_left:
                    self.pos.x = wall.rect.left - self.hitbox_offset_x - self.rect.width
                elif min_overlap == overlap_right:
                    self.pos.x = wall.rect.right - self.hitbox_offset_x
                elif min_overlap == overlap_top:
                    self.pos.y = wall.rect.top - self.hitbox_offset_y - self.rect.height
                elif min_overlap == overlap_bottom:
                    self.pos.y = wall.rect.bottom - self.hitbox_offset_y

                self.rect.x = int(self.pos.x) + self.hitbox_offset_x
                self.rect.y = int(self.pos.y) + self.hitbox_offset_y
                return  # Resolve only first collision
        self.update_pos()

    def recoil_on_damage(self, player_rect, max_recoil_distance=20, min_recoil_distance=10):
        #adds recoil when an enemy is damaged (when called)
        direction = self.pos - pygame.Vector2(player_rect.center)
        distance = direction.length()
        if distance > 0:
            direction = direction.normalize()
            recoil_strength = max(min(distance * 0.5, max_recoil_distance), min_recoil_distance)
            self.recoil_velocity = direction * recoil_strength
        else:
            self.recoil_velocity = pygame.Vector2(0, 0)

    def attack_player(self, player):
        #plays the attack animation
        if self.rect.colliderect(player.rect) and not self.attacking:
            self.attacking = True
            #plays random attack animation
            attack_num = random.randint(1, 2)
            #changes the current anim if 1 or 2 
            self.current_anim = self.attack_anim if attack_num == 1 else self.attack_anim_2
            self.attack_start_time = pygame.time.get_ticks()

        if self.attacking:
            attack_duration = 450
            if pygame.time.get_ticks() - self.attack_start_time >= attack_duration:
                #checks if  the attack duration is finished
                self.attacking = False
                self.current_anim = self.idle_anim

    def update(self, player, wall_group):
        #updates
        self.previous_pos = self.pos.copy()

        if self.dying:
            step_count = 5
            step_velocity = self.recoil_velocity / step_count
            for _ in range(step_count):
                self.pos += step_velocity
                self.check_wall_collision(wall_group)
            self.recoil_velocity *= 0.85

            if self.recoil_velocity.length_squared() < 0.1:
                self.dying = False
                self.dead = True
                self.enemy_death_channel.play(enemy_death_S)
                # Add corpse logic here if needed
                self.kill()
        else:
            if self.recoil_velocity.length_squared() > 0.01:
                step_count = 5
                step_velocity = self.recoil_velocity / step_count
                for _ in range(step_count):
                    self.pos += step_velocity
                    self.check_wall_collision(wall_group)
                self.recoil_velocity *= 0.6
            else:
                self.recoil_velocity = pygame.Vector2(0, 0)
                self.player_finding(player)
                self.attack_player(player)
                # self.wander_state() # Uncomment for idle wandering

            self.check_wall_collision(wall_group)

        self.image = self.get_frame()


# Runner subclass with movement and agro
class Runner(Enemy):
    def __init__(self, pos, speed, health, damage):
        # Pass animations directly to the Enemy constructor
        #subclass of the enemy class
        super().__init__(
            pos=pos,
            speed=speed,
            health=health,
            damage=damage,
            idle_anim=enemies["runner"]["idle"],
            run_anim=enemies["runner"]["run"],
            attack_anim=enemies["runner"]["attack"],
            attack_anim_2=enemies["runner"]["attack_2"],
            falling_frame=enemies["runner"]["falling"]
        )
        
    def movement(self, player):
        #runner movement set to chase player
        if self.found and not self.hit and not getattr(self, 'player_invunrable', False):
            self.current_anim = self.run_anim
            direction = pygame.Vector2(player.rect.center) - self.rect.center
            if direction.length_squared() != 0:
                direction = direction.normalize()
                self.pos += direction * self.speed
                self.update_direction(direction)
                self.update_pos()

    def movement_agro(self, player):
        #movement agro (when hit set to chase player)
        if self.hit and not getattr(self, 'player_invunrable', False):
            now = pygame.time.get_ticks()
            #checks if the alert duration is finished
            if now - self.alert_timer > self.alert_duration:
                self.hit = False
                self.alert_timer = 0
                self.alert = False
                self.found = False
            else:
                self.alert = True

            if self.alert:
                #if alert is true the current anim is run anim
                self.current_anim = self.run_anim
                direction = pygame.Vector2(player.rect.topright) - self.pos
                if direction.length_squared() != 0:
                    #updates pos and direction
                    direction = direction.normalize()
                    self.pos += direction * self.speed
                    self.update_direction(direction)
                    self.update_pos()


    def update(self, player, wall_group):
        #overrides previous update animation
        self.previous_pos = self.pos.copy()
        if self.dying:
            step_count = 5
            step_velocity = self.recoil_velocity / step_count
            for _ in range(step_count):
                self.pos += step_velocity
                self.check_wall_collision(wall_group)
                self.update_pos()
            self.recoil_velocity *= 0.85
            if self.recoil_velocity.length_squared() < 0.1:
                self.dying = False
                self.dead = True
                self.enemy_death_channel.play(enemy_death_S)
                corpse_x = self.rect.centerx - (enemies["runner"]["dead"].get_width() // 2)
                corpse_y = self.rect.centery - (enemies["runner"]["dead"].get_height() // 2)
                enemy_dead = Enemy_dead(corpse_x, corpse_y, self.facing_right)
                enemy_dead_group.add(enemy_dead)
                self.kill()
        else:
            if self.recoil_velocity.length_squared() > 0.01:
                step_count = 5
                step_velocity = self.recoil_velocity / step_count
                for _ in range(step_count):
                    self.pos += step_velocity
                    self.check_wall_collision(wall_group)
                    self.update_pos()
                self.recoil_velocity *= 0.6
            else:
                self.recoil_velocity = pygame.Vector2(0, 0)
                # Uncomment this if you want enemies to wander when idle
                # self.wander_state()
                self.player_finding(player)
                self.attack_player(player)
                if not self.attacking:
                    self.movement(player)
                    self.movement_agro(player)
                self.check_wall_collision(wall_group)
        self.image = self.get_frame()
