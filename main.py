
import pygame
import random
import math


''' All images found on Google Images '''

################################################################################
################################# Game Class ###################################
################################################################################

# Adapted framework from: http://blog.lukasperaza.com/getting-started-with-pygame/
class Game(object):

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=400, height=600, fps=50,title = 'Doodle Jump!'):
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.dx = 50
        self.dy = self.height-150
        self.dj = False
        self.dvy = 0
        self.day = 1
        self.mx = 100
        self.my = 300
        self.monRight = True
        self.timeElap = 0
        self.fakeTime = 0


    def init(self):
        self.offset = 0
        self.mode = 'menu'
        monster = Monster(self.width//2,-400,1,1) # 1st monster
        self.monsters = [monster]
        self.bullets = []
        self.player = 'single'
 

    def timerFired(self,dt):
        if self.mode!='gameOver':
            self.timeElap += dt
            if self.timeElap%10 == 0:
                if self.fakeTime >= 1:
                    self.fakeTime -= 0.1
                else: self.fakeTime += 0.1
                if self.mode == 'game':
                    self.score += 1
                    if self.player == 'multi':
                        self.score2+= 1


    def mouseMotion(self,x,y):
        pass


    def mousePressed(self,x,y):
        if self.mode == 'menu':
            self.splashScreenMousePressed(x,y)
        elif self.mode == 'gameOver':
            self.gameOverMousePressed(x,y)
        elif self.mode == 'help':
            self.helpScreenMousePressed(x,y)


    def helpScreenMousePressed(self,x,y):
        if 160<=x<=260 and 500<=y<=550:
            self.mode = 'menu'


    def splashScreenMousePressed(self,x,y):
        if 250<=x<=350 and 250<=y<=300:
            self.mode = 'game'
            self.player = 'single'
            self.initPlayerOne()
        if 250<=x<=350 and 450<=y<=500:
            self.mode = 'help'
        if 250<=x<=350 and 350<=y<=400:
            self.mode = 'game'
            self.player = 'multi'
            self.initPlayerOne()
            self.initPlayerTwo()


    def initPlayerOne(self):
        # initialize p1
        self.p1 = Player(self.width//2, self.height-200,1)
        platform = Platform(self.width//2,self.height-50) # 1st platform
        self.platforms = [platform]
        self.score = 0
        self.energy = 100


    def initPlayerTwo(self):
        # initialize p2
        self.p2 = Player(self.width//2 - 100,self.height-200,2)
        platform = Platform(self.width//2-100,self.height-50)
        self.platforms.append(platform)
        self.score2 = 0
        self.energy2 = 100


    def gameOverMousePressed(self,x,y):
        if 155<=x<=265 and 350<=y<=400:
            self.init() 


    def mouseReleased(self,x,y):
        pass


    def mouseDrag(self,x,y):
        pass


    def keyPressed(self,keyCode,modifier):
        if self.mode == 'game':
            self.p1.keyPressed(keyCode,modifier)
            if self.player == 'multi':
                self.p2.keyPressed(keyCode,modifier)


    def keyReleased(self,keyCode,modifier):
        pass


    def redrawAll(self,screen):
        if self.mode == 'menu':
            self.splashScreenRedrawAll(screen)
        if self.mode == 'help':
            self.helpScreenRedrawAll(screen)
        if self.mode == 'game':
            self.gameScreenRedrawAll(screen)
        if self.mode == 'gameOver':
            if self.player == 'multi':
                self.multiGameOverRedrawAll(screen)
            else:
                self.gameOverRedrawAll(screen)


    def multiGameOverRedrawAll(self,screen):
        self.drawBackground(screen)

        if self.score > self.score2:
            winner = 'Player 1 '
        elif self.score < self.score2:
            winner = 'Player 2 '
        else:
            winner = 'Both '

        file = pygame.font.match_font('al-seana')
        font = pygame.font.Font(file,70)
        red = (204,0,0)
        text = winner + 'won!'
        gameOver = font.render(text, True,red)
        screen.blit(gameOver,(25,100))

        finalScore = max(self.score,self.score2)
        score = font.render('score: ' + str(finalScore),True,(0,0,0))
        screen.blit(score,(25,200))

        color = (255,255,224)
        pygame.draw.ellipse(screen,color,(155,350,100,50))
        pygame.draw.ellipse(screen,(0,0,0),(155,350,100,50),2)
        font = pygame.font.Font(file,35)
        menu = font.render('menu',True,(0,0,0))
        screen.blit(menu,(175,350))


    def helpScreenRedrawAll(self,screen):
        self.drawBackground(screen)

        file = pygame.font.match_font('al-seana')
        font = pygame.font.Font(file,70)
        red = (204,0,0)
        howtoplay = font.render('how to play', True,red)
        screen.blit(howtoplay,(65,50))

        font = pygame.font.Font(file,30)
        text = 'use arrow keys to move'
        help1 = font.render(text,True,(0,0,0))
        screen.blit(help1,(75,200))

        monster = pygame.image.load('Images/monster1.png').convert_alpha()
        screen.blit(monster,(self.mx,self.my))
        self.updateMonster()

        text = 'press SPACE to shoot monsters'
        help2 = font.render(text,True,(0,0,0))
        screen.blit(help2,(50,400))

        color = (255,255,224)
        pygame.draw.ellipse(screen,color,(160,500,100,50))
        pygame.draw.ellipse(screen,(0,0,0),(160,500,100,50),2)

        font = pygame.font.Font(file,35)
        menu = font.render('menu',True,(0,0,0))
        screen.blit(menu,(180,500))


    # help screen monster moves left + right
    def updateMonster(self):
        if self.monRight:
            self.mx += 5
        else:
            self.mx -= 5
        if self.mx>=300:
            self.monRight = False
        if self.mx<=100:
            self.monRight = True


    def gameOverRedrawAll(self,screen):
        self.drawBackground(screen)

        file = pygame.font.match_font('al-seana')
        font = pygame.font.Font(file,70)
        red = (204,0,0)
        gameOver = font.render('game over!', True,red)
        screen.blit(gameOver,(75,100))
        finalScore = self.score
        score = font.render('score: ' + str(finalScore),True,(0,0,0))
        screen.blit(score,(25,200))

        color = (255,255,224)
        pygame.draw.ellipse(screen,color,(155,350,100,50))
        pygame.draw.ellipse(screen,(0,0,0),(155,350,100,50),2)
        font = pygame.font.Font(file,35)
        menu = font.render('menu',True,(0,0,0))
        screen.blit(menu,(175,350))


    def splashScreenRedrawAll(self,screen):
        self.drawBackground(screen)

        file = pygame.font.match_font('al-seana')
        font = pygame.font.Font(file,70)
        red = (204,0,0)
        doodleJump = font.render('doodle jump!',True,red)
        screen.blit(doodleJump,(100,100))

        plat = pygame.image.load('Images/platform.png').convert_alpha()
        x,y = 50,self.height-100
        screen.blit(plat,(x,y))

        doodle = pygame.image.load('Images/player.png').convert_alpha()
        w,h = doodle.get_size()
        screen.blit(doodle,(self.dx,self.dy))

        color = (255,255,224)
        pygame.draw.ellipse(screen,color,(250,250,100,50))
        pygame.draw.ellipse(screen,(0,0,0),(250,250,100,50),2)
        font = pygame.font.Font(file,35)
        play = font.render('play',True,(0,0,0))
        screen.blit(play,(275,250))

        pygame.draw.ellipse(screen,color,(250,350,100,50))
        pygame.draw.ellipse(screen,(0,0,0),(250,350,100,50),2)
        multi = font.render('multi',True,(0,0,0))
        screen.blit(multi,(270,350))


        pygame.draw.ellipse(screen,color,(250,450,100,50))
        pygame.draw.ellipse(screen,(0,0,0),(250,450,100,50),2)
        hlp = font.render('help',True,(0,0,0))
        screen.blit(hlp,(275,450))

        self.updateDoodle(x,y,w,h)


    # menu screen doodle jumps up + down   
    def updateDoodle(self,x,y,w,h):
        time = self.fakeTime
        reboundVelocity = -20
        if not self.dj: # gravity pulling player down
            self.dvy += self.day * time
            self.dy += self.dvy * time
            # check if on platform
            if self.doodleHitPlatform(x,y,w,h):
                self.dj = True
        if self.dj: # jumping off platform
            self.dvy = reboundVelocity
            self.dj = False


    def doodleHitPlatform(self,x,y,w,h):
        platform = Platform(x,y)
        platSize = platform.getSize()
        width,height = platSize[0],platSize[1]
        # colliding with platform
        if self.dy + h >= platform.y and self.dy< platform.y + height and self.dx+30>=platform.x-10 and self.dx+w-30<=platform.x+width+10:
            return True
        return False


    def gameScreenRedrawAll(self,screen):
        self.drawBackground(screen)

        file = pygame.font.match_font('al-seana')
        font = pygame.font.Font(file,30)
        score = font.render(str(self.score),True,(255,0,0))
        screen.blit(score,(10,0))

        if self.player == 'multi':
            score = font.render(str(self.score2),True,(0,0,255))
            screen.blit(score,(self.width-30,0))

        for platform in self.platforms:
            platform.draw(screen,self.offset)

        for monster in self.monsters:
            monster.draw(screen,self.offset)

        self.p1.draw(screen)
        if self.player == 'multi':
            self.p2.draw(screen)
            self.drawEnergies(screen)

    def drawEnergies(self,screen):
        pygame.draw.rect(screen,(0,0,0),(10,30,self.energy,10))
        pygame.draw.rect(screen,(0,0,0),(self.width-110,30,self.energy2,10))


    def drawBackground(self,screen):
        # grid background
        color = (255,255,224)
        rows,cols = 40,40
        for row in range(rows):
            for col in range(cols):
                x0,y0,x1,y1 = self.getCellBounds(row,col)
                pygame.draw.rect(screen,color,(x0,y0,x1,y1),1)


    def getCellBounds(self,row,col):
        rows,cols = 40,40
        x0 = self.width/cols * col
        y0 = self.height/rows * row
        x1 = self.width/cols * (col+1)
        y1 = self.height/rows * (row+1)
        return x0,y0,x1,y1


    def updateBoard(self):
        # move board up when player is more than 3/4 way up
        if self.player != 'multi' and self.p1.y <= self.height//4:
            self.offset -= abs((self.p1.vy))
            self.score += 50

            # remove platform if new loc is off board 
            for platform in self.platforms: 
                if platform.y-self.offset >= self.height:
                    self.platforms.remove(platform) 

            # remove monster if new loc is off board
            for monster in self.monsters:
                if monster.y - self.offset >= self.height:
                    self.monsters.remove(monster)

        if self.player == 'multi' and self.p1.y <= self.height//4 and self.p2.y<=self.height//4:
            self.offset -= abs((self.p1.vy))
            self.score += 50
            self.score2 += 50

            # remove platform if new loc is off board 
            for platform in self.platforms: 
                if platform.y-self.offset >= self.height:
                    self.platforms.remove(platform) 

            # remove monster if new loc is off board
            for monster in self.monsters:
                if monster.y - self.offset >= self.height:
                    self.monsters.remove(monster)

        # only 5 platforms exist at a time
        while len(self.platforms) < 5: 
            # new loc randomly generated based on last platform loc
            # so player can jump from platform to platform
            last = self.platforms[-1]
            x = random.randrange(0,self.width-100)
            y = random.randrange((last.y-150),(last.y-50))
            newPlatform = Platform(x,y)
            self.platforms.append(newPlatform)

        # only 2 monsters exist at a time
        while len(self.monsters) < 2:
            # new monster randomly generated above old monster
            last = self.monsters[-1]
            x = random.randrange(0,self.width-100)
            y = random.randrange((last.y-600),(last.y-400))
            # random monster type
            monType = random.randrange(1,7)
            # random monster movement
            move = random.randrange(0,2)
            newMonster = Monster(x,y,monType,move)
            self.monsters.append(newMonster)

    def updateEnergies(self):
        if self.energy <= 0 or self.energy2 <= 0:
            DoodleJump.mode = 'gameOver'

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()

        playing = True

        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False

            screen.fill((255, 255, 255))

            if self.mode == 'game':
                # update player
                self.p1.update(self.fakeTime,self.platforms,self.monsters,self.offset)
                # move player
                self.p1.move(self.fakeTime)
                # updating bullets
                self.bullets = self.p1.getBullets()

                for bullet in self.bullets:
                    bullet.update(self.fakeTime)
                    if bullet.y>=self.height:
                        self.bullets.remove(bullet)
                    # hitting another player
                    if self.player == 'multi' and bullet.isHittingPlayer(self.p2,self.offset):
                        self.score += 50
                        self.score2 -= 1 
                        self.energy2 -= 1
                # hitting a monster
                for bullet in self.bullets:
                    for monster in self.monsters:
                        if bullet.isHittingMonster(monster,self.offset):
                            self.score += 100 
                            self.monsters.remove(monster)


                if self.player == 'multi':
                    self.p2.move(self.fakeTime)
                    self.p2.update(self.fakeTime,self.platforms,self.monsters,self.offset)
                    self.bullets2 = self.p2.getBullets()

                    for bullet in self.bullets2:
                        bullet.update(self.fakeTime)
                        if bullet.y>=self.height:
                            self.bullets2.remove(bullet)
                        # hitting another player
                        if bullet.isHittingPlayer(self.p1,self.offset):
                            self.score2 += 50
                            self.score -= 1
                            self.energy -= 1

                    # hitting a monster
                    for bullet in self.bullets2:
                        for monster in self.monsters:
                            if bullet.isHittingMonster(monster,self.offset):
                                self.score2 += 100
                                self.monsters.remove(monster)

                # move monsters
                for monster in self.monsters:
                    if monster.mve == 1:
                        monster.move()

                self.updateBoard()
                if self.player == 'multi':
                    self.updateEnergies() # check if energy runs out

            self.redrawAll(screen)

    
            pygame.display.flip()
        pygame.quit()



################################################################################
################################ Player Class ##################################
################################################################################

class Player(Game):

    def __init__(self,x,y,player):
        super(Player,self).__init__()
        self.x = x
        self.y = y
        self.player = player
        self.jump = False
        self.vy = 0
        self.ay = 1
        self.shooting = False
        self.bullets = []


    def draw(self,screen):
        if self.shooting:
            img = 'Images/shoot' + str(self.player) + '.png'
        else:
            img = 'Images/player' + str(self.player) + '.png'
        self.image = pygame.image.load(img).convert_alpha()
        screen.blit(self.image,(self.x,self.y))
        for bullet in self.bullets:
            bullet.draw(screen)


    def update(self,time,platforms,monsters,offset):
        if self.shooting:
            img = 'Images/shoot' + str(self.player) + '.png'
        else:
            img = 'Images/player' + str(self.player) + '.png'
        self.image = pygame.image.load(img).convert_alpha()
        self.size = self.image.get_size()
        self.w,self.h = self.image.get_size()
        pygame.transform.scale(self.image,(int(self.w),int(self.h)))
        self.rect = pygame.Rect(self.x,self.y-offset,self.x+self.w,self.y+self.h-offset)

        # physics concepts act on player
        reboundVelocity = -15
        if not self.jump: # gravity pulling player down
            self.vy += self.ay * time
            self.y += self.vy * time
            # check if on platform
            if self.isOnPlatform(platforms,offset):
                self.jump = True
        if self.jump: # jumping off platform
            self.vy = reboundVelocity
            self.jump = False
        # check if hitting a monster
        if self.isOnMonster(monsters,offset):
            DoodleJump.mode = 'gameOver'
        if self.y>=self.height: DoodleJump.mode = 'gameOver'


    def isOnPlatform(self,platforms,ofst):
        for platform in platforms:
            if platform.y - ofst < 0: continue
            platSize = platform.getSize()
            width,height = platSize[0],platSize[1]
            # colliding with platform
            if self.y + self.h >= platform.y-ofst and self.y< platform.y-ofst + height and self.x+30>=platform.x-10 and self.x+self.w-30<=platform.x+width+10:
                return True
        return False


    def isOnMonster(self,monsters,offset):
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        for monster in monsters:
            if monster.y - offset < 0: continue
            monsterRect = monster.getRect(offset)
            # colliding with monster
            if self.rect.colliderect(monsterRect):
                return True
        return False


    def move(self,time):
        # can hold down left + right arrow keys 
        keys = pygame.key.get_pressed()
        if self.player == 1:
            if keys[pygame.K_RIGHT]: 
                self.x += 10
                self.y -= 5
            if keys[pygame.K_LEFT]:
                self.x -= 10
                self.y -= 5

        if self.player == 2:
            if keys[pygame.K_a]:
                self.x -= 10
                self.y -= 5
            if keys[pygame.K_d]:
                self.x += 10
                self.y -= 10

        # wraparound sides
        if self.x < 0:
            self.x = self.width
        elif self.x >= self.width:
            self.x = 0


    def keyPressed(self,keyCode,modifier):
        if self.player == 1:
            if keyCode == pygame.K_SPACE:
                self.shooting = True
                self.shoot()
            else:
                self.shooting = False

        if self.player == 2:
            if keyCode == pygame.K_s:
                self.shooting = True
                self.shoot()
            else:
                self.shooting = False


    def shoot(self):
        # shoot a bullet
        newBullet = Bullet(self.x+20,self.y + 20,False)
        self.bullets.append(newBullet)
        # if bullet falls off screen, remove it
        for bullet in self.bullets:
            if bullet.y >= self.height:
                self.bullets.remove(bullet)


    def getBullets(self):
        return self.bullets



################################################################################
############################### Platform Class #################################
################################################################################

class Platform(object):


    def __init__(self,x,y):
        self.x = x
        self.y = y


    def draw(self,screen,offset):
        img = pygame.image.load('Images/platform.png').convert_alpha()
        screen.blit(img,(self.x,self.y-offset))


    def getSize(self):
        image = pygame.image.load('Images/platform.png').convert_alpha()
        size = image.get_size()
        return size

################################################################################
############################### Monster Class ##################################
################################################################################

class Monster(object):
    

    def __init__(self,x,y,num,move):
        self.origX = x
        self.x = x
        self.y = y
        self.type = num
        self.mve = move
        self.moveRight = True
        self.width = 400
        self.imagesInit()


    # scale all images
    def imagesInit(self):
        self.monster1 = pygame.image.load('Images/monster1.png').convert_alpha()
        w,h = self.monster1.get_size()
        pygame.transform.scale(self.monster1,(int(w),int(h)))

        self.monster2 = pygame.image.load('Images/monster2.png').convert_alpha()
        w,h = self.monster2.get_size()
        pygame.transform.scale(self.monster2,(int(w),int(h)))

        self.monster3 = pygame.image.load('Images/monster3.png').convert_alpha()
        w,h = self.monster3.get_size()
        pygame.transform.scale(self.monster3,(int(w),int(h)))

        self.monster4 = pygame.image.load('Images/monster4.png').convert_alpha()
        w,h = self.monster4.get_size()
        pygame.transform.scale(self.monster4,(int(w),int(h)))

        self.monster5 = pygame.image.load('Images/monster5.png').convert_alpha()
        w,h = self.monster5.get_size()
        pygame.transform.scale(self.monster5,(int(w),int(h)))

        self.monster6 = pygame.image.load('Images/monster6.png').convert_alpha()
        w,h = self.monster5.get_size()
        pygame.transform.scale(self.monster5,(int(w),int(h)))
        self.monsters = [0,self.monster1,self.monster2,self.monster3,self.monster4,self.monster5,self.monster6]


    def draw(self,screen,offset):
        img = self.monsters[self.type]
        screen.blit(img,(self.x,self.y-offset))


    def getSize(self):
        img = self.monsters[self.type]
        size = img.get_size()
        return size


    def getRect(self,ofst):
        w,h = self.getSize()
        x0,y0 = self.x,self.y-ofst
        return pygame.Rect(x0,y0,w,h)


    def move(self):
        # random speed
        speed = random.randrange(1,6)
        # moving sideways back + forth
        if self.x >= self.origX + 100:
            self.moveRight = False
        elif self.x <= self.origX:
            self.moveRight = True
        if self.moveRight:
            self.x += speed
        else:
            self.x -= speed


################################################################################
############################### Bullet Class ###################################
################################################################################

class Bullet(object):


    def __init__(self,x,y,fall):
        self.x = x
        self.y = y
        self.vy = 0
        self.ay = 0.1
        self.shootVel = -10
        self.fall = fall
        self.imageInit()

    # scale image
    def imageInit(self):
        self.bullet = pygame.image.load('Images/bullet.png').convert_alpha()
        w,h = self.bullet.get_size()
        pygame.transform.scale(self.bullet,(int(w),int(h)))
        self.rect = pygame.Rect(self.x,self.y,w,h)


    def draw(self,screen):
        screen.blit(self.bullet,(self.x,self.y))


    # physics implementation of bullets
    # gravity pulls bullets down
    def update(self,time):
        if self.fall:
            self.vy += self.ay * time
            self.y += self.vy * time
        if not self.fall:
            self.vy = self.shootVel
            self.fall = True


    def isHittingMonster(self,monster,ofst):
        w,h = monster.getSize()
        # colliding with monster
        if monster.x<=self.x<=monster.x+w and monster.y-ofst<=self.y<=monster.y+h-ofst:
            return True
        return False


    def isHittingPlayer(self,player,ofst):
        # colliding with other player
        if player.x<=self.x<=player.x+player.w and player.y-ofst<=self.y<=player.y+player.h-ofst:
            return True
        return False



DoodleJump = Game()
DoodleJump.run()
