#created on 9/03/2021


import pygame
from pygame.locals import *
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self.location = 0
        self.move_ticker = 0
        self.img = pygame.image.load('soccer.png')
        self.img = pygame.transform.scale(self.img, (30, 30))
        self.score = 0
        self.rect = pygame.rect.Rect((260, 360, 100, 20))
        self.ball_x = 290
        self.ball_y = 345
        self.ball_movex = 0.12
        self.ball_movey = 0.12
        self.begin = False
        self.bricks = {}
        self.invisible_bricks =[]
        self._first = True

    def on_init(self):
        pygame.init()
        pygame.font.init()
        self.scorefont = pygame.font.SysFont('Comic Sans MS', 30)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.fill((255,255,255))
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_w:
			self.begin = True
		if event.key == pygame.K_d:
			if self.rect.right < 640:
				self.rect.move_ip(20, 0)
		if event.key == pygame.K_a:
			if self.rect.left > 0:
				self.rect.move_ip(-20, 0)
    def on_loop(self):
			self._display_surf.fill((255,255,255))
			for i in range(12):
				for j in range(8): 
					brick_name = str(i)+str(j)
					if brick_name in self.invisible_bricks:
						break
					self.bricks[brick_name] = pygame.rect.Rect((55*i, 25*j, 50, 20))
					if i%2 ==0:
						pygame.draw.rect(self._display_surf, (0, 0, 255), self.bricks[brick_name])
					else:
						pygame.draw.rect(self._display_surf, (0, 255, 255), self.bricks[brick_name])
	#print len(self.bricks) 
	if self.move_ticker > 0:
		self.move_ticker -= 1
	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[K_d]:
		if self.move_ticker == 0:
			self.move_ticker = 150
			if self.rect.right < 640:
				self.rect.move_ip(20, 0)
	if keys_pressed[K_a]:
		if self.move_ticker == 0:
			self.move_ticker = 150
			if self.rect.left > 0:
				self.rect.move_ip(-20, 0)
	self.paddle = pygame.draw.rect(self._display_surf, (0, 255, 0), self.rect)
	self.collision_handler()
	self.ball = self._display_surf.blit(self.img, (self.ball_x, self.ball_y))
	textsurface = self.scorefont.render(str(self.score)+' points', False, (0, 0, 0))
	self._display_surf.blit(textsurface,(320,380))
    
    def checkhit(self, brick):
		
		if self.ball_y > brick.bottom:
			return False
		if self.ball_x+30 < brick.left:
			return False
		if self.ball_x > brick.right:
			return False
		if self.ball_y+30 < brick.top:
			return False
		if self.ball_y <= brick.bottom and self.bally > brick.bottom:
			self.ball_movey = abs(self.ball_movey)
			return True
		if self.ball_x+30 >= brick.left and self.ballx+30 > brick.left:
			self.ball_movex = -abs(self.ball_movex)
			return True
		if self.ball_x <= brick.right and self.ballx > brick.right:
			self.ball_movex = abs(self.ball_movex)
			return True
		if self.ball_y+30 >= brick.top and self.bally+30 < brick.top:
			self.ball_movey = -abs(self.ball_movey)
			return True
		return False
			
    def collision_handler(self):
if self._first:    
	self.ball_movex = 0
if self.begin:
	self.ballx = self.ball_x
	self.bally = self.ball_y
	self.ball_x += self.ball_movex
	self.ball_y += self.ball_movey
else:
	self.ball_x, self.ball_y = self.rect.center
	self.ball_y -= 30
	self.ball_x -= 10
	return
for i in range(12):
	for j in range(8):  
		brick_name = str(i)+str(j)
		if brick_name in self.invisible_bricks:
			break
		if self.checkhit(self.bricks[brick_name]):
			del self.bricks[brick_name]
			self.invisible_bricks.append(brick_name)
			self.score += 1
			self._first = False
			break

if self.ball_x < 0:
	self.ball_movex = abs(self.ball_movex)
	self._first = False
if self.ball_x+30 > 640:
	self.ball_movex = -abs(self.ball_movex)
	self._first = False
if self.ball_y < 0:
	self.ball_movey = abs(self.ball_movey)
	self._first = False
if self.ball_y+30 > 360:
	if self.rect.left-5 < self.ball_x + 15 and self.rect.right+5 > self.ball_x + 15:
		if self.ball_movex < 0:
			self.ball_movex = -0.12
		else:
			self.ball_movex = 0.12
		self.ball_movey = -abs(self.ball_movey)
		F = (self.ball_x+15 - self.rect.left) / self.rect.width
		if self.ball_movex < 0:
			F = 1.0 - F
		F += 0.5
		self.ball_movex = F*self.ball_movex
	else:
		self.ball_x, self.ball_y = self.rect.center
		self.ball_y  = 345
		self.ball_x -= 10
		del self.invisible_bricks[:]
		self.bricks.clear()
		self.score = 0
		self._first = True
		self.begin = False
    def on_render(self):
        pygame.display.update()
        
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
