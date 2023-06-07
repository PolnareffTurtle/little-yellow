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
        if keys[pygame.K_p]:
            print(self.shadows)

    def putshadows(self):
        if len(self.shadows) > 3:
            self.shadows = self.shadows[-3:]
        i=1
        for shadow in self.shadows[::-1]:
            if i==1:
                pygame.draw.circle(screen,'white',shadow,(self.rect.width*2/3))
            pygame.draw.circle(screen,'#4aa150',shadow,(self.rect.width)/(2+0.2*i))
            shadownum = Text(str(i),int(self.rect.width/2),'white',shadow[0],shadow[1],False)
            shadownum.text_blit()
            i+=1

    def checkborder(self):
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
        self.checkborder()

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
        
screen = pygame.display.set_mode((720,720))
pygame.display.set_caption('Little Yellow')
clock = pygame.time.Clock()
game_active = False
greenbg = pygame.image.load('graphics/greenbg.jpeg').convert()
shadows=[]

#-------------------------GROUPS--------------------------------------
player = pygame.sprite.GroupSingle()
player.add(Player())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
        #        print('hi')
                player.sprites()[0].shadows.append((player.sprites()[0].rect.centerx,player.sprites()[0].rect.centery))
            if event.key == pygame.K_f and player.sprites()[0].shadows:
                player.sprites()[0].rect.centerx = player.sprites()[0].shadows[-1][0]
                player.sprites()[0].rect.centery = player.sprites()[0].shadows[-1][1]
                player.sprites()[0].shadows.pop()
    #background
    screen.fill('#65db6d')

    #player
    player.update()
    player.draw(screen)


    clock.tick(60)

    pygame.display.update()