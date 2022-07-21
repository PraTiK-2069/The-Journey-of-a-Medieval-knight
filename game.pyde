import os, glob, copy
import random
add_library('minim')
player = Minim(this)
path = os.getcwd()

class Game:
    def __init__(self, w, h, g):
        self.animations_hero = ['_walking','_throwing','_axe' , '_ghost', '_aoe']
        self.animations_enemies = ['_walking', '_attacking', '_dead']
        self.frames_hero = [9, 8, 6, 16, 9]
        self.frames_enemies = {"enemy_1": [9, 11, 1], "enemy_2": [9, 8, 1]}
        self.w = w
        self.h = h
        self.g = g
        self.score = 0
        self.Hero = Hero(100, 300, self.g, 10, "hero", self.animations_hero, self.frames_hero, 0, 100)
        self.bg = loadImage(path+'/layers/game_background_1.png')
        self.bgMusic = player.loadFile(path+"/Saga-of-Knight.mp3")
        self.bgMusic.loop()
        self.pause = False
        self.sound = False
        self.enemies = []
        for i in range(10):
            enemyType = random.choice(["enemy_1", "enemy_2"])
            self.enemies.append(Enemies(1300+200*(i)*((-1)**i), 300+i*10, self.g,10, enemyType, self.animations_enemies, self.frames_enemies[enemyType], 0, self.Hero, 3))
        
    
    def display(self):
        image(self.bg, 0, 0, self.w, self.h)
    
    def hits(self):
        if self.sound == True:
            self.bgMusic.loop()
        for e in self.enemies:
            if e.dir ==0 and e.x <= self.Hero.hit[0]-35 and e.x > self.Hero.hit[0]-100 and e.y < self.Hero.hit[1] + 35 and e.y > self.Hero.hit[1] - 35:
                e.hitpoints -= 1
            if e.dir ==1 and e.x >= self.Hero.hit[0]+35 and e.x < self.Hero.hit[0]+100 and e.y > self.Hero.hit[1] - 35 and e.y < self.Hero.hit[1] + 35:
                e.hitpoints -= 1
            
            if e.hero.ghost == True and (e.hero.x-e.x)**2 + (e.hero.y-e.y)**2 < 24000 and (e.hero.keyHandler[RIGHT] or e.hero.keyHandler[LEFT]or e.hero.keyHandler[UP] or e.hero.keyHandler[DOWN]):
                e.hitpoints -=0.10
            
    def killcount(self):
        for e in self.enemies:
            if e.hitpoints < 1 and e.deathframe >= 60:
                self.enemies.remove(e)
                self.score += 1
                    
    def new_enemies(self):
        if len(self.enemies)<5:
            for i in range(4):
                enemyType = random.choice(["enemy_1", "enemy_2"])
                self.enemies.append(Enemies(1310, 470-75*i, self.g,10, enemyType, self.animations_enemies, self.frames_enemies[enemyType], 0, self.Hero, 3))
                self.enemies.append(Enemies(-30, 470-75*i, self.g,10, enemyType, self.animations_enemies, self.frames_enemies[enemyType], 0, self.Hero, 3))
    
class Creature:
    def __init__(self, x, y, g, r, charName, images, F, hitpoints):
        self.x = x
        self.y = y
        self.g = g
        self.r = r
        self.vx = 0
        self.vy = 0
        self.charName = charName
        self.img = ["" for i in range(len(images))]
        self.f = 0
        self.F = F
        self. w = ["" for i in range(len(images))]
        self.h = ["" for i in range(len(images))]
        self.hitpoints = hitpoints
        self.deathframe = 0

        for i in range(len(images)):
            self.img[i] = loadImage(path+"/"+charName+"/"+charName+images[i]+'.png')
            sizeSprite = 0
            sizeSprite = PImage()
            sizeSprite = loadImage(path+"/"+charName+"/"+charName+images[i]+'.png')
            self.w[i] = sizeSprite.width/F[i]
            self.h[i] = sizeSprite.height
        
        
    def update(self):
        if self.hitpoints > 0:
            self.x += self.vx
            self.y += self.vy
            if self.y +self.r > self.g:
                self.y = self.g - self.r
    
            
            
        

class Hero(Creature):
    def __init__(self, x, y, g,r, charName, images, F, dir, hitpoints):
        Creature.__init__(self, x, y, g,r, charName, images,F, hitpoints)
        self.keyHandler = {LEFT: False, RIGHT: False, UP: False, DOWN: False, "Attack": False}
        self.dir = 1
        self.ghost = False
        self.hit = [0, 0]
    def update_hit(self):
        self.hit = [0, 0]
    def update(self):
        if self.keyHandler[LEFT]:
            self.vx = -15
        elif self.keyHandler[RIGHT]:
            self.vx = 15
        else:
            self.vx = 0
        
        if self.keyHandler[UP]:
            self.vy = -10
        elif self.keyHandler[DOWN]:
            self.vy = 10
        else: self.vy = 0
        
        self.x += self.vx
        self.y += self.vy
        
        if self.y +self.r > self.g:
            self.y = self.g - self.r
            
        if self.y +self.r < 250 :
            self.y = 250
            
        if self.x +self.r > 1280:
            self.x = 1280 - self.r*2
            
        if self.x +self.r < 0 :
            self.x = self.r
    def ghostAttack(self):
        if self.keyHandler[RIGHT] or self.keyHandler[LEFT]or self.keyHandler[UP] or self.keyHandler[DOWN]:
            if self.ghost == True:
                image(self.img[4], self.x-self.r-100, self.y-self.r-100, 300, 300, 0, 0, self.w[4], self.h[4])
    def display(self):
        if self.ghost == False:
            figure = self.img[0]
        elif self.ghost == True:
            figure = self.img[3]
            
        if self.keyHandler[RIGHT] or self.keyHandler[LEFT]or self.keyHandler[UP] or self.keyHandler[DOWN]:
            self.f = (self.f+1)%self.F[4]
            if self.f == 0:
                self.f = 1
                
            if self.keyHandler[RIGHT] or (self.dir == 1 and self.keyHandler[UP]) or ((self.dir == 1 and self.keyHandler[DOWN])):
                image(figure, self.x-self.r, self.y-self.r, 100, 100, self.f*self.w[0], 0, (self.f+1)*self.w[0], self.h[0])
            elif self.keyHandler[LEFT] or (self.dir == 0 and self.keyHandler[UP]) or (self.dir == 0 and self.keyHandler[DOWN]):
                image(figure, self.x-self.r, self.y-self.r, 100, 100, (self.f+1)*self.w[0], 0, self.f*self.w[0], self.h[0])
            
        elif self.keyHandler['Attack'] and self.ghost == False:
            self.f = (self.f+1)%self.F[1]
            if self.f == 0:
                self.f = 1
            if self.dir == 1:
                image(self.img[1], self.x-self.r, self.y-self.r, 100, 100, self.f*self.w[1], 0, (self.f+1)*self.w[1], self.h[1])
                image(self.img[2], self.x-self.r+(self.f-2)*70, self.y-self.r-12 , 100, 100, self.f*self.w[1], 0, (self.f+1)*self.w[2], self.h[2])
                self.hit[0] = self.x-self.r+(self.f-2)*70
                self.hit[1] = self.y-self.r-12
            elif self.dir == 0:
                image(self.img[1], self.x-self.r, self.y-self.r, 100, 100, (self.f+1)*self.w[1], 0, self.f*self.w[1], self.h[1]) 
                image(self.img[2], self.x-self.r-(self.f-2)*70, self.y-self.r-12, 100, 100, (self.f+1)*self.w[2], 0, self.f*self.w[2], self.h[2])   
                self.hit[0] = self.x-self.r-(self.f-2)*70     
                self.hit[1] = self.y-self.r-12
        else:
            self.f = 0
            if self.dir == 1: 
                image(figure, self.x-self.r, self.y-self.r, 100, 100, 0, 0,self.w[0], self.h[0])
            else:
                image(figure, self.x-self.r, self.y-self.r, 100, 100, self.w[0], 0,0, self.h[0])

class Enemies(Creature):   
    def __init__(self, x, y, g,r, charName, images, F, dir, hero, hitpoints):
        Creature.__init__(self, x, y, g,r, charName, images,F, hitpoints)
        self.dir = 1   
        self.hero = hero
        self.hitpoints = hitpoints
    def update(self):
        if self.hitpoints > 0:
            self.x += self.vx
            self.y += self.vy
            if self.x < self.hero.x:
                self.vx = 3
                self.dir = 1
            elif self.x > self.hero.x:
                self.vx = -3
                self.dir = 0
            else: 
                self.x = self.hero.x
                self.vx = 0
            
            #Version_1
            """if self.y < self.hero.y:
                self.vy = 3
            elif self.y > self.hero.y: 
                self.vy = -3
            else: 
                self.vy = 0"""
                    
            # Version_2
            """if self.y < self.hero.y and (self.hero.x-self.x)**2 + (self.hero.y-self.y)**2 < 40000:
                self.vy = 3
            elif self.y > self.hero.y and (self.hero.x-self.x)**2 + (self.hero.y-self.y)**2 < 40000: 
                self.vy = -3
            else: 
                self.vy = 0"""
                
            #Version_3
            if self.y < self.hero.y and (self.hero.x-self.x)**2 < 5625:
                self.vy = 3
            elif self.y > self.hero.y and (self.x - self.hero.x)**2 < 5625: 
                self.vy = -3
            else: 
                self.vy = 0
    def display(self):
        if self.hitpoints > 0 and (self.x-self.hero.x)**2+(self.y-self.hero.y)**2 > 5000:
            figure = self.img[0]
            self.f = (self.f+1)%self.F[0]
            if self.f == 0:
                self.f = 1  
            if self.dir == 1:
                image(figure, self.x-self.r, self.y-self.r, 100, 100, self.f*self.w[0], 0, (self.f+1)*self.w[0], self.h[0])
            else:
                image(figure, self.x-self.r, self.y-self.r, 100, 100, (self.f+1)*self.w[0], 0, self.f*self.w[0], self.h[0])
        elif self.hitpoints > 0:
            self.hero.hitpoints -= 0.5
            self.vx = 0
            self.vy = 0
            figure = self.img[1]
            self.f = (self.f+1)%self.F[1]
            if self.f == 0:
                self.f = 1  
            if self.dir == 1:
                image(figure, self.x-self.r, self.y-self.r, 100, 100, self.f*self.w[1], 0, (self.f+1)*self.w[1], self.h[1])
            else:
                image(figure, self.x-self.r, self.y-self.r, 100, 100, (self.f+1)*self.w[1], 0, self.f*self.w[1], self.h[1])
            
        elif self.hitpoints <= 0:
            self.vx = 0
            self.vy = 0
            figure = self.img[2]
            self.f = 0
            self.deathframe += 1
            
            if self.dir == 1:
                image(figure, self.x-self.r, self.y-self.r, 100, 100, self.f*self.w[2], 0, (self.f+1)*self.w[2], self.h[2])
            else:
                image(figure, self.x-self.r, self.y-self.r, 100, 100, (self.f+1)*self.w[2], 0, self.f*self.w[2], self.h[2])
            
        

game = Game(1280, 720, 470)

def setup():
    size(game.w, game.h)
    frameRate(12)

def draw():
    gameScore = "Total Kills: " + str(game.score)
    if game.pause == False and game.Hero.hitpoints > 0:
        background(255)
        game.display()
        game.hits()
        game.killcount()
        game.Hero.update_hit()
        game.new_enemies()
        objects = []
        objects.extend(game.enemies)
        objects.append(game.Hero)
        objects.sort(key=lambda x: x.y, reverse=False)
        game.Hero.ghostAttack()
        for e in objects:
            e.update()
            e.display()
        textSize(32)
        text(gameScore, 50, 40)
        points = "Hero Hit points:" + str(game.Hero.hitpoints)
        text(points, 50, 70)
    elif game.pause == True and game.Hero.hitpoints > 0: 
        background(255)
        img = loadImage(path+'/hero/pause.png')
        image(img, 0, 0, 1280, 720)
        textSize(32)
        text(gameScore, 50, 100)
    else:
        img = loadImage(path+'/hero/dead.jpeg')
        image(img, 0, 0, 1280, 720)
        textSize(64)
        text(gameScore, 200, 100)
        text("Click Here To Start A New Game", 200, 525)
        
        
        


def keyPressed():
    global game
    if key == 't' and game.Hero.ghost == False:
        game.Hero.ghost = True
    elif key == 't' and game.Hero.ghost == True:
        game.Hero.ghost = False
    
    if key == 'm' and game.sound == False:
        game.sound = True
    elif key == 'm' and game.sound == True:
        game.sound = False
        
    if keyCode == LEFT:
        game.Hero.keyHandler[LEFT] = True
        game.Hero.dir = 0
    elif keyCode == RIGHT:
        game.Hero.keyHandler[RIGHT] = True
        game.Hero.dir = 1
    elif keyCode == UP:
        game.Hero.keyHandler[UP] = True
    elif keyCode == DOWN:
        game.Hero.keyHandler[DOWN] = True
    elif key == " ":
        game.Hero.keyHandler["Attack"] = True
    
    if key == 'p' and game.pause == False:
        game.pause = True
    elif key == 'p' and game.pause == True:
        game.pause = False
    


    

def keyReleased():
    if keyCode == LEFT:
        game.Hero.keyHandler[LEFT] = False
    elif keyCode == RIGHT:
        game.Hero.keyHandler[RIGHT] = False
    elif keyCode == UP:
        game.Hero.keyHandler[UP] = False
    elif keyCode == DOWN:
        game.Hero.keyHandler[DOWN] = False
    elif key == " ":
        game.Hero.keyHandler["Attack"] = False

def mouseClicked():
    global game
    if game.Hero.hitpoints <= 0:
        game = Game(1280, 720, 470)
