import pygame
from time import time
from random import randint

pygame.init()

WIDTH_SC = 800
HEIGHT_SC = 700
screen = pygame.display.set_mode((WIDTH_SC, HEIGHT_SC))

running = True

clock = pygame.time.Clock()

#Color
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

class Snake():
    def __init__(self,x,y):
        self.body = [[x,y]]
        self.WIDTH_SNAKE = 20
        self.HEIGHT_SNAKE = 20
        self.direction = ""
        self.score = 0
        #time
        self.start_time_run = time()
        self.current_time_run = time()
        self.update_time_run = 0.10  #0.08->0.04
    
    def draw(self): #draw snake
        for part in self.body:
            if self.body.index(part) == 0:
                pygame.draw.rect(screen, RED, (20*part[0], 20*part[1], self.WIDTH_SNAKE, self.HEIGHT_SNAKE))
            else:
                pygame.draw.rect(screen, BLUE, (20*part[0], 20*part[1], self.WIDTH_SNAKE, self.HEIGHT_SNAKE))      
    
    def update(self):
        if self.current_time_run - self.start_time_run >= self.update_time_run:
                if self.direction == "right":
                    self.body.insert(0, [self.body[0][0]+1, self.body[0][1]])
                    self.body.pop(-1)
                if self.direction == "left":
                    self.body.insert(0, [self.body[0][0]-1, self.body[0][1]])
                    self.body.pop(-1)
                if self.direction == "up":
                    self.body.insert(0, [self.body[0][0], self.body[0][1]-1])
                    self.body.pop(-1)
                if self.direction == "down":
                    self.body.insert(0, [self.body[0][0], self.body[0][1]+1])
                    self.body.pop(-1)
                  
                #Update the time to subtract
                self.start_time_run = time()
                #speed update
                if self.score >= 20:
                    self.update_time_run = 0.04
                
x=5
y=5             
snake = Snake(x,y) 
  
food = [randint(0,int(WIDTH_SC/snake.WIDTH_SNAKE)-1), randint(0,int(HEIGHT_SC/snake.HEIGHT_SNAKE)-1)]

game_over = False
round_1 = True #there is a collision with the wall
round_2 = False #across the wall
start = False

#tạo chữ
font = pygame.font.SysFont('Brush Script MT', 50)
font_small = pygame.font.SysFont('Brush Script MT', 40)
font_text = pygame.font.SysFont('Brush Script MT', 60)

game_over_text = font_text.render("Game Over", True, GREEN)
game_over_text_rect = game_over_text.get_rect(center=(WIDTH_SC/2,200))
play_again_text = font.render("Press Enter To Play Again", True, (0,255,255))
play_again_text_rect = play_again_text.get_rect(center=(WIDTH_SC/2,250))

round_1_text = font_small.render("Round 1", True, RED)
round_1_text_rect = round_1_text.get_rect(center=(WIDTH_SC/2,230))
round_2_text = font_small.render("Round 2", True, RED)
round_2_text_rect = round_2_text.get_rect(center=(WIDTH_SC/2,270))

while running:
    clock.tick(60)
    
    #Update current time
    snake.current_time_run = time()
    
    screen.fill(BLACK)
    
    tail_snake_x = snake.body[-1][0]
    tail_snake_y = snake.body[-1][1]
     
    #draw snake
    snake.draw()
    
    #draw food
    pygame.draw.rect(screen, RED, (20*food[0], 20*food[1], snake.WIDTH_SNAKE, snake.HEIGHT_SNAKE))
    
    if start == False:
        pygame.draw.rect(screen, (96,96,96), (int(WIDTH_SC/2-70),200,140,100))
        if round_1 == True and round_2 == False:
            pygame.draw.rect(screen, (51,255,255), (int(WIDTH_SC/2-60),210,120,40))
        elif round_2 == True and round_1 == False:
            pygame.draw.rect(screen, (51,255,255), (int(WIDTH_SC/2-60),250,120,40))
        screen.blit(round_1_text, round_1_text_rect)
        screen.blit(round_2_text, round_2_text_rect)

        
    else: #start == True 
        #snake movement and movement speed
        if game_over == False:
            snake.update()
            
        else: #game_over==True
            screen.blit(game_over_text, game_over_text_rect)
            screen.blit(play_again_text,play_again_text_rect)
        
    #when snake eats food
    if snake.body[0][0] == food[0] and snake.body[0][1] == food[1]:
        snake.body.append([tail_snake_x, tail_snake_y])
        snake.score += 1
        food = [randint(0,int(WIDTH_SC/snake.WIDTH_SNAKE)-1), randint(0,int(HEIGHT_SC/snake.HEIGHT_SNAKE)-1)]
        if food in snake.body:
            food = [randint(0,int(WIDTH_SC/snake.WIDTH_SNAKE)-1), randint(0,int(HEIGHT_SC/snake.HEIGHT_SNAKE)-1)]
    
    #Check if the snake's head is touching the body
    for part in snake.body[1:]:
        if snake.body[0][0]==part[0] and snake.body[0][1]==part[1]:
            game_over = True
    
    #game mode
    if round_1 == True and (snake.body[0][1]<0 or snake.body[0][1]>34 or snake.body[0][0]<0 or snake.body[0][0]>39): #có tường
        game_over = True
        
    elif round_2 == True: #across the wall
        if snake.body[0][0]>39: #The snake's head goes past the right screen
            snake.body[0][0]=0
        elif snake.body[0][0]<0: #The snake's head goes past the left screen
            snake.body[0][0]=39
        elif snake.body[0][1]<0: #The snake's head goes past the upper screen
            snake.body[0][1]=34
        elif snake.body[0][1]>34: #The snake's head goes past the bottom screen
            snake.body[0][1]=0
        
    #score
    score_text = font.render("score:"+str(snake.score), True, (96,96,96))
    screen.blit(score_text,(5,5))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #game control buttons
        if event.type == pygame.KEYDOWN:
            #choose game mode
            if start == False:
                if event.key == pygame.K_UP or event.key == pygame.K_w: #play round 1
                    round_1 = True
                    round_2 = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s: #play round 2
                    round_2 = True
                    round_1 = False
                if event.key == pygame.K_RETURN:
                    start = True
                    
            else: #start == True
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.direction != "left":
                    snake.direction = "right"
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.direction != "right":
                    snake.direction = "left"
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.direction != "down":
                    snake.direction = "up"
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.direction != "up":
                    snake.direction = "down"
            
            #play again
            if event.key == pygame.K_RETURN and game_over == True:
                start = False
                game_over = False
                snake.body = [[x,y]]
                snake.direction = ""
                snake.score = 0
                snake.start_time_run = time()
                snake.update_time_run = 0.08
                
    pygame.display.flip()
pygame.quit()