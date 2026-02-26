import pygame
from assets import *

primary = True
secoundary = False
primary_B = False
secoundary_B = False

class Weapon:
    def __init__(self, name, price, speed, reload, reload_time, gun_image, bullet_image, bullet_shell_image,
                 number_of_bullets, spread, recoil, recoil_decay, damage, range_, distance, firerate, fire_type,
                 bounce, shoot_sound, reload_sound, empty_sound):
        self.name = name
        self.price = price
        self.speed = speed
        self.reload_size = reload
        self.current_reload = reload
        self.reload_time = reload_time
        self.gun_image = gun_image
        self.bullet_image = bullet_image
        self.bullet_shell_image = bullet_shell_image
        self.number_of_bullets = number_of_bullets
        self.spread = spread
        self.recoil = recoil
        self.recoil_decay = recoil_decay
        self.damage = damage
        self.range = range_
        self.distance = distance
        self.firerate = firerate
        self.type = fire_type
        self.bounce = bounce
        self.shoot_sound = shoot_sound
        self.reload_sound = reload_sound
        self.empty_sound = empty_sound


# === Weapon Instances ===
pistol = Weapon(
    name="Pistol", price=25,
    speed=26, reload=14, reload_time=472,   # pistol reload
    gun_image=weapons["Pistol"]["gun"], bullet_image=weapons["Pistol"]["bullet"], bullet_shell_image=weapons["Pistol"]["shell"],
    number_of_bullets=1, spread=2, recoil=15, recoil_decay=0.65, damage=1, range_=500, distance=1200,
    firerate=120, fire_type="single", bounce=0,
    shoot_sound=pistol_shoot_S, reload_sound=pistol_reload_S, empty_sound=pistol_empty_S
)

shotgun = Weapon(
    name="Shotgun", price=75,
    speed=28, reload=14, reload_time=1000,   # shotgun reload
    gun_image=weapons["Shotgun"]["gun"], bullet_image=weapons["Shotgun"]["bullet"], bullet_shell_image=weapons["Shotgun"]["shell"],
    number_of_bullets=5, spread=20, recoil=40, recoil_decay=0.55, damage=3, range_=350, distance=800,
    firerate=300, fire_type="single", bounce=0,
    shoot_sound=Shotgun_shoot, reload_sound=Shotgun_reload, empty_sound=pistol_empty_S
)

ak47 = Weapon(
    name="AK47", price=1,
    speed=35, reload=14, reload_time=1500,   # automatic reload
    gun_image=weapons["AK47"]["gun"], bullet_image=weapons["AK47"]["bullet"], bullet_shell_image=weapons["AK47"]["shell"],
    number_of_bullets=1, spread=5, recoil=30, recoil_decay=0.55, damage=1, range_=500, distance=1000,
    firerate=100, fire_type="automatic", bounce=0,
    shoot_sound=pistol_shoot_S, reload_sound=AK47_reload, empty_sound=pistol_empty_S
)

sniper = Weapon(
    name="Sniper", price=150,
    speed=50, reload=14, reload_time=1600,   # sniper reload
    gun_image=weapons["SniperRifle"]["gun"], bullet_image=weapons["SniperRifle"]["bullet"], bullet_shell_image=weapons["SniperRifle"]["shell"],
    number_of_bullets=1, spread=0, recoil=50, recoil_decay=0.6, damage=15, range_=800, distance=3000,
    firerate=800, fire_type="single", bounce=0,
    shoot_sound=Sniper_shoot, reload_sound=Sniper_reload, empty_sound=pistol_empty_S
)

deagle = Weapon(
    name="Desert Eagle", price=90,
    speed=28, reload=14, reload_time=472,   # pistol reload
    gun_image=weapons["DesertEagle"]["gun"], bullet_image=weapons["DesertEagle"]["bullet"], bullet_shell_image=weapons["DesertEagle"]["shell"],
    number_of_bullets=1, spread=3, recoil=30, recoil_decay=0.55, damage=4, range_=450, distance=1200,
    firerate=200, fire_type="single", bounce=0,
    shoot_sound=DesertEagle_shoot, reload_sound=DesertEagle_reload, empty_sound=pistol_empty_S
)

uzi = Weapon(
    name="UZI", price=80,
    speed=32, reload=14, reload_time=1500,   # automatic reload
    gun_image=weapons["UZI"]["gun"], bullet_image=weapons["UZI"]["bullet"], bullet_shell_image=weapons["UZI"]["shell"],
    number_of_bullets=1, spread=7, recoil=20, recoil_decay=0.7, damage=1, range_=300, distance=600,
    firerate=80, fire_type="automatic", bounce=0,
    shoot_sound=SMG_shoot, reload_sound=SMG_reload, empty_sound=pistol_empty_S
)

scar = Weapon(
    name="SCAR", price=130,
    speed=33, reload=14, reload_time=1500,   # automatic reload
    gun_image=weapons["SCAR"]["gun"], bullet_image=weapons["SCAR"]["bullet"], bullet_shell_image=weapons["SCAR"]["shell"],
    number_of_bullets=1, spread=4, recoil=28, recoil_decay=0.6, damage=2, range_=700, distance=1100,
    firerate=180, fire_type="automatic", bounce=0,
    shoot_sound=pistol_shoot_S, reload_sound=AK47_reload, empty_sound=pistol_empty_S
)

machinegun = Weapon(
    name="Machine Gun", price=150,
    speed=34, reload=14, reload_time=1500,   # automatic reload
    gun_image=weapons["MachineGun"]["gun"], bullet_image=weapons["MachineGun"]["bullet"], bullet_shell_image=weapons["MachineGun"]["shell"],
    number_of_bullets=1, spread=8, recoil=45, recoil_decay=0.5, damage=1.5, range_=500, distance=1100,
    firerate=60, fire_type="automatic", bounce=0,
    shoot_sound=SMG_shoot, reload_sound=SMG_reload, empty_sound=pistol_empty_S
)

bulldawk = Weapon(
    name="Bulldawk", price=100,
    speed=28, reload=14, reload_time=1000,   # shotgun reload
    gun_image=weapons["Bulldawk"]["gun"], bullet_image=weapons["Bulldawk"]["bullet"], bullet_shell_image=weapons["Bulldawk"]["shell"],
    number_of_bullets=4, spread=35, recoil=35, recoil_decay=0.6, damage=4, range_=400, distance=850,
    firerate=300, fire_type="single", bounce=0,
    shoot_sound=Shotgun_shoot, reload_sound=Shotgun_reload, empty_sound=pistol_empty_S
)

facecleaver = Weapon(
    name="Face Cleaver", price=110,
    speed=26, reload=14, reload_time=1000,   # shotgun reload
    gun_image=weapons["FaceCleaver"]["gun"], bullet_image=weapons["FaceCleaver"]["bullet"], bullet_shell_image=weapons["FaceCleaver"]["shell"],
    number_of_bullets=6, spread=40, recoil=50, recoil_decay=0.5, damage=6, range_=350, distance=700,
    firerate=400, fire_type="single", bounce=0,
    shoot_sound=Shotgun_shoot, reload_sound=Shotgun_reload, empty_sound=pistol_empty_S
)

echo_rail = Weapon(
    name="EchoRail", price=200,
    speed=55, reload=14, reload_time=1600,   # sniper reload
    gun_image=weapons["EchoRail"]["gun"], bullet_image=weapons["EchoRail"]["bullet"], bullet_shell_image=weapons["EchoRail"]["shell"],
    number_of_bullets=1, spread=0, recoil=55, recoil_decay=0.55, damage=20, range_=1000, distance=3000,
    firerate=600, fire_type="single", bounce=6,
    shoot_sound=Sniper_shoot, reload_sound=Sniper_reload, empty_sound=pistol_empty_S
)

rattleback = Weapon(
    name="Rattleback", price=140,
    speed=34, reload=14, reload_time=1500,   # automatic reload
    gun_image=weapons["Rattleback"]["gun"], bullet_image=weapons["Rattleback"]["bullet"], bullet_shell_image=weapons["Rattleback"]["shell"],
    number_of_bullets=1, spread=6, recoil=32, recoil_decay=0.55, damage=1, range_=600, distance=1000,
    firerate=90, fire_type="automatic", bounce=2,
    shoot_sound=pistol_shoot_S, reload_sound=AK47_reload, empty_sound=pistol_empty_S
)

revolver = Weapon(
    name="Revolver", price=85,
    speed=29, reload=14, reload_time=472,   # pistol reload
    gun_image=weapons["revolver"]["gun"], bullet_image=weapons["revolver"]["bullet"], bullet_shell_image=weapons["revolver"]["shell"],
    number_of_bullets=1, spread=2, recoil=35, recoil_decay=0.55, damage=6, range_=500, distance=1200,
    firerate=250, fire_type="single", bounce=0,
    shoot_sound=pistol_shoot_S, reload_sound=pistol_reload_S, empty_sound=pistol_empty_S
)

boomer = Weapon(
    name="Boomer", price=125,
    speed=30, reload=14, reload_time=1000,   # shotgun-style reload (since it shoots multiple)
    gun_image=weapons["boomer"]["gun"], bullet_image=weapons["boomer"]["bullet"], bullet_shell_image=weapons["boomer"]["shell"],
    number_of_bullets=2, spread=40, recoil=28, recoil_decay=0.6, damage=7, range_=450, distance=1000,
    firerate=220, fire_type="single", bounce=1,
    shoot_sound=pistol_shoot_S, reload_sound=pistol_reload_S, empty_sound=pistol_empty_S
)

# === Weapon Shop ===
weapon_shop = [
    pistol, shotgun, ak47, sniper, deagle, uzi, scar, machinegun, bulldawk, facecleaver,
    echo_rail, rattleback, revolver, boomer
]





primary_gun =pistol
secoundary_gun = uzi

#starting
current_gun = primary_gun

def update_assets(dash_cooldown,current_gun):
    #update assets according to stats
    
    ui["crosshair"]["reload"].cooldown = current_gun.reload_time / len(ui["crosshair"]["reload"].frames)
    if current_gun.firerate <= 150:
        ui["crosshair"]["shoot"].cooldown = current_gun.firerate / len(ui["crosshair"]["shoot"].frames)
    
    effects["muzzleflash"].cooldown = current_gun.firerate / len(effects["muzzleflash"].frames)
    if effects["muzzleflash"].cooldown > 100:
        effects["muzzleflash"].cooldown = 50
    ui["dash_cooldown"].cooldown = dash_cooldown / len(ui["dash_cooldown"].frames)




def gun_switching(event_list,current_gun,primary_gun,secoundary_gun,primary,secoundary):


    for event in event_list:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                gun_switching_S.play()
                current_gun = primary_gun
                primary = True
                secoundary = False

            elif event.key == pygame.K_2:
                gun_switching_S.play()
                current_gun = secoundary_gun
                secoundary = True
                primary = False

    return current_gun, primary, secoundary
