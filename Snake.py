from math import e
import os
import random
import curses
width,height = (5,5)


up, down, left, right = -width,+width,-1, +1

SNAKE = "*"
HEAD = "@"
FOOD = "+"

class Direction:
    def __init__(self,directionName,map_):
        self.map_ = map_
        self.dirDict = {"UP":-map_.width,"DOWN":map_.width,"LEFT":-1,"RIGHT":+1}
        self.direction = self.dirDict.get(directionName) or self.dirDict["UP"] # set certain direction or default direction if invalid

    def toPosition(self,count):
        return Position(self.map_,self.direction * count) # maybe count can be negative?

    def opposite(self):
        return Direction([i[0] for i in self.dirdict.items() if i[1] == -self.direction][0],self.dirDict["DOWN"])


class Position:
    def __init__(self,maps,pos: int):
        self.map_ = maps
        self.positionInt = pos

    def plus(self,pos):
        return Position(self.map_,(self.positionInt + pos.positionInt) % self.map_.size()) # "%": check overflow

    def toXY(self):
        return (self.positionInt // self.map_.width,self.positionInt % self.map_.width)

    def fromXY(self,map_,X,Y):
        return Position(map_, (Y-1)*map_.width + X)

class Map:
    def __init__(self,fill,width,height,window: curses.window):
        self.window = window
        self.map_ = [fill]*width*height
        self.filling = fill
        self.width = width
        self.height = height
        self.drt_UP = Direction("UP",self)
        self.drt_DOWN = Direction("DOWN",self)
        self.drt_LEFT = Direction("LEFT",self)
        self.drt_RIGHT = Direction("RIGHT",self)


    def size(self):
        return len(self.map_)
    
    def print(self,pos,obj):
        self.map_[pos.positionInt] = obj

    def test(self,pos,obj):
        return self.map_[pos.positionInt] == obj

    def get(self,pos):
        return self.map_[pos.positionInt]

    def render(self):
        for index,char in enumerate(self.map_):
            lines, cols = Position(self,index).toXY()
            self.window.addch(lines,cols*2,ord(char))
        self.window.refresh()


class SnakeDiedError(Exception):
    pass


class moving:
    
    def __init__(self,position:Position,direction:Direction,map_:Map):
        self.position = position
        self.direction = direction
        self.map_ = map_


    def move(self):
        self.position = self.position.plus(self.direction.toPosition(1))
    

    def turn(self,direction: Direction):
        self.direction = direction
    

class SnakeTail(moving):


    def follow(self,head):
        self.map_.print(self.position,self.map_.filling)
        self.move()
        self.turn(head.turner.get(self.position) or self.direction)
        head.turner.print(self.position,None) # turn completed


class SnakeHead(moving):

    def __init__(self,position: Position,direction: Direction,map_: Map):
        super().__init__(position,direction,map_)
        self.full = False
        self.turner = Map(None,map_.width,map_.height,None)
        self.map_.print(self.position, HEAD)


    def invalid(self):
        return self.map_.test(self.position,SNAKE)
    
    def turn(self,direction: Direction):
        if abs(direction.direction) != abs(self.direction.direction): # no backward
            super().turn(direction)
            self.turner.print(self.position,direction)

    def isFull(self):
        return self.map_.test(self.position,FOOD)

    def move(self):
        self.map_.print(self.position,SNAKE)
        super().move()
        if self.invalid():
            raise SnakeDiedError
        elif self.isFull():
            self.full = True
        self.map_.print(self.position,HEAD)


class Snake:

    def __init__(self,map_):
        self.map_ = map_
    
    def move(self):
        self.head.move()
        if not self.head.full:
            self.tail.follow(self.head)
        else :
            self.head.full = False
            feed(self.map_)
            
    
    def turn(self,direction):
        self.head.turn(direction)

    def spawn(self,position):
        self.head = SnakeHead(position,self.map_.drt_UP,self.map_)
        self.tail = SnakeTail(position.plus(self.map_.drt_DOWN.toPosition(2)),self.map_.drt_UP,self.map_)
        self.map_.print(position.plus(self.map_.drt_DOWN.toPosition(1)),SNAKE)
        self.map_.print(position.plus(self.map_.drt_DOWN.toPosition(2)),SNAKE)



def feed(map_:Map):
    index = Position(map_,random.randint(0,map_.size()-1))
    count=0
    while not map_.test(index,map_.filling):
        index = Position(map_,random.randint(0,map_.size()-1))
        count+=1
        if count > map_.size()+1:
            return
    map_.print(index,FOOD)
stdscr = curses.initscr()
def main(stdscr:curses.window):
    win = stdscr.derwin(height+1,width*2,int((curses.LINES - height)//2), int((curses.COLS - width*2)//2))

    map_ = Map('-',width,height,win)
    snake = Snake(map_)
    snake.spawn(Position(map_,map_.size() // 2))

    feed(map_)
    map_.render()
    while True:
        try:
            key = stdscr.getch()
            if key == ord('w'):
                snake.turn(map_.drt_UP)
            elif key == ord('s'):
                snake.turn(map_.drt_DOWN)
            elif key == ord('a'):
                snake.turn(map_.drt_LEFT)
            elif key == ord('d'):
                snake.turn(map_.drt_RIGHT)
            elif key == ord('q'):
                return
            snake.move()
            map_.render()
        except SnakeDiedError:
            print('Snake is dead!')
            return
curses.wrapper(main)
exit()