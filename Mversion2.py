# Game Code Template
from uagame import Window
import time
import pygame
from pygame.locals import *
import random
import math


# User-defined functions
#clicked_image_list = []
start_time = time.time()
def main():
    global clicked_image_list
    clicked_image_list = []
    window = Window('Tic Tac Toe', 600,430)
    
    # The following statement needs to be included as we are doing 
    # window update in the code instead of having uagame do the update
    window.set_auto_update(False)
    # create Game object using window as argument
    game = Game(window)
    # Play the Game object
    game.play()
    # Close the window
    window.close()
    
    

# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, window):
        # Initialize a Game.
        # - self is the Game to initialize
        # - window is the uagame window object
        
        # Game Class always has the following 4 instance attributes
        self.window = window
        Tile.set_window(window) # call a class method
        self.pause_time = 0.04 # smaller is faster game
        self.close_clicked = False
        self.continue_game = True
        # NEW ATTRIBUTES
        self.board = []
        
        
        self.timer = 0
        
        self.dt = 0
        
        self.clock = pygame.time.Clock()
        
        self.turn = 0
        
        self.origi_image = pygame.image.load("image0.bmp")
        
        self.copy_board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        
        self.num_of_pair = 0
        
        self.wait = 0
        
     #create the image list and ramdom it            
        image_list = []
        for index in range(1,9):
            image = pygame.image.load("image"+str(index)+".bmp")
            image_list.append(image)
        image_list = image_list+ image_list
        
        random.shuffle(image_list)
        
        
        self.image_list = []
        
        pre_image = 0
        
        count = 0
        print(image_list)
        while count<16:
            image = image_list[0]
            if image == pre_image:
                print("repeat")
                image_list.append(image)
                image_list.pop(0)
                image = image_list[0]
            image_list.pop(0)
            pre_image = image
            self.image_list.append(image)
            count+=1
            
            
        
        
        random.shuffle(self.image_list)
  #let self.copy_board record the fix position of the board image              
        n = 0
        for x in range(4):
            for y in range(4):   
                self.copy_board[x][y] = self.image_list[n]          
                n += 1
               
                   
        self.pre_image = False
        
        self.create_board()   
             
    
    def create_board(self):
        for row_index in range(4):
            row = self.create_row(row_index)
            self.board.append(row)
            
    def create_row(self,row_index):
      
        row = []
        width = 110
        height = self.window.get_height()//4
        for col_index in range(4):
            x = width * col_index
            y = height * row_index   
            
            tile = Tile(x,y,width,height)
         
     
            row.append(tile)
        return row
            
    
    def play(self):
       
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked :  # until player clicks close box
            # play frame
           
            
            self.handle_event()
         
            self.draw()  
           
            self.update() 
            
            self.dt = self.clock.tick(60)/1000
      
                     
            if self.continue_game:
                self.timer += self.dt
                
                self.decide_continue()
            
 
           
    def handle_event(self):
        # Handle each user event by changing the game state
        # appropriately.
        # - self is the Game whose events will be handled.

        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
        if event.type == MOUSEBUTTONUP and self.continue_game:
            self.handle_mouse_up(event.pos)
                 
            
    def handle_mouse_up(self,position):
        
        
        return_value = False
        width = 110
        height = self.window.get_height()//4       
        image1 = 0
        image2 = 1
         
        for row in self.board:
                                       
            for tile in row:
                    
                return_value = tile.select(position)
             
                if return_value == True:
                                                  
                    column_index = self.board.index(row)
                    row_index = row.index(tile)   
                    
                    image = self.copy_board[column_index][row_index]
                                         
                    tile.content = image
                                 
                    clicked_image_list.append(image)                                                            
                                           
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        
        self.window.clear()
      
      # time record and show            
        time_text = math.floor(self.timer)                  
        number = str(time_text)          
        font = pygame.font.SysFont("comicsansms", 72)        
        text = font.render(number, True, (255, 255, 255))             
        surface =  Tile.window.get_surface()       
        surface.blit(text,(480,0))
             
        
        for row in self.board:
        
            for tile in row:
                                                            
                tile.draw()     
        
        self.window.update()
        if self.wait == 1:
            self.wait = 0
            pygame.time.delay(1000)
       
    
    def update(self):
      # compare two images user choose 
        if len(clicked_image_list)==2 and clicked_image_list[0] != clicked_image_list[1]:
            self.wait = 1
            for row in self.board:           
                for tile in row:                 
                    if tile.content == clicked_image_list[0] or tile.content == clicked_image_list[1]:                       
                        tile.content = tile.origi_image  
                        
            clicked_image_list.pop()
            clicked_image_list.pop()             
                    
                        
                                                
                
        elif len(clicked_image_list)==2 and clicked_image_list[0] == clicked_image_list[1]:
          
            self.num_of_pair += 1
            if self.num_of_pair==8:
                self.continue_game = False
                
            clicked_image_list.pop()
            clicked_image_list.pop()               
                       
            
            
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        # Write code to check if game should continue or not
        pass
    
       
class Tile:
    # Class Attributes
    window = None
    fg_color = 'white'
    border_size = 3
    font_size = 133
    
    
    @classmethod
    def set_window(cls,window_from_Game):
        cls.window = window_from_Game
    #INSTANCE METHODS
    
    def __init__(self,x,y,width,height):
        self.rect = pygame.Rect(x,y,width,height)
        
        self.origi_image = pygame.image.load("image0.bmp") 
         
        self.content = self.origi_image
        self.flashing = False
        self.x = x
        self.y = y
       
           
    
    def draw(self):
      
        surface = Tile.window.get_surface()
        if self.flashing:
            # draw white rectangle
            pygame.draw.rect(surface,pygame.Color(Tile.fg_color),self.rect)
        
            self.flashing = False
        else:
            # black rectangle with white border
            surface = pygame.draw.rect(surface,pygame.Color(Tile.fg_color),self.rect,Tile.border_size)
            self.draw_content()
         
          
             
    def draw_content(self):
             
        surface = Tile.window.get_surface()
        horizontal_left_over = self.rect.width - 100
        vertical_left_over = self.rect.height - 100
        content_x = self.rect.x + horizontal_left_over//2
        content_y = self.rect.y + vertical_left_over//2        
        surface.blit(self.content,(content_x,content_y))
       
                              
    def select(self,position):
        return_value = False
        if self.rect.collidepoint(position):

            if self.content == self.origi_image: 
                
                           
                return_value = True  
            
            else:
             
                self.flashing = True    
        
        return return_value        
    
                
main()

