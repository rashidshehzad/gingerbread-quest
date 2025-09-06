import sys

import pygame, time, random
from pygame.locals import QUIT
from matrix import Vector
from math import *
from polish import *

from physobj import physobj, bigwall, item

pygame.init()
global dimensions
dimensions=Vector([[1000, 700]])
screen = pygame.display.set_mode(dimensions.gettuple(0))
pygame.display.set_caption('Hello World!')
fps=50
substeps=2
global wall_width, wall_height, gravity, scroll, half_dimension
jump_time=10
scroll=Vector([[0, 0]])
gravity=Vector([[0, 2]])
#gravity=Vector([[0, 0]])
wall_width, wall_height = 28, 28

global half_dimension, bg_size
half_dimension=[500, 350]


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
  wall.mobile=False
  wall.id=["wall", wall.id[1]]
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
gingerbread=physobj(Vector([[0, 0], [25, 0], [25, 47], [0, 47]]), 20, 0)
gingerbread.translation(Vector([[10, 320]]))
gingerbread.id[0]="Gingerbread"
#objects=[gingerbread, create_big_wall(-15,15,8,1,15,10), item(Vector([[100, 300]]), 0)]
objects=[gingerbread, create_big_wall(-25, 0, -10, 15, 8, 1, 0), create_big_wall(-25, 15, 10, 22, 8, 1, 0), item(Vector([[100, 300]]), 0), create_big_wall(15, 15, 40, 22, 8, 1, 0), create_big_wall(40, 15, 50, 22, 8, 1, 1), create_big_wall(50, 5, 60, 22, 8, 1, 0), create_big_wall(60, 5, 70, 22, 8, 1, -1), create_big_wall(70, 15, 90, 22, 8, 1, 0), create_candy_cane(72, 15, 10)]
objects=create_house(objects, 20, 15, 1)
objects=create_house(objects, 50, 5, 2)
#Ice wall - create_big_wall(15,15,8,2,5,1)
pygame.display.update()

def remove_object(id):
  for i in range(len(objects)):
    if objects[i].id==id:
      objects.pop(i)
      break

def collision_response(a, b):
  global remaining_jump, jump_time
  a2=(angvector(a.rotation)*(a.pos-a.pivot))+a.pivot+a.velocity
  if b.mobile:
    b2=(angvector(b.rotation)*(b.pos-b.pivot))+b.pivot+b.velocity
  else:
    b2=b.pos
  collision_a=a.pos.collision(a2, b.pos, b2)
  collision_b=b.pos.collision(b2, a.pos, a2)
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
  if collision!="none" and b.collision_response:
    a.moved=True
    b.moved=True
  if collision!="none" and b.collision_response==False:
    #print("1")
    if b.id[0]=="Collectible":
      #print("2")
      a.inventory.append(b.id[1])
      remove_object(b.id)
  elif collision!="none" and b.collision_response:
    #write("Wrong", 200, 200, (200, 50, 178))
    #print(a.id)
    dir=a.velocity.projscalar(Vector([[0, 1]]))
    if a.id[0]=="Gingerbread":
      #print("GINGRER")
      if dir>0:
        #print("Reset.")
        remaining_jump=jump_time
      #print(dir>=0)
    elif b.id[0]=="Gingerbread":
      #print("GINGRER")
      #print(dir>=0)
      if dir>0:
        #print("Reset.")
        remaining_jump=jump_time
    total_force=a.mass*a.acceleration+b.mass*b.acceleration
    total_momentum=a.mass*a.velocity+b.mass*b.velocity
    reverse_time=(collision[3]-1)
    side_b=collision[2][1]-collision[2][0]
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
background_image=pygame.image.load("images/Ninja Background large.png")
bg_size=Vector([[4645, 945]])
while True:
  screen.fill((100,100,100))
  write(str(remaining_jump), 200, 200, (200, 58, 170))
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
      if event.key == pygame.K_SPACE:
        side+=1
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

  if commands[0]:
    #objects[0].aforces[0]=[objects[0].aforces[0][0], objects[0].aforces[0][1]+Vector([[-4, 0]])]
    objects[0].add_force(Vector([[-1.5, 0]]), objects[0].pivot, "c_left")
  #else:
  #  objects[0].remove_force("c_left")
  if commands[1]:
    #objects[0].aforces[0]=[objects[0].aforces[0][0], objects[0].aforces[0][1]+Vector([[4, 0]])]
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

  for i in range(len(objects)):
    objects[i].moved=False
  for s in range(substeps):
    for i in range(len(objects)):
      if i>=len(objects):
        break
      if objects[i].mobile:
        objects[i].add_force(gravity, objects[i].pivot, "gravity")
      if objects[i].collision_response:
        objects[i].calc_aforces()
      for j in range(len(objects)):
        if j>=len(objects):
          break
        if i!=j and objects[i].mobile and objects[i].collision_response:
          collision_response(objects[i], objects[j])
      if objects[i].mobile and objects[i].moved==False:
        objects[i].move()
  char_pos=[objects[0].pivot[0][0], objects[0].pivot[0][1]]
  scroll=Vector([[half_dimension[0]-char_pos[0], half_dimension[1]-char_pos[1]]])
  pos=Vector([[0, -1*bg_size[0][1]+dimensions[0][1]]])+1/5*(scroll+Vector([[10, 320]]))
  #screen.blit(background_image, pos.gettuple(0))
  for i in range(1, len(objects)):
    limits=objects[i].find_range()
    #print("x_range - ", limits[0], limits[1])
    x_range=interval_MTV(limits[0], limits[1], 0, dimensions[0][0])
    y_range=interval_MTV(limits[2], limits[3], 0, dimensions[0][1])
    if x_range!="none" and y_range!="none":
      objects[i].draw()
  write(str(scroll), 300, 200, (200, 50, 178))
  objects[0].draw()
  pygame.display.update()
  time.sleep(1/fps)
