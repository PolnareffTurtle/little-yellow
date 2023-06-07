import pygame
from sys import exit
pygame.init()
scale = 0.5
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
        self.bordermode = 'bounded'
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
            self.speed = 3
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
        if self.bordermode == 'bounded':
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > 720:
                self.rect.right = 720
            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > 720:
                self.rect.bottom = 720
        elif self.bordermode == 'unbounded':
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
    def __init__(self,type,speed,direction=None,bordermode='bounded'):
        super().__init__()
        self.type = type
        if self.type == 'spikewall':
            self.direction = direction
            self.image = pygame.image.load('graphics/spikewall.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,direction,1)
            self.rect = self.image.get_rect(midbottom=(360,0))
            self.mask = pygame.mask.from_surface(self.image)
            if self.direction == 90:
                self.rect.midright = (0,360)
            elif self.direction == 180:
                self.rect.midtop = (360,720)
            elif self.direction == -90:
                self.rect.midleft = (720,360)
        self.speed = speed
        self.bordermode = bordermode

    def movement(self):
        if self.direction == 0:
            self.rect.y += self.speed
        elif self.direction == 180:
            self.rect.y -= self.speed
        elif self.direction == 90:
            self.rect.x += self.speed
        elif self.direction == -90:
            self.rect.x -= self.speed

    #def check_border(self):
     #   if self.bordermode == 'bounded':
      #      if self.rect.right < 0:
       #         self.rect.left = 0
        #    elif self.rect.right > 720:
         #       self.rect.right = 720
          #  if self.rect.top < 0:
           #     self.rect.top = 0
            #elif self.rect.bottom > 720:
             #   self.rect.bottom = 720
    def check_border(self):
        if self.bordermode == 'bounded':
            if self.rect.right < 0 or self.rect.left > 720 or self.rect.top > 720 or self.rect.bottom < 0:
                self.kill()
        elif self.bordermode == 'unbounded':
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

class Level():
    def __init__(self,index):
        self.index = index
        self.complete = False
        self.start_time=0

    def level_run(self):
        if self.index == 1:
            self.obstacle_check = Obstacle('spikewall', 5, 0, 'bounded')
            obstacles.add(self.obstacle_check)

        elif self.index == 2:
            self.obstacle_check = Obstacle('spikewall', 1, 0, 'unbounded')
            obstacles.add(self.obstacle_check)
            obstacles.add(Obstacle('spikewall', 2, 90, 'unbounded'))
            obstacles.add(Obstacle('spikewall', 3, -90, 'unbounded'))

        elif self.index == 3:
            obstacles.add(Obstacle('spikewall', 1, -90, 'unbounded'))
            obstacles.add(Obstacle('spikewall',10,0,'unbounded'))
            self.start_time=pygame.time.get_ticks()

        if self.complete:
            #print('complete')
            self.index+=1
            self.complete = False
        #print(self.index)

    def complete_check(self):
        if self.index == 1:
            self.complete = self.obstacle_check.rect.bottom > 720
        elif self.index == 2:
            self.complete = self.obstacle_check.rect.bottom > 720
        if self.complete:
            #print("hi")

            self.index += 1
            self.complete = False
            return True

    def update(self):
        self.complete_check()
        if self.index == 3:
            if pygame.time.get_ticks()-self.start_time == 4000:
                obstacles.add(Obstacle('spikewall',20,180,'bounded'))


def checkcollisions():
    if pygame.sprite.spritecollide(player,obstacles,False,pygame.sprite.collide_mask):
        player.shadows.clear()
        obstacles.empty()
        player.rect.center = (360,360)
        return False
    return True


screen = pygame.display.set_mode((720,720))
pygame.display.set_caption('Little Yellow')
clock = pygame.time.Clock()
game_active = False

#-------------------------GROUPS--------------------------------------
#player_group = pygame.sprite.GroupSingle()
#player = Player()
#player_group.add(player)
#obstacles = pygame.sprite.Group()
#obstacles.add(Obstacle('spikewall',1,0,'unbounded'))
#obstacles.add(Obstacle('spikewall',2,90,'unbounded'))
#obstacles.add(Obstacle('spikewall',3,-90,'unbounded'))
#obstacles.add(Obstacle('spikewall',4,180,'unbounded'))
levels = Level(1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active:
            #print(levels.index)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                player_group = pygame.sprite.GroupSingle()
                player = Player()
                player_group.add(player)
                obstacles = pygame.sprite.Group()
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
        title_text = Text('Little Yellow',100,'yellow',360,300,False)
        title_text.text_blit()
        level_text = Text(f'Level {levels.index}',50,'white',360,400,False)
        level_text.text_blit()

    clock.tick(60)
    pygame.display.update()