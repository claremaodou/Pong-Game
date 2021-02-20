# Pong Game
import pygame

# User-defined functions
def main():
   # initialize all pygame modules 
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Pong Game')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play()  
   # quit pygame and clean up the pygame window
   pygame.quit() 
   
# User-defined classes
class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      self.small_ball = Ball('white', 5, [50, 50], [4, 4], self.surface)
      self.paddle = Paddle(50,10, 10, 60, 'white', [0, 0], self.surface)
      self.paddle2 = Paddle(450, 10, 10, 60, 'white', [0, 0], self.surface)

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         x = self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.KEYDOWN:
            x = self.handle_keydown(event)
         if event.type == pygame.KEYUP:
            self.handle_keyup(event)
     
   def handle_keyup(self, event):
      #if event key is not pressed then paddle will not move:
      if event.key == pygame.K_a:
         self.paddle.stop()  
      if event.key == pygame.K_q:
         self.paddle.stop() 
      if event.key == pygame.K_p:
         self.paddle2.stop()
      if event.key == pygame.K_l:
         self.paddle2.stop()      
         
   def handle_keydown(self, event):
      #if event key is pressed then paddle will move:
      if event.key == pygame.K_q:
         self.paddle.moveUp()
      if event.key == pygame.K_a:
         self.paddle.moveDown() 
      if event.key == pygame.K_p:
         self.paddle2.moveUp()    
      if event.key == pygame.K_l:
         self.paddle2.moveDown()      
         
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      self.surface.fill(self.bg_color) # clear the display surface first
      # draw all text
      text_string = '0'
      text_fg_color = pygame.Color('white')
      text_bg_color = pygame.Color('black')
      text_font = pygame.font.SysFont('',70)
      text_image = text_font.render(text_string, True, text_fg_color, text_bg_color)
      text_top_left_corner = (10, 10)
      text_top_left_corner2 = (470, 10)
      self.surface.blit(text_image, text_top_left_corner)  
      self.surface.blit(text_image, text_top_left_corner2)
      self.small_ball.draw()
      self.paddle.draw()
      self.paddle2.draw()
      pygame.display.update() # make the updated surface appear on the display

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update 
      point = self.small_ball.get_point()
      ball_hit_paddle = self.paddle.collide_point(point)
      ball_hit_paddle2 = self.paddle2.collide_point2(point)
      self.small_ball.move(ball_hit_paddle, ball_hit_paddle2)
      self.paddle.move()
      self.paddle2.move()

class Paddle:
   def __init__(self, x, y, width, height, color, velocity, surface):
      self.rect = pygame.Rect(x, y, width, height) # "geometry" of the rectangle
      self.color = pygame.Color(color)
      self.velocity = velocity
      self.surface = surface
          
   def move(self): 
      self.rect.move_ip(self.velocity[1], self.velocity[0])
      if self.rect.top <= 0 or self.rect.bottom >= self.surface.get_height(): 
         self.velocity[0] = 0            

   def moveUp(self):
      self.velocity[0] = -10
           
   def moveDown(self):
      self.velocity[0] = 10 
      
   def stop(self):
      self.velocity[0] = 0
   
   def draw(self):
      pygame.draw.rect(self.surface, self.color, self.rect)
   
   def collide_point(self, point):
      ball_hit_paddle = self.rect.collidepoint(point)
      return ball_hit_paddle
   
   def collide_point2(self, point):
      ball_hit_paddle2 = self.rect.collidepoint(point)
      return ball_hit_paddle2      
         
class Ball:
   # An object in this class represents a ball that moves 
   
   def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
      # Initialize a Ball.
      # - self is the Ball to initialize
      # - color is the pygame.Color of the ball
      # - center is a list containing the x and y int
      #   coords of the center of the ball
      # - radius is the int pixel radius of the ball
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object
      # - score is the amount of times the ball hits the opposite wall

      self.color = pygame.Color(ball_color)
      self.radius = ball_radius
      self.center = ball_center
      self.velocity = ball_velocity
      self.surface = surface
      self.score = 0
      self.score2 = 0
      
   def get_point(self):
      # gets the point of the ball
      # - self is the Ball
      point= [self.center[0], self.center[1] ]
      return point
   
   def move(self, ball_hit_paddle, ball_hit_paddle2):
      # Change the location of the Ball by adding the corresponding 
      # speed values to the x and y coordinate of its center
      # - self is the Ball
      # - ball_hit_paddle is a bool on whether the ball hit the paddle
      # - ball_hit_paddle2 is a bool on whether the ball hit the 2nd paddle
         
      # sets the speed of the ball
      for i in range(0,2):
         self.center[i] = (self.center[i] + self.velocity[i])
         
      # changes direction if ball hits left wall 
      if self.center[0]<self.radius:
         self.velocity[0] = -self.velocity[0]
         self.score +=1
         print("Player 1:", self.score)
            
      # changes direction if ball hits top wall
      if self.center[1]<self.radius:
         self.velocity[1] = -self.velocity[1]
         self.score2 += 1
         print("Player 2:", self.score2)
         
       #changes direction if ball hits right wall
      if self.center[0] + self.radius > self.surface.get_width():
         self.velocity[0] = -self.velocity[0]
         
       # changes direction if ball hits bottom wall
      if self.center[1] + self.radius > self.surface.get_height():
         self.velocity[1] = -self.velocity[1]
      
      # changes direction if ball hits paddle
      if ball_hit_paddle == 1:
         if self.velocity[0] < 1:
            self.velocity[0] = -self.velocity[0]   
      
      # changes direction if ball hits paddle2
      if ball_hit_paddle2 == 1:
         if self.velocity[0] > 1:
            self.velocity[0] = -self.velocity[0]
        
   def draw(self):
      # Draw the ball on the surface
      # - self is the Ball
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)


main()
