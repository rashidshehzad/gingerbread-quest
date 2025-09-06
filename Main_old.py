#Modules imported on lines 12-21. This also imports the majority of classes from the physobj and matrix modules.
#Classes: Column on 129, bg_house on 143
#From lines 176 to 262, the background is randomly generated using cubic interpolation.
#From 280 to 327 physobj and bigwall class methods are overwritten to work with pygame.
#Subroutines for reading level data from file defined on lines 467 to 503
#Collision response subroutine lines 515 to 612. Use advanced algorithm+collision response





import sys
#Imports pygame, time, random and maths modules.
import pygame, time, random
from pygame.locals import QUIT
from math import *
#matrix and polish modules were both created by me
from matrix import Vector
from polish import *
#Physobj module was also created by me.
from physobj import physobj, bigwall, item

#This subroutine finds the current file's path, to access files in its location.
def find_file_root():
    temp=__file__
    temp=temp.split("\\")
    file_root=""
    for i in range(len(temp)-1):
        file_root+=temp[i]+"/"
    return file_root
file_root=find_file_root()

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

test_queue=queue(5)
for i in range(5):
    test_queue.add(i)
for i in range(5):
    print(test_queue.current())
    test_queue.remove()

#Pygame initialised
pygame.init()
#Global variables for screen size, player lives, current level and game state.
global dimensions, lives, level, game_state
level=1
#Lives = [Life, hp]
lives=[3, 1]

#Creates a list containing frames for the lives' UI
live_images=[]
for i in range(1,5):
    live_images.append(pygame.image.load(file_root+"images/Life"+str(i)+".png"))
dimensions=Vector([[1000, 700]])
#Creates the pygame screen.
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
#l_acceleration and r_acceleration are used to stop the player inputs from accelerating the player too fast.
#However, other forces and friction can still speed up the player more.
l_acceleration=0
r_acceleration=0
level_won=False
game_won=False
#bg_zoom is used for the x and y zoom scale of the background terrain (Class Column, Line 124) generated in level 1.
bg_zoom=[0.5, 0.5]
#Half_dimension is half the size of the screen. It's used for calculations involving the centre of the screen.
half_dimension=[500, 350]
#Scroll is the offset applied to where the objects appear on screen, to create a scrolling effect.
scroll=Vector([[0, 0]])
bg_height=100

#Subroutine to solve a quadratic equation.
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
#Can also be zoomed in according to bg_zoom.
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
        self.image=pygame.image.load(file_root+"images/House4"+str(type)+".png")
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
#The current environment. The environment's properties decide how the background will be generated, but I have only created 1 example.
environment=0
#Bounds is the size of the background terrain, meaning it exists between x values 0 and 10000.
global bounds
bounds=[0, 10000]
#Dampening is used in the terrain generation to decide how much smaller the offset will be each time.
dampening=0.5
offset_range=[-10, 10]
#Function for giving a random value between 2 bounds
def random_range(range):
    return random.randint(bounds[0], bounds[1])
#Function used for giving the hight of a column in the background, according to the formula of cubic interpolation.
def cubic_interpolation(y0, y1, y2, y3, x):
  a0 = -(y0/2)+(3*y1/2)-(3*y2/2)+(y3/2)
  a1 = y0-(5*y1/2)+(2*y2)-(y3/2)
  a2 = (y2 - y0)/2
  a3 = y1
  return(a0*x**3+a1*x**2+a2*x+a3)
#Splits a line into 2 lines, and changes the new central point's y value by offset.
#It is the same as creating a bump in the middle of a line, whose height is decided by the value of offset.
def split_line(a, b, offset):
    mid=(1/2)*(a+b)
    length=(b-a).magnitude()
    offset=(bounds[1]-bounds[0])/length*offset
    return mid+offset
#The function for generating the lines used in the terrain generation.
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

        temp_lines.append(b)
        lines=temp_lines
        offset=[int(offset[0][0]*dampening), int(offset[0][1]*dampening)]
    return lines
gradient=random_range(environments[0][1])/(bounds[1]-bounds[0])
c=random_range(environments[0][2])/100
lines=[Vector([[bounds[0], c]]), Vector([[bounds[1], bounds[1]*gradient+c]])]
cuts=6
lines=cut_lines(lines, cuts, offset_range, dampening)
#Converts a list of lines into a list of columns that will appear in the background.
#The height of these columns matches the equation between any 2 lines.
def generate_cubic_terrain(lines):
    #distance is the distance between any 2 lines.
    distance=(bounds[1]-bounds[0])/(2**cuts)
    #2 lines are added to the beginning and end of the list for cubic interpolation to work.
    lines.insert(0, 2*lines[0]-lines[1])
    lines.append(2*(lines[len(lines)-1])-lines[len(lines)-2])
    #Terrain is the list containing all the columns which will be rendered as the background.
    terrain=[]
    #Current_line keeps track of the lines being interpolated between.
    current_line=0
    for i in range(bounds[0], bounds[1]):
        #If the current x value goes outside the current line's range, current_line is increased by 1.
        #Several values used in calculations are also recalculated. This is more efficient than calculating them for each x value.
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
            #Houses are added to their own background_houses list.
            #This is done here seperately from the addition of columns to the list terrain.
            for j in range(len(x)):
                i_value=distance*(x[j]+current_line-1)+bounds[0]
                if x[j]-current_line+1>=lines[current_line][0][0] and x[j]-current_line+1<=lines[current_line+1][0][0]:
                    nd_derivative=(6*a0*x[j])+(2*a1)
                    #If the gradient of the function allows a house to be built, it's added to background_houses.
                    if nd_derivative<=0:
                        interpolation=int(cubic_interpolation(y0, y1, y2, y3, x[j]))
                        background_houses.append(bg_house((i_value, -interpolation), 1))
        #The x value is adjusted to interpolate between 0 and 1.
        x=(i-bounds[0])/distance-current_line+1
        #Interpolation is a value calculated for each x value to decide the height of the column.
        interpolation=int(cubic_interpolation(y0, y1, y2, y3, x))
        #2 columns, which represent different colours, are added to the terrain list.
        terrain.append(Column([i-bounds[0], 0], interpolation-50, (0,0,11)))
        terrain.append(Column([i-bounds[0], 50-interpolation], 50, (0,0,80)))
    return terrain
#This function takes the list terrain as a parameter, and draws each element, which will be an instance of Class column.
#However, background_houses is treated as a global and is drawn seperately.
def draw_terrain(terrain):
    global background_houses
    for i in range(len(terrain)):
        terrain[i].draw()
    for i in range(len(background_houses)):
        background_houses[i].draw()
terrain=generate_cubic_terrain(lines)

#Interval_MTV figures out the Minimum Translation Vector between a 1D interval.
def interval_MTV(a_min, a_max, b_min, b_max):
  #a_right and a_left are the 2 posible MTV directions
  a_right=b_max-a_min
  a_left=a_max-b_min
  #a_right and a_left
  if a_right<0 or a_left<0:
    return [False]
  elif a_right<a_left:
    return [a_right, b_max]
  else:
    return [-a_left, a_max]
#Creates a 2D rotation matrix which rotates a 2D vector by thatangle.
def angvector(angle):
  return Vector([[cos(radians(angle)), sin(radians(angle))], [-sin(radians(angle)), cos(radians(angle))]])
#Several draw methods are defined outside of their classes before being assigned to their classes.
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
    self.image_counter+=1
    self.image=pygame.image.load(file_root+"images/"+str(item.image_sets[self.type][1][self.image_counter // self.frame_duration]))
  else:
    self.image_counter=0
  screen.blit(self.image, (self.hitbox[0][0]+scroll[0][0]+self.offset[0][0], self.hitbox[0][1]+scroll[0][1]+self.offset[0][1]))
def draw_square(pos):
  width=5
  pygame.draw.rect(screen, (34, 139, 34), (pos[0][0]-width, pos[0][1]-width, width, width))

#The methods are made part of the classes.
physobj.draw=draw
bigwall.draw=draw_big_wall
item.draw=draw_item

#A subroutine used for writing text to the screen. The font used is a global declared beforehand.
font = pygame.font.Font('freesansbold.ttf', 25)
def write(message, x, y, colour):
    #Creates the text message
    text = font.render(message, True, colour)
    #Displays the text message
    screen.blit(text, (x, y))

#These functions are used when reading from the level file to create an instance of an object.
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
  wall.id=["w", wall.id[1], type]
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

#Although the gingerbread player is inluded in the objects list, it is created seperately and given certain attributes before being added to the list.
global gingerbread
gingerbread=physobj(Vector([[0, 0], [25, 0], [25, 47], [0, 47]]), 20, 0)
gingerbread.draw_hitbox=False
gingerbread.translation(Vector([[10, 320]]))
startx, starty = 10, 320
gingerbread.id[0]="Gingerbread"

pygame.display.update()

#This function is used to convert string data from the save file into a vector object which is returned.
def generate_vector(string):
    #string is in format [x1/y1[x2/y2
    vector_temp=string.split("[")
    vector_temp.pop(0) #First element is empty when splitting from first character [
    for i in range(len(vector_temp)):
        vector_temp[i]=vector_temp[i].split("/")
        #vector_temp[i].pop(0)
    for i in range(len(vector_temp)):
        for j in range(len(vector_temp[i])):
            vector_temp[i][j]=int(vector_temp[i][j])
    return Vector(vector_temp)

#Puts the gingerbread back at the beginning of the level.
def reset_gingerbread():
    gingerbread=physobj(Vector([[0, 0], [25, 0], [25, 47], [0, 47]]), 20, 0)
    gingerbread.draw_hitbox=False
    gingerbread.translation(Vector([[10, 320]]))
    startx, starty = 10, 320
    gingerbread.id[0]="Gingerbread"
    gingerbread.moved=False
    return gingerbread

#Increases the lives/score
def lives_increment(collectible):
    if collectible=="Cookie":
        if lives[1]>0 and lives[1]<4:
            lives[1]=4
        else:
            lives[0]+=1
    else:
        if lives[1]<4:
            lives[1]+=1
        else:
            lives[0]+=1
            lives[1]=1

#Decreases the lives/score
def lives_decrement():
    if lives[1]>0:
        lives[1]=0
    else:
        if lives[0]>0:
            lives[0]-=1

#This function reads a file, and reads its data to create a list of objects.
#This functon is responsible for loading in and creating the level.
def read_file(filename):
    #The gingerbread man is declare first.
    #All his values are reset so he ends up at the start of the next level, rather than spawning in at the wrong place.
    gingerbread=reset_gingerbread()
    #The level list is created, with only the gingerbread man initially.
    level=[gingerbread]
    try:
        f=open(file_root+filename+".txt", "r")
    except:
        #If the file doesn't exist or can't be read, the current level is returned instead.
        global objects
        global game_won
        objects[0]=gingerbread
        #If there is no file to read, the programme assumes the game's been won.
        game_won=True
        return objects
    for line in f:
        try:
            #Each line is splt into several "arguaments", which contain information such as the object type, and its properties such as position.
            arguaments=line.split(",")
            #Depending on the object type, which is always the first arguament, the matching function is used to create an instance of it.
            if arguaments[0]=="create_big_wall":
                level.append(create_big_wall(int(arguaments[1]), int(arguaments[2]), int(arguaments[3]), int(arguaments[4]), int(arguaments[5]), int(arguaments[6]), int(arguaments[7])))
            elif arguaments[0]=="item":
                print(arguaments)
                vector=wall_width*generate_vector(arguaments[1])
                level.append(item(vector, int(arguaments[2])))
            elif arguaments[0]=="create_candy_cane":
                level.append(create_candy_cane(int(arguaments[1]), int(arguaments[2]), int(arguaments[3])))
            elif arguaments[0]=="create_house":
                create_house(level, int(arguaments[1]), int(arguaments[2]), int(arguaments[3]))
            elif arguaments[0]=="create_wall":
                level.append(create_wall(int(arguaments[1]), int(arguaments[2]), int(arguaments[3]), int(arguaments[4])))
        except:
            #If there was an error reading a line, it's skipped, and an error message is printed.
            print("Failed on line", line)
    return level
    
#The current level, known as objects, is loaded from the current level.
objects=read_file("level"+str(level))
#A subroutine for removing an object with the matching ID from the level.
#Used when, for example, a collectible is collected by the player and should be removed.
def remove_object(id):
  for i in range(len(objects)):
    if objects[i].id==id:
      objects.pop(i)
      break
#collision_response finds out if a and b are colliding, and then changes their velocities and positions accordingly.
def collision_response(a, b):
  global remaining_jump, jump_time, level, objects, level_won
  #Variables such as the level, and how much jump the player has left are made global initially.
  #This is technically inefficient as they aren't always needed, since not all collisions involve the player.

  #a1 and b1 are the current hitboxes of a and b.
  a1=a.gethitbox()
  b1=b.gethitbox()
  #a2 and b2 are their positions in the next frame, and depends on if they are mobile or not.
  a2=(angvector(a.rotation)*(a1-a.pivot))+a.pivot+a.velocity
  if b.mobile:
    b2=(angvector(b.rotation)*(b1-b.pivot))+b.pivot+b.velocity
  else:
    b2=b.gethitbox()
  #2 collision checks are made on a and b (using the collision function), as the order can matter in the algorithm.
  collision_a=a1.collision(a2, b1, b2)
  collision_b=b1.collision(b2, a1, a2)
  #The following if statements are used to check which collision value should be used.
  if collision_a=="none" and collision_b=="none":
    collision="none"
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
        collision=collision_b
        switched="b"
  #If there has been a collision, and b has no collision response, new positions or velocities aren't needed.
  if collision!="none" and b.collision_response==False:
      #Makes a check to see if b is a collectible, since all collectibles have no collision response.
      if b.id[0]=="Collectible":
          #If b is also the finish flag, the level is increased by 1, and level_won is set to True.
          if b.id[1]==3:
              level_won=True
              print("SWEETEST VICTORY!!")
              level+=1
              objects=read_file("level"+str(level))
          #Otherwise, b is a normal collectible and is added to the inventory of a (the player in this case).
          else:
              a.inventory.append(b.id[1])
              remove_object(b.id)
  #If there has been a collision, and b DOES have a collision response, it will need to be calculated here.
  elif collision!="none" and b.collision_response:
    #a and b's moved values are set to True, indicating they have been moved on the current frame. This means they won't be checked against each other again.
    a.moved=True
    b.moved=True
    #side_b is the side of b with which a is colliding.
    side_b=collision[2][1]-collision[2][0]
    #a's velocity is split into 2 components, horizontal and vertical.
    v_dir=a.velocity.projscalar(Vector([[0, 1]]))
    h_dir=a.velocity.projscalar(Vector([[1, 0]]))
    #If a is the gingerbread man, his remaining jump is reset if his vertical velocity is positive.
    if a.id[0]=="Gingerbread":
      if v_dir>0:
        remaining_jump=jump_time
      #If the player has hit lava, they are killed and reset.
      try:
        if b.id[2]==9:
            position=(objects[0].pos+scroll+Vector([[-50, -48]])).getrow(0)
            screen.blit(pygame.image.load(file_root+"images/Woops.png"), (position[0], position[1]))
            pygame.display.update()
            time.sleep(1)
            objects[0]=reset_gingerbread()
            lives_decrement()
      except:
        pass
    #If b instead is the gingerbread man, the same is done, but to b instead.
    elif b.id[0]=="Gingerbread":
      if v_dir>0:
        remaining_jump=jump_time
      #If the player has hit lava, they are killed and reset.
      try:
        if a.id[2]==9:
            objects[0]=reset_gingerbread()
            lives_decrement()
      except:
        pass
    total_force=a.mass*a.acceleration+b.mass*b.acceleration
    total_momentum=a.mass*a.velocity+b.mass*b.velocity
    #The new velocities of a and b are calculated depending on the time taken for the collision.
    reverse_time=(collision[3]-1)
    normal=Vector([[-side_b[0][1], side_b[0][0]]])

    remnant_a=(1-collision[3])*a.velocity
    #The new velocities are calculated by adding together the projections of the horizontal and veritcal aspects.
    vertical=(-1*remnant_a*b.bounciness).proj(normal)
    horizontal=(a.velocity*b.friction).proj(side_b)
    a.velocity=vertical+horizontal
    a.translation(a.velocity)
    if b.mobile:
      b.translation(reverse_time*b.velocity)

#The pressed-state of each key (left, right, up, down) is stored in the list keys.
keys=[False, False, False, False]
#A seperate list, commands, stores whether the corresponsing command should be performed.
commands=keys
#remaining_jump stores how much more the player can jump.
remaining_jump=0
background_image=pygame.transform.scale(pygame.image.load(file_root+"images/Ninja Background.png"), (4645, 945))
bg_size=Vector([[4645, 945]])
#The variable game_state indicates that the game should play, as the level has been loaded.
game_state="level_loaded"
#This is the gameplay loop. It carries on until broken.
while game_won==False:
  level_won=False
  #Takes user input to check which key is pressed and which isn't.
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

  #For each true key, the corresponding key is also made True.
  #They can also be set to False if that key is no longer pressed.
  for i in range(len(keys)):
    if keys[i]:
      commands[i]=True
    else:
      commands[i]=False
  if game_state=="level_loaded":
      #Adds forces in the right direction to move the player, depending on which command.
      #For example, jumping adds an unpwards force to the gingerbread man.
      if commands[0]:
        #Before adding a right or left force, a variable is used to check if the character can speed up anymore.
        #This means that after holding the right or left key for long enough, the player can no longer accelerate.
        if l_acceleration<10:
            objects[0].add_force(Vector([[-1.5, 0]]), objects[0].pivot, "c_left")
      if commands[1]:
        if r_acceleration<10:
            objects[0].add_force(Vector([[1.5, 0]]), objects[0].pivot, "c_right")
      #Remaining_jump checks how much further the player can jump, to prevent them flying infinitely.
      if commands[2]:
        if remaining_jump>0:
          objects[0].add_force(Vector([[0, -10]]), objects[0].pivot, "c_up")
          remaining_jump-=1
      else:
        remaining_jump=0
      if commands[3]:
        objects[0].add_force(Vector([[0, 10]]), objects[0].pivot, "c_down")

      #If the character has the left command, l_acceleration is incremented.
      if objects[0].find_force("c_left")!="none":
          if l_acceleration<10:
              l_acceleration+=1
      #Otherwise, it's decreased by 1.
      else:
          if l_acceleration>0:
              l_acceleration-=1
      #The same is done for the right force and r_acceleration.
      if objects[0].find_force("c_right")!="none":
          if r_acceleration<10:
              r_acceleration+=1
      else:
          if r_acceleration>0:
              r_acceleration-=1
      #All objects' moved attribute is set to False, as they haven't yet moved in this frame.
      for i in range(len(objects)):
        objects[i].moved=False
      #Rather than only doing collision checks once, they are done "substeps" time to be more accurate.
      #I have set it to 2, so after the collision check are done, they are done again the second time to be sure.
      for s in range(substeps):
        #If the player reached the finish flag, these collision checks aren't needed, and the level has been reset anyway.
        if level_won:
          break
        for i in range(len(objects)):
          #When objects, such as collectibles, are removed from the list, this check is needed to break the loop.
          if i>=len(objects):
            break
          #If an object can move, gravity is applied to it.
          if objects[i].mobile:
            objects[i].add_force(gravity, objects[i].pivot, "gravity")
          #If the object is supposed to have a collision response, it's forces are caluclated.
          if objects[i].collision_response:
            objects[i].calc_aforces()
          #All the objects are checked against one another, so long as neither has been moved yet.
          for j in range(len(objects)):
            if level_won:
              break
            if j>=len(objects):
              break
            if i!=j and objects[i].mobile and objects[i].collision_response:
              collision_response(objects[i], objects[j])
          if level_won:
              break

          #This method compares only the player to each other object.
          #if i!=0:
          #    collision_response(objects[0], objects[i])
          #If an object can move, but hasn't, it is now forced to move.
          if objects[i].mobile and objects[i].moved==False:
            objects[i].move()
      #The player's new position is retrieved to update the screen's scrolling.
      #Scrolling is done in such a way that the character is always at the centre of the screen.
      char_pos=[objects[0].pivot[0][0], objects[0].pivot[0][1]]
      scroll=Vector([[half_dimension[0]-char_pos[0], half_dimension[1]-char_pos[1]]])
      pos=Vector([[0, -1*bg_size[0][1]+dimensions[0][1]]])+1/5*(scroll+Vector([[10, 320]]))

      #The screen is filled to overwrite the previous frame, avoiding trails.
      screen.fill((0,0,61))
      #Level2 has its own unique background. All other levels use the terrain generation instead.
      if level==2:
          screen.blit(background_image, (scroll[0][0]-startx-half_dimension[0], scroll[0][1]-starty+half_dimension[1]))
      else:
          draw_terrain(terrain)

      #Draws all the objects which appear on screen.
      for i in range(1, len(objects)):
        #X and Y limits of the object are calculated.
        limits=objects[i].find_range()
        x_range=interval_MTV(limits[0], limits[1], 0, dimensions[0][0])
        y_range=interval_MTV(limits[2], limits[3], 0, dimensions[0][1])
        #If the object's x and y ranges appear on screen, it is drawn.
        if x_range!="none" and y_range!="none":
          objects[i].draw()
      objects[0].draw()
      for i in range(len(objects[0].inventory)):
          if i>len(objects[0].inventory):
              break
          else:
              if objects[0].inventory[i]==1:
                  lives_increment("Cookie")
                  objects[0].inventory.pop(i)
              elif objects[0].inventory[i]==0:
                  lives_increment("Bread")
                  objects[0].inventory.pop(i)
      for i in range(lives[0]):
          screen.blit(live_images[3], (30+(i)*50, 30))
          if i==lives[0]-1 and lives[1]>0:
              screen.blit(live_images[lives[1]-1], (30+(i+1)*50, 30))
      #Displays the next level message.
      if level_won and game_won==False:
          screen.fill((0,0,0))
          write("Level "+str(level)+"!", half_dimension[0]-70, half_dimension[1]-10, (255, 255, 255))
          pygame.display.update()
          time.sleep(3)
  pygame.display.update()
  time.sleep(1/fps)

#Displays the player's score and win message at the end.
screen.fill((0,0,0))
for i in range(lives[0]):
    screen.blit(live_images[3], (30+(i)*50, 30))
    if i==lives[0]-1 and lives[1]>0:
        screen.blit(live_images[lives[1]-1], (30+(i+1)*50, 30))
score=lives[0]*4+lives[1]
screen.blit(pygame.image.load(file_root+"images/You win.png"), (half_dimension[0]-162, half_dimension[1]-95))
write("You got a score of "+str(score)+"!", half_dimension[0]-120, half_dimension[1]-10, (255, 255, 255))
pygame.display.update()
time.sleep(10)
