from pygame import *
from random import randint,choice

class GameSprite(sprite.Sprite):
    def __init__(self, img, x,y,w,h, speed):
        super().__init__()
        self. image = transform.scale(image.load(img), (w,h))
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.rect.h = h
        self.rect.w = w
    def reset(self):
        win.blit(self.image,(self.rect.x, self.rect.y))
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)

class Food(GameSprite):
    def __init__(self,img,x,y,w,h,speed):
        super().__init__(img,x,y,w,h,speed)
        self.images = list()
        self.images.append(self.image)

    def add_image(self,img):
        w = self.rect.w
        h = self.rect.h
        new_image = transform.scale(image.load(img),(w,h))
        self.images.append(new_image)

    def new_position(self):
        self.rect.x = randint(5,1350-self.rect.w)
        self.rect.y = randint(5,760-self.rect.h)
        self.image = choice(self.images)

class Snake(GameSprite):
    def __init__(self,img,x,y,w,h,speed):
        super().__init__(img,x,y,w,h,speed)
        self.images = list()
        self.images.append(self.image)
        for i in range(3):
            self.image=transform.rotate(self.image,90)
            self.images.append(self.image)

    def update(self,direction):
        if direction =='left':
            self.rect.x -= self.speed
            self.image = self.images[0]
        if direction =='right':
            self.rect.x += self.speed
            self.image = self.images[2]
        if direction =='up':
            self.rect.y -= self.speed
            self.image = self.images[3]
        if direction =='down':
            self.rect.y += self.speed
            self.image = self.images[1]



#создай окно игры
# infoOdject = display.Info()
win_h = 768
win_w = 1366
win = display.set_mode((win_w,win_h),FULLSCREEN)
display.set_caption('Змея')

#задай фон сцены
background = transform.scale(image.load('fon.jpg'),(win_w,win_h))
head = Snake('head.png', 350,250,60,60,3)
tale = Snake('telo.png',-100,-100,60,60,0)
food  = Food('apple.png', 100,100,60,60,0)
food.add_image('food.png')
food.add_image('pizza.png')
food.add_image('rol.png')
food.add_image('finograd.png')
food.add_image('dragon.png')
food.add_image('tomato.png')

# подключение шрифтов
font.init()
font1 = font.Font(None, 36)


game = True
direction = 'stop'
finish = False
eat = 0
snake = [head]

clock = time.Clock()
FPS = 60

while game:
    # поверка нажатия на кнопку выход
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_q:
            food.new_position()
        if e.type == KEYDOWN:
            if e.key ==K_w:
                direction = 'up'
            if e.key ==K_s:
                direction = 'down'
            if e.key ==K_d:
                direction = 'right'
            if e.key ==K_a:
                direction = 'left'
            if e.key ==K_SPACE:
                direction = 'stop'
    if finish != True:
        win.blit(background,(0,0))
        food.reset()
        
        for i in range(len(snake)-1, 0, -1):
            snake[i].rect.x = snake[i-1].rect.x
            snake[i].rect.y = snake[i-1].rect.y
            snake[i].reset()
        head.update(direction)
        head.reset()


        if head.rect.x<5 or head.rect.x>1366-60-5:
            finish = True
        if head.rect.y<5 or head.rect.x>1366-60-5:
            finish = True
        if head.rect.colliderect(food.rect):
            food.new_position()
            eat += 1
            tale.rect.x = head.rect.x
            tale.rect.y = head.rect.y
            snake.append(tale)
   
    display.update()
    clock.tick(FPS)