# Tu-Yen Dang frk3nx and Emily Wu qjk7xs

# ----------------------------------------------CHECK POINT ONE INFORMATION---------------------------------------------
#### OVERALL DESCRIPTION ####
# For players, the game's objective is to reach the end point (located on the right) using a move-able character with
# their keyboard. There will also be enemies that walk back and forth around the map; if the character touches the
# enemy, the player will lose the game and have to restart. (UPDATE: The character also loses if it falls off the map.)
# Once the character reaches the end point, the player wins and a "win" screen will be displayed.
#### REQUIRED FEATURES ####
# 1. User Input: Our game will allow users to use the arrow keys (up, down, left, right) to move the main
#    character/player around the map.   UPDATE: up was changed to the space bar, and down is not implemented.
# 2. Start Screen: The start screen will have the name of our game, student IDs, and basic instructions. From there,
#    the game will begin when a key (s) is pressed.
# 3. Game Over: The game will be "lost" when the player touches an enemy. Once they touch the enemy, the game over
#    screen will appear. UPDATE: the player can also lose if the character falls off the screen.
# 4. Small Enough Window: The window size of the game will be 800 x 600.
# 5. Graphics/Images: We will be drawing our own designs for each gamebox character/entity and background.

#### OPTIONAL FEATURES ####
# 1. Restart from Game Over: When the game is "lost", the game over screen will appear. From there, the user may press
#    a key (r) to restart the game in the initial setup.
# 2. Sprite Animation: When the main player moves, they will have animated movements. We also hope to implement sprite
#    animation for the enemies as well.
# 3. Enemies: There will be enemies that will be walking back and forth and if the player touches one, the game will
#    end and the player will need to restart the game from the beginning.
# 4. Scrolling Level: We want the map to be fairly large (larger than the window size). This will be accomplished by
#    moving the camera in our game and having a background image to show that the screen is scrolling.

# CHECKPOINT TWO was removed because it had no comments and was just previous code that we have already updated for the
# final submission.

# ------------------------------------------------------FINAL CODE------------------------------------------------------
# SET UP
import pygame
import gamebox

camera = gamebox.Camera(800, 600)

# SPRITESHEETS
seelie_stillR = gamebox.load_sprite_sheet("seelie_still_spritesheet.png", 1, 2)
seelie_stillL = gamebox.load_sprite_sheet("seelie_stillL_spritesheet.png", 1, 2)
seelie_moveR = gamebox.load_sprite_sheet("seelie_move_spritesheet.png", 1, 2)
seelie_moveL = gamebox.load_sprite_sheet("seelie_moveL_spritesheet.png", 1, 2)

slime_moveL = gamebox.load_sprite_sheet("slimeL_spritesheet.png", 1, 5) # slimes are the enemies
slime_moveR = gamebox.load_sprite_sheet("slimeR_spritesheet.png", 1, 5)


# VARIABLES
# counter
counter = 0
alive = False
start = 0
# character
chara_frame = 0
character = gamebox.from_image(200, 420, seelie_stillR[chara_frame])
character.yspeed = 0
last_key_pressed = pygame.K_RIGHT
# enemy
enemy1_frame = 0
enemy1 = gamebox.from_image(1700, 450, slime_moveL[enemy1_frame])
enemy2 = gamebox.from_image(2200, 450, slime_moveL[enemy1_frame])
enemy3 = gamebox.from_image(2900, 450, slime_moveL[enemy1_frame])
enemy_movement = 5
# win
goal = gamebox.from_image(3150, 115, "goal.png")
win = gamebox.from_text(400, 300, "YOU WIN!", 80, "yellow")
# game over screen
game_over = gamebox.from_text(400, 300, "GAME OVER", 80, "red")
restart_text = gamebox.from_text(400, 450, "Press 'r' to restart", 40, "white")
# start screen
start_screen = [
  gamebox.from_text(400, 100, "SEELIE JUMP!", 75, "white"),
  gamebox.from_text(400, 200, "Tu-Yen Dang frk3nx and Emily Wu qjk7xs", 30, "white"),
  gamebox.from_text(400, 300, "Instructions: reach the end on the right to win the game.", 30, "white"),
  gamebox.from_text(400, 350, "Use left and right arrows keys to move and space bar to jump.", 30, "white"),
  gamebox.from_text(400, 400, "Make sure to avoid enemies or you will lose the game!", 30, "white"),
  gamebox.from_text(400, 450, "Press 's' to start", 40, "white")
]
# floors
floors = [
   gamebox.from_image(200, 550, "floor1.png"),
   gamebox.from_image(450, 500, "floor2.png"),
   gamebox.from_image(700, 500, "floor3.png"),
   gamebox.from_image(1060, 200, "platform1.png"),
   gamebox.from_image(1350, 530, "floor4.png"),
   gamebox.from_image(1600, 600, "floor5.png"),
   gamebox.from_image(2150, 600, "floor6.png"),
   gamebox.from_image(2150, 300, "platform2.png"),
   gamebox.from_image(2850, 600, "floor7.png"),
   gamebox.from_image(3150, 500, "floor8.png"),
   gamebox.from_image(2700, 320, "platform3.png"),
   gamebox.from_image(2900, 200, "platform4.png")
]
# background
background = gamebox.from_image(1600, 300, "background.png")

# FUNCTION
def tick(keys):
   """
   This function takes all the above variables, and uses them to create a working game. Firstly, there are conditions
   created in order to make the start screen, game over screen, and win screen. These are done by using equality
   operators. There is also camera scrolling implemented based on the playable character's x-position on the screen.
   Then, there are the character movements and inputs themselves. The movement includes left, right, and jumping (which
   also has gravity implemented). Character movement also has sprite animations. There are also three enemies and their
   movements are also defined; they also have sprite animations. Finally, the losing condition is when either the
   character falls off screen, or if it touches an enemy. The only win condition is if the character touches the goal.
   Going back to the start screen, there are instructions on how to play and the player can press 's' to start the game.
   For the game over screen, the game will stop and the game over text will display. Players can press 'r' to restart.
   """
   # GLOBALS
   global alive, start, start_screen, chara_frame, enemy1_frame, counter, character, last_key_pressed
   global enemy_movement, slime_moveL, slime_moveR

   # START SCREEN
   if not alive and start == 0:
       for text in start_screen:
           camera.draw(text)
       if pygame.K_s in keys:
           start = 1
           alive = True

   # GAME RUNNING
   if alive and start != 0:
       # Camera Scrolling
       if 400 <= character.x < 2800:
           camera.x = character.x
       elif character.x >= 2800:
           camera.x = 2800
       # -- Character movements --
       character.speedx = 5
       # Character move right
       if pygame.K_RIGHT in keys:
           last_key_pressed = pygame.K_RIGHT
           character.x += 15
           # Character move animation
           counter += 1
           if counter % 2 == 0:
               chara_frame += 1
               if chara_frame == 2:
                   chara_frame = 0
               character.image = seelie_moveR[chara_frame]
               counter = 0
       # Character move left
       elif pygame.K_LEFT in keys:
           last_key_pressed = pygame.K_LEFT
           character.x -= 15
           # Character move animation
           counter += 1
           if counter % 2 == 0:
               chara_frame += 1
               if chara_frame == 2:
                   chara_frame = 0
               character.image = seelie_moveL[chara_frame]
               counter = 0
       # Character still animations
       else:
           # Character face right
           if last_key_pressed == pygame.K_RIGHT:
               counter += 1
               if counter % 4 == 0:
                   chara_frame += 1
                   if chara_frame == 2:
                       chara_frame = 0
                   character.image = seelie_stillR[chara_frame]
                   counter = 0
           # Character face left
           if last_key_pressed == pygame.K_LEFT:
               counter += 1
               if counter % 4 == 0:
                   chara_frame += 1
                   if chara_frame == 2:
                       chara_frame = 0
                   character.image = seelie_stillL[chara_frame]
                   counter = 0
       # Slimes
       if enemy_movement < 0:
           if counter % 6 == 0:
               enemy1_frame += 1
               if enemy1_frame == 4:
                   enemy1_frame = 0
               enemy1.image = slime_moveL[enemy1_frame]
               enemy2.image = slime_moveL[enemy1_frame]
               enemy3.image = slime_moveL[enemy1_frame]
               counter = 0
       if enemy_movement > 0:
           if counter % 6 == 0:
               enemy1_frame += 1
               if enemy1_frame == 4:
                   enemy1_frame = 0
               enemy1.image = slime_moveR[enemy1_frame]
               enemy2.image = slime_moveR[enemy1_frame]
               enemy3.image = slime_moveR[enemy1_frame]
               counter = 0

       camera.draw(background)
       camera.draw(character)
       camera.draw(enemy1)
       camera.draw(enemy2)
       camera.draw(enemy3)

       # Slime 1 Movement
       if enemy1.bottom_touches(floors[5]):
           enemy1.move_to_stop_overlapping(floors[5])
       if 1525 < enemy1.x < 1750:
           enemy1.xspeed = enemy_movement
           enemy1.move_speed()
       if enemy1.x >= 1750 or enemy1.x <= 1525:
           enemy_movement = -enemy_movement
           enemy1.xspeed = enemy_movement
           enemy1.move_speed()
       # Slime 2 Movement
       if enemy2.bottom_touches(floors[6]):
           enemy2.move_to_stop_overlapping(floors[6])
       if 1950 < enemy2.x < 2350:
           enemy2.xspeed = enemy_movement
           enemy2.move_speed()
       if enemy2.x >= 2350 or enemy2.x <= 1950:
           enemy_movement = -enemy_movement
           enemy2.xspeed = enemy_movement
           enemy2.move_speed()
       # Slime 3 Movement
       if enemy3.bottom_touches(floors[8]):
           enemy3.move_to_stop_overlapping(floors[8])
       if 2400 < enemy3.x < 3050:
           enemy3.xspeed = enemy_movement
           enemy3.move_speed()
       if enemy3.x >= 3050 or enemy3.x <= 2400:
           enemy_movement = -enemy_movement
           enemy3.xspeed = enemy_movement
           enemy3.move_speed()

       # Gravity and Jump
       character.yspeed += 7
       character.y = character.y + character.yspeed
       for floor in floors:
           if character.bottom_touches(floor):
               character.yspeed = 0
               character.move_to_stop_overlapping(floor)
               if pygame.K_SPACE in keys:
                   character.speedy = -50
           if character.left_touches(floor, 20):
               character.move_to_stop_overlapping(floor)
           if character.right_touches(floor, 20):
               character.move_to_stop_overlapping(floor)
           camera.draw(floor)
       camera.draw(goal)

       # -- Lose Conditions --
       # Touch enemy
       if character.touches(enemy1, -10, -20) or character.touches(enemy2, -10, -20) or character.touches(enemy3, -10, -20):
           alive = False
       # Fall off screen
       if character.y > 630:
           alive = False
       # -- Win Condition --
       if character.touches(goal, -10, -20):
           alive = False
           start = 2
           win.x = camera.x
           camera.draw(win)

   # GAME OVER
   if not alive and start == 1:
       game_over.x = camera.x
       camera.draw(game_over)
       restart_text.x = camera.x
       camera.draw(restart_text)
       if pygame.K_r in keys:
           character.y = 420
           character.x = 200
           camera.x = 400
           alive = True

   camera.display()

# EXECUTION
ticks_per_second = 10
gamebox.timer_loop(ticks_per_second, tick)

# All animations and illustrations were drawn by us.