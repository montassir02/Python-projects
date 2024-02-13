import pygame
import time
class Tile:
    def __init__(self, x, y, width, height):
        self.x=x
        self.y=y
        self.pos = (x, y)
        self.width=width-5
        self.heigth=height-5
        self.abs_x = (x * width)+5
        self.abs_y = (y * height)+5
        self.abs_pos = (self.abs_x, self.abs_y)
        self.color='white'
        self.rect = pygame.Rect(
			self.abs_x,
			self.abs_y,
			self.width,
			self.heigth
		)
        self.state=False

    def draw(self,display,x,o,state):
        if state=='':
            pygame.draw.rect(display, self.color, self.rect)
        if state=='x':
            display.blit(x,self.abs_pos)
        if state=='o':
            display.blit(o,self.abs_pos)

    def simdraw(self,display):
        pygame.draw.rect(display, self.color, self.rect)

    def det_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.abs_x<mouse_x<self.abs_x+self.width:
            if self.abs_y<mouse_y<self.abs_y+self.heigth:
                if pygame.mouse.get_pressed()[0]:
                    time.sleep(0.2)
                    return True






