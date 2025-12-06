import pygame
import gamesetting as gs

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
   pass

  def draw(self, window, x_offset=0, y_offset=0):
    """Render enemy sprite with camera offsets applied to both axes."""
    window.blit(self.image, (int(self.x) - int(x_offset), int(self.y) - int(y_offset)))


