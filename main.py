import pygame
from sys import exit
import math
from random import randint

pygame.init()
scale = 0.5

#--------------------EVENTS----------------------------------------
NEXT = pygame.USEREVENT + 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/playericon.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,0.05*scale)
        self.rect = self.image.get_rect(center = (360,360))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 10*scale
        self.shadows=[]
        self.spacedown=False
        self.border_mode = 'bounded'
    def player_input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x-=self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y-= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y+=self.speed
        if keys[pygame.K_LSHIFT]:
            self.speed = 4
        else:
            self.speed = 10
        #for event in pygame.event.get():
        #    if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
        #        print('hi')
        #        self.shadows.append((self.rect.centerx,self.rect.centery))
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            #    self.rect.centerx = self.shadows[-1][0]
            #    self.rect.centery = self.shadows[-1][1]
            #    self.shadows.pop()



        #if keys[pygame.K_SPACE] and not self.spacedown:
        #    self.shadows.append((self.rect.centerx, self.rect.centery))
        #    self.spacedown=True
        ##else:
         #   self.spacedown=False
        #if keys[pygame.K_p]:
            #print(self.shadows)

    def putshadows(self):
        if len(self.shadows) > 3:
            self.shadows = self.shadows[-3:]
        i=1
        for shadow in self.shadows:
            if i==1:
                pygame.draw.circle(screen,'white',shadow,(self.rect.width*2/3))
            pygame.draw.circle(screen,'#4aa150',shadow,(self.rect.width)/(2+0.2*i))
            shadownum = Text(str(i),int(self.rect.width/2),'white',shadow[0],shadow[1],False)
            shadownum.text_blit()
            i+=1

    def check_border(self):
        if self.border_mode == 'bounded':
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > 720:
                self.rect.right = 720
            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > 720:
                self.rect.bottom = 720
        elif self.border_mode == 'unbounded':
            if self.rect.right < 0:
                self.rect.left = 720
            elif self.rect.left > 720:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = 720
            elif self.rect.top > 720:
                self.rect.bottom = 0


    def update(self):
        self.putshadows()
        self.player_input()
        self.check_border()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type,speed,angle=None,border_mode='bounded',rotate_speed=None,flip=False,centerpos=None):
        super().__init__()
        self.type = type
        self.angle = angle
        if self.type == 'spikewall':
            self.image = pygame.image.load('graphics/spikewall.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,self.angle,1)
            if centerpos:
                self.rect = self.image.get_rect(center=centerpos)
            else:
                self.rect = self.image.get_rect(midright=(0, 360))
            self.mask = pygame.mask.from_surface(self.image)
            if self.angle == 90:
                self.rect.midtop = (360,720)
            elif self.angle == 180:
                self.rect.midleft = (720,360)
            elif self.angle == -90:
                self.rect.midbottom = (360,0)
        elif self.type == 'spike_windmill':
            self.i=1
            self.flip=flip
            self.rotate_speed = rotate_speed
            self.image = pygame.image.load('graphics/spike_windmill.png').convert_alpha()
            self.image = pygame.transform.flip(self.image,self.flip,False)
            self.ref_image = self.image
            self.rect = self.image.get_rect()
            self.copy = self.rect
            self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.border_mode = border_mode

    def movement(self):
        #print(self.rect.centery - math.sin(math.radians(self.angle)) * self.speed)
        self.rect.center = (
            self.rect.centerx + math.cos(math.radians(self.angle)) * self.speed,
            self.rect.centery - math.sin(math.radians(self.angle)) * self.speed
        )

        if self.type == 'spike_windmill':
            if self.flip:
                self.image = pygame.transform.rotate(self.ref_image,self.i*-self.rotate_speed)
            else:
                self.image = pygame.transform.rotate(self.ref_image,self.i*self.rotate_speed)
            self.i+=1
            self.mask = pygame.mask.from_surface(self.image)


    def check_border(self):
        if self.border_mode == 'bounded':
            if self.rect.right < 0 or self.rect.left > 720 or self.rect.top > 720 or self.rect.bottom < 0:
                self.kill()
        elif self.border_mode == 'unbounded':
            if self.rect.right < 0:
                self.rect.left = 720
            elif self.rect.left > 720:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = 720
            elif self.rect.top > 720:
                self.rect.bottom = 0
    def update(self):
        self.check_border()
        self.movement()

class Text():
    def __init__(self,text,size,color,xpos,ypos,hover,key=None):
        self.key = key
        self.text = text
        self.color = color
        self.hover = hover
        self.center = (xpos,ypos)
        self.font = pygame.font.Font(None,size)
        self.font2 = pygame.font.Font(None,int(size*1.5))
        self.image = self.font.render(text,True,color)
        self.rect = self.image.get_rect(center=self.center)

    def text_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.image = self.font2.render(self.text,True,self.color)
            self.rect = self.image.get_rect(center=self.center)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.image = self.font.render(self.text,True,self.color)
            self.rect = self.image.get_rect(center=self.center)

    def clicked(self,key=None):
        mousedown = pygame.mouse.get_pressed()[0]
        keydown = pygame.key.get_pressed()[key]
        if self.rect.collidepoint(pygame.mouse.get_pos()) and mousedown or keydown:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            return True

    def text_blit(self):
        if self.hover:
            self.text_hover()
        screen.blit(self.image,self.rect)

#class Button():
#    def __init__(self,type,):


class Level():
    def __init__(self,index):
        self.index = index
        self.complete = False
        self.start_time=0

    def level_run(self):
        if self.index == 1:
            self.obstacle_check = Obstacle('spikewall', 5, -90, 'bounded')
            obstacles.add(self.obstacle_check)

        elif self.index == 2:
            self.obstacle_check = Obstacle('spikewall', 1, -90, 'unbounded')
            obstacles.add(self.obstacle_check)
            obstacles.add(Obstacle('spikewall', 2, 0, 'unbounded',))
            obstacles.add(Obstacle('spikewall', 3, 180, 'unbounded'))

        elif self.index == 3:
            self.obstacle_check = Obstacle('spikewall', 1, 180, 'unbounded')
            obstacles.add(self.obstacle_check)
            obstacles.add(Obstacle('spikewall',10,-90,'unbounded'))
            #self.start_time=pygame.time.get_ticks()

        elif self.index == 4:
            player.rect.center = (100,100)
            self.obstacle_check = Obstacle('spikewall',2,0,'unbounded')
            #obstacles.add(self.obstacle_check)
            obstacles.add(Obstacle('spike_windmill',0,0,'bounded',1))
            obstacles.add(self.obstacle_check)

        elif self.index == 5:
            player.rect.center = (360,360)
            #self.obstacle_check = Obstacle('spikewall',4,-45,'unbounded')
            #self.obstacle_check.rect.center = (0,720)
            self.obstacle_check = Obstacle('spikewall',1,0,'unbounded')
            obstacles.add(self.obstacle_check)
            obstacles.add(Obstacle('spikewall',10,45,'unbounded',centerpos=(0,720)))
            obstacles.add(Obstacle('spikewall',4,-45,'unbounded',centerpos=(0,0)))

        elif self.index == 6:
            player.rect.center = (300, 360)
            self.obstacle_check = Obstacle('spikewall',2,-90,'unbounded')
            obstacles.add(self.obstacle_check)
            obstacles.add(Obstacle('spikewall',10,180,'unbounded'))
            obstacles.add(Obstacle('spikewall',3,90,'unbounded'))



        #print(self.index)

    def complete_check(self):

        if self.index == 1:
            self.complete = self.obstacle_check.rect.bottom > 720
        elif self.index == 2:
            self.complete = self.obstacle_check.rect.bottom > 720
        elif self.index == 3:
            self.complete = self.obstacle_check.rect.left < 0
        elif self.index == 4:
            self.complete = self.obstacle_check.rect.right > 720
        elif self.index == 5:
            self.complete = self.obstacle_check.rect.right > 720
            #self.complete = self.obstacle_check.rect.right>720
        elif self.index == 6:
            self.complete = self.obstacle_check.rect.bottom > 720
        if self.complete:
            #print("hi")
            if self.index == 6:
                self.index = 0
            else:
                self.index += 1
            self.complete = False
            return True

    def update(self):
        self.complete_check()
        #if self.index == 3:
            #if pygame.time.get_ticks()-self.start_time == 4000:
                #obstacles.add(Obstacle('spikewall',20,180,'bounded'))

class Music():
    def __init__(self):
        self.mlist = ['sounds/shostakovich.wav','sounds/brahms.wav',
                      'sounds/lacrimosa.wav','sounds/requiem.wav','sounds/fortuna.wav']
        self.index = randint(0,4)
        pygame.mixer.music.load(self.mlist[self.index])
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(NEXT)
        pygame.mixer.music.set_volume(0.5)
    def mnext(self):
        self.index=(self.index+1)%len(self.mlist)
        pygame.mixer.music.load(self.mlist[self.index])
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(NEXT)
        pygame.mixer.music.set_volume(0.5)


def checkcollisions():
    if pygame.sprite.spritecollide(player,obstacles,False,pygame.sprite.collide_mask):
        player.shadows.clear()
        obstacles.empty()
        player.rect.center = (360,360)
        return False
    return True

#---------------------INITIALIZE------------------------------------
screen = pygame.display.set_mode((720,720))
pygame.display.set_caption('Little Yellow')
clock = pygame.time.Clock()
game_active = False
musics = Music()

#-------------------------GROUPS--------------------------------------
#player_group = pygame.sprite.GroupSingle()
#player = Player()
#player_group.add(player)
#obstacles = pygame.sprite.Group()
#obstacles.add(Obstacle('spikewall',1,0,'unbounded'))
#obstacles.add(Obstacle('spikewall',2,90,'unbounded'))
#obstacles.add(Obstacle('spikewall',3,-90,'unbounded'))
#obstacles.add(Obstacle('spikewall',4,180,'unbounded'))
levels = Level(6)





while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == NEXT:
            musics.mnext()

        if not game_active:
            #print(levels.index)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                levels.level_run()
                #obstacles.add(Obstacle('spikewall', 4, 180, 'unbounded'))
        else:
            if event.type == pygame.KEYDOWN:
                #create shadow
                if event.key == pygame.K_d:
                    player.shadows.append((player.rect.centerx,player.rect.centery))
                #flash to shadow
                if event.key == pygame.K_f and player.shadows:
                    player.rect.centerx = player.shadows[0][0]
                    player.rect.centery = player.shadows[0][1]
                    player.shadows.pop(0)

    if game_active:
        #background
        screen.fill('#65db6d')

        #player
        player.update()
        player_group.draw(screen)
        obstacles.update()
        obstacles.draw(screen)

        if levels.complete_check():
            game_active = False
            #print('next level')
        if game_active:
            game_active = checkcollisions()


    else:
        screen.fill('#65db6d')
        player_group = pygame.sprite.GroupSingle()
        player = Player()
        player_group.add(player)
        obstacles = pygame.sprite.Group()
        if levels.index == 0:
            win_message = Text('YOU WIN!!!!!!!', 100, 'yellow', 360, 360, False)
            win_message.text_blit()
        else:
            screen.fill('#65db6d')
            title_text = Text('Little Yellow',100,'yellow',360,300,False)
            title_text.text_blit()
            level_text = Text(f'Level {levels.index}',50,'white',360,400,False)
            level_text.text_blit()

    clock.tick(60)
    pygame.display.update()