import pygame
from assets import *
from weapon import *
from weapon_creation import *
from effects import *
import math
import random
import time
from enemy_spawning import *
#globals


#cursor
Mouse_shooting = False
reload_mouse = False
gun_empty = False

dash_animation = True

previous_score = 0
score_anim_timer = 0

#overlay
overlay_low = None
overlay = None

gun_upgrades = [
    {
        "name": "Increase Damage",
        "cost": 100,
        "effect": lambda guns: [
            setattr(gun, "damage", gun.damage + 1) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Faster Fire Rate",
        "cost": 120,
        "effect": lambda guns: [
            setattr(gun, "firerate", max(gun.firerate - 3, 1)) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Reduce Recoil",
        "cost": 90,
        "effect": lambda guns: [
            setattr(gun, "recoil", max(gun.recoil - 0.5, 0)) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Increase Recoil",
        "cost": 90,
        "effect": lambda guns: [
            setattr(gun, "recoil", gun.recoil + 0.5) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Increase Bullets",
        "cost": 80,
        "effect": lambda guns: [
            setattr(gun, "number_of_bullets", gun.number_of_bullets + 1) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Reduce Spread",
        "cost": 100,
        "effect": lambda guns: [
            setattr(gun, "spread", max(gun.spread - 0.5, 0)) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Increase Spread",
        "cost": 100,
        "effect": lambda guns: [
            setattr(gun, "spread", gun.spread + 0.5) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Toggle Fire Type",
        "cost": 150,
        "effect": lambda guns: [
            setattr(gun, "type", "automatic" if gun.type == "single" else "single")
            for gun in guns if gun is not None
        ]
    }
]


gun_upgrades.extend([
    {
        "name": "Increase Bounce",
        "cost": 110,
        "effect": lambda guns: [
            setattr(gun, "bounce", gun.bounce + 1) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Reduce Bounce",
        "cost": 90,
        "effect": lambda guns: [
            setattr(gun, "bounce", max(gun.bounce - 1, 0)) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Increase Range",
        "cost": 120,
        "effect": lambda guns: [
            setattr(gun, "distance", gun.distance + 50) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Reduce Range",
        "cost": 100,
        "effect": lambda guns: [
            setattr(gun, "distance", max(gun.distance - 50, 1)) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Increase Bullet Speed",
        "cost": 130,
        "effect": lambda guns: [
            setattr(gun, "speed", gun.speed + 2) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Reduce Bullet Speed",
        "cost": 110,
        "effect": lambda guns: [
            setattr(gun, "speed", max(gun.speed - 2, 1)) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Faster Fire Rate",
        "cost": 150,
        "effect": lambda guns: [
            setattr(gun, "firerate", max(gun.firerate - 2, 1)) for gun in guns if gun is not None
        ]
    },
    {
        "name": "Slower Fire Rate",
        "cost": 120,
        "effect": lambda guns: [
            setattr(gun, "firerate", gun.firerate + 2) for gun in guns if gun is not None
        ]
    }
])
# Player upgrades
player_upgrades = [
    {
        "name": "Speed +1",
        "cost": 50,
        "effect": lambda player: setattr(player, "speed", player.speed + 1)
    },
    {
        "name": "Speed +2",
        "cost": 100,
        "effect": lambda player: setattr(player, "speed", player.speed + 2)
    },
    {
        "name": "Heal to Max",
        "cost": 75,
        "effect": lambda player: setattr(player, "health", player.max_health)
    },
    {
        "name": "Dash Cooldown -100ms",
        "cost": 80,
        "effect": lambda player: setattr(player, "dash_cooldown", max(0.1, player.dash_cooldown - 100))
    }
]


def DrawMouse(screen, shooting,shot_attempted,has_enough_ammo):
    global Mouse_shooting, reload_mouse, gun_empty

    #checks if mouse input
    mouse_down = pygame.mouse.get_pressed()[0]
    #gets the mouse position
    mx, my = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    reloading = keys[pygame.K_r]

    # Handle reload animation
    if reloading and not reload_mouse and not shooting:
        reload_mouse = True
        ui["crosshair"]["reload"].frame_index = 0

    if reload_mouse:
        img = ui["crosshair"]["reload"].update()
        screen.blit(img, img.get_rect(center=(mx, my)))
        if ui["crosshair"]["reload"].frame_index >= len(ui["crosshair"]["reload"].frames) - 1:
            reload_mouse = False
        return

    # Handle empty gun animation if player tried to shoot with no ammo
    if shot_attempted and not has_enough_ammo and not Mouse_shooting:
        if not gun_empty:
            gun_empty = True
            ui["crosshair"]["empty"].frame_index = 0
            current_gun.empty_sound.play()

    if gun_empty:
        img = ui["crosshair"]["empty"].update()
        screen.blit(img, img.get_rect(center=(mx, my)))
        if ui["crosshair"]["empty"].frame_index >= len(ui["crosshair"]["empty"].frames) - 1:
            gun_empty = False
        return

    # Handle shooting animation (purely visual)
    if shooting and not reload_mouse:
        if not Mouse_shooting:
            Mouse_shooting = True
            ui["crosshair"]["shoot"].frame_index = 0

    if Mouse_shooting:
        img = ui["crosshair"]["shoot"].update()
        if ui["crosshair"]["shoot"].frame_index >= len(ui["crosshair"]["shoot"].frames) - 1:
            Mouse_shooting = False
    else:
        img = ui["crosshair"]["idle"].update()
        
    #then blits depending on the image used and the pos of the mouse
    screen.blit(img, img.get_rect(center=(mx, my)))


def DashRechargeUI(screen, player):
    global dash_animation
    now = pygame.time.get_ticks()

    # just updates the dash animation
    image = ui["dash_cooldown"].frames[-1]

    # Dash is still cooling down
    if now - player.dash_start < player.dash_cooldown:
        elapsed = now - player.dash_start
        cooldown_ratio = elapsed / player.dash_cooldown
        frame_index = int(cooldown_ratio * len(ui["dash_cooldown"].frames))
        frame_index = min(frame_index, len(ui["dash_cooldown"].frames) - 1)
        image = ui["dash_cooldown"].frames[frame_index]

    screen.blit(image, (860, -40))


def AmmoDecreaseUI(screen,offsetx,offsety,current_gun):
    #the ui for the ammo which is synced with current_gun.current_reload
    max_ammo = current_gun.reload_size
    current_ammo = current_gun.current_reload
    index = max_ammo - current_ammo
    img = ui["ammo"].frames[index]
    screen.blit(img,(50+offsetx,25+offsety))

def HealthDecreaseUI(screen,max_health,health,offsetx,offsety):
    #changes the health UI based on the health of the player class
    #also changes the health profile based on how much health is left
    index = max_health - health
    if health >= max_health * 0.75:
        img2 = ui["health_profile"].frames[0]
    elif health < max_health * 0.75 and health > max_health * 0.25:
        img2 = ui["health_profile"].frames[1]
    elif health <= max_health * 0.25:
        img2 = ui["health_profile"].frames[2]
        
    img = ui["health_bar"].frames[index]
    screen.blit(img,(80+offsetx,-35+offsety))
    screen.blit(img2,(-160+offsetx,-160+offsety))

def Gun_UI(screen, primary, secondary, current_gun):
    #the gun ui is used to display which gun is being used
    if primary and not secondary:
        img = ui["gun_ui"].frames[0]
        slot_rect = pygame.Rect(-45, 840, img.get_width(), img.get_height())  # slot position
    elif secondary and not primary:
        img = ui["gun_ui"].frames[1]
        slot_rect = pygame.Rect(112, 840, img.get_width(), img.get_height())

    # Scale gun image
    gun_img = current_gun.gun_image
    width, height = gun_img.get_size()
    gun_img = pygame.transform.scale(gun_img, (int(width * 1.5), int(height * 1.5)))

    # Center gun in slot
    gun_rect = gun_img.get_rect(center=slot_rect.center)

    # Draw UI and gun
    screen.blit(img, (30, 850))
    screen.blit(gun_img, gun_rect.topleft)


def CreatePixelatedOverlay(screen_size,range_, pixel_factor=5, overshoot=40,
                            gradient_detail=8, center_alpha=0,):
    #pixelated overlay creates a surface adding a fading graphic based on the range of the current gun
    global overlay_low, full_size, overshoot_amount
    fade_zone_ratio = range_ * 0.00134

    #overshoots a bit so its fully on screen
    overshoot_amount = overshoot
    full_size = (screen_size[0] + overshoot, screen_size[1] + overshoot)

    low_res_size = (full_size[0] // pixel_factor, full_size[1] // pixel_factor)
    overlay_low = pygame.Surface(low_res_size, pygame.SRCALPHA)

    center_x = low_res_size[0] / 2
    center_y = low_res_size[1] / 2
    max_dist = math.hypot(center_x, center_y)

    fade_radius = max_dist * fade_zone_ratio  # size of fading area near center
    #adds a circle fade effect
    for y in range(0, low_res_size[1], gradient_detail):
        for x in range(0, low_res_size[0], gradient_detail):
            dist = math.hypot(x - center_x, y - center_y)

            if dist > fade_radius:
                alpha = 255  # solid black outside fade zone
            else:
                t = dist / fade_radius  # 0 at center, 1 at fade edge
                alpha = int(center_alpha + (255 - center_alpha) * t)

            block_rect = pygame.Rect(x, y, gradient_detail, gradient_detail)
            overlay_low.fill((15, 17, 48, alpha), block_rect)


def CutTransparentHole(world_pos, radius, pixel_factor=5, feather=10):
    global overlay_low
    #just cuts a circle in the overlay surface and the alpha is set to 0

    if overlay_low is None:
        return
    
    screen_pos = camera.apply_pos(world_pos)

    adjusted_pos = (
        int((screen_pos[0] + overshoot_amount // 2) // pixel_factor),
        int((screen_pos[1] + overshoot_amount // 2) // pixel_factor)
    )

    max_radius = radius // pixel_factor
    inner_radius = max_radius - feather
    if inner_radius < 0:
        inner_radius = 0

    # Draw fully transparent inner circle to "cut out"  in the overlay
    pygame.draw.circle(overlay_low, (0, 0, 0, 0), adjusted_pos, inner_radius)


def DrawOverlay(screen, screen_size, offset_x, offset_y, pixel_factor=5):
    global overlay_low, overlay, full_size, overshoot_amount
    #then blits everything on the overlay

    if overlay_low is None:
        return

    # Scale the low-res overlay up to full size
    overlay = pygame.transform.scale(overlay_low, full_size)

    # Draw overlay with offset adjusted by half of the overshoot
    draw_x = -offset_x - overshoot_amount // 2
    draw_y = -offset_y - overshoot_amount // 2
    screen.blit(overlay, (draw_x, draw_y))

def is_enemy_visible(player_center, light_radius, enemy_center):
    #distance = (pygame.Vector2(player_center) - pygame.Vector2(enemy_center)).length()
    #return distance <= light_radius
    return True


def fade_out(screen, fade_out_b):
    if fade_out_b:
        # get current frame from animation
        img = effects["fade out"].update()
        # center it on screen (assuming your surface matches screen size)
        rect = img.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
        screen.blit(img, rect)
        
        if effects["fade out"].frame_index == len(effects["fade out"].frames) - 1:
            fade_out_b = False  # fade done
        return fade_out_b
def fade_in(screen, fade_in_b):
    if fade_in_b:
        # get current frame from "fade in" animation
        img = effects["fade in"].update()
        rect = img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(img, rect)

        # check if fade in finished using the right animation
        if effects["fade in"].frame_index == len(effects["fade in"].frames) - 1:
            fade_in_b = False  # fade done
        return fade_in_b
    
    return fade_in_b

def score_display(score, screen, font, previous_score):
    global score_anim_timer
    score = round(score)

    screen_width = screen.get_width()
    top_y = 160  # distance from top

    if previous_score is None:
        previous_score = score

    if score != previous_score:
        score_anim_timer = 20
        previous_score = score

    text_surface = font.render(str(score), True, (255, 255, 255))

    if score_anim_timer > 0:
        scale_factor = 2 + random.uniform(-0.5, 1.0)
        angle = random.uniform(-15, 15)

        # Small vertical offset for animation
        offset_y = random.randint(1, 3)

        # Apply rotation and scaling
        text_surface = pygame.transform.rotozoom(text_surface, angle, scale_factor)

        # Center top horizontally
        text_rect = text_surface.get_rect(center=(screen_width // 2, top_y + offset_y))
        screen.blit(text_surface, text_rect)

        score_anim_timer -= 1
    else:
        # Scale normally (doubling size)
        scaled_surface = pygame.transform.scale(text_surface, (text_surface.get_width() * 2, text_surface.get_height() * 2))

        # Center top horizontally
        text_rect = scaled_surface.get_rect(center=(screen_width // 2, top_y))
        screen.blit(scaled_surface, text_rect)

    return previous_score

font = pygame.font.Font(r"sprites/UI/font.otf", 100)

def money_display(screen,money):
    #just displays the money and the coin rotating animation
    coin_img = ui["coin_UI"].update()
    screen_width = screen.get_width()
    top_y = 50

    text_surface = font.render(str(money),True,(255,255,255))
    text_rect = text_surface.get_rect(center=(1920 -(screen_width // 16),top_y))
    
    screen.blit(text_surface,text_rect)
    screen.blit(coin_img,(1830,10))
    

def draw_button(screen, rect, image, hover_image, click_image):
    mouse_pos = pygame.mouse.get_pos()
    mouse_down = pygame.mouse.get_pressed()[0]
    hover = rect.collidepoint(mouse_pos)

    # Decide which image to show
    if hover:
        current_img = click_image if mouse_down else hover_image
    else:
        current_img = image

    # Draw the image at the correct place
    screen.blit(current_img, rect.topleft)

    return hover and mouse_down

def is_on_camera(object_, camera, buffer=100):
    #checks if object is on camera to stop lag

    cam_rect = pygame.Rect(
        camera.offset.x - buffer,
        camera.offset.y - buffer,
        camera.screen_width + buffer * 2,
        camera.screen_height + buffer * 2
    )

    return cam_rect.colliderect(object_.rect)

def death_screen(screen):
    #simple death screen for when enemy dies gives option to leave game
    screen.fill((40,40,40))
    button_image2= ui["menu"]["exit_button"].frames[0]
    button_hover_image2 = ui["menu"]["exit_button"].frames[1]
    button_click_image2 = ui["menu"]["exit_button"].frames[2]


    button_rect2 = button_image2.get_rect(topleft=(788,790))
    back = draw_button(screen,button_rect2,button_image2,button_hover_image2,button_click_image2)

    return back

def draw_main_menu(screen):
    # You'll need to add main_menu_frame to your assets
    # screen.blit(main_menu_frame,(0,0))

    # Load or access button images
    button_image = ui["menu"]["play_button"].frames[0]
    button_hover_image = ui["menu"]["play_button"].frames[1]
    button_click_image = ui["menu"]["play_button"].frames[2]

    button_image2= ui["menu"]["exit_button"].frames[0]
    button_hover_image2 = ui["menu"]["exit_button"].frames[1]
    button_click_image2 = ui["menu"]["exit_button"].frames[2]

    button_image3 = ui["menu"]["highscore_button"].frames[0]
    button_hover_image3 = ui["menu"]["highscore_button"].frames[1]
    button_click_image3 = ui["menu"]["highscore_button"].frames[2]

    button_image4 = ui["menu"]["settings_button"].frames[0]
    button_hover_image4 = ui["menu"]["settings_button"].frames[1]
    button_click_image4 = ui["menu"]["settings_button"].frames[2]

    
    # You'll need to add title_frame to your assets
    # screen.blit(title_frame,(300,100))
    
    # Properly position the button
    button_rect = button_image.get_rect(topleft=(710,580))
    button_rect2 = button_image2.get_rect(topleft=(788,790))
    button_rect3 =button_image3.get_rect(topleft=(701,650))
    button_rect4 = button_image.get_rect(topleft=(710,720))
    
    # Draw the button
    play = draw_button(screen, button_rect, button_image, button_hover_image,button_click_image)
    leave = draw_button(screen,button_rect2,button_image2,button_hover_image2,button_click_image2)
    highscore = draw_button(screen,button_rect3,button_image3,button_hover_image3,button_click_image3)
    settings =draw_button(screen,button_rect4,button_image4,button_hover_image4,button_click_image4)
    if play:
        pygame.display.update()  
        pygame.time.delay(150)
    if highscore:
        pygame.display.update()
        pygame.time.delay(150)
        
    return play,leave,highscore

shop_upgrades_selection = []
shop_weapons_selection = []
shop_initialized = False
bought_upgrades = set()
bought_weapons = set()

def draw_shop(screen, player, score, money, primary_gun, secondary_gun, current_gun):
    global shop_initialized, mouse_was_down, shop_upgrades_selection, shop_weapons_selection

    screen.fill((30, 30, 40))  # simple background

    font = pygame.font.Font(None, 28)
    title_font = pygame.font.Font(None, 50)

    mouse_pos = pygame.mouse.get_pos()
    mouse_down = pygame.mouse.get_pressed()[0]
    mouse_clicked = mouse_down and not mouse_was_down
    mouse_was_down = mouse_down

    # Initialize shop items
    if not shop_initialized:
        shop_gun_upgrades = random.sample(gun_upgrades, min(2, len(gun_upgrades)))
        shop_player_upgrades = random.sample(player_upgrades, min(2, len(player_upgrades)))
        shop_upgrades_selection = shop_gun_upgrades + shop_player_upgrades

        available_weapons = [w for w in weapon_shop if w not in [primary_gun, secondary_gun]]
        shop_weapons_selection = random.sample(available_weapons, min(4, len(available_weapons)))

        bought_upgrades.clear()
        bought_weapons.clear()
        shop_initialized = True

    # ==== Title ====
    screen.blit(title_font.render("SHOP", True, (255, 255, 0)), (screen.get_width()//2 - 50, 20))

    # ==== Player Stats ====
    stats_x, stats_y = 50, 100
    pygame.draw.rect(screen, (50,50,80), (stats_x-10, stats_y-10, 220, 150))
    pygame.draw.rect(screen, (200,200,255), (stats_x-10, stats_y-10, 220, 150), 2)
    screen.blit(font.render("PLAYER STATS", True, (255,255,255)), (stats_x, stats_y-30))
    stats_list = [
        f"HEALTH: {player.health}/{player.max_health}",
        f"SPEED: {player.speed}",
        f"DASH CD: {player.dash_cooldown}",
        f"SCORE: {score}",
        f"MONEY: ${money}"
    ]
    for i, text in enumerate(stats_list):
        screen.blit(font.render(text, True, (255,255,255)), (stats_x, stats_y + i*25))

    # ==== Upgrades ====
    y = 100
    screen.blit(font.render("UPGRADES", True, (255, 255, 0)), (300, y-30))
    for upg in shop_upgrades_selection:
        rect = pygame.Rect(300, y, 200, 40)
        color = (100,100,100) if upg['name'] in bought_upgrades else (0,180,0)
        pygame.draw.rect(screen, color, rect)
        screen.blit(font.render(f"{upg['name']} - {'BOUGHT' if upg['name'] in bought_upgrades else '$'+str(upg['cost'])}", True, (255,255,255)), (rect.x+5, rect.y+5))
        if rect.collidepoint(mouse_pos) and mouse_clicked and money >= upg['cost'] and upg['name'] not in bought_upgrades:
            money -= upg['cost']
            if upg in gun_upgrades:
                upg['effect']([primary_gun, secondary_gun])
            else:
                upg['effect'](player)
            bought_upgrades.add(upg['name'])
        y += 50

    # ==== Weapons ====
    y = 100
    screen.blit(font.render("WEAPONS", True, (255,255,0)), (550, y-30))
    slots = ["PRIMARY","SECONDARY","PRIMARY","SECONDARY"]
    for i, wpn in enumerate(shop_weapons_selection):
        rect = pygame.Rect(550, y, 200, 40)
        color = (100,100,100) if wpn.name in bought_weapons else (180,0,0)
        pygame.draw.rect(screen, color, rect)
        text = f"{wpn.name} - {'SOLD' if wpn.name in bought_weapons else '$'+str(wpn.price)} ({slots[i]})"
        screen.blit(font.render(text, True, (255,255,255)), (rect.x+5, rect.y+5))
        if rect.collidepoint(mouse_pos) and mouse_clicked and money >= wpn.price and wpn.name not in bought_weapons:
            money -= wpn.price
            bought_weapons.add(wpn.name)
            if i in [0,2]:
                primary_gun = wpn
                current_gun = primary_gun
            else:
                secondary_gun = wpn
                current_gun = secondary_gun
        y += 50

    # ==== Convert Score → Money ====
    convert_rect = pygame.Rect(50, 270, 200, 40)
    pygame.draw.rect(screen, (0,0,180) if convert_rect.collidepoint(mouse_pos) else (0,0,120), convert_rect)
    screen.blit(font.render("Convert 10 SCORE → $", True, (255,255,255)), (convert_rect.x+5, convert_rect.y+5))
    if convert_rect.collidepoint(mouse_pos) and mouse_down and score>=10:
        score -= 10
        money += 1

            # ==== Primary Gun Stats ====
    y = 330
    if primary_gun:
        screen.blit(font.render(f"PRIMARY: {primary_gun.name}", True, (255,255,0)), (50, y))
        y += 25
        primary_stats = [
            ("Bullet Speed", primary_gun.speed),
            ("Bullet Damage", primary_gun.damage),
            ("Number of Bullets", primary_gun.number_of_bullets),
            ("Spread", primary_gun.spread),
            ("Recoil", primary_gun.recoil),
            ("Shoot Distance", primary_gun.distance),
            ("Fire Rate", primary_gun.firerate),
            ("Gun Type", primary_gun.type),
            ("Bounce", primary_gun.bounce)
        ]
        for name, value in primary_stats:
            screen.blit(font.render(f"{name}: {value}", True, (255,255,255)), (60, y))
            y += 20

    # ==== Secondary Gun Stats ====
    y += 20
    if secondary_gun:
        screen.blit(font.render(f"SECONDARY: {secondary_gun.name}", True, (255,255,0)), (50, y))
        y += 25
        secondary_stats = [
            ("Bullet Speed", secondary_gun.speed),
            ("Bullet Damage", secondary_gun.damage),
            ("Number of Bullets", secondary_gun.number_of_bullets),
            ("Spread", secondary_gun.spread),
            ("Recoil", secondary_gun.recoil),
            ("Shoot Distance", secondary_gun.distance),
            ("Fire Rate", secondary_gun.firerate),
            ("Gun Type", secondary_gun.type),
            ("Bounce", secondary_gun.bounce)
        ]
        for name, value in secondary_stats:
            screen.blit(font.render(f"{name}: {value}", True, (255,255,255)), (60, y))
            y += 20

    # ==== Exit Button ====
    exit_rect = pygame.Rect(300, 500, 200, 50)
    pygame.draw.rect(screen, (0,180,0) if exit_rect.collidepoint(mouse_pos) else (0,120,0), exit_rect)
    screen.blit(font.render("EXIT SHOP", True, (0,0,0)), (exit_rect.x+40, exit_rect.y+10))
    leave = False
    if exit_rect.collidepoint(mouse_pos) and mouse_clicked:
        leave = True
        shop_initialized = False

    return leave, player, score, money, primary_gun, secondary_gun
