from cgi import test
from datetime import datetime
import math
import random
import time
import pygame


def draw(paused, screen, all_sprites, targets, laser, player, counter, done):
    if done:
        screen.fill((0,0,0))
        font = pygame.font.Font('freesansbold.ttf', 32)

        # create a text surface object,
        # on which text is drawn on it.
        image = font.render("You lost with a score of: "+str(counter.score), True, (0,255,0), (0,0,255))
        # create a rectangular object for the
        # text surface object
        rect = image.get_rect()
        rect.center = ((SCREEN_WIDTH )/2, (SCREEN_HEIGHT - image.get_height())/2 )
        screen.blit(image, rect)
        pygame.display.flip()
        return True

    if paused:
        screen.blit(pygame.transform.scale(pygame.image.load('Pause.png'),PAUSE_SIZE),((SCREEN_WIDTH-PAUSE_SIZE[0])/2, (SCREEN_HEIGHT - PAUSE_SIZE[1])/2))
        pygame.display.flip()
        return False
    if targets.__len__() < 10 :
        nuke = Nuke(SCREEN_WIDTH, random.randint(PAUSE_SIZE[1]/4,SCREEN_HEIGHT * 3/4), random.random() / 3)
        plane = Plane(SCREEN_WIDTH, random.randint(PAUSE_SIZE[1]/4,SCREEN_HEIGHT * 3/4), random.random())
        target = random.choices([nuke,plane], weights=(5,1))
        targets.add(target)
        all_sprites.add(target)
    screen.fill((18, 15, 184))
    screen.blit(pygame.transform.scale(pygame.image.load('Play.png'), (PAUSE_SIZE[0] / 4, PAUSE_SIZE[1] / 4)), (0,0))
    laser.update(player, screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    for entity in all_sprites:
        if isinstance(entity, Nuke):
            if entity.rect.x - entity.rect.width/2 < 0:
                counter.lives-=1
                entity.kill()
                if counter.lives <=0:
                    return True
        elif isinstance(entity, Plane):
            if entity.rect.x - entity.rect.width/2 < 0:
                entity.kill()

        entity.update()
        screen.blit(entity.image, entity.rect)
    pygame.display.flip()
    return False


SCREEN_WIDTH = 800

SCREEN_HEIGHT = 600

LASER_OFFSET = 12

PAUSE_SIZE = (200,200)
PI = math.pi
class Laser(pygame.sprite.Sprite):
    def __init__(self, off, cool):
        super(Laser, self).__init__()
        self.width = 1
        self.off = off
        self.start = (0,0)
        self.end = (0,0)
        self.cool = cool
        self.last = datetime.now()
    def update(self, player, surf, width, height):
        color = (255,0,0)
        if (datetime.now() - self.last).total_seconds() < self.cool:
            color = (0,255,0)
        angle = math.atan2(pygame.mouse.get_pos()[1] - player.y, pygame.mouse.get_pos()[0] - player.x)

        laser_start = (player.x + (self.off * math.sin(PI/2 - angle)), player.y + (self.off * math.cos(PI/2 - angle)))

        # adjust to screen edge
        edge_pointx = laser_start[0] + (width * 2) * math.cos(angle)
        edge_pointy = laser_start[1] + (height * 2) * math.sin(angle)
    
        self.start = laser_start
        self.end = (edge_pointx, edge_pointy)

        # draw line
    
        pygame.draw.line(surf,color, laser_start, (edge_pointx, edge_pointy), self.width)
    def fire(self, player, surf, targets, an_time, all_sprites, counter, done):
        time = datetime.now()
        if (time - self.last).total_seconds() < self.cool:
            return
        i = 0
        while (datetime.now() - time).total_seconds() < an_time:
            if ((datetime.now() - time).total_seconds())>i * an_time/4:
                i+=1
                self.width+=5
            draw(False, surf, all_sprites, targets, self, player, counter, done)
            self.test_fire(targets, counter)
        self.width = 1
        self.last = time
    def test_fire(self, targets, counter):
        for t in targets:
            if self.is_in(t.rect.center[0], t.rect.center[1], t.rect.width, t.rect.height):
                if isinstance(t, Nuke):
                    counter.score+=10
                elif isinstance(t, Plane):
                    counter.score-=100
                t.kill()
    def is_in(self, x, y, width, height):
        slope = float(self.end[1] - self.start[1])/(self.end[0] - self.start[0])
        exact_x = self.end[0] - (self.end[1] - y)/slope
        if x - width/2 < exact_x + self.width and x - width/2 > exact_x - self.width:
            return True
        elif x + width/2 < exact_x + self.width and x + width/2 > exact_x - self.width:
            return True
        elif x < exact_x + self.width and x > exact_x - self.width:
            return True
        exact_y = self.end[1] - slope*(self.end[0] - x)
        if y - height/2 < exact_y + self.width and y - height/2 > exact_y - self.width:
            return True
        elif y + height/2 < exact_y + self.width and y + height/2 > exact_y - self.width:
            return True
        elif y < exact_y + self.width and y > exact_y - self.width:
            return True
        return False



def rot_center_fn( image, angle, x, y):
    
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        return rotated_image, new_rect

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.const_image = pygame.image.load('Player.png')
        self.rect = self.const_image.get_rect()
        self.image = self.const_image
        self.x = x
        self.y = y
        self.angle = 0
    def update(self):
        self.rot_to_mouse()
    def rot_center(self):
        (self.image,self.rect) = rot_center_fn(self.const_image, self.angle, self.x, self.y)
    
    def rot_to_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        self.rot_center()

class Nuke(pygame.sprite.Sprite):
    def __init__(self,x,y, speed):
        super(Nuke, self).__init__()
        self.image = pygame.image.load('Nuke.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed = speed
        self.x = x
        self.y = y
    def update(self):
        self.x -= self.speed
        self.rect.topleft = (round(self.x), self.y)
class Counter(pygame.sprite.Sprite):
    def __init__(self, lives):
        super(Counter, self).__init__()
        self.score=0
        self.lives=lives
        # create a font object.
        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        self.font = pygame.font.Font('freesansbold.ttf', 32)
 
        self.text = "Score: " + str(self.score) + " Lives: " + str(self.lives)

        # create a text surface object,
        # on which text is drawn on it.
        self.image = self.font.render(self.text, True, (0,255,0), (0,0,255))
        # create a rectangular object for the
        # text surface object
        self.rect = self.image.get_rect()

        self.rect.center = (self.rect.center[0] + PAUSE_SIZE[0]/4, self.rect.center[1])
    def update(self):
        self.text = "Score: " + str(self.score) + " Lives: " + str(self.lives)
        self.image = self.font.render(self.text, True, (0,255,0), (0,0,255))

class Plane(pygame.sprite.Sprite):
    def __init__(self,x,y, speed):
        super(Plane, self).__init__()
        self.image = pygame.image.load('Plane.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed = speed
        self.x = x
        self.y = y
    def update(self):
        self.x -= self.speed
        self.rect.topleft = (round(self.x), self.y)
    



