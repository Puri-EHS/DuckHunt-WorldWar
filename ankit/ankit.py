import pygame
from image_obj import image_object
from player_gun import PlayerGun
import constants


if not constants.USE_MOUSE:
    import multiprocessing as mp
    from gesture import get_points

pygame.mixer.init()

def depth_movement(obj_depth, move_amount):
    if obj_depth != 0:
        obj_move = move_amount/obj_depth
    else:
        obj_move = 0
    return obj_move

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

    all_image_objects = []

    back_image = image_object("../Images/Environments/Duck Hunt Savanna-1.png.png", 1536,790,400,300,5)
    all_image_objects.append(back_image)

    ##duck_image = image_object("5a0193067ca233f48ba6272c.png", 300, 300, 400, 250, 4)
    ##all_image_objects.append(duck_image)

    backbush_image = image_object("../Images/Environments/SavannahShrubFront.png", 2100, 500, 400, 200, 4)
    all_image_objects.append(backbush_image)

    bush_image = image_object("../Images/Environments/SavannahShrubFront.png", 2100, 700, 400, 315, 2)
    all_image_objects.append(bush_image)

    sec_bush_image = image_object("../Images/Environments/SavannahShrubFront.png", 2100, 900, 400, 400, 2)
    all_image_objects.append(sec_bush_image)

    bar_ui = image_object("../bar.png", 0, 25, 750, 160, 0)
    ammo_ui = image_object("../Images/Weapons/ammo4.png", 100, 200, 750, 75, 0)

    # Main game loop
    running = True
    crouched = False
    jump = False
    current_x = 0
    ammo = 4
    fired_cd = 0
    reload_time = 0
    reloading = False


    gun = PlayerGun()

    shooting = False

    while running:
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
            for image in all_image_objects:
                image.image_rect.x += depth_movement(image.depth, move_speed)
            for bullet in gun.bullets:
                bullet.posx += depth_movement(3, move_speed)

        if keys[pygame.K_RIGHT] and current_x >= -250:
            current_x -= depth_movement(5, move_speed)
            for image in all_image_objects:
                image.image_rect.x -= depth_movement(image.depth, move_speed)
            for bullet in gun.bullets:
                bullet.posx -= depth_movement(3, move_speed)
        
        if keys[pygame.K_DOWN] and crouched == False:
            crouched = True
            move_speed = 5
            for image in all_image_objects:
                image.image_rect.y -= depth_movement(image.depth, 500)
            for bullet in gun.bullets:
                bullet.posy -= depth_movement(3, 500)
        
        if keys[pygame.K_UP] and crouched == True:
            crouched = False
            move_speed = 8
            for image in all_image_objects:
                image.image_rect.y += depth_movement(image.depth, 500)
            for bullet in gun.bullets:
                bullet.posy += depth_movement(3, 500)
        
        if keys[pygame.K_SPACE] and ammo > 0 and fired_cd == 0:
            shooting = True
            fired_cd = 50
            ammo -= 1
            ammo_str = "../Images/Weapons/ammo" + str(ammo) + ".png"
            ammo_ui = image_object(ammo_str, 100, 200, 750, 75, 0)
            
    
        if ammo == 0 and reloading == False:
            reloading = True
            reload_time = 150
        elif ammo == 0:
            reload_time -= 1

        if ammo == 0 and reloading == True and reload_time == 0:
            reloading = False
            ammo = 4
            ammo_ui = image_object("../Images/Weapons/ammo4.png", 100, 200, 750, 75, 0)

        if reloading:
            bar_ui = image_object("../bar.png", reload_time/2, 25, 750, 160, 0)
        elif fired_cd > 0:
            bar_ui = image_object("../bar.png", fired_cd, 25, 750, 160, 0)

        # Draw the image
        for image in all_image_objects:
            screen.blit(image.image, image.image_rect)
        # Update the display
        if fired_cd > 0:
            fired_cd -= 1
        
        screen.blit(bar_ui.image, bar_ui.image_rect)
        screen.blit(ammo_ui.image, ammo_ui.image_rect)

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
