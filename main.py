import pygame

class paddle:

    def __init__(self,x_pos,y_pos,width,height,velocity):

        self.x = x_pos
        self.y = y_pos
        self.w = width
        self.h = height
        self.v = velocity
        
    def draw(self):
        pygame.draw.rect(window,(255,255,255),(self.x,self.y,self.w,self.h))
        

class ball:

    def __init__(self,x_pos,y_pos,width,height,velocity):
        self.x = x_pos
        self.y = y_pos 
        self.w = width
        self.h = height
        self.v = velocity
        self.dirx = 0
        self.diry = 1
    def draw(self):
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        pygame.draw.rect(window,(255,255,255),(self.x,self.y,self.w,self.h))

    def move(self):
        self.x += self.v*self.dirx
        self.y += self.v*self.diry

class bricks:

    def __init__(self):
        self.bricks_list = []
        self.bricks_colours_list = []
        self.bricks_colours = [(255,0,0),(0,255,0),(0,0,255)]
    
    def make_bricks(self):
        color = 0

        #this part was trial and error and a bit from online:
        a = 10
        b = 25
        y = 50
        for i in range(int((window_height/3)/a)):
            x = 50
            for j in range(int(window_width/b - 6)):
                brick = pygame.Rect(x,y,b,a)
                self.bricks_list.append(brick)
                self.bricks_colours_list.append(self.bricks_colours[color])
                x += 27
                color +=1
                if(color>2):
                    color =0
            y += 12

    def draw_bricks(self):
        for brick in self.bricks_list:
            brick_color = self.bricks_colours_list[self.bricks_list.index(brick)]
            pygame.draw.rect(window,brick_color,brick)

def paddle_collision():
    ball.diry = -1
    if ball.dirx == 0:
        if paddle.x<=ball.x<=ball.x+paddle.w/2:
            ball.dirx = -1
        else:
            ball.dirx = 1
    #pygame.mixer.music.load(sound_bounce)
    #pygame.mixer.music.load(r'/sounds/sound_bounce.wav')
    #pygame.mixer.music.play()

def display_text():
    font = pygame.font.Font('freesansbold.ttf',30)
    cyan = pygame.Color(0,255,255)
    text = font.render("Score: %i Lives: %i" % (score,lives),True,cyan)
    window.blit(text,((window_width-text.get_width())/2,window_height*2/3))

def game_finish(text):
    font = pygame.font.Font('freesansbold.ttf',40)
    yellow = pygame.Color(255,255,0)   
    text = font.render(" %s "%text,True,yellow)
    window.blit(text,((window_width-text.get_width())/2,window_height*2/3))

def redraw_window():
    window.fill((0,0,0))
    paddle.draw()
    ball.move()
    ball.draw()
    bricks.draw_bricks()
    if end_screen:
        game_finish(text)
    else:
        display_text()

    pygame.display.update()


#INITIALIZATIONS

#pygame initialize
pygame.init()

#window set up
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("BRICK SMASH")

#needed for tick
clock = pygame.time.Clock()

#paddle initialize
paddle = paddle(window_width/2,window_height-50,85,10,2)
paddle.draw()

#ball initialize
ball = ball(window_width/2,paddle.y-20,8,8,1)
ball.draw()

#bricks initialize
bricks = bricks()
bricks.make_bricks()
bricks.draw_bricks()

#score and lives
score = 0
lives = 3
end_screen = False
display_text()

#sounds
pygame.mixer.init()
#sound_bounce = '/sounds/sound_bounce.wav'
#sound_blip = '/sounds/sound_blip.wav'


#main game loop
run = True
while(run):
    clock.tick(500)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    #move paddle left
    if(keys[pygame.K_LEFT] and 0<=paddle.x):
        paddle.x -= paddle.v

    #move paddle right
    if(keys[pygame.K_RIGHT] and paddle.x<=window_width-paddle.w):
        paddle.x += paddle.v

    #Paddle Collision
    if((paddle.x<=ball.x<=paddle.x+paddle.w)and(paddle.y<=ball.y<=paddle.y+paddle.h)):
        paddle_collision()

    #Wall Collision
    if ball.y>=window_height:
        lives -= 1
        paddle.x, paddle.y = window_width/2,window_height-50
        ball.x, ball.y = window_width/2,paddle.y-20
        ball.dirx =0
        pygame.time.wait(1000)
    if ball.y<=0:
        ball.diry = 1
    if ball.x<=0:
        ball.dirx = 1
    if ball.x+ball.w>=window_width:
        ball.dirx = -1

    #Brick Collision
    collision = ball.rect.collidelist(bricks.bricks_list)
    if  collision!= -1:
        bricks.bricks_list.pop(collision)
        bricks.bricks_colours_list.pop(collision)#so that brick color doesn't change
        ball.diry = 1
        score += 1 
        #pygame.mixer.music.load(sound_blip)
        #pygame.mixer.music.load(r'/sounds/sound_blip.wav')
        #pygame.mixer.music.play()
    
    #game_win:
    if len(bricks.bricks_list)==0:
        text = "Congratulations ! You Won !"
        end_screen = True
        redraw_window()
        pygame.time.wait(5000)
        run = False
    #game_lose:
    if lives<=0:
        text = "Sorry, You Lost"
        end_screen = True
        redraw_window()
        pygame.time.wait(5000)
        run = False

    redraw_window()


pygame.quit()
quit()
