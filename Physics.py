from math import *
from matrix import *

def angvector(angle):
  #Original  - 
  #return Vector([[cos(angle), -sin(angle)], [sin(angle), cos(angle)]])
  #Radians - 
  #print("angle - ",angle,'\n\n',Vector([[cos(radians(angle)), sin(radians(angle))], [-sin(radians(angle)), cos(radians(angle))]]))
  return Vector([[cos(radians(angle)), sin(radians(angle))], [-sin(radians(angle)), cos(radians(angle))]])
  
class physobj():
  # def __init__(self, pos, rotation, velocity, colour):
  id=0
  
  def __init__(self, pos: Vector, mass):
    self.velocity=Vector([[0, 0]])
    self.id=physobj.id
    self.mobile=True
    physobj.id+=1
    self.pos = pos
    self.mass = mass
    #if len(velocity[0])==1:
    #  for i in range(len(self.pos[0])):
    #    velocity.vector[0].append(velocity[0][0])
    #    velocity.vector[1].append(velocity[1][0])
    self.pivot = self.pos.cofmass()
    self.colour = (156, 8, 97)
    self.rotation=0
    #rotational_acceleration is an integer.
    #It will be added onto self.rotation and into angvector
    self.rotational_acceleration=0
    #aforces = affecting forces
    self.aforces=[]


    self.pos.polygonate()
    print("sel.pos - ",self.pos)
    print("polygonated - ", self.pos.polygonate())
    self.rotational_inertia=Vector.polynertia(self.pos, self.mass)
    #self.pos.polygons=polygonate(self.pos)
    #print(self.rotation, "type self.rotation - ", type(self.rotation))
    #print(self.pos, "self.pos - ", type(self.pos))

  def translation(self, vec):
    self.pos=self.pos+vec
    
  def calc_vel_rot(self):
    #aforces = [[force, contact, id], ...]
    self.rotational_acceleration=0
    self.acceleration=Vector([[0, 0]])
    for i in range(len(self.aforces)):
      if self.aforces[i][2][0]=="c":
        self.aforces[i][1]=self.pivot
      self.acceleration+=(1/self.mass)*self.aforces[i][0]
      self.rotational_acceleration+=Vector.calculate_rotational_acceleration(self.pos, self.rotational_inertia, self.mass, self.aforces[i][0], self.aforces[i][1])
    self.rotation+=self.rotational_acceleration
    self.velocity+=self.acceleration
    #For when it actually works:
    #self.rotation+=self.rotational_acceleration

  def find_force(self, id):
    #Returns the position of a force, or "none" otherwise.
    pos="none"
    for i in range(len(self.aforces)):
      if self.aforces[i][2]==id:
        pos=i
        break
    return pos
    
  def add_force(self, force, contact, id):
    #addable is the position the force will be sent to.
    addable=self.find_force(id)
    if addable=="none":
      self.aforces.append([force, contact, id])
    else:
      self.aforces[addable]=[force, contact, id]
  
  def remove_force(self, id):
    #removable is the position the force will be removed from.
    removable=self.find_force(id)
    if removable!="none":
      self.aforces.pop(removable)
  
  def move(self):
    self.calc_vel_rot()
    rotation=angvector(self.rotation)
    temppos=self.pos-self.pivot
    #print(self.rotation)
    self.pivot=self.pivot+self.velocity
    self.pos = (rotation * temppos)+ self.pivot
    self.pivot = self.pos.cofmass()
    #self.pos=self.pos+self.velocity
  
      #print(i, self.pos.polygons[i])

def check_bounds(list, vel):
  #within_bounds is true unless proved otherwise
  within_bounds=True
  try:
    if (vel[0]<list[0]):
      within_bounds=False
  except:
    pass
  try:
    if (vel[0]>list[1]):
      within_bounds=False
  except:
    pass
  try:
    if (vel[1]<list[2]):
      within_bounds=False
  except:
    pass
  try:
    if (vel[1]>list[3]):
      within_bounds=False
  except:
    pass
  return within_bounds


class character(physobj):

  def find_frame(self):
    #Cframe stands for Current Frame
    #Cframe is represented as [index of set of frames, index of frame within that set of frames]
    try:
      self.calc_vel_rot()
    except:
      self.velocity=Vector([[0, 0]])
    cframe=self.cframe
    vel=self.velocity[0]
    if check_bounds(self.frames[0], vel):
      found=True
    else:
      found=False
    if found==False:
      for i in range(len(self.frames)):
        if i!=cframe[0]: #If i is cframe[0], we already know it doesn't match.
          if check_bounds(self.frames[i], vel):
            found=True
            cframe=[i, self.frame[i][5]]
            break
    self.image=pygame.image.load("images/"+self.frames[cframe[0]][4][cframe[1]])
    if cframe[1]<len(self.frames[cframe[0]][4])-1:
      cframe[1]+=1
    else:
      cframe[1]=0
    
  def __init__(self, pos, mass, frames):
    self.mobile=True
    self.velocity=Vector([[0, 0]])
    self.id=physobj.id
    physobj.id+=1
    self.frames=frames
    self.cframe=[0, self.frames[0][5]]
    self.find_frame()
    #Frames are formatted as:
    #minx, maxx, miny, maxy, [frames that match these criteria], current frame
    self.pos = pos
    self.mass = mass
    #if len(velocity[0])==1:
    #  for i in range(len(self.pos[0])):
    #    velocity.vector[0].append(velocity[0][0])
    #    velocity.vector[1].append(velocity[1][0])
    self.pivot = self.pos.cofmass()
    self.colour = (156, 8, 97)
    self.rotation=0
    #rotational_acceleration is an integer.
    #It will be added onto self.rotation and then into angvector
    self.rotational_acceleration=0
    #aforces = affecting forces
    self.aforces=[]


    self.pos.polygonate()
    print("sel.pos - ",self.pos)
    print("polygonated - ", self.pos.polygonate())
    self.rotational_inertia=Vector.polynertia(self.pos, self.mass)

class wall(physobj):
  #types: [["image", minhealth, maxhealth],...],...
  wall_size=(28, 28)
  types=[[["images/Rock reflect.png", 0, 10]]]

  def find_frame(self):
    self.current_frame=-1
    self.image=pygame.image.load("images/Error.png")
    for i in range(len(wall.types[self.type])):
      if self.health>=wall.types[self.type][i][1] and self.health<=wall.types[self.type][i][2]:
        self.image=pygame.image.load(wall.types[self.type][i][0])
        self.current_frame=i

  def __init__(self, pos, health, mass, type):
    self.mobile=False
    x=wall.wall_size[0]*pos[0]
    y=wall.wall_size[1]*pos[1]
    self.aforces=[]
    self.velocity=Vector([[0, 0]])
    self.pos=Vector([[x, y], [x+wall.wall_size[0], y], [x+wall.wall_size[0], y+wall.wall_size[1]], [x, y+wall.wall_size[1]]])
    self.health=health
    self.mass=mass
    self.type=type
    self.pivot=self.pos.cofmass()
    self.find_frame()
    #self.image=pygame.image.load(wall.types[type])
    self.id=physobj.id
    physobj.id+=1

  def move(self):
    pass
  
