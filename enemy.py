import pygame
import gamesetting as gs
from random import choice

class Enemy(pygame.sprite.Sprite):
  def __init__(self, game, image_dict,group, row_num, col_num, size):
    super().__init__(group)
    self.GAME = game


    # Attributes (dependent on our enemy type)
    self.speed = 1               # Speed of the enemy
    self.wall_hack = False       # Enemy can move through walls 
    self.chase_player = False    # Enemy will chase the player
    self.Los = 0                 # Distance enemy can see player
    self.see_player_hack = False # # Enemy can see player through walls 


    # Level Matrix spawn coordinates
    self.row = row_num
    self.col = col_num

    # Spaw Coordinates of enemy
    self.size = size
    self.x = self.col * self.size
    self.y = (self.row * self.size) + gs.Y_OFFSET

    # Other Attributes
    self.destroyed = False
    self.direction = 'left'  # Initial direction
    self.dir_mvmt = {"left": -self.speed, "right": self.speed,
                     "up": -self.speed, "down": self.speed}

    # Enemy Animation and Images
    self.index = 0
    self.action = f"walk_{self.direction}"
    self.image_dict = image_dict

    self.image = self.image_dict[self.action][self.index]
    self.rect = self.image.get_rect(topleft=(self.x, self.y))

  def update(self):
   self.movement()


  def draw(self, window, x_offset=0, y_offset=0):
    """Render enemy sprite with camera offsets applied to both axes."""
    window.blit(self.image, (int(self.x) - int(x_offset), int(self.y) - int(y_offset)))

  def movement(self):
    """Method that incorporate all movement conditions to enable
      enemy to move around the game area"""
    # Return out of method, if enemy is destroyed
    if self.destroyed:
      return
    
    # Move enemy along the x or y axis, dependent on move direction
    move_direction = self.action.split("_")[1]
    if move_direction in ["left","right"]:
      self.x += self.dir_mvmt[move_direction]
    else: 
      self.y += self.dir_mvmt[move_direction]  

    # Reset the direction listing for the char to choose from
    directions = ["left","right","up","down"]
    collision = False

    # Collision detection with Hard Blocks
    self.new_direction(self.GAME.groups["hard_block"], move_direction, directions)

    # Collision detection with Soft Blocks
    self.new_direction(self.GAME.groups["soft_block"], move_direction, directions)

    # Collision detection with Bombs
    self.new_direction(self.GAME.groups["bomb"], move_direction, directions)

    # Update the rect position of the enemy with the new x, y coordinates
    self.rect.update(self.x, self.y, self.size, self.size)


  def collision_detection_blocks(self, group, direction):
     # Collision detection 
    for block in group:
      # compare each block for collision with enemy char rect
      if block.rect.colliderect(self.rect):
        # Reverse direction upon collision
        if direction == "left" and self.rect.right > block.rect.right:
           self.x = block.rect.right
           return direction
        if direction == "right" and self.rect.left < block.rect.left:
           self.x = block.rect.left - self.size
           return direction
        if direction == "up" and self.rect.bottom > block.rect.bottom:
           self.y = block.rect.bottom
           return direction
        if direction == "down" and self.rect.top < block.rect.top:
           self.y = block.rect.top - self.size     
           return direction   
    return None    
  
  def new_direction(self,group,move_direction,directions):
      dir = self.collision_detection_blocks(group, move_direction) 
      if dir:   
        directions.remove(dir)
        new_direction = choice(directions) 
        self.action = f"walk_{new_direction}"