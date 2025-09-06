#Modules imported on lines 12-21. This also imports the majority of classes from the physobj and matrix modules.
#Classes: Column on 112, bg_house on 126
#From lines 156 to 237, the background is randomly generated using cubic interpolation.
#From 252 to 297 physobj class methods are overwritten to work with pygame.







import sys

import pygame, time, random
from pygame.locals import QUIT
from math import *
#matrix and polish modules were both created by me
from matrix import Vector
from polish import *
#Pygame module
from physobj import physobj, bigwall, item

#Queue item currently ignored. I am keeping it in the code in case I use it later.
class queue():
    def __init__(self, length):
        self.front=0
        self.end=0
        self.queue=[]
        for i in range(length):
            self.queue.append("NULL")
    def add(self, item):
        self.end+=1
        try:
            self.queue[self.end]=item
        except:
            self.queue.append(item)
    def remove(self):
        if self.end>0 and self.end>self.front:
            self.queue[self.end]="NULL"
        self.end-=1
    def current(self):
        return self.queue[self.end]
    def return_all(self):
        return self.queue

#level1=[gingerbread, create_big_wall(-25, 0, -10, 15, 8, 1, 0), create_big_wall(-25, 15, 10, 22, 8, 1, 0), item(Vector([[100, 300]]), 0), create_big_wall(15, 15, 40, 22, 8, 1, 0), create_big_wall(40, 15, 50, 22, 8, 1, 1), create_big_wall(50, 5, 60, 22, 8, 1, 0), create_big_wall(60, 5, 70, 22, 8, 1, -1), create_big_wall(70, 15, 90, 22, 8, 1, 0), create_candy_cane(72, 15, 10), item(Vector([[32*wall_width, 14*wall_height]]), 1), item(Vector([[72*wall_width, 5*wall_height]]), 3)]
#level1=create_house(level1, 20, 15, 1)
#level1=create_house(level1, 50, 5, 2)
#level2=[gingerbread, create_big_wall(-30, 0, -18, 37, 8, 1, 0), create_big_wall(-18, 19, -10, 37, 8, 1, -1), create_big_wall(-10, 27, 120, 37, 8, 1, 0), create_big_wall(-10, 15, 10, 22, 8, 1, 0), create_big_wall(10, 15, 30, 22, 8, 2, 0), create_big_wall(40, 15, 50, 22, 8, 2, 0), create_big_wall(60, 15, 70, 22, 8, 1, 0), create_big_wall(72, 13, 73, 22, 8, 1, 0), create_big_wall(75, 11, 76, 22, 8, 1, 0)]
#create_big_wall(x, y, x2, y2, mass, type, slope)

#Pygame initialised
pygame.init()
#Global variables for screen size, player lives (will make it an attribute at some point), current level and game state.
global dimensions, lives, level, game_state
level=1
#Lives = [Life, hp]
lives=[3, 1]

#A list containing images for the lives' UI
live_images=[]
for i in range(1,5):
    live_images.append(pygame.image.load("images/Life"+str(i)+".png"))
dimensions=Vector([[1000, 700]])

screen = pygame.display.set_mode(dimensions.gettuple(0))
pygame.display.set_caption('Hello World!')
fps=50

#Substeps is used to decide how many times collision adjustments will be made each frame.
substeps=2

#Global variables that give the width and height of the walls, the force of gravity, and current camera scroll.
global wall_width, wall_height, gravity, scroll, half_dimension
jump_time=10
scroll=Vector([[0, 0]])
gravity=Vector([[0, 2]])
wall_width, wall_height = 28, 28

global bg_zoom, half_dimension, bg_height, startx, starty, level_won, l_acceleration, r_acceleration
l_acceleration=0
r_acceleration=0
level_won=False
bg_zoom=[0.5, 0.5]
half_dimension=[500, 350]
scroll=Vector([[0, 0]])
bg_height=100

#Subroutine to solve a quadratic equation
def solve_quadratic(a, b, c):
  if abs(a)<=0:
    if abs(b)<=0:
      if abs(c)<=0:
        return [0] #0 always equal to 0, so infinitely many solutions. Pick smallest one
      else:
        return []
    else:
      return [-c/b]
  else:
    radicand=b*b - (4*a*c)
    if abs(radicand)<=0:
      return [-b/(2*a)]
    elif radicand>0:
      determinant=sqrt(radicand)
      return [(-b-determinant)/(2*a), (-b+determinant)/(2*a)]
    else:
      return []

#Column class is used as part of the background terrain generation.
#Displays a column of a certain height, starting from a certain x, y pos.
#Can also be zoomed in.
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
        pygame.draw.rect(screen, self.colour, pygame.Rect(x, y-height+dimensions[0][1], nextx-x, height))

#Bg_house is a class which displays a single house as part of the background.
class bg_house():
    house_sizes=[[16, 13], [16, 13], [19, 13], [30, 24]]
    house_sizes[0]=[64, 52]
    def __init__(self, pos, type):
        self.pos=pos
        self.type=type
        self.normal_resolution=bg_house.house_sizes[self.type-1]
        self.image=pygame.image.load("images/House4"+str(type)+".png")
    def draw(self):
        centre=half_dimension
        #x=int((self.pos[0]-centre[0]+scroll[0][0])*bg_zoom[0])+centre[0]
        #y=int((self.pos[1]-centre[1]+scroll[0][1])*bg_zoom[1])+centre[1]
        resolution=(self.normal_resolution[0]*bg_zoom[0], self.normal_resolution[1]*bg_zoom[1])
        x=int((self.pos[0]-resolution[0]-centre[0]+scroll[0][0])*bg_zoom[0])+centre[0]
        y=int((self.pos[1]-self.normal_resolution[1]-centre[1]+scroll[0][1])*bg_zoom[1])+centre[1]
        screen.blit(pygame.transform.scale(self.image, resolution), (x, y+dimensions[0][1]+resolution[1]))

#A list containing all the background_houses to be displayed.
background_houses=[]
#Env name, gradient range, height range
environments=[["Forest", [0, 20], [70, 100]]]
environment=0
global bounds
bounds=[0, 10000]
dampening=0.5
offset_range=[-10, 10]
#Subroutine for giving a random value between 2 bounds
def random_range(range):
    return random.randint(bounds[0], bounds[1])
#Subroutine uses for gibing the hight of a column in the background, according to the formula of cubic interpolation.
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
def generate_cubic_terrain(lines):
    distance=(bounds[1]-bounds[0])/(2**cuts)
    lines.insert(0, 2*lines[0]-lines[1])
    lines.append(2*(lines[len(lines)-1])-lines[len(lines)-2])
    terrain=[]
    current_line=0
    for i in range(bounds[0], bounds[1]):
        if i>=lines[current_line+1][0][0]:
            current_line+=1
            y0=lines[current_line-1][0][1]
            y1=lines[current_line][0][1]
            y2=lines[current_line+1][0][1]
            y3=lines[current_line+2][0][1]
            a0 = -(y0/2)+(3*y1/2)-(3*y2/2)+(y3/2)
            a1 = y0-(5*y1/2)+(2*y2)-(y3/2)
            a2 = (y2 - y0)/2
            a3 = y1
            x=solve_quadratic(3*a0, 2*a1, a2)
            for j in range(len(x)):
                i_value=distance*(x[j]+current_line-1)+bounds[0]
                if x[j]-current_line+1>=lines[current_line][0][0] and x[j]-current_line+1<=lines[current_line+1][0][0]:
                    nd_derivative=(6*a0*x[j])+(2*a1)
                    #print(nd_derivative)
                    if nd_derivative<=0:
                        interpolation=int(cubic_interpolation(y0, y1, y2, y3, x[j]))
                        background_houses.append(bg_house((i_value, -interpolation), 1))
            #try:
            #    if lines[current_line-1][0][1]<lines[current_line][0][1] and lines[current_line][0][1]>lines[current_line+1][0][1]:
            #        interpolation=int(cubic_interpolation(y0, y1, y2, y3, (i-bounds[0])/distance-current_line+1))
            #        background_houses.append(bg_house((i, -interpolation), 1))
            #except:
            #    pass
        x=(i-bounds[0])/distance-current_line+1
        #print("x - ",x)
        interpolation=int(cubic_interpolation(y0, y1, y2, y3, x))
        #if interpolation-int(cubic_interpolation(y0, y1, y2, y3, x-1))<10 and int(cubic_interpolation(y0, y1, y2, y3, x+1))-interpolation<10:
        #    print("Manual")
        #    background_houses.append(bg_house((i-bounds[0], -interpolation), 1))
        terrain.append(Column([i-bounds[0], 0], interpolation-50, (0,0,11)))
        terrain.append(Column([i-bounds[0], 50-interpolation], 50, (0,0,80)))
    return terrain
def draw_terrain(terrain):
    global background_houses
    for i in range(len(terrain)):
        terrain[i].draw()
    for i in range(len(background_houses)):
        background_houses[i].draw()
terrain=generate_cubic_terrain(lines)


def interval_MTV(a_min, a_max, b_min, b_max):
  #a_right and a_left are the 2 posible MTV directions
  a_right=b_max-a_min
  a_left=a_max-b_min
  if a_right<0 or a_left<0:
    return [False]
  elif a_right<a_left:
    return [a_right, b_max]
  else:
    return [-a_left, a_max]
def angvector(angle):
  return Vector([[cos(radians(angle)), sin(radians(angle))], [-sin(radians(angle)), cos(radians(angle))]])
def draw(self):
    points=[]
    if self.draw_hitbox:
      for i in range(len(self.pos)):
        points.append((self.pos+scroll).gettuple(i))
      pygame.draw.polygon(screen, self.colour, points)
    if self.has_image:
      self.find_frame()
      screen.blit(self.image, (self.pos+scroll+self.offset).gettuple(0))
def draw_big_wall(self):
  points=[]
  if self.draw_hitbox:
    for i in range(len(self.pos)):
      points.append((self.pos+scroll+self.offset).gettuple(i))
    pygame.draw.polygon(screen, self.colour, points)
  if self.has_image:
    self.find_frame()
    x, y = self.pos[0][0], self.pos[0][1]
    for i in range(self.length):
      start=-int((i)*self.slope)
      for j in range(start, self.height):
        #print(-1*(y+j)*wall_height)
        if j==start and self.slope<0:
          screen.blit(self.image[1], (x+i*wall_width+scroll[0][0]+self.offset[0][0], y+(j)*wall_height+scroll[0][1]+self.offset[0][1]))
        elif j==start and self.slope>0:
          screen.blit(self.image[2], (x+i*wall_width+scroll[0][0]+self.offset[0][0], y+(j-1)*wall_height+scroll[0][1]+self.offset[0][1]))
          screen.blit(self.image[0], (x+i*wall_width+scroll[0][0]+self.offset[0][0], y+j*wall_height+scroll[0][1]+self.offset[0][1]))
        else:
          screen.blit(self.image[0], (x+i*wall_width+scroll[0][0]+self.offset[0][0], y+j*wall_height+scroll[0][1]+self.offset[0][1]))
def draw_item(self):
  if self.draw_hitbox:
    points=[]
    for i in range(len(self.hitbox)):
      points.append((self.hitbox+scroll+self.offset).gettuple(i))
    pygame.draw.polygon(screen, (150, 150, 150), points)
  if self.image_counter<len(item.image_sets[self.type][1])*self.frame_duration-1:
    #if self.image_counter%item.image_sets[self.type][0]==0:
    self.image_counter+=1
    self.image=pygame.image.load("images/"+str(item.image_sets[self.type][1][self.image_counter // self.frame_duration]))
  else:
    self.image_counter=0
  screen.blit(self.image, (self.hitbox[0][0]+scroll[0][0]+self.offset[0][0], self.hitbox[0][1]+scroll[0][1]+self.offset[0][1]))
def draw_square(pos):
  #print("square pos - ", pos)
  width=5
  pygame.draw.rect(screen, (34, 139, 34), (pos[0][0]-width, pos[0][1]-width, width, width))
font = pygame.font.Font('freesansbold.ttf', 25)
def write(message, x, y, colour):
    #Creates the text message
    text = font.render(message, True, colour)
    #Displays the text message
    screen.blit(text, (x, y))

physobj.draw=draw
bigwall.draw=draw_big_wall
item.draw=draw_item

def create_wall(x, y, mass, type):
  width, height= wall_width, wall_height
  wall=physobj(Vector([[x*width, y*height], [(x+1)*width, y*height], [(x+1)*width, (y+1)*height], [x*width, (y+1)*height]]), mass, type)
  wall.draw_hitbox=False
  wall.mobile=False
  wall.id=["wall", wall.id[1]]
  if type==1:
    wall.bounciness=0.5
    wall.friction=0.9
  elif type==2:
    wall.bounciness=0.5
    wall.friction=0.99
  elif type==8:
    wall.bounciness=2
    wall.friction=1
  return wall
def create_candy_cane(x, y, mass):
  width, height = wall_width, wall_height
  cane=physobj(Vector([[x*width-23, y*height-30], [x*width, y*height-30], [x*width, y*height], [x*width-23, y*height]]), mass, 7)
  cane.mobile=False
  cane.draw_hitbox=False
  cane.collision_response=False
  return cane
def create_big_wall(x, y, x2, y2, mass, type, slope):
  width, height= wall_width, wall_height
  wall=bigwall(Vector([[x*width, y*height], [(x2)*width, (y*height-(x2-x)*width*slope)], [(x2)*width, (y2)*height], [x*width, (y2)*height]]), mass, type, x2-x, y2-y)
  wall.mobile=False
  wall.slope=slope
  wall.id=["w", wall.id[1]]
  if type==1:
    wall.bounciness=0.5
    wall.friction=0.9
  elif type==2:
    wall.bounciness=0.5
    wall.friction=0.99
  elif type==8:
    wall.bounciness=1
    wall.friction=1
  return wall
def create_row(list, x1, y1, length, mass, type):
  for i in range(length):
    list.append(create_wall(x1+i, y1, mass, type))
  return list
def create_column(list, x1, y1, height, mass, type):
  for i in range(height):
    list.append(create_wall(x1, y1+i, mass, type))
  return list
def create_house(list, x1, y1, type):
  x1=x1*wall_width
  y1=y1*wall_width-165
  if type==1:
    roof_vector=Vector([[x1+33, y1+3], [x1+231, y1+3], [x1+261, y1+54], [x1, y1+54]])
  elif type==2:
    roof_vector=Vector([[x1, y1], [x1+261, y1], [x1+261, y1+54], [x1, y1+54]])
  house_vector=Vector([[x1+30, y1+54], [x1+231, y1+54], [x1+231, y1+165], [x1+30, y1+165]])
  if type==1:
    roof=physobj(roof_vector, 50, 3)
    house=physobj(house_vector, 100, 4)
    roof.offset=Vector([[-33, -3]])
  elif type==2:
    roof=physobj(roof_vector, 50, 5)
    house=physobj(house_vector, 100, 6)
    house.offset=Vector([[-30, 0]])
  house.collision_response=False
  house.draw_hitbox=False
  roof.draw_hitbox=True
  roof.mobile=False
  house.mobile=False
  list.append(roof)
  list.append(house)
  return list

triangle=physobj(Vector([[100, 100], [200, 100], [100, 150]]), 10, -1)
triangle.rotation=0.1
global gingerbread
gingerbread=physobj(Vector([[0, 0], [25, 0], [25, 47], [0, 47]]), 20, 0)
gingerbread.draw_hitbox=False
gingerbread.translation(Vector([[10, 320]]))
startx, starty = 10, 320
gingerbread.id[0]="Gingerbread"
#objects=[gingerbread, create_big_wall(-15,15,8,1,15,10), item(Vector([[100, 300]]), 0)]

#Ice wall - create_big_wall(15,15,8,2,5,1)
pygame.display.update()

def generate_vector(string):
    #string is [x1/y1[x2/y2
    vector_temp=string.split("[")
    vector_temp.pop(0) #First element is empty when splitting from first character [
    for i in range(len(vector_temp)):
        vector_temp[i]=vector_temp[i].split("/")
        #vector_temp[i].pop(0)
    for i in range(len(vector_temp)):
        for j in range(len(vector_temp[i])):
            vector_temp[i][j]=int(vector_temp[i][j])
    return Vector(vector_temp)

def read_file(filename):
    gingerbread=physobj(Vector([[0, 0], [25, 0], [25, 47], [0, 47]]), 20, 0)
    gingerbread.draw_hitbox=False
    gingerbread.translation(Vector([[10, 320]]))
    startx, starty = 10, 320
    gingerbread.id[0]="Gingerbread"
    level=[gingerbread]
    f=open(filename+".txt", "r")
    for line in f:
        try:
            arguaments=line.split(",")
            if arguaments[0]=="create_big_wall":
                level.append(create_big_wall(int(arguaments[1]), int(arguaments[2]), int(arguaments[3]), int(arguaments[4]), int(arguaments[5]), int(arguaments[6]), int(arguaments[7])))
            elif arguaments[0]=="item":
                vector=generate_vector(arguaments[1])
                level.append(item(vector, int(arguaments[2])))
            elif arguaments[0]=="create_candy_cane":
                level.append(create_candy_cane(int(arguaments[1]), int(arguaments[2]), int(arguaments[3])))
            elif arguaments[0]=="create_house":
                create_house(level, int(arguaments[1]), int(arguaments[2]), int(arguaments[3]))
            elif arguaments[0]=="create_wall":
                level.append(create_wall(int(arguaments[1]), int(arguaments[2]), int(arguaments[3]), int(arguaments[4])))
        except:
            print("Failed on line", line)
    return level


level1=[gingerbread, create_big_wall(-25, 0, -10, 15, 8, 1, 0), create_big_wall(-25, 15, 10, 22, 8, 1, 0), item(Vector([[100, 300]]), 0), create_big_wall(15, 15, 40, 22, 8, 1, 0), create_big_wall(40, 15, 50, 22, 8, 1, 1), create_big_wall(50, 5, 60, 22, 8, 1, 0), create_big_wall(60, 5, 70, 22, 8, 1, -1), create_big_wall(70, 15, 90, 22, 8, 1, 0), create_candy_cane(72, 15, 10), item(Vector([[32*wall_width, 14*wall_height]]), 1), item(Vector([[72*wall_width, 5*wall_height]]), 3)]
level1=create_house(level1, 20, 15, 1)
level1=create_house(level1, 50, 5, 2)
level2=[gingerbread, create_big_wall(-30, 0, -18, 37, 8, 1, 0), create_big_wall(-18, 19, -10, 37, 8, 1, -1), create_big_wall(-10, 27, 120, 37, 8, 1, 0), create_big_wall(-10, 15, 10, 22, 8, 1, 0), create_big_wall(10, 15, 30, 22, 8, 2, 0), create_big_wall(40, 15, 50, 22, 8, 2, 0), create_big_wall(60, 15, 70, 22, 8, 1, 0), create_big_wall(72, 13, 73, 22, 8, 1, 0), create_big_wall(75, 11, 76, 22, 8, 1, 0)]
if level==1:
    objects=level1
elif level==2:
    objects=level2
objects=read_file("level"+str(level))
def remove_object(id):
  for i in range(len(objects)):
    if objects[i].id==id:
      objects.pop(i)
      break

def collision_response(a, b):
  global remaining_jump, jump_time, level, objects, level_won
  #if b.id[0]=="Gingerbread":
  #    a, b=b, a
  a1=a.gethitbox()
  b1=b.gethitbox()
  a2=(angvector(a.rotation)*(a1-a.pivot))+a.pivot+a.velocity
  if b.mobile:
    b2=(angvector(b.rotation)*(b1-b.pivot))+b.pivot+b.velocity
  else:
    b2=b.gethitbox()
  collision_a=a1.collision(a2, b1, b2)
  collision_b=b1.collision(b2, a1, a2)
  if collision_a=="none" and collision_b=="none":
    collision="none"
    #write("None", 200, 200, (200, 50, 178))
  else:
    if collision_a=="none":
      collision=collision_b
      switched="b"
    elif collision_b=="none":
      collision=collision_a
      switched="a"
    else:
      if collision_a[3]<=collision_b[3]:
        collision=collision_a
        switched="a"
      else:
        write("Switch", 200, 300, (200, 50, 178))
        collision=collision_b
        switched="b"
  if collision!="none" and b.collision_response==False:
      if b.id[0]=="Collectible":
          if b.id[1]==3:
              level_won=True
              print("SWEETEST VICTORY!!")
              level+=1
              objects=read_file("level"+str(level))
          else:
              a.inventory.append(b.id[1])
              remove_object(b.id)
  #if collision!="none" and b.collision_response==False:
  elif collision!="none" and b.collision_response:
    a.moved=True
    b.moved=True
    side_b=collision[2][1]-collision[2][0]
    v_dir=a.velocity.projscalar(Vector([[0, 1]]))
    h_dir=a.velocity.projscalar(Vector([[1, 0]]))
    if a.id[0]=="Gingerbread":
      if v_dir>0:
        remaining_jump=jump_time
      #print(dir>=0)
    elif b.id[0]=="Gingerbread":
      #print("GINGRER")
      #print(dir>=0)
      if v_dir>0:
        #print("Reset.")
        remaining_jump=jump_time
    total_force=a.mass*a.acceleration+b.mass*b.acceleration
    total_momentum=a.mass*a.velocity+b.mass*b.velocity
    reverse_time=(collision[3]-1)
    normal=Vector([[-side_b[0][1], side_b[0][0]]])
    #negative_normal=-1*normal
    #remnant=a.velocity.proj(negative_normal)-a.velocity
    #a.translation(collision[3]*a.velocity-a.velocity)
    remnant_a=(1-collision[3])*a.velocity
    vertical=(-1*remnant_a*b.bounciness).proj(normal)
    horizontal=(a.velocity*b.friction).proj(side_b)
    a.velocity=vertical+horizontal
    a.translation(a.velocity)
    if b.mobile:
      b.translation(reverse_time*b.velocity)
    #rotation_amount=a.rotation*reverse_time
    #print(rotation_amount)
    #a.rotate(reverse_time*a.rotation)
    #write(str(collision[3]), 200, 200, (200, 50, 178))

keys=[False, False, False, False]
commands=keys
remaining_jump=0
background_image=pygame.transform.scale(pygame.image.load("images/Ninja Background.png"), (4645, 945))
bg_size=Vector([[4645, 945]])
game_state="level_loaded"
while True:
  level_won=False
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
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT:
        keys[0]=False
      if event.key == pygame.K_RIGHT:
        keys[1]=False
      if event.key == pygame.K_UP:
        keys[2]=False
      if event.key == pygame.K_DOWN:
        keys[3]=False

  for i in range(len(keys)):
    if keys[i]:
      commands[i]=True
    else:
      commands[i]=False
  if game_state=="level_loaded":
      if commands[0]:
        #objects[0].aforces[0]=[objects[0].aforces[0][0], objects[0].aforces[0][1]+Vector([[-4, 0]])]
        if l_acceleration<10:
            objects[0].add_force(Vector([[-1.5, 0]]), objects[0].pivot, "c_left")
      #else:
      #  objects[0].remove_force("c_left")
      if commands[1]:
        #objects[0].aforces[0]=[objects[0].aforces[0][0], objects[0].aforces[0][1]+Vector([[4, 0]])]
        if r_acceleration<10:
            objects[0].add_force(Vector([[1.5, 0]]), objects[0].pivot, "c_right")
      #else:
      #  objects[0].remove_force("c_right")
      if commands[2]:
        #objects[0].aforces[0]=[objects[0].aforces[0][0], objects[0].aforces[0][1]+Vector([[0, -4]])]
        if remaining_jump>0:
          objects[0].add_force(Vector([[0, -10]]), objects[0].pivot, "c_up")
          remaining_jump-=1
      else:
        remaining_jump=0
      #else:
      #  objects[0].remove_force("c_up")
      if commands[3]:
        #objects[0].aforces[0]=[objects[0].aforces[0][0], objects[0].aforces[0][1]+Vector([[0, 4]])]
        objects[0].add_force(Vector([[0, 10]]), objects[0].pivot, "c_down")
      #else:
      #  objects[0].remove_force("c_down")

      if objects[0].find_force("c_left")!="none":
          if l_acceleration<10:
              l_acceleration+=1
      else:
          if l_acceleration>0:
              l_acceleration-=1
      if objects[0].find_force("c_right")!="none":
          if r_acceleration<10:
              r_acceleration+=1
      else:
          if r_acceleration>0:
              r_acceleration-=1

      for i in range(len(objects)):
        objects[i].moved=False
      for s in range(substeps):
        if level_won:
          break
        for i in range(len(objects)):
          if i>=len(objects):
            break
          if objects[i].mobile:
            objects[i].add_force(gravity, objects[i].pivot, "gravity")
          if objects[i].collision_response:
            objects[i].calc_aforces()
          for j in range(len(objects)):
            if level_won:
              break
            if j>=len(objects):
              break
            if i!=j and objects[i].mobile and objects[i].collision_response:
              collision_response(objects[i], objects[j])
          if level_won:
              break
          if objects[i].mobile and objects[i].moved==False:
            objects[i].move()
      char_pos=[objects[0].pivot[0][0], objects[0].pivot[0][1]]
      scroll=Vector([[half_dimension[0]-char_pos[0], half_dimension[1]-char_pos[1]]])
      pos=Vector([[0, -1*bg_size[0][1]+dimensions[0][1]]])+1/5*(scroll+Vector([[10, 320]]))

      screen.fill((0,0,61))
      if level==2:
          screen.blit(background_image, (scroll[0][0]-startx-half_dimension[0], scroll[0][1]-starty+half_dimension[1]))
      elif level==1:
          draw_terrain(terrain)


      #screen.blit(background_image, pos.gettuple(0))
      for i in range(1, len(objects)):
        limits=objects[i].find_range()
        #print("x_range - ", limits[0], limits[1])
        x_range=interval_MTV(limits[0], limits[1], 0, dimensions[0][0])
        y_range=interval_MTV(limits[2], limits[3], 0, dimensions[0][1])
        if x_range!="none" and y_range!="none":
          objects[i].draw()
      objects[0].draw()
      for i in range(len(objects[0].inventory)):
          if i>len(objects[0].inventory):
              break
          else:
              if objects[0].inventory[i]==1:
                  if lives[1]>0:
                      lives[1]=4
                  else:
                      lives[0]+=1
                  objects[0].inventory.pop(i)
      for i in range(lives[0]):
          screen.blit(live_images[3], (30+(i)*50, 30))
          if i==lives[0]-1 and lives[1]>0:
              screen.blit(live_images[lives[1]-1], (30+(i+1)*50, 30))
      write(str(r_acceleration), 200, 200, (200, 178, 50))
  pygame.display.update()
  time.sleep(1/fps)
