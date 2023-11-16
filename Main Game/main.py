import pygame
from image_obj import image_object
from player_gun import PlayerGun
import constants
from NewTestCharacter import dude2
from TestCharacter import dude
from bird_obj import bird_object

if not constants.USE_MOUSE:
    import multiprocessing as mp
    from gesture import get_points


def depth_movement(obj_depth, move_amount):
    if obj_depth != 0:
        obj_move = move_amount/obj_depth
    else:
        obj_move = 0
    
    return obj_move

def hp_to_bar_x(current, max):
    percent_hp = (current/max)*100
    x_val = 0 - 125 + (2.45*percent_hp)
    print (x_val)
    return x_val

def main(queue):
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    screen_width = 800
    screen_height = 600

    # Create the screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Image Move Test")
    move_speed = 8

    all_image_objects = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

    back_image = image_object("Main Game/Duck Hunt Savanna-1.png.png", 1536,790,400,300,5)
    all_image_objects[5].append(back_image)

    backbush_image = image_object("Main Game/FrontShrubSavannah-1.png.png", 2100, 500, 400, 200, 4)
    all_image_objects[4].append(backbush_image)

    bush_image = image_object("Main Game/SavannahShrubFront.png", 2100, 1000, 400, 200, 2)
    all_image_objects[2].append(bush_image)

    sec_bush_image = image_object("Main Game/SavannahShrubFront.png", 2100, 1200, 400, 275, 2)
    all_image_objects[2].append(sec_bush_image)

    duck_hp_max = 500
    duck_obj = bird_object("5a0193067ca233f48ba6272c.png", 200, 200, 600, 200, 4, duck_hp_max, 1)
    ai = dude2(600, 200, 0.1, duck_obj.image_rect)



    bar_ui = image_object("Main Game/bar.png", 0, 25, 750, 160, 0)
    ammo_ui = image_object("Main Game/ammo4.png", 100, 200, 750, 75, 0)
    hit_point_ui = image_object("Main Game/hit_point_ui.png", 250, 75, 120, 50, 0)
    hit_point_bar = image_object("Main Game/bar.png", 250, 70, 120, 60, 0)
    # hitbar hidden at x = -125, aka move left a total of 245
    # 0% = -125; 100% = 120


    # Main game loop
    running = True
    crouched = False
    current_x = 0
    ammo = 4
    fired_cd = 0
    reload_time = 0
    reloading = False
    y_from_origin = 0
    

    gun = PlayerGun()
    player_gun_damage = 100
    shooting = False
    hit_tic = 0
    hit_image = image_object("Main Game/hit_img.png", 90, 90, 400, 300, 4)
    while running:
        x_moved_last_tick = 0
        ai.update()
        hit = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
            ##if event.type == pygame.MOUSEBUTTONDOWN:
                ##if event.button == 1:
                    ##shooting = True
            ##elif event.type == pygame.MOUSEBUTTONUP:
                ##if event.button == 1:
                    ##shooting = False
        # Clear the screen
        screen.fill((255, 255, 255))

        keys = pygame.key.get_pressed()


        # Update image position
        if keys[pygame.K_LEFT] and current_x <= 250:    
            current_x += depth_movement(5, move_speed)
            i = 6
            while i > 0:
                i -= 1
                for image in all_image_objects[i]:
                    image.image_rect.x += depth_movement(image.depth, move_speed)
            x_moved_last_tick += depth_movement(4, move_speed)

        if keys[pygame.K_RIGHT] and current_x >= -250:
            current_x -= depth_movement(5, move_speed)
            i = 6
            while i > 0:
                i -= 1
                for image in all_image_objects[i]:
                    image.image_rect.x -= depth_movement(image.depth, move_speed)
            x_moved_last_tick -= depth_movement(4, move_speed)

        if keys[pygame.K_DOWN] and crouched == False:
            crouched = True
            move_speed = 5
            i = 6
            while i > 0:
                i -= 1
                for image in all_image_objects[i]:
                    image.image_rect.y -= depth_movement(image.depth, 500)
            y_from_origin -= depth_movement(4, 500)

        if keys[pygame.K_UP] and crouched == True:
            crouched = False
            move_speed = 8
            i = 6
            while i > 0:
                i -= 1
                for image in all_image_objects[i]:
                    image.image_rect.y += depth_movement(image.depth, 500)
            y_from_origin += depth_movement(4, 500)
        
        if keys[pygame.K_SPACE] and ammo > 0 and fired_cd == 0 and crouched == False:
            shooting = True
            fired_cd = 50
            ammo -= 1
            ammo_str = "Main Game/ammo" + str(ammo) + ".png"
            ammo_ui = image_object(ammo_str, 100, 200, 750, 75, 0)
            
            if (gun.crosshair_coords[0] - duck_obj.image_rect.x < 150) and (gun.crosshair_coords[0] - duck_obj.image_rect.x > -25):
                if (gun.crosshair_coords[1] - duck_obj.image_rect.y < 200) and (gun.crosshair_coords[1] - duck_obj.image_rect.y > -25):
                    duck_obj.hp -= player_gun_damage
                    hit_tic = 5
                    hit_image = image_object("Main Game/hit_img.png", 90, 90, gun.crosshair_coords[0], gun.crosshair_coords[1], 4)

        if ammo == 0 and reloading == False:
            reloading = True
            reload_time = 150
        elif ammo == 0:
            reload_time -= 1

        if ammo == 0 and reloading == True and reload_time == 0:
            reloading = False
            ammo = 4
            ammo_ui = image_object("Main Game/ammo4.png", 100, 200, 750, 75, 0)

        if reloading:
            bar_ui = image_object("Main Game/bar.png", reload_time/2, 25, 750, 160, 0)
        elif fired_cd > 0:
            bar_ui = image_object("Main Game/bar.png", fired_cd, 25, 750, 160, 0)


        ai.duck_rect.x += x_moved_last_tick
        ai.update()

        duck_obj.update()
        hit_point_bar.image_rect.centerx = hp_to_bar_x(duck_obj.hp, duck_hp_max)
    
        # Draw the image
        i = 6
        while i > 0:
            i -= 1
            if i == 4:
                screen.blit(duck_obj.image, duck_obj.image_rect)
            for image in all_image_objects[i]:
                screen.blit(image.image, image.image_rect)
        # Update the display
        if fired_cd > 0:
            fired_cd -= 1
        
        screen.blit(bar_ui.image, bar_ui.image_rect)
        screen.blit(ammo_ui.image, ammo_ui.image_rect)
        screen.blit(hit_point_bar.image, hit_point_bar.image_rect)
        screen.blit(hit_point_ui.image, hit_point_ui.image_rect)
        
        if hit_tic > 0:
            screen.blit(hit_image.image, hit_image.image_rect)
            hit_tic -= 1

        gun.update(queue)
        gun.render(screen)

        if shooting:
            gun.shoot()
            shooting = False

        gun.update_bullets(screen)

        pygame.display.flip()
   

if __name__ == '__main__':
    if not constants.USE_MOUSE:
        q = mp.Queue()
        print("starting duck hunt...")
        p1 = mp.Process(target=get_points, args=(q,))
        p1.start()

        main(q)
    else:
        main(None)

    if not constants.USE_MOUSE:
        p1.kill()
