
import pygame
import random
from color import Color
from point import Point
from direction import Direction
from existance import Existance
from action import Action
import math

pygame.init()
font = pygame.font.SysFont('arial', 25)
# constants
BLOCKSIZE = 20
SPEED = 16


class SnakeGame:

    def __init__(self, animate = False):
        self.animate = animate
        self.width = 480
        self.height = 360
        if animate:
            self.display = pygame.display.set_mode(size = (self.width, self.height))
            self.clock = pygame.time.Clock()
         
        # initializing the game state
        self.direction = Direction.RIGHT
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head, 
                      Point(self.width/2 - BLOCKSIZE, self.height/2),
                      Point(self.width/2 - 2*BLOCKSIZE, self.height/2)]
        self.score = 0.0
        self.food = None
        self.place_food()

        # second element will be popped after first iteration so it's value is not improtant
        self.dist_to_food = [self.calculate_distance(self.head, self.food), 0]  

        self.reward = 0

    

        
    def get_direction(self, current_direction, action):
        directions = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]
        if action == Action.FORWARD:
            return current_direction
        if action == Action.LEFT:
            return directions[(current_direction.value + 1) % 4]  # direction will be one to the right (with higher index) in directions list
        if action == Action.RIGHT:
            # direction will be one to the left (with lower index) in directions list
            # since indices cant be negative, it's not implemented with -1 step but rather with +3
            return directions[(current_direction.value + 3) % 4]  
            

    def place_food(self):
        x = int(random.randint(0, self.width - BLOCKSIZE)/BLOCKSIZE)*BLOCKSIZE
        y = int(random.randint(0, self.height - BLOCKSIZE)/BLOCKSIZE)*BLOCKSIZE
        self.food = Point(x, y)
        for p in self.snake:
            if self.food.x == p.x and self.food.y == p.y:
                self.place_food()


    def calculate_distance(self, pointA, pointB):
        return math.sqrt((pointA.x - pointB.x)**2 + (pointA.y - pointB.y)**2)

    def play_step(self, action):
        # important NOTE: how rewards are distributed is very important in reinforcement learning
        # colision must be avoided for any cost, so the negative reward is higher for making colision than for
        # eating a food. Also, it's important to notice that every empty step is slight minus reward

        self.direction = self.get_direction(self.direction, action)

        # move
        self.move(self.direction)
        self.snake.insert(0, self.head)
        # place new food if eaten and move snake
        if (self.head.x == self.food.x) and (self.head.y == self.food.y):
            self.score += 1
            self.reward = 20
            self.place_food()
        else:
            self.reward = -1
            self.snake.pop()

        # check if game is over
        game_over = False
        if self.is_colision():
            self.reward = -50
            game_over = True
            return game_over

        

        self.dist_to_food.insert(0, self.calculate_distance(self.head, self.food)) # adding new distance
        self.dist_to_food.pop()  # removing oldest one
        # result is current distance and previous one

        # update pygame.ui
        if self.animate:
            self.update_ui()
            self.clock.tick(SPEED)

        # return if game over and show score       
        return game_over

    def get_reward(self):
        return self.reward

    def get_states(self):
        # ukoliko se bude cudno ponasalo proveriti ovu logiku ovde!

        if self.direction == Direction.LEFT:
            if self.is_colision(Point(self.head.x - BLOCKSIZE, self.head.y)): # if there is obstacle in front
                obs_infront = 1 # 1 if obstacle exist
            else:
                obs_infront = 0
            if self.is_colision(Point(self.head.x, self.head.y + BLOCKSIZE)): # if there is obstacle in left
                obs_left = 1
            else:
                obs_left = 0
            if self.is_colision(Point(self.head.x, self.head.y - BLOCKSIZE)): # if there is obstacle in left
                obs_right = 1
            else:
                obs_right = 0

            # check if food is behind or not
            if self.food.x > self.head.x:
                food_infront = 0
                food_behind = 1
            elif self.food.x < self.head.x:
                food_infront = 1
                food_behind = 0
            else:
                food_infront = 0
                food_behind = 0

            # check if food is left or right
            if self.food.y > self.head.y:
                food_left = 1
                food_right = 0
            elif self.food.y < self.head.y:
                food_left = 0
                food_right = 1
            else:
                food_left = 0
                food_right = 0
            

        if self.direction == Direction.RIGHT:
            if self.is_colision(Point(self.head.x + BLOCKSIZE, self.head.y)): # if there is obstacle in front
                obs_infront = 1 # 1 if obstacle exist
            else:
                obs_infront = 0
            if self.is_colision(Point(self.head.x, self.head.y - BLOCKSIZE)): # if there is obstacle in left
                obs_left = 1
            else:
                obs_left = 0
            if self.is_colision(Point(self.head.x, self.head.y + BLOCKSIZE)): # if there is obstacle in right
                obs_right = 1
            else:
                obs_right = 0

            # check if food is behind or not
            if self.food.x < self.head.x:
                food_infront = 0
                food_behind = 1
            elif self.food.x > self.head.x:
                food_infront = 1
                food_behind = 0
            else:
                food_infront = 0
                food_behind = 0

            # check if food is left or right
            if self.food.y < self.head.y:
                food_left = 1
                food_right = 0
            elif self.food.y > self.head.y:
                food_left = 0
                food_right = 1
            else:
                food_left = 0
                food_right = 0
            
            
        if self.direction == Direction.UP:
            if self.is_colision(Point(self.head.x, self.head.y + BLOCKSIZE)): # if there is obstacle in front
                obs_infront = 1 # 1 if obstacle exist
            else:
                obs_infront = 0
            if self.is_colision(Point(self.head.x - BLOCKSIZE, self.head.y)): # if there is obstacle in left
                obs_left = 1
            else:
                obs_left = 0
            if self.is_colision(Point(self.head.x + BLOCKSIZE, self.head.y)): # if there is obstacle in right
                obs_right = 1
            else:
                obs_right = 0

            # check if food is behind or not
            if self.food.y > self.head.y:
                food_infront = 0
                food_behind = 1
            elif self.food.y < self.head.y:
                food_infront = 1
                food_behind = 0
            else:
                food_infront = 0
                food_behind = 0

            # check if food is left or right
            if self.food.x < self.head.x:
                food_left = 1
                food_right = 0
            elif self.food.x > self.head.x:
                food_left = 0
                food_right = 1
            else:
                food_left = 0
                food_right = 0
            

        if self.direction == Direction.DOWN:
            if self.is_colision(Point(self.head.x, self.head.y - BLOCKSIZE)): # if there is obstacle in front
                obs_infront = 1 # 1 if obstacle exist
            else:
                obs_infront = 0
            if self.is_colision(Point(self.head.x + BLOCKSIZE, self.head.y)): # if there is obstacle in left
                obs_left = 1
            else:
                obs_left = 0
            if self.is_colision(Point(self.head.x - BLOCKSIZE, self.head.y)): # if there is obstacle in right
                obs_right = 1
            else:
                obs_right = 0

            # check if food is behind or not
            if self.food.y < self.head.y:
                food_infront = 0
                food_behind = 1
            elif self.food.y > self.head.y:
                food_infront = 1
                food_behind = 0
            else:
                food_infront = 0
                food_behind = 0

            # check if food is left or right
            if self.food.x < self.head.x:
                food_left = 0
                food_right = 1
            elif self.food.x > self.head.x:
                food_left = 1
                food_right = 0
            else:
                food_left = 0
                food_right = 0
            
        
        food_distance = self.calculate_distance(self.food, self.head)
        return obs_infront, obs_left, obs_right, food_distance, food_left, food_right, food_infront, food_behind 



    def is_colision(self, point = None):
        if point == None:
            point = self.head
        
        if (point.x > self.width - BLOCKSIZE) or (point.x < 0) or (point.y > self.height - BLOCKSIZE) or (point.y < 0):
            return True
        for part in self.snake[1:]:
            if (part.x == point.x) and (part.y == point.y):
                return True
        return False

    def move(self, direction):
        x = self.head.x
        y = self.head.y
       
        if direction == Direction.RIGHT:
            x += BLOCKSIZE
        if direction == Direction.LEFT:
            x -= BLOCKSIZE
        if direction == Direction.UP:
            y -= BLOCKSIZE
        if direction == Direction.DOWN:
            y += BLOCKSIZE
        self.head = Point(x, y)

    def update_ui(self):
        self.display.fill(Color.BLACK.value)

        for pt in self.snake:
            pygame.draw.rect(self.display, Color.YELLOWLIGHT.value, pygame.Rect(pt.x, pt.y, BLOCKSIZE, BLOCKSIZE))
            pygame.draw.rect(self.display, Color.YELLOWDARK.value, pygame.Rect(pt.x + 3, pt.y + 3, BLOCKSIZE - 6, BLOCKSIZE - 6))

        pygame.draw.rect(self.display, Color.RED.value, pygame.Rect(self.food.x, self.food.y, BLOCKSIZE, BLOCKSIZE))

        text = font.render(f"Score {self.score}", True, Color.WHITE.value)
        self.display.blit(text, [0, 0])
        pygame.display.flip() # updates changes 



