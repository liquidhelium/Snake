import os
import random
width,height = (20,9)

map = ["-"]*width*height

up, down, left, right = -width,+width,-1, +1

SNAKE = "*"
HEAD = "@"
FOOD = "+"

class SnakeDiedError(Exception):
    pass
class moving:
    
    def __init__(self,position,direction):
        self.position = position
        self.direction = direction


    def move(self):
        self.position = (self.position + self.direction ) % len(map) # no width overflow check
    

    def turn(self,direction):
        self.direction = direction
    

class SnakeTail(moving):


    def follow(self,head):
        map[self.position] = "-"
        self.move()
        self.turn(head.turner[self.position] or self.direction)
        head.turner[self.position] = None


class SnakeHead(moving):

    def __init__(self,position,direction):
        super().__init__(position,direction)
        self.full = False
        self.turner = [None]*len(map)
        map[self.position] = HEAD


    def invalid(self):
        return map[self.position] == SNAKE
    
    def turn(self,direction):
        if abs(direction) != abs(self.direction): # no backward
            super().turn(direction)
            self.turner[self.position] = direction
    def isFull(self):
        return map[self.position] == FOOD

    def move(self):
        map[self.position] = SNAKE
        super().move()
        if self.invalid():
            raise SnakeDiedError
        elif self.isFull():
            self.full = True
        map[self.position] = HEAD 


class Snake:

    def __init__(self,position):
        self.head = SnakeHead(position,up)
        self.tail = SnakeTail(position + 2*down,up)
        map[position + down] = SNAKE
        map[position + 2*down] = SNAKE
    
    def move(self):
        self.head.move()
        if not self.head.full:
            self.tail.follow(self.head)
        else :
            self.head.full = False
            feed()
            
    
    def turn(self,direction):
        self.head.turn(direction)

def render(map,width):
    for position,char in enumerate(map):
        print(char,end = " ")
        if (position+1) % width == 0 and position != 0:
            print()

def feed():
    index = random.randint(0,len(map)-1)
    while not map[index] == '-':
        index = random.randint(0,len(map)-1)
    map[index] = FOOD


snake = Snake(len(map) // 2)
import msvcrt
feed()
render(map,width)
while True:
    try:
        key = msvcrt.getch()
        if key == b'w':
            snake.turn(up)
        elif key == b's':
            snake.turn(down)
        elif key == b'a':
            snake.turn(left)
        elif key == b'd':
            snake.turn(right)
        snake.move()
        os.system('cls')
        render(map,width)
    except SnakeDiedError:
        print('Snake is dead!')
        break
input()