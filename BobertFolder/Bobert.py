
import pygame
import sys
from image_obj import image_object
import time
from Gun import Gun
from NewTestCharacter import dude2

def depth_movement(obj_depth, move_amount):
    if obj_depth != 0:
        obj_move = move_amount/obj_depth
    else:
        obj_move = 0
    
    return obj_move

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Image Move Test")
move_speed = 8

##dictionary containing all game layers. Game will have 6 depth layers, and each object will be added to the corseponding list in the dict
all_image_objects = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

back_image = image_object("Images/Environments/Duck Hunt Savanna-1.png.png", 1536,790,400,300,5)
all_image_objects[5].append(back_image)



duck_image = image_object("5a0193067ca233f48ba6272c.png", 100, 100, 600, 200, 4)
ai = dude2(600, 200, 3, duck_image.image_rect)


backbush_image = image_object("Images/Environments/SavannahBackBush.png", 2100, 700, 400, 400, 4)
all_image_objects[4].append(backbush_image)

bush_image = image_object("Images/Environments/SavannahShrubFront.png", 2100, 1100, 400, 175, 2)
all_image_objects[2].append(bush_image)

sec_bush_image = image_object("Images/Environments/SavannahShrubFront.png", 2100, 1200, 400, 250, 2)
all_image_objects[2].append(sec_bush_image)

# Main game loop
running = True
crouched = False
jump = False
current_x = 0
ammo = 4
fired_cd = 0
reload_time = 0
reloading = False
x_from_origin = 0
y_from_origin = 0

gun = Gun()

shooting = False

while running:
    ai.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
            
        for bullet in gun.bullets:
            bullet.posx += depth_movement(3, move_speed)
        x_from_origin += depth_movement(4, move_speed)

    if keys[pygame.K_RIGHT] and current_x >= -250:
        current_x -= depth_movement(5, move_speed)
        i = 6
        while i > 0:
            i -= 1
            for image in all_image_objects[i]:
                image.image_rect.x -= depth_movement(image.depth, move_speed)
        for bullet in gun.bullets:
            bullet.posx -= depth_movement(3, move_speed)
        x_from_origin -= depth_movement(4, move_speed)

    if keys[pygame.K_DOWN] and crouched == False:
        crouched = True
        move_speed = 5
        i = 6
        while i > 0:
            i -= 1
            for image in all_image_objects[i]:
                image.image_rect.y -= depth_movement(image.depth, 500)
        for bullet in gun.bullets:
            bullet.posy -= depth_movement(3, 500)
        y_from_origin -= depth_movement(4, 500)

    if keys[pygame.K_UP] and crouched == True:
        crouched = False
        move_speed = 8
        i = 6
        while i > 0:
            i -= 1
            for image in all_image_objects[i]:
                image.image_rect.y += depth_movement(image.depth, 500)
        for bullet in gun.bullets:
            bullet.posy += depth_movement(3, 500)
        y_from_origin += depth_movement(4, 500)

    if keys[pygame.K_SPACE] and ammo > 0 and fired_cd == 0:
        shooting = True
        fired_cd = 50
        ammo -= 1
        ammo_str = "Images/Weapons/ammo" + str(ammo) + ".png"
        ammo_ui = image_object(ammo_str, 50, 100, 765, 50, 0)
        print(pygame.mouse.get_pos())
   
    if ammo == 0 and reloading == False:
        reloading = True
        reload_time = 150
    elif ammo == 0:
        reload_time -= 1

    if ammo == 0 and reloading == True and reload_time == 0:
        reloading = False
        ammo = 4
        ammo_ui = image_object("Images/Weapons/ammo4.png", 50, 100, 765, 50, 0)



    ai.update()
    # Draw the image
    i = 6
    while i > 0:
        i -= 1
        if i == 4:
            screen.blit(duck_image.image, duck_image.image_rect)
        for image in all_image_objects[i]:
            screen.blit(image.image, image.image_rect)
    # Update the display
    if fired_cd > 0:
        fired_cd -= 1
    

    gun.update ()
    gun.render(screen)

    if shooting:
        gun.shoot(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        shooting = False

    gun.update_bullets(screen)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()