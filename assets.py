import pygame
import os
from settings import *

# --- CONSTANTS ---
BLACK = (0, 0, 0)
BG = (60, 60, 60)

# --- CORE CLASSES ---
class Spritesheet:
    def __init__(self, image):
        self.sheet = image
    #this uses the w,h to cut out the spritesheet into seperate frames applying colour key and scale effects
    def get_image(self, frame, w, h, scale, colorkey=None, use_colorkey=False):
        image = pygame.Surface((w, h), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (frame * w, 0, w, h))
        image = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
        if use_colorkey:
            image.set_colorkey(colorkey)
        return image


class AnimationController:#used to add a cooldown between frames and updates them
    def __init__(self, frames, cooldown):
        self.frames = frames
        self.cooldown = cooldown
        self.last_update = pygame.time.get_ticks()
        self.frame_index = 0

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.cooldown:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_update = now
        return self.frames[self.frame_index]

# --- GLOBAL ASSET DICTIONARIES ---
weapons = {}
player = {}
enemies = {}
effects = {}
ui = {}

# --- HELPER FUNCTIONS ---

def load_spritesheet_frames(sheet_img, frame_count, w, h, scale, colorkey, use_colorkey):
    #helper function
    sheet = Spritesheet(sheet_img)
    return [sheet.get_image(i, w, h, scale, colorkey, use_colorkey) for i in range(frame_count)]





# --- MAIN LOADER ---

weapons = {
    "Pistol": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/pistol.png").convert_alpha(), 1, 40, 30, 2.5, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/pistol bullets.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/pistol shells.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
    "DesertEagle": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/DesertEagle.png").convert_alpha(), 1, 40, 30, 3, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/pistol bullets.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/pistol shells.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
    "UZI": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/UZI.png").convert_alpha(), 1, 40, 30, 3, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/pistol bullets.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/pistol shells.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
    "AK47": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/AK47.png").convert_alpha(), 1, 40, 30, 3, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/automatic bullets.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/automatic shells.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
    "SCAR": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/SCAR.png").convert_alpha(), 1, 40, 30, 3, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/automatic bullets.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/automatic shells.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
    "MachineGun": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/MachineGun.png").convert_alpha(), 1, 40, 30, 3, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/automatic bullets.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/automatic shells.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
    "Bulldawk": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/Bulldawk.png").convert_alpha(), 1, 40, 30, 3, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/shotgun bullets.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/shotgun shells.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
    "Shotgun": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/Shotgun.png").convert_alpha(), 1, 40, 30, 3, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/shotgun bullets.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/shotgun shells.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
    "FaceCleaver": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/FaceCleaver.png").convert_alpha(), 1, 40, 30, 3, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/shotgun bullets.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/shotgun shells.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
    "SniperRifle": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/SniperRifle.png").convert_alpha(), 1, 40, 30, 3, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/sniper bullet.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/sniper shell.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
    "EchoRail": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/EchoRail.png").convert_alpha(), 1, 40, 30, 3, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/sniper bullet.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/sniper shell.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
    "Rattleback": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/Rattleback.png").convert_alpha(), 1, 40, 30, 3, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/automatic bullets.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/automatic shells.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
    "revolver": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/revolver.png").convert_alpha(), 1, 40, 30, 3, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/pistol bullets.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/pistol shells.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
    "boomer": {
        "gun": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/boomer.png").convert_alpha(), 1, 40, 30, 3, BLACK, False)[0],
        "bullet": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/pistol bullets.png").convert_alpha(), 1, 8, 5, 10, BLACK, False)[0],
        "shell": load_spritesheet_frames(pygame.image.load(r"sprites/weapons/pistol shells.png").convert_alpha(), 1, 5, 5, 7, BLACK, False)[0]
    },
}
        

player_ = {
    "player1": {
        "idle": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/player/player1.png").convert_alpha(), 4, 24, 24, 4.5, BLACK, True), 75
        ),
        "run": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/player/player1.png").convert_alpha(), 11, 24, 24, 4.5, BLACK, True)[4:11], 75
        ),
        "shadow": load_spritesheet_frames(pygame.image.load(r"sprites/player/medium_shadow.png").convert_alpha(), 1, 16, 10, 3.5, BLACK, False)[0]
    }
}

enemies = {
    "runner": {
        "idle": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/ENEMY/xeno-grunt-idle.png").convert_alpha(), 2, 64, 64, 4.5, BLACK, True), 100
        ),
        "run": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/ENEMY/xeno-grunt-run.png").convert_alpha(), 8, 64, 64, 4.5, BLACK, True), 75
        ),
        "attack": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/ENEMY/xeno-grunt-attack-1.png").convert_alpha(), 9, 64, 64, 4.5, BLACK, True), 50
        ),
        "attack_2": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/ENEMY/xeno-grunt-attack-2.png").convert_alpha(), 8, 64, 64, 4.5, BLACK, True), 50
        ),
        "falling": load_spritesheet_frames(pygame.image.load(r"sprites/ENEMY/xeno-grunt-knockback.png").convert_alpha(), 1, 64, 64, 4.5, BLACK, True)[0],
        "dead": load_spritesheet_frames(pygame.image.load(r"sprites/ENEMY/xeno-grunt-death-grounded.png").convert_alpha(), 1, 64, 64, 4.5, BLACK, True)[0]
    }
}

effects = {
    "muzzleflash": AnimationController(
        load_spritesheet_frames(pygame.image.load(r"sprites/effects/mussleflash.png").convert_alpha(), 6, 10, 10, 8, BLACK, False), 25
    ),
    "explosion": AnimationController(
        load_spritesheet_frames(pygame.image.load(r"sprites/effects/explosion.png").convert_alpha(), 5, 20, 20, 9, BLACK, False), 65
    ),
    "fade in": AnimationController(
        load_spritesheet_frames(pygame.image.load(r"sprites/effects/fade in.png").convert_alpha(), 21, 384, 216, 5, BLACK, False), 40
    ),
    "fade out": AnimationController(
        load_spritesheet_frames(pygame.image.load(r"sprites/effects/fade out.png").convert_alpha(), 21, 384, 216, 5, BLACK, False),40
        
    ),
    "smoke": load_spritesheet_frames(pygame.image.load(r"sprites/effects/smoke.png").convert_alpha(), 1, 10, 10, 5, BLACK, True)[0],
    "clip": load_spritesheet_frames(pygame.image.load(r"sprites/effects/clip.png").convert_alpha(), 1, 10, 10, 5, BLACK, False)[0],
    "spark": load_spritesheet_frames(pygame.image.load(r"sprites/effects/spark.png").convert_alpha(), 1, 5, 5, 20, BLACK, False)[0],
    "blood": load_spritesheet_frames(pygame.image.load(r"sprites/effects/blood.png").convert_alpha(), 1, 5, 5, 15, BLACK, False)[0],
    "vignette": load_spritesheet_frames(pygame.image.load(r"sprites/effects/red overlay.png").convert_alpha(), 1, 640, 400, 3, BLACK, False)[0],
    
}

ui = {
    "crosshair": {
        "idle": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/UI/crosshairidle.png").convert_alpha(), 4, 50, 50, 2.5, BLACK, True), 80
        ),
        "shoot": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/UI/crosshairshooting.png").convert_alpha(), 5, 75, 75, 2.5, BLACK, True), 30
        ),
        "reload": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/UI/crosshairreload.png").convert_alpha(), 12, 50, 50, 2.5, BLACK, True), 34
        ),
        "empty": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/UI/reloadfail.png").convert_alpha(), 5, 75, 75, 2.5, BLACK, True), 40
        )
    },
    "ammo": AnimationController(
        load_spritesheet_frames(pygame.image.load(r"sprites/UI/ammoUI.png").convert_alpha(), 14, 75, 50, 5, BLACK, False), 100
    ),
    "health_profile": AnimationController(
        load_spritesheet_frames(pygame.image.load(r"sprites/UI/player_health_profile.png").convert_alpha(), 3, 100, 100, 5, BLACK, False), 100
    ),
    "health_bar": AnimationController(
        load_spritesheet_frames(pygame.image.load(r"sprites/UI/healthbar.png").convert_alpha(), 10, 75, 50, 5, BLACK, False), 100
    ),
    "dash_cooldown": AnimationController(
        load_spritesheet_frames(pygame.image.load(r"sprites/UI/dash_cooldown_UI.png").convert_alpha(), 10, 40, 40, 5, BG, True), 100
    ),
    "gun_ui": AnimationController(
        load_spritesheet_frames(pygame.image.load(r"sprites/UI/gun_UI.png").convert_alpha(), 2, 80, 80, 4, BG, True), 100
    ),
    "coin_UI": AnimationController(
        load_spritesheet_frames(pygame.image.load(r"sprites/items/coin.png").convert_alpha(), 5, 10, 10, 10, BG, True), 100
    ),
    "menu": {
        "play_button": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/UI/play_button.png").convert_alpha(), 3, 141, 21, 2.5, BG, True), 100
        ),
        "exit_button": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/UI/exit_button.png").convert_alpha(), 3, 72, 21, 2.5, BG, True), 100
        ),
        "highscore_button": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/UI/highscore_button.png").convert_alpha(), 3, 159, 21, 2.5, BG, True), 100
        ),
        "settings_button": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/UI/Settings.png").convert_alpha(), 3, 150, 21, 2.5, BG, True), 100
        )
    },
    "shop": {
        "shop_sign": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/UI/shop sign.png").convert_alpha(), 3, 141, 21, 2.5, BG, True), 100
        ),
        "highscore_button": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/UI/highscore_button.png").convert_alpha(), 3, 159, 21, 2.5, BG, True), 100
        ),
        "settings_button": AnimationController(
            load_spritesheet_frames(pygame.image.load(r"sprites/UI/Settings.png").convert_alpha(), 3, 150, 21, 2.5, BG, True), 100
        )
    }
}


textures = {
    "floor_texture": load_spritesheet_frames(pygame.image.load(r"sprites/textures/floor tile.png").convert_alpha(), 1, 20, 20, 5, BLACK, True)[0],
    "right_wall": load_spritesheet_frames(pygame.image.load(r"sprites/textures/wall tileset.png").convert_alpha(), 5, 20, 20, 5, BLACK, True)[0],
    "bottom_wall": load_spritesheet_frames(pygame.image.load(r"sprites/textures/wall tileset.png").convert_alpha(), 5, 20, 20, 5, BLACK, True)[1],
    "left_wall": load_spritesheet_frames(pygame.image.load(r"sprites/textures/wall tileset.png").convert_alpha(), 5, 20, 20, 5, BLACK, True)[2],
    "top_wall": load_spritesheet_frames(pygame.image.load(r"sprites/textures/wall tileset.png").convert_alpha(), 5, 20, 20, 5, BLACK, True)[3],
    "wall_texture": load_spritesheet_frames(pygame.image.load(r"sprites/textures/wall texture.png").convert_alpha(), 1, 30, 30, 3.3, BLACK, True)[0],
    
}



font = pygame.font.Font(r"sprites/UI/font.otf", 70)

# ============================================================================
# AUDIO

# Audio Channels  ( some are defined in functions or in classes
game_music_channel = pygame.mixer.Channel(20)
fade_channel = pygame.mixer.Channel(19)

# Music
game_music = pygame.mixer.Sound("audio/Game_music.wav")

# Player Audio
player_footstep = pygame.mixer.Sound("audio/player/footsteps.mp3")
dash_S = pygame.mixer.Sound("audio/player/dash.mp3")

# Enemy Audio
enemy_death_S = pygame.mixer.Sound("audio/enemy/enemy_death_SFX.mp3")
enemy_hurt_S = pygame.mixer.Sound("audio/enemy/enemyHurt.wav")

# Weapon Audio
pistol_shoot_S = pygame.mixer.Sound("audio/pistol/Pistol Fire 3.mp3")
pistol_reload_S = pygame.mixer.Sound("audio/pistol/Pistol Reload.wav")
pistol_empty_S = pygame.mixer.Sound("audio/pistol/Pistol Empty.wav")

# General Audio Effects
explosion_S = pygame.mixer.Sound("audio/other/explosion.wav")
HitHurt_S = pygame.mixer.Sound("audio/other/HitHurt.wav")
gun_switching_S = pygame.mixer.Sound("audio/other/gun_switching.wav")
ambient_noise_s = pygame.mixer.Sound("audio/other/ambient_noise_1.mp3")
heartbeat_S = pygame.mixer.Sound("audio/other/hearbeat.mp3")
fade_out_S = pygame.mixer.Sound("audio/other/transition sound.wav")
fade_in_S = pygame.mixer.Sound("audio/other/transition sound 2.wav")





SMG_reload = pygame.mixer.Sound("audio/weapons/SMG reload.mp3")
SMG_shoot = pygame.mixer.Sound("audio/weapons/SMG shoot.mp3")
DesertEagle_shoot =pygame.mixer.Sound("audio/weapons/DesertEagle shoot.mp3")
DesertEagle_reload =pygame.mixer.Sound("audio/weapons/DesertEagle reload.mp3")
AK47_shoot =pygame.mixer.Sound("audio/weapons/AK47 shoot.mp3")
AK47_reload =pygame.mixer.Sound("audio/weapons/AK47 reload.mp3")
Shotgun_shoot =pygame.mixer.Sound("audio/weapons/Shotgun shot.mp3")
Shotgun_reload =pygame.mixer.Sound("audio/weapons/Shotgun reload.mp3")
Sniper_shoot =pygame.mixer.Sound("audio/weapons/Sniper shot.mp3")
Sniper_reload = pygame.mixer.Sound("audio/weapons/Sniper reload.mp3")


