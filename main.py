import pygame
from sys import exit
import math
from random import randint
import asyncio

pygame.init()

#--------------------EVENTS----------------------------------------
NEXT = pygame.USEREVENT + 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 0.5
        self.image = pygame.image.load('graphics/playericon.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,0.05*self.scale)
        self.rect = self.image.get_rect(center = (360,360))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 10*self.scale
        self.shadows=[]
        self.spacedown=False
        self.border_mode = 'bounded'
    def player_input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x-=self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y-= self.speed
        if keys[pygame.K_s]:
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
                pygame.draw.circle(app.screen,'white',shadow,(self.rect.width*2/3))
            pygame.draw.circle(app.screen,'#4aa150',shadow,(self.rect.width)/(2+0.2*i))
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
    def __init__(self,text,size,color,xpos,ypos,hover=None,key=None):
        self.key = key
        self.text = text
        self.color = color
        self.hover = hover
        self.center = (xpos,ypos)
        self.font = pygame.font.Font('fonts/UbuntuTitling-Bold.ttf',size)
        self.font2 = pygame.font.Font('fonts/UbuntuTitling-Bold.ttf',int(size*1.5))
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
        app.screen.blit(self.image,self.rect)

class Button(pygame.sprite.Sprite):
    def __init__(self,centerpos,type='level',level=None,width=400,height=100,color='white'):
        super().__init__()
        #surf = pygame.Surface(width,height)
        self.type = type
        if self.type == 'play':
            self.image = pygame.image.load('graphics/assets/png/Buttons/Square-Medium/ArrowRight/Default.png').convert_alpha()
        elif self.type == 'home':
            self.image = pygame.image.load('graphics/assets/png/Buttons/Square-Medium/Home/Default.png').convert_alpha()
        elif self.type == 'level':
            self.level = level
            self.image = pygame.image.load('graphics/assets/png/Button/Square-Medium/Default/Background.png').convert_alpha()
        elif self.type == 'level_select':
            self.image = pygame.image.load('graphics/assets/png/Buttons/Square-Medium/Levels/Default.png').convert_alpha()
        elif self.type == 'mute':
            self.soundon = pygame.image.load('graphics/assets/png/Buttons/Square-Medium/SoundOn/Default.png').convert_alpha()
            self.soundoff = pygame.image.load('graphics/assets/png/Buttons/Square-Medium/SoundOff/Default.png').convert_alpha()
            if app.pausemusic:
                self.image = self.soundoff
            else:
                self.image = self.soundon
        self.rect = self.image.get_rect(center=centerpos)
        if self.type == 'level':
            self.text = Text(str(self.level),50,'white',self.rect.centerx,self.rect.centery)
        self.mousedown=False

    def clicked(self):

        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.mousedown=True
            #print('hi')

        else:
            if self.mousedown:
                #print('clicked')
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.mousedown=False
                return True

        #mousedown = pygame.mouse.get_pressed()[0]
        #keydown = pygame.key.get_pressed()[key]
        #if self.rect.collidepoint(pygame.mouse.get_pos()) and mousedown:
        #    print('clicked')
        #    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        #    return True

    def update(self):
        if self.type == 'level':
            self.text.text_blit()
        #if self.type == 'mute':
            #print(self.toggle)

        if self.clicked():
            #print('hji')
            if self.type == 'play':
                #print('play')
                app.game_state = GameState.GAME_RUNNING
            elif self.type == 'home':
                #print('go back')
                app.game_state = GameState.MAIN_MENU
            elif self.type == 'level':
                app.levels.index = self.level
                app.game_state = GameState.GAME_RUNNING
            elif self.type == 'level_select':
                app.game_state = GameState.LEVEL_SELECT
            elif self.type == 'mute':
                app.pausemusic = not app.pausemusic


        if self.type == 'mute':
            if app.pausemusic:
                self.image = self.soundoff
            else:
                self.image = self.soundon



class Level():
    def __init__(self,index):
        self.index = index
        self.complete = False
        self.start_time=0
        self.obstacle_check = None

    def level_run(self):
        if self.index == 1:
            self.obstacle_check = Obstacle('spikewall', 5, -90, 'bounded')
            app.obstacles.add(self.obstacle_check)

        elif self.index == 2:
            self.obstacle_check = Obstacle('spikewall', 1, -90, 'unbounded')
            app.obstacles.add(self.obstacle_check)
            app.obstacles.add(Obstacle('spikewall', 2, 0, 'unbounded',))
            app.obstacles.add(Obstacle('spikewall', 3, 180, 'unbounded'))

        elif self.index == 4:
            app.player.rect.center = (360, 360)
            self.obstacle_check = Obstacle('spikewall', 1, -90, 'unbounded')
            app.obstacles.add(self.obstacle_check)
            app.obstacles.add(Obstacle('spikewall', 1, 0, 'unbounded'))
            app.obstacles.add(Obstacle('spikewall', 1, 180, 'unbounded'))
            app.obstacles.add(Obstacle('spikewall', 1, 90, 'unbounded'))


        elif self.index == 3:
            self.obstacle_check = Obstacle('spikewall', 1, 180, 'unbounded')
            app.obstacles.add(self.obstacle_check)
            app.obstacles.add(Obstacle('spikewall',10,-90,'unbounded'))
            #self.start_time=pygame.time.get_ticks()



        elif self.index == 5:
            app.player.rect.center = (360,360)
            #self.obstacle_check = Obstacle('spikewall',4,-45,'unbounded')
            #self.obstacle_check.rect.center = (0,720)
            self.obstacle_check = Obstacle('spikewall',1,0,'unbounded')
            app.obstacles.add(self.obstacle_check)
            app.obstacles.add(Obstacle('spikewall',10,45,'unbounded',centerpos=(0,720)))
            app.obstacles.add(Obstacle('spikewall',4,-45,'unbounded',centerpos=(0,0)))

        elif self.index == 6:
            app.player.rect.center = (300, 360)
            self.obstacle_check = Obstacle('spikewall',2,-90,'unbounded')
            app.obstacles.add(self.obstacle_check)
            app.obstacles.add(Obstacle('spikewall',10,180,'unbounded'))
            app.obstacles.add(Obstacle('spikewall',3,90,'unbounded'))





        #print(self.index)

    def complete_check(self):

        if self.index == 1:
            self.complete = self.obstacle_check.rect.bottom > 720
        elif self.index == 2:
            self.complete = self.obstacle_check.rect.bottom > 720
        elif self.index == 3:
            self.complete = self.obstacle_check.rect.left < 0
        elif self.index == 4:
            self.complete = self.obstacle_check.rect.bottom > 720
        elif self.index == 5:
            self.complete = self.obstacle_check.rect.right > 720
        elif self.index == 6:
            self.complete = self.obstacle_check.rect.bottom > 720
        if self.complete:
            app.obstacles.empty()
            app.player.shadows.clear()
            if self.index == 7:
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
        self.pause = False
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
    def update(self):
        if app.pausemusic:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

class GameState():
    MAIN_MENU = 1
    LEVEL_SELECT = 2
    GAME_RUNNING = 3


class App():
    def __init__(self):
        #---------------------INITIALIZE------------------------------------
        self.screen = pygame.display.set_mode((720,720))
        pygame.display.set_caption('Little Yellow')
        self.clock = pygame.time.Clock()
        self.game_active = False
        self.musics = Music()
        self.pausemusic = False
        self.game_state = GameState.MAIN_MENU
        self.running = True

        #-------------------------GROUPS--------------------------------------
        self.player_group = pygame.sprite.GroupSingle()
        self.player = Player()
        self.player_group.add(self.player)
        self.obstacles = pygame.sprite.Group()
        self.levels = Level(1)

    def checkcollisions(self):
        if pygame.sprite.spritecollide(self.player, self.obstacles, False, pygame.sprite.collide_mask):
            self.player.shadows.clear()
            self.obstacles.empty()
            self.player.rect.center = (360, 360)
            return False
        return True

    def quit_game(self):
        self.running = False
        pygame.quit()
        exit()
        #additional things that happen when quit game can be put here

    async def main_menu(self):
        #print('homescreen')
        self.running = True
        self.buttons = pygame.sprite.Group()
        self.buttons.add(Button((300,450),type='play'))
        self.buttons.add(Button((420,450),type='level_select'))
        self.buttons.add(Button((600,100),type='mute'))
        while self.game_state == GameState.MAIN_MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    self.quit_game()
                if event.type == NEXT:
                    self.musics.mnext()
            self.screen.fill('#65db6d')
            self.title_text = Text('Little Yellow', 100, 'white', 360, 300, False)
            self.title_text.text_blit()
            self.buttons.draw(self.screen)
            self.buttons.update()
            self.musics.update()
            self.clock.tick(60)
            pygame.display.update()

            await asyncio.sleep(0)

    async def level_select(self):
        #print('homescreen')
        self.running=True
        self.buttons = pygame.sprite.Group()
        #adding the level buttons
        for y in range(5):
            for x in range(5):
                self.buttons.add(Button((160+x*100,100+y*100),type='level',level=5*y+x+1))
        self.buttons.add(Button((360,630),type='home'))
        self.buttons.add(Button((600,100),type='mute'))
        while self.game_state == GameState.LEVEL_SELECT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == NEXT:
                    self.musics.mnext()
            self.screen.fill('#65db6d')
            #title_text = Text('Little Yellow', 100, 'white', 360, 300, False)
            #title_text.text_blit()
            self.buttons.draw(self.screen)
            self.buttons.update()
            self.musics.update()
            self.clock.tick(60)
            pygame.display.update()

            await asyncio.sleep(0)

    async def game(self):
        self.buttons = pygame.sprite.Group()
        self.buttons.add(Button((360, 450), type='home'))
        self.buttons.add(Button((600, 100), type='mute'))

        while self.game_state == GameState.GAME_RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == NEXT:
                    self.musics.mnext()

                if not self.game_active:
                    #print(levels.index)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_active = True
                        self.levels.level_run()
                        #obstacles.add(Obstacle('spikewall', 4, 180, 'unbounded'))
                else:
                    if event.type == pygame.KEYDOWN:
                        #create shadow
                        if event.key == pygame.K_n:
                            self.player.shadows.append((self.player.rect.centerx,self.player.rect.centery))
                        #flash to shadow
                        if event.key == pygame.K_m and self.player.shadows:
                            self.player.rect.centerx = self.player.shadows[0][0]
                            self.player.rect.centery = self.player.shadows[0][1]
                            self.player.shadows.pop(0)

            if self.game_active:
                #background
                self.screen.fill('#65db6d')

                #player
                self.player.update()
                self.player_group.draw(self.screen)
                self.obstacles.update()
                self.obstacles.draw(self.screen)

                if self.levels.complete_check():
                    self.game_active = False
                    #print('next level')
                if self.game_active:
                    self.game_active = self.checkcollisions()


            else:

                self.screen.fill('#65db6d')
                self.buttons.draw(self.screen)
                self.buttons.update()
                #player_group = pygame.sprite.GroupSingle()
                #player = Player()
                #player_group.add(player)
                #obstacles = pygame.sprite.Group()
                if self.levels.index == 0:
                    self.win_message = Text('YOU WIN!!!!!!!', 100, 'white', 360, 360, False)
                    self.win_message.text_blit()
                else:
                    #screen.fill('#65db6d')
                    #title_text = Text('Little Yellow',100,'white',360,300,False)
                    #title_text.text_blit()
                    self.level_text = Text(f'Level {self.levels.index}',100,'white',360,300,False)
                    self.level_text.text_blit()
            self.musics.update()
            self.clock.tick(60)
            pygame.display.update()

            await asyncio.sleep(0)

    async def game_loop(self):
        while self.running:
            if self.game_state == GameState.MAIN_MENU:
                await self.main_menu()
            elif self.game_state == GameState.LEVEL_SELECT:
                await self.level_select()
            elif self.game_state == GameState.GAME_RUNNING:
                await self.game()

if __name__ == '__main__':
    app = App()
    asyncio.run(app.game_loop())