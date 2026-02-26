import pygame
import random
from assets import *
import math
from weapon_creation import *
from settings import *


shake_duration = 0
shake_magnitude = 0
shake_offset = [0, 0]

UI = False
shake_duration_UI = 0
shake_magnitude_UI = 0
shake_offset_UI = [0,0]

particles = pygame.sprite.Group()

mussle_anim_active = False
mouse_was_down_mussle = False


explosion_group = pygame.sprite.Group()


def mussle_flash_animation(screen, facing_right, pos,reloading,shooting):
    global mussle_anim_active, mouse_was_down_mussle

    #checks if shooting is active
    if shooting and not mussle_anim_active:
        #sets animation to true so can play one loop
        mussle_anim_active = True
        #sets the frame to the first one
        effects["muzzleflash"].frame_index = 0  # Restart animation

    #checks if animation active
    if mussle_anim_active:
        #updates the image if the cooldown has passed for the animation
        img = effects["muzzleflash"].update()

        #calculating angle mouse is at so can blit the image at that angle
        mx,my = pygame.mouse.get_pos()
        hx = pos[0]
        hy = pos[1]

        dx,dy = mx - hx,my - hy
        angle = math.degrees(math.atan2(-dy,dx))
        rad_angle = math.radians(angle)
        #offset applied to make it so it appears after the gun
        offset_x = math.cos(rad_angle) * 45
        offset_y = -math.sin(rad_angle) * 45
        hx = pos[0] +offset_x
        hy = pos[1] +offset_y

        
        if not facing_right:
            #flips if not player.facing_right
            img = pygame.transform.flip(img, False, True)


        #then it rotates the image based on the angle of the mouse from the player
        img = pygame.transform.rotate(img, angle)
        
        r = img.get_rect(center=(hx, hy))
        #sets color key again because if image is flipped need to apply again
        img.set_colorkey(BLACK)
        #blits the image
        screen.blit(img, r.topleft)

        # Stop animation when finished
        if effects["muzzleflash"].frame_index >= len(effects["muzzleflash"].frames) - 1:
            mussle_anim_active = False


def trigger_screenshake(duration, magnitude,UI):
    #applies the screenshake based on he values passed on the function
    global shake_duration, shake_magnitude,shake_duration_UI,shake_magnitude_UI
    if  UI == 0:
        shake_duration = duration
        shake_magnitude = magnitude
    if  UI == 1:
        shake_duration_UI = duration
        shake_magnitude_UI = magnitude


def update_screenshake(clock):
    #randomises the shake magnitude of the x and y to give a shake effect
    global shake_offset, shake_duration, shake_magnitude,shake_offset_UI,shake_duration_UI,shake_magnitude_UI
    if shake_duration > 0:
        shake_offset[0] = random.uniform(-shake_magnitude, shake_magnitude)
        shake_offset[1] = random.uniform(-shake_magnitude, shake_magnitude)
        shake_duration -= clock.get_time()
        #also applies to the UI screenshake
        shake_offset_UI[0] = random.uniform(-shake_magnitude_UI, shake_magnitude_UI)
        shake_offset_UI[1] = random.uniform(-shake_magnitude_UI, shake_magnitude_UI)
        shake_duration_UI -= clock.get_time()
    else:
        shake_offset = [0, 0]
        shake_offset_UI = [0,0]


def get_shake_offset(UI):
    #returns the shake offset
    if  UI == 0:
        return shake_offset
    else:
        return shake_offset_UI


class Particle(pygame.sprite.Sprite):#particle class to add particles
    def __init__(self, x, y, image, lifetime, offset_x, offset_y, rotation, rotation_speed, gravity, drag, vx, vy):
        super().__init__()
        #variables to change the way the particle moves
        self.x = x + offset_x
        self.y = y + offset_y
        self.original_image = image.convert_alpha()
        self.image = self.original_image.copy()

        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.rotation = rotation
        self.rotation_speed = rotation_speed

        self.vx = vx
        self.vy = vy
        self.gravity = gravity
        self.drag = drag

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        # Always update, even offscreen
        if self.lifetime <= 0:
            self.kill()  # Remove from group
            return

        self.lifetime -= 1

        # Physics
        self.vx *= self.drag
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

        # Rotation
        self.rotation += self.rotation_speed

        # Fade
        fade_start = self.max_lifetime * 0.25
        alpha = int(255 * (self.lifetime / fade_start)) if self.lifetime < fade_start else 255

        # Update image and rect
        rotated_image = pygame.transform.rotate(self.original_image, self.rotation)
        rotated_image.set_alpha(alpha)
        self.image = rotated_image
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def draw(self, screen, camera):
        #draws the effect on the camera
        screen_pos = camera.apply_pos((int(self.x), int(self.y)))
        screen.blit(self.image, self.image.get_rect(center=screen_pos))



def spawn_shell(x, y, image, facing_right,current_gun):
    #function to spawn the bullet shell
    for i in range(current_gun.number_of_bullets):
        lifetime = random.randint(30, 40)
        offset_x = random.randint(2, 5) if facing_right else random.randint(-5, -2)
        offset_y = random.randint(-10, 0)  # just a little above the gun
        rotation = random.uniform(0, 360)
        rotation_speed = random.uniform(-5, 5)
        gravity = 0.3
        drag = 0.98  
        vx = random.uniform(-5, 2) * random.choice([-1,1])
        vy = random.uniform(-8, -4)

        shell = Particle(x, y, image, lifetime, offset_x, offset_y, rotation,
                         rotation_speed, gravity, drag, vx, vy)
        particles.add(shell)


def spawn_smoke(x, y, image):
    #function for smoke
    lifetime = random.randint(10,15)
    offset_x =random.randint(0,5)
    offset_y =random.randint(-10,0)
    rotation = random.uniform(0, 360)
    rotation_speed = random.uniform(-5,5)
    gravity = 0.3
    drag = random.uniform(0.96,0.99)
    vx = random.uniform(-1.3,1.3) * random.choice([-1,1])
    vy = random.uniform(-1.5,-2.5)
    smoke = Particle(x, y, image, lifetime, offset_x, offset_y, rotation,rotation_speed,gravity,drag,vx,vy)
    particles.add(smoke)

    
def spawn_clip(x,y,image,facing_right):
    #function for spawning clip
    lifetime = random.randint(30, 40)
    offset_x = random.randint(2, 5) if facing_right else random.randint(-5, -2)
    offset_y = random.randint(-5,5)
    rotation = random.randint(0, 360)
    rotation_speed = random.uniform(-5,5)
    gravity = 0.3
    drag = 0.98
    vx = random.uniform(-5,2) * random.choice([-1,1])
    vy = random.uniform(-8,-4)
    clip = Particle(x, y, image, lifetime, offset_x, offset_y, rotation,rotation_speed,gravity,drag,vx,vy)
    particles.add(clip)

def spawn_blood(x, y, image, amount=5):
    #spawns blood particles
    for _ in range(amount):
        lifetime = random.randint(20, 50)
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)
        rotation = random.uniform(0, 360)
        rotation_speed = random.uniform(-2, 2)
        gravity = 0.2
        drag = 0.9

        # Random spread direction
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.5, 3.5)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed - 2  # initial burst slightly upward

        particle = Particle(x, y, image, lifetime, offset_x, offset_y, rotation,
                            rotation_speed, gravity, drag, vx, vy)
        particles.add(particle)
    

class Explosion(pygame.sprite.Sprite):
    #adds explosions 
    def __init__(self, x, y, angle, current_gun):
        super().__init__()
        
        if angle > 90 or angle < -90:
            self.offset_x = -20  # Left
        else:
            self.offset_x = 20   # Right
        self.offset_y = -90
        
        self.x = x + self.offset_x
        self.y = y + self.offset_y
        self.angle = angle
        self.current_gun = current_gun

        self.animation = effects["explosion"]

        self.image = self.animation.frames[0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):#updates the animation and kills them when ended
        self.image = self.animation.update()
        self.rect.topleft = (self.x, self.y)
        #self.image = pygame.transform.rotate(self.image, self.angle)

        if self.animation.frame_index >= len(self.animation.frames) - 1:
            self.kill()  # Automatically removes from all sprite groups


def blood_effect(screen, invulnerable, blood_alpha):
    #adds a blood vignette to the screen and slowly decreases it until alpha =0
    if invulnerable and blood_alpha > 0:
        img = effects["vignette"].copy()
        img.set_alpha(blood_alpha)
        screen.blit(img, (0, 0))

        blood_alpha -= 2.5
        blood_alpha = max(blood_alpha, 0)
    
    return blood_alpha
