import pygame
import random
import time


class SnakeBody():
    def __init__(self,x,y) -> None:
        self.width = 5
        self.position = (x,y)

    def draw(self,surface,color):
        pygame.draw.circle(surface,color,self.position,self.width)

class Snake:
    color = "green"
    def __init__(self) -> None:
        self.direction = "right"
        self.body = []
        self.body.append(SnakeBody(350,350))
        self.body.append(SnakeBody(345,350))
        self.body.append(SnakeBody(340,350))

    def draw(self,surface):
        for body in self.body:
            body.draw(surface,self.color)
   
    def set_direction(self,direction):
        self.direction = direction  

    def moveSnake(self):
        counter = 1
        for body in reversed(self.body):
            tmp = list(body.position)
            if (counter < len(self.body)):
                reversed_list = list(reversed(self.body))
                body.position = reversed_list[counter].position
                counter += 1
            else:
                tmp = list(body.position)
                if self.direction == "right":
                    tmp[0] +=10
                if self.direction == "left":
                    tmp[0] -=10
                if self.direction == "up":
                    tmp[1] -=10
                if self.direction == "down":
                    tmp[1] +=10
                self.body[0].position = tuple(tmp)

class Board:
    def __init__(self,snake) -> None:
        self.score = 1
        self.snake = snake
        self.width = 700
        self.height = 700
        self.screen = pygame.display.set_mode((self.height,self.width))
        self.dots = []
        self.score = 1

    def checkLost(self):
        head = list(self.snake.body[0].position)
        if (head[0] > 700 or head[0] < 0 or head[1] > 700 or head[1] < 0):
            return True
        else:
            return False

    def checkDots(self):
        head = list(self.snake.body[0].position)
        tmp = 0
        for dot in self.dots:
            dot_position = list(dot.position)
            if ((dot_position[0] <= int(head[0]) + 5 and dot_position[0] >= int(head[0]) - 5)
                 and (dot_position[1] <= int(head[1]) + 5 and dot_position[1] >= int(head[1]) - 5)):
                self.increase_score()
                last_body = self.snake.body[-1].position
                if self.snake.direction == "right":
                    x = last_body[0]-10
                    y = last_body[1]
                if self.snake.direction == "left":
                    x = last_body[0]+10
                    y = last_body[1]
                if self.snake.direction == "up":
                    x = last_body[0]
                    y = last_body[1]+10
                if self.snake.direction == "down":
                    x = last_body[0]
                    y = last_body[1]-10
                self.snake.body.append(SnakeBody(x,y))
                tmp = dot 
                break
        if tmp != 0:
            self.dots.remove(tmp)
            tmp = 0

    def drawSnake(self):
        self.snake.draw(self.screen)

    def draw_dots(self):
        for dot in self.dots:
            dot.draw(self.screen)

    def add_dot(self,dot):
        self.dots.append(dot)

    def draw_text(self,text):
        self.screen.blit(text,(20,20))

    def draw_text_end(self,text):
        self.screen.blit(text,(350,350))

    def increase_score(self):
        self.score += 1

class Dot:
    def __init__(self) -> None:
        self.position = (random.randint(0,700),random.randint(0,700)) 
        self.width = 5
        self.color = "orange"

    def draw(self,surface):
        pygame.draw.circle(surface,self.color,self.position,self.width)

    

pygame.init()
clock = pygame.time.Clock()
running = True


snake = Snake()
board = Board(snake)
font_size = 15
font = pygame.font.Font(pygame.font.get_default_font(), font_size)
start_time = time.time()
start_time2 = start_time
sleep = 0.1

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            #board.increase_score()
            if event.key == pygame.K_DOWN:
                board.snake.set_direction("down")
            if event.key == pygame.K_UP:
                board.snake.set_direction("up")
            if event.key == pygame.K_LEFT:
                board.snake.set_direction("left")
            if event.key == pygame.K_RIGHT:
                board.snake.set_direction("right")
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    board.screen.fill("black")

    if time.time() - start_time  >= 5:
        board.add_dot(Dot())
        start_time = time.time()
    if (sleep-0.01 > 0):
        if time.time() - start_time2 >=25:
            sleep -= 0.01
            start_time2 = time.time()

    # RENDER YOUR GAME HERE
    board.drawSnake()
    board.snake.moveSnake()
    board.checkDots()
    board.draw_dots()
    score_text = font.render(f"Score: {board.score} ", True, (255,255,255), None)
    board.draw_text(score_text)
    # flip() the display to put your work on screen
    pygame.display.flip()
    time.sleep(sleep)

    if board.checkLost() is True:
        board.screen.fill("black")
        score_text = font.render("You LOST!!!", True, (255,255,255), None)
        board.draw_text_end(score_text)
        pygame.display.flip()
        time.sleep(2)
        break


    clock.tick(60)  # limits FPS to 60

pygame.quit()