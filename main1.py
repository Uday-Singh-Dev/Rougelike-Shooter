import pygame
import math
from settings import *
from assets import *
from player import *
from weapon import *
from UI import *
from effects import *
from weapon_creation import *
from enemy import *
from objects import *
import random
from enemy_spawning import *


#make enemy go away from walls


primary_gun =echo_rail
secoundary_gun = uzi
current_gun = primary_gun

blood_alpha = 0
fade_out_b = False
fade_in_b = False

money = 50
player_score = 1
previous_score = 0
level = 1
round_ = 0


_round_anim_active = False
completed = False











# Initialize player
player = Player((3000, 3000), speed=7, health=9)

#enemy_spawning(player, enemy_group, wall_group, level, round_)




# Game loop
running = True
game_state = "menu"
#game_music_channel.play(game_music,loops = -1)


running = True


while running:
    dt = clock.tick(FPS)  # ms since last frame

    # --- Event Handling ---
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    # --- Menu State ---
    if game_state == "menu":
        pygame.mouse.set_visible(True)

        play, leave, highscore = draw_main_menu(screen)

        if play:
            fade_channel.play(fade_out_S)
            fade_out_b = True
            game_state = "fading_to_playing"
            pygame.event.clear(pygame.MOUSEBUTTONDOWN)
        elif leave:
            fade_channel.play(fade_out_S)
            fade_out_b = True
            game_state = "fading_to_quit"
        elif highscore:
            fade_channel.play(fade_out_S)
            fade_out_b = True
            game_state = "fading_to_highscore"

    # --- Shop State ---
    elif game_state == "shop":
        pygame.mixer.stop()
        pygame.mouse.set_visible(True)
        leave, player, player_score, money, primary_gun, secoundary_gun = draw_shop(
            screen, player, player_score, money,
            primary_gun, secoundary_gun, current_gun
        )
        current_gun = primary_gun

        if leave:
            fade_channel.play(fade_out_S)
            player.pos.x =3000
            player.pos.y = 3000
            fade_out_b = True
            game_state = "fading_to_playing_from_shop"
            pygame.event.clear(pygame.MOUSEBUTTONDOWN)
    elif game_state == "game over":
        pygame.mouse.set_visible(True)
        back = death_screen(screen)
        if back:
            fade_channel.play(fade_out_S)
            fade_out_b = True
            game_state = "fading_to_quit"

    # --- Playing State ---
    elif game_state == "playing":
        pygame.mouse.set_visible(False)
        CreatePixelatedOverlay(screen.get_size(), current_gun.range)

        update_screenshake(clock)
        offset_x, offset_y = get_shake_offset(0)
        offset_x_UI, offset_y_UI = get_shake_offset(1)

        if dt > 0:  # freeze player/enemies during hitstop
            player.update(current_gun, wall_group)
            camera.follow(player.rect)

        # --- Floor ---
        floor_offset_x = -camera.offset.x
        floor_offset_y = -camera.offset.y
        screen.blit(floor_surface, (
            floor_offset_x % texture_width - texture_width,
            floor_offset_y % texture_height - texture_height
        ))

        # --- Dead Enemies ---
        for enemy_dead in enemy_dead_group:
            if is_on_camera(enemy_dead, camera):
                screen.blit(enemy_dead.image, camera.apply(enemy_dead.rect))

        # --- Player ---
        player_frame = player.get_frame()
        player_draw_pos = pygame.Vector2(player.pos.x + offset_x, player.pos.y + offset_y)
        player_rect = pygame.Rect(player_draw_pos.x, player_draw_pos.y, player_frame.get_width(), player_frame.get_height())
        shadow_sprite = player_["player1"]["shadow"]
        shadow_pos = pygame.Rect(player_rect.x + 25, player_rect.y + 70, shadow_sprite.get_width(), shadow_sprite.get_height())
        screen.blit(shadow_sprite, camera.apply(shadow_pos))
        screen.blit(player_frame, camera.apply(player_rect))

        # --- Enemy Spawning ---
        if dt > 0:
            if not spawn_enemies:
                spawn_timer += dt
                if spawn_timer >= spawn_delay:
                    enemy_spawning(player, enemy_group, wall_group, level, round_)
                    spawn_enemies = True
            else:
                enemy_group.update(player, wall_group)

        # --- Draw Enemies ---
        for enemy in enemy_group:
            if is_on_camera(enemy, camera):
                enemy_frame = enemy.get_frame()
                enemy_draw_pos = pygame.Vector2(enemy.pos.x + offset_x, enemy.pos.y + offset_y)
                enemy_rect = pygame.Rect(enemy_draw_pos.x, enemy_draw_pos.y, enemy_frame.get_width(), enemy_frame.get_height())
                screen.blit(enemy_frame, camera.apply(enemy_rect))
                pygame.draw.rect(screen, (255, 0, 0), (
                    enemy.pos.x + 104,
                    enemy.pos.y + 95,
                    77,
                    95
                ), 2)

        # --- Guns & Shooting ---
        current_gun, primary, secoundary = gun_switching(event_list, current_gun, primary_gun, secoundary_gun, primary, secoundary)
        player.draw_gun(screen, camera, current_gun, offset_x, offset_y)

        shooting, shoot_attempted, has_enough_ammo = handle_shooting(
            screen, player.rect, player.facing_right,
            player.gun_pos, player.reloading,
            recoil_stats, current_gun
        )

        score_container = {"score": 0}
        if dt > 0:
            bullet_group.update(screen, current_gun, enemy_group, wall_group, player, score_container)
        player_score += score_container["score"]

        blood_alpha, game_state, player_score = player.collision_check(enemy_group, player, blood_alpha, game_state, player_score)

        for bullet in bullet_group:
            if is_on_camera(bullet, camera):
                screen.blit(bullet.image, camera.apply(bullet.rect))
                CutTransparentHole(bullet.rect.center, 150)

        # --- Explosions ---
        if dt > 0:
            explosion_group.update()
        for explosion in explosion_group:
            if is_on_camera(explosion, camera):
                screen.blit(explosion.image, camera.apply(explosion.rect))
                CutTransparentHole(explosion.rect.center, 300)

        # --- Particles ---
        for particle in particles.sprites():
            if dt > 0:
                particle.update()
            if is_on_camera(particle, camera):
                particle.draw(screen, camera)

        update_assets(player.dash_cooldown, current_gun)
        screen_pos = camera.apply_pos(player.gun_pos)
        mussle_flash_animation(screen, player.facing_right, screen_pos, player.reloading, shooting)

        # --- Walls ---
        for wall in wall_group:
            if is_on_camera(wall, camera):
                screen.blit(wall.image, camera.apply(wall.rect))

        CutTransparentHole(player.rect.center, current_gun.range)
        DrawOverlay(screen, screen.get_size(), offset_x, offset_y)
        
        #UI 1
        HealthDecreaseUI(screen, player.max_health, player.health, offset_x_UI, offset_y_UI)
        AmmoDecreaseUI(screen, offset_x_UI, offset_y_UI, current_gun)
        DashRechargeUI(screen, player)
        Gun_UI(screen, primary, secoundary, current_gun)
        money_display(screen,money)

        # --- Round Animations ---
        if round_start_animation_started:
            _round_anim_active = update_round_animation(screen)
            if not _round_anim_active:
                round_start_animation_started = False
        else:
            _round_anim_active = False

        if spawn_enemies:
            round_, _round_anim_active, completed = round_completed(screen, enemy_group, round_, _round_anim_active, completed, spawn_enemies)
        else:
            completed = False

        if completed:
            if not round_complete_animation_started:
                start_round_complete_animation()
                round_complete_animation_started = True

            _round_anim_complete_active = update_round_complete_animation(screen)

            if not _round_anim_complete_active:
                level += 1
                enemy_dead_group.empty()
                enemy_group.empty()
                bullet_group.empty()
                explosion_group.empty()
                particles.empty()
                fade_out_b = True
                fade_channel.play(fade_out_S)
                game_state = "fading_to_shop"
                
                completed = False
                spawn_enemies = False
                spawn_timer = 0
                round_complete_animation_started = False
                round_start_animation_started = True
        else:
            round_complete_animation_started = False
            _round_anim_complete_active = False

        # --- UI & Mouse ---
        previous_score = score_display(player_score, screen, font, previous_score)
        blood_alpha = blood_effect(screen, player.invunrable, blood_alpha)
        DrawMouse(screen, shooting, shoot_attempted, has_enough_ammo)

    # --- Handle Fade ---
    if fade_out_b:
        fade_out_b = fade_out(screen, fade_out_b)
        if not fade_out_b:
            # After fade out, determine next state
            if game_state == "fading_to_playing":
                game_state = "playing"
                round_ = start_round_animation(round_)
                round_start_animation_started = True
                spawn_timer = 0
                spawn_enemies = False
                completed = False
                fade_in_b = True
                fade_channel.play(fade_in_S)
            elif game_state == "fading_to_shop":
                game_state = "shop"
                fade_in_b = True
                fade_channel.play(fade_in_S)
            elif game_state == "fading_to_highscore":
                game_state = "highscore"
                fade_in_b = True
                fade_channel.play(fade_in_S)
            elif game_state == "fading_to_quit":
                pygame.quit()
            elif game_state == "fading_to_playing_from_shop":
                game_state = "playing"
                round_ = start_round_animation(round_)
                fade_in_b = True
                fade_channel.play(fade_in_S)

    elif fade_in_b:
        fade_in_b = fade_in(screen, fade_in_b)

    # --- End of frame ---
    pygame.display.flip()
