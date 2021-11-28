import pygame
from pygame import display, image, time
import random
import os

IMAGES_PATH = "Images/"

PPS = 0
DELTATIME=1/60
bg = pygame.image.load(IMAGES_PATH+"SandTextureRadioactive.png")

class Game():
    global PPS
    # constants
    windowHeight = 800
    windowWidth = 800
    PPS = windowHeight/5

    # types of different eatable things
    soup = image.load(IMAGES_PATH+"soup.png")
    barrel = image.load(IMAGES_PATH+"RadioactiveBarrel.png")
    health = image.load(IMAGES_PATH+"health_pak.png")
    back = image.load(IMAGES_PATH+"HazmatManBack.png")
    front = image.load(IMAGES_PATH+"HazmatManFront.png")
    right = image.load(IMAGES_PATH+"HazmatManRight.png")
    left = image.load(IMAGES_PATH+"HazmatManLeft.png")

    def __init__(self):
        self.screen = display.set_mode([800, 800])
        self.running = True

def button(menu, xpos, ypos, text):
    font = pygame.font.SysFont(None, 30)
    text_img = font.render(text, True, "BLACK")
    x, y, w , h = text_img.get_rect()
    x, y = xpos, ypos
    pygame.draw.rect(menu, "WHITE", (x, y, w, h))
    return menu.blit(text_img, (xpos, ypos))

# Turn left, go forwards, go right
# Direction = [0,0,0]

# would you not do like 0,1,2,3 -> n,e,s,w
class Player(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, direction, speed, size):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = xpos  # 0 to window width
        self.ypos = ypos  # 0 to window height
        self.direction = direction  # ['n', 'e', 's', 'w']
        self.speed = speed  # float between 0 and 1
        self.radiationMultiplier = 1.0
        self.radiation = 0.0 # from 0 to 100 (float, 2 decimal points)
        self.dead = False # boolean
        self.size = size
        self.image = game.front #UH WAT DIS
        self.keysDown=[False,False,False,False] # up,down,left,right

    def getSize(self):
        return self.size

    def getXPos(self):
        return self.xpos

    def getYPos(self):
        return self.ypos

    def move(self):
        # up,down,left,right
        if player.keysDown[0] == True:
            self.ypos-=self.speed*DELTATIME*PPS*self.radiationMultiplier
            self.image = game.back
        elif player.keysDown[1] == True:
            self.ypos+=self.speed*DELTATIME*PPS*self.radiationMultiplier
            self.image = game.front
        if player.keysDown[2] == True:
            self.xpos-=self.speed*DELTATIME*PPS*self.radiationMultiplier
            self.image = game.left
        elif player.keysDown[3] == True:
            self.xpos+=self.speed*DELTATIME*PPS*self.radiationMultiplier
            self.image = game.right

    # Determined by radation level
    def setRadiation(self):
        # Some funcky function that give radiation poisoning
        ## self.radiationMultiplier = (100-(self.radiation+(5*(self.radiation**(1/12)))))/100

        self.radiationMultiplier = 1-((self.radiation**12)/(10**24))

        if self.radiation >= 100:
            self.dead = True

        # Background radiation
        #                 1/60
        self.radiation += 1/15

    def keyCheck(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                player.direction='n'
                self.keysDown[0]=True
            elif event.key==pygame.K_RIGHT:
                player.direction='e'
                self.keysDown[3]=True
            if event.key==pygame.K_DOWN:
                player.direction='s'
                self.keysDown[1]=True
            if event.key==pygame.K_LEFT:
                player.direction='w'
                self.keysDown[2]=True
        if  event.type == pygame.KEYUP:
            if event.key==pygame.K_UP:
                self.keysDown[0]=False
            if event.key==pygame.K_RIGHT:
                self.keysDown[3]=False
            if event.key==pygame.K_DOWN:
                self.keysDown[1]=False
            if event.key==pygame.K_LEFT:
                self.keysDown[2]=False

    def collidehdl(self): #handle collision
        global foods
        global game
        if self.xpos<0:
            self.direction='e'
            self.xpos=0
        elif self.xpos>game.windowWidth-32:
            self.direction='w'
            self.xpos=game.windowWidth-32
        if self.ypos<0:
            self.direction='s'
            self.ypos=0
        elif self.ypos>game.windowHeight-32:
            self.direction='n'
            self.ypos=game.windowHeight-32

        foods_collided=[] # list of index of foods collided with
        for food in foods:
            if collidechk(self,food):
                foods_collided.append(food)

        for i in foods_collided:
            #add radioactive calc stuff here
            if player.radiation + i.radiation >= 0:
                player.radiation += i.radiation
            foods.remove(i)

class Food(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, image, radiation):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.radiation = radiation
        self.xpos = xpos
        self.ypos = ypos
        self.size=(32,32)

def spawnPlayer(game):
    xpos=random.randint(50, game.windowWidth-50)
    ypos=random.randint(50, game.windowHeight-50)
    direction = 's'
    speed = 1
    return Player(xpos,ypos,direction,speed,(32,32))


def spawnFood(game, foods):
    #spawn food away from player
    colliding = True
    xpos = random.randint(50, game.windowWidth - 50)
    ypos = random.randint(50, game.windowHeight - 50)
    while colliding:
        for i in range(len(foods)):
            if (xpos > foods[i].xpos and (xpos + 32) < foods[i].xpos) or ((ypos > foods[i].ypos) and (ypos + 32) < foods[i].ypos):
                xpos = random.randint(50, game.windowWidth - 50)
                ypos = random.randint(50, game.windowHeight - 50)
                break
        else:
            colliding = False

    food_type = random.choice([game.soup, game.barrel, game.health])
    if food_type == game.soup:
        rad = -2.5
    elif food_type == game.barrel:
        rad = 10
    elif food_type == game.health:
        rad = -5.5

    return Food(xpos, ypos, food_type, rad)

def place_food():
    global foods
    foods.clear()
    food_group.remove()
    number = random.randint(5, 10)
    for i in range(number):
        food = spawnFood(game, foods)
        foods.append(food)
        food_group.add(food)

def collidechk(obj1,obj2):
    if obj2.xpos<=obj1.xpos<obj2.xpos+obj2.size[0] and obj2.ypos<=obj1.ypos<obj2.ypos+obj2.size[1]:
        return True
    if obj2.xpos<=obj1.xpos+obj1.size[0]<obj2.xpos+obj2.size[0] and obj2.ypos<=obj1.ypos+obj1.size[1]<obj2.ypos+obj2.size[1]:
        return True
    if obj2.xpos<=obj1.xpos+obj1.size[0]<obj2.xpos+obj2.size[0] and obj2.ypos<=obj1.ypos<obj2.ypos+obj2.size[1]:
        return True
    if obj2.xpos<=obj1.xpos<obj2.xpos+obj2.size[0] and obj2.ypos<=obj1.ypos+obj1.size[1]<obj2.ypos+obj2.size[1]:
        return True
    return False

def paused():
    global pause, pause_time, gametime
    text = pygame.font.SysFont(None, 24)
    text_img = text.render('Game paused', True, "WHITE")
    game.screen.blit(text_img, (game.windowWidth/2 - 50, game.windowHeight/2 - 10))
    display.flip()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause_time = int(pygame.time.get_ticks()/1000) - menu_time - gametime
                    pause = False

def gameloop():
    global pause_time, gametime
    pause_time = 0
    global pause
    pause = False
    once = 0
    global foods
    clock = time.Clock()
    food_clock = time.Clock()
    place_food()
    while game.running:
        # For each pygame event
        if player.dead == True:
                print("Dead")
                game.running = False
                break
        for event in pygame.event.get():
            # If quit event (close button) called then

            if event.type == pygame.QUIT:
                game.running = False
                # Break out of loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = True
                    paused()

            player.keyCheck(event)
        player.move()
        player.setRadiation()
        # debugging
        #print("Radiation",str(round(player.radiation, 2))+"%", "Radiation Mul" + str(player.radiationMultiplier))
        player.collidehdl()
        player.update()

        gametime = int(pygame.time.get_ticks()/1000) - menu_time - pause_time

        font = pygame.font.SysFont(None, 24)
        rad_text = "Radiation: " + str(round(player.radiation, 1)) + "%"
        img = font.render(rad_text, True, "WHITE")
        time_text = "Time: " + str(gametime)
        time_font = pygame.font.SysFont(None, 24)
        time_img = time_font.render(time_text, True, "WHITE")

        #gametime = int(pygame.time.get_ticks()/1000) - menu_time
        if gametime%10 == 0 and once == 0:
            place_food()
            once = 1
        elif gametime%10 != 0:
            once = 0

        # Update frame
        game.screen.blit(bg, (0,0))

        for i in range(len(foods)):
            game.screen.blit(foods[i].image,(foods[i].xpos,foods[i].ypos))

        game.screen.blit(img, (game.windowWidth - 145, 15))

        game.screen.blit(player.image,(player.xpos,player.ypos))
        game.screen.blit(time_img, (15, 15))
        display.flip()
        game.screen.fill((0,0,0,128))
        # display.update()
        clock.tick(60)

    over_text = "GAME OVER"
    over_font = pygame.font.SysFont(None, 24)
    over_img = over_font.render(over_text, True, "WHITE")
    game.screen.blit(over_img, (game.windowWidth/2 - 30, game.windowHeight/2 - 10))
    display.flip()
    game.screen.fill((0,0,0,128))
    pygame.time.wait(1000)
    pygame.quit()
    quit()

def start_menu():
    global menu_time
    intro = True
    menu = display.set_mode([800, 800])
    menu.fill((0,0,0,128))
    menu_font = pygame.font.SysFont(None, 48)
    menu_img = menu_font.render("HUNGRY HUNGRY WASTEMAN", True, "WHITE")
    menu.blit(menu_img, (game.windowWidth/2 - 250, 30))
    start = button(menu, game.windowWidth/2 - 20, game.windowHeight/2 - 10, "START")
    display.flip()
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.collidepoint(pygame.mouse.get_pos()):
                    menu_time = int(pygame.time.get_ticks()/1000)
                    gameloop()

if __name__ == "__main__":
    global foods
    food_group = pygame.sprite.Group()
    foods = []
    pygame.init()
    game = Game()
    player = spawnPlayer(game)
    start_menu()
