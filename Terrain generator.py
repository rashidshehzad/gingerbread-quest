import pygame, sys
from pygame.locals import QUIT
import random
from matrix import Vector

pygame.init()
dimensions=Vector([[1000, 700]])
screen = pygame.display.set_mode(dimensions.gettuple(0))
pygame.display.set_caption('This landmass does not exist.')

global scroll, bg_zoom, half_dimension, bg_height
bg_zoom=[1, 1]
half_dimension=[500, 350]
scroll=Vector([[0, 0]])
bg_height=100

class Column():
    def __init__(self, pos, height, colour):
        self.pos=pos
        self.height=height
        self.colour=colour
    def draw(self):
        centre=half_dimension
        x=int((self.pos[0]-centre[0]+scroll[0][0])*bg_zoom[0])+centre[0]
        nextx=int((self.pos[0]+1-centre[0]+scroll[0][0])*bg_zoom[0])+centre[0]
        y=int((self.pos[1]-centre[1]+scroll[0][1])*bg_zoom[1])+centre[1]
        height=bg_zoom[1]*self.height
        #print("x - ",x)
        #print("y - ",y)
        #print("height - ",height)
        pygame.draw.rect(screen, self.colour, pygame.Rect(x, y-height, nextx-x, height))

#Env name, gradient range, height range
environments=[["Forest", [-10, 20], [70, 100]]]
environment=0
global bounds
bounds=[0, 10000]
dampening=0.5
offset_range=[-50, 50]
def random_range(range):
    return random.randint(bounds[0], bounds[1])
def cubic_interpolation(y0, y1, y2, y3, x):
  a0 = -(y0/2)+(3*y1/2)-(3*y2/2)+(y3/2)
  a1 = y0-(5*y1/2)+(2*y2)-(y3/2)
  a2 = (y2 - y0)/2
  a3 = y1
  return(a0*x**3+a1*x**2+a2*x+a3)
def split_line(a, b, offset):
    mid=(1/2)*(a+b)
    length=(b-a).magnitude()
    offset=(bounds[1]-bounds[0])/length*offset
    return mid+offset
def cut_lines(lines, cuts, offset_range, dampening):
    for i in range(cuts):
        temp_lines=[]
        for j in range(len(lines)-1):
            offset=Vector([[0, random_range(offset_range)/100]])
            a=lines[j]
            b=lines[j+1]
            mid=split_line(a, b, offset)
            temp_lines.append(a)
            temp_lines.append(mid)
            #print(a, mid, b)
        temp_lines.append(b)
        lines=temp_lines
        #print("i  - ",i,"\nlines - ")
        #for j in range(len(lines)):
        #    print(lines[j])
        offset=[int(offset[0][0]*dampening), int(offset[0][1]*dampening)]
    return lines
gradient=random_range(environments[0][1])/(bounds[1]-bounds[0])
c=random_range(environments[0][2])/100
lines=[Vector([[bounds[0], c]]), Vector([[bounds[1], bounds[1]*gradient+c]])]
cuts=6
lines=cut_lines(lines, cuts, offset_range, dampening)
for i in range(len(lines)):
    print(lines[i])
def generate_cubic_terrain(lines):
    distance=(bounds[1]-bounds[0])/(2**cuts)
    lines.insert(0, 2*lines[0]-lines[1])
    lines.append(2*(lines[len(lines)-1])-lines[len(lines)-2])
    terrain=[]
    current_line=1
    for i in range(bounds[0], bounds[1]):
        if i>=lines[current_line+1][0][0]:
            current_line+=1
        y0=lines[current_line-1][0][1]
        y1=lines[current_line][0][1]
        y2=lines[current_line+1][0][1]
        y3=lines[current_line+2][0][1]
        interpolation=int(cubic_interpolation(y0, y1, y2, y3, (i-bounds[0])/distance-current_line+1))
        terrain.append(Column([i-bounds[0], 0], interpolation, (124,252,0)))
    return terrain
def draw_terrain(terrain):
    for i in range(len(terrain)):
        terrain[i].draw()
terrain=generate_cubic_terrain(lines)
draw_terrain(terrain)
pygame.display.update()

keys = [False, False, False, False, False, False]
#Scroll left, scroll right, scroll up, scroll down, zoom in
#
commands=[False, False, False, False, False, False]
while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        keys[0]=True
      if event.key == pygame.K_RIGHT:
        keys[1]=True
      if event.key == pygame.K_UP:
        keys[2]=True
      if event.key == pygame.K_DOWN:
        keys[3]=True
      if event.key == pygame.K_z:
        keys[4]=True
      if event.key == pygame.K_x:
        keys[5]=True
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT:
        keys[0]=False
      if event.key == pygame.K_RIGHT:
        keys[1]=False
      if event.key == pygame.K_UP:
        keys[2]=False
      if event.key == pygame.K_DOWN:
        keys[3]=False
      if event.key == pygame.K_z:
        keys[4]=False
      if event.key == pygame.K_x:
        keys[5]=False


  for i in range(len(keys)):
    if keys[i]:
      commands[i]=True
    else:
      commands[i]=False

  if commands[0]:
    scroll=Vector([[scroll[0][0]+2/bg_zoom[0], scroll[0][1]]])
  if commands[1]:
    scroll=Vector([[scroll[0][0]-2/bg_zoom[0], scroll[0][1]]])
  if commands[2]:
    #print("Up.")
    scroll=Vector([[scroll[0][0], scroll[0][1]+2/bg_zoom[1]]])
  if commands[3]:
    #print("Down.")
    scroll=Vector([[scroll[0][0], scroll[0][1]-2/bg_zoom[1]]])
  if commands[4]:
    bg_zoom=[bg_zoom[0]*1.1, bg_zoom[1]*1.1]
  if commands[5]:
    bg_zoom=[bg_zoom[0]/1.1, bg_zoom[1]/1.1]
    #pixelsize=[pixelsize[0]*1.1, pixelsize[1]*1.1]
  screen.fill((0, 0, 0))
  draw_terrain(terrain)
  pygame.display.update()
