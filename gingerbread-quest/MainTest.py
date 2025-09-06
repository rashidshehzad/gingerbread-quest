import pygame, sys
from pygame.locals import QUIT
import time
import copy
from math import *

from matrix import *
from physics import *

global width
width=10

a=Vector([[3, -2]])
b=Vector([[1, 7]])
print("A's angle with b - ",a.angle(b))


def draw(self):
  self.pos.polygonate()
  points = []
  #print("self.pos - ", self.pos)
  for i in range(len(self.pos.vector)):
    points.append((self.pos.vector[i][0], self.pos.vector[i][1]))
    pygame.draw.line(screen, (34,139,34), points[i], (self.pivot[0][0], self.pivot[0][1]))
  #print("Len of points: ", len(points))
  if len(points)>2:
    pygame.draw.polygon(screen, self.colour, points)
  pygame.draw.circle(screen, (30,144,255), self.pivot.gettuple(0), 5)
  i=0
  for polygon in self.pos.polygons:
    i+=1
    #v1=polygon.getc(1)-polygon.getc(0)
    #v2=polygon.getc(2)-polygon.getc(0)
    #pygame.draw.circle(screen, (30,144,255), (proj(v1, v2)+polygon.getc(0)).gettuple(0), 5)
    #print(proj(v1, v2)+polygon.getc(0))
    try:
      polygon.draw(Vector([self.pos[0]]), (5+(i*50)%255, 71+(i*50)%255, 42+(i*50)%255))
    except:
      pass

def draw_char(self):
  self.find_frame()
  screen.blit(self.image, self.pos.gettuple(0))

physobj.draw=draw
character.draw=draw_char


def draw_square(pos):
  #print("square pos - ", pos)
  pygame.draw.rect(screen, (34, 139, 34), (pos[0][0]-width, pos[0][1]-width, width, width))

def draw_coloured_square(pos, colour):
  pygame.draw.rect(screen, colour, (pos[0][0]-width, pos[0][1]-width, width, width))

font = pygame.font.Font('freesansbold.ttf', 25)

def write(message, x, y, colour):
    #Creates the text message
    text = font.render(message, True, colour)
    #Displays the text message
    screen.blit(text, (x, y))
