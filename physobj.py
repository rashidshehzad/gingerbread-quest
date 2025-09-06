#Modules imported on lines 8 to 11, including my own matrix module.
#Class item declared on line 48
#Class Physobj declared on line 101
#Class bigwall inherits from Physobj on line 244


global file_root
#This subroutine finds the current file's path, to access files in its location.
def find_file_root():
    temp=__file__
    temp=temp.split("\\")
    file_root=""
    for i in range(len(temp)-1):
        file_root+=temp[i]+"/"
    return file_root
file_root=find_file_root()
from math import *
from sys import _current_frames
from matrix import *
#Angvector creates a rotation matrix which corresponds to that angle.
def angvector(angle):
  return Vector([[cos(radians(angle)), sin(radians(angle))], [-sin(radians(angle)), cos(radians(angle))]])
#Checks if the player's velocity matches the conditions for the frame set.
def check_bounds(list, vel):
  conditions=[False, False, False, False]
  try:
    if (vel[0][0]>list[0]):
      conditions[0]=True
  except:
    conditions[0]=True
  try:
    if (vel[0][0]<list[1]):
      conditions[1]=True
  except:
    conditions[1]=True
  try:
    if (vel[0][1]>list[2]):
      conditions[2]=True
  except:
    conditions[2]=True
  try:
    if (vel[0][1]<list[3]):
      conditions[3]=True
  except:
    conditions[3]=True
  within_bounds=conditions[0] and conditions[1] and conditions[2] and conditions[3]
  return within_bounds
#Checks if a single integer is within a range.
def check_state(list, state):
  within_bounds=True
  try:
    if not (state>list[0] and state<list[1]):
      within_bounds=False
  except:
    pass
  return within_bounds
#Performs a check to see what image set a physobj should use.
#Calls check_state or check_bounds depending on if it's the player or a tile.
def check_frame(list, state):
  if len(list)==5:
    return check_bounds(list, state)
  elif len(list)==2:
    return check_state(list, state)
  elif len(list)==1:
    return True

#Item class stores a hitbox, image_sets, etc.
class item():
  #Each item object has a unique ID to avoid selecting the wrong item.
  #This is done by using a static variable to give the id values.
  #It increments each time a new object is instantiated.
  id=1
  #Image sets stores the frames of each item type.
  #An image set with more than frame alternates during run_time to animate.
  image_sets=[
    [5, ["BreadB.png", "Bread SpecialB.png"], [54, 34]],
    [1, ["Life4.png"], [27, 27]],
    [5, ["Bread.png", "Bread Special.png"], [27, 17]],
    [1, ["YOU WIN2.png"], [364, 296]]
  ]
  #Generates a rectangular matrix hitbox
  def create_hitbox(self, pos, width, height):
    x, y = pos[0][0], pos[0][1]
    self.hitbox=Vector([[x, y], [x+width, y], [x+width, y+height], [x, y+height]])
  def __init__(self, pos, type):
    self.pos=pos
    #Offset is used to move the image if it doesn't match the hitbox.
    self.offset=Vector([[0, 0]])
    self.type=type
    self.id=["Collectible", self.type, item.id]
    item.id+=1
    #draw_hitbox is only used for testing. mobile allows the object to move, which items cannot do.
    self.draw_hitbox=False
    self.mobile=False
    #collision_response decides if the object will be cause a response in a collided object.
    #Since items can be passed through, this s false.
    self.collision_response=False
    self.image_counter=0
    #Stores the current image.
    self.image=pygame.image.load(file_root+"images/"+str(item.image_sets[self.type][1][self.image_counter]))
    #How long the character stays on each frame.
    self.frame_duration=item.image_sets[self.type][0]
    dimensions=item.image_sets[self.type][2]
    #Creates a rectangular hitbox for itself
    self.create_hitbox(self.pos, dimensions[0], dimensions[1])
  def gethitbox(self):
    return self.hitbox
  def find_range(self):
        smallest_x="none"
        biggest_x="none"
        smallest_y="none"
        biggest_y="none"
        for i in range(len(self.pos)):
          if smallest_x=="none":
              smallest_x=self.pos[i][0]
          elif self.pos[i][0]<smallest_x:
              smallest_x=self.pos[i][0]
          if biggest_x=="none":
              biggest_x=self.pos[i][0]
          elif self.pos[i][0]>biggest_x:
              biggest_x=self.pos[i][0]
          if smallest_y=="none":
              smallest_y=self.pos[i][1]
          elif smallest_y<self.pos[i][1]:
              smallest_y=self.pos[i][1]
          if biggest_y=="none":
              biggest_y=self.pos[i][1]
          elif biggest_y>self.pos[i][1]:
              biggesty_y=self.pos[i][1]
        return smallest_x, biggest_x, smallest_y, biggest_y

#Physobj includes frame data, bounciness and friction, mass, hitbox, and other physics data.
class physobj():
  id=1
  #Frame data is stored in the following format:
  #[[minx, maxx, miny, maxy], [frames] OR
  #[[minx, maxx], [tileset]
  image_sets=[[[[2], ["Gingerbread man idle.png"]],
               [["any", -0.1, "any", "any", 2], ["Gingerbread man running left1.png", "Gingerbread man running left2.png", "Gingerbread man running left3.png"]],
               [[0.1, "any", "any", "any", 2], ["Gingerbread man running1.png", "Gingerbread man running2.png", "Gingerbread man running3.png"]]
               ],
              [[["any", "any"], [["Rock reflect.png", "Rock triangle left.png", "Rock triangle right.png"]]]],
              [[["any", "any"], [["Ice Cube.png", "Ice cube triangle left.png", "Ice cube triangle right.png"]]]],
              [[["any", "any"], ["House roof2.png"]]],
              [[["any", "any"], ["House bottom2.png"]]],
              [[["any", "any"], ["Bakery top.png"]]],
              [[["any", "any"], ["Bakery bottom.png"]]],
              [[["any", "any"], ["Candy cane.png"]]],
              [[["any", "any"], [["Alien jelly.png", "Alien jelly.png", "Alien jelly.png"]]]],
              [[["any", "any"], [["Lava cube.png", "Lava cube triangle left.png", "Lava cube triangle right.png"]]]],
             ]
  def __init__(self, hitbox, mass, image_set):
    self.pos=hitbox
    self.collision_response=True
    self.bounciness=1
    self.offset=Vector([[0, 0]])
    self.friction=1
    if image_set>=0:
      self.images=physobj.image_sets[image_set]
      self.has_image=True
      self.draw_hitbox=False
      self.current_frame=[0, 0]
    else:
      self.has_image=False
      self.draw_hitbox=True
    self.inventory=[]
    self.mobile=True
    self.pivot=self.pos.cofmass()
    self.polygons=self.pos.polygonate()
    self.mass=mass
    self.health=self.mass
    self.velocity=Vector([[0, 0]])
    self.acceleration=Vector([[0, 0]])
    self.rotation=0
    self.rotational_acceleration=0
    self.rotational_inertia=Vector.polynertia(self.pos, self.mass)
    self.aforces=[]
    self.id=["p", physobj.id]
    self.colour=(150, 150, 150)
    physobj.id+=1
  def gethitbox(self):
    return self.pos
  def translation(self, vector):
    self.pos+=vector
    self.pivot=self.pos.cofmass()
  def calc_aforces(self):
    #aforces = [[force, contact, id], ...]
    self.acceleration=Vector([[0, 0]])
    self.rotational_acceleration=0
    for i in range(len(self.aforces)):
      if (self.aforces[i][2][0]==self.id[0] and self.aforces[i][2][1]==self.id[1]) or self.aforces[i][2][0]=="c":
        self.aforces[i][1]=self.pivot
      self.acceleration+=(1/self.mass)*self.aforces[i][0]
      self.rotational_acceleration+=Vector.calculate_rotational_acceleration(self.pos, self.rotational_inertia, self.mass, self.aforces[i][0], self.aforces[i][1])
    self.rotation+=self.rotational_acceleration
    self.velocity+=1*self.acceleration
  def find_force(self, id):
    pos="none"
    for i in range(len(self.aforces)):
      if self.aforces[i][2]==id:
        pos=i
        break
    return pos
  def add_force(self, force, contact, id):
    pos=self.find_force(id)
    if pos=="none":
      self.aforces.append([force, contact, id])
    else:
      self.aforces[pos]=[force, contact, id]
  def remove_force(self, id):
    pos=self.find_force(id)
    if pos!="none":
      self.aforces.pop(pos)
  def find_range(self):
      smallest_x="none"
      biggest_x="none"
      smallest_y="none"
      biggest_y="none"
      for i in range(len(self.pos)):
          if smallest_x=="none":
              smallest_x=self.pos[i][0]
          elif self.pos[i][0]<smallest_x:
              smallest_x=self.pos[i][0]
          if biggest_x=="none":
              biggest_x=self.pos[i][0]
          elif self.pos[i][0]>biggest_x:
              biggest_x=self.pos[i][0]
          if smallest_y=="none":
              smallest_y=self.pos[i][1]
          elif smallest_y<self.pos[i][1]:
              smallest_y=self.pos[i][1]
          if biggest_y=="none":
              biggest_y=self.pos[i][1]
          elif biggest_y>self.pos[i][1]:
              biggesty_y=self.pos[i][1]
      return smallest_x, biggest_x, smallest_y, biggest_y
  def move(self):
    if self.mobile:
      self.pos+=self.velocity
      self.pivot = self.pos.cofmass()
      self.aforces=[]
  def set_frames(self, limits, frames):
    self.limits=limits
    self.frames=frames
  def find_frame(self):
    self.calc_aforces()
    current_frame=self.current_frame[0]
    within_bounds=check_frame(self.images[current_frame][0], self.velocity)
    if within_bounds:
      if self.current_frame[1]<len(self.images[current_frame][1])-1:
        self.current_frame[1]+=1
      else:
        self.current_frame[1]=0
    if len(self.images[current_frame][0])==1 or within_bounds==False:
      for i in range(len(self.images)):
        if i!=current_frame:
          within_bounds=check_frame(self.images[i][0], self.velocity)
          if within_bounds:
            self.current_frame=[i, 0]
    if type(self.images[self.current_frame[0]][1][self.current_frame[1]])!=list:
      self.image=pygame.image.load(file_root+"images/"+str(self.images[self.current_frame[0]][1][self.current_frame[1]]))
    else:
      self.image=[]
      for i in range(len(self.images[self.current_frame[0]][1][self.current_frame[1]])):
        self.image.append(pygame.image.load(file_root+"images/"+str(self.images[self.current_frame[0]][1][self.current_frame[1]][i])))
  def translation(self, amount):
    self.pos+=amount
    self.pivot=self.pos.cofmass()
  def rotate(self, amount):
    self.pos=angvector(amount)*self.pos

#Bigwall inherits from physobj to avoid creating multiple walls where only one is needed.
class bigwall(physobj):
  def __init__(self, hitbox, mass, image_set, length, height):
    self.pos=hitbox
    if image_set>=0:
      self.images=physobj.image_sets[image_set]
      self.has_image=True
      self.draw_hitbox=False
      self.current_frame=[0, 0]
    else:
      self.has_image=False
      self.draw_hitbox=True
    self.bounciness=0.5
    self.friction=0.95
    self.mobile=True
    self.collision_response=True
    self.pivot=self.pos.cofmass()
    self.polygons=self.pos.polygonate()
    self.mass=mass
    self.health=self.mass
    self.velocity=Vector([[0, 0]])
    self.acceleration=Vector([[0, 0]])
    self.rotation=0
    self.rotational_acceleration=0
    self.rotational_inertia=Vector.polynertia(self.pos, self.mass)
    self.aforces=[]
    self.id=["wall", physobj.id]
    self.offset=Vector([[0, 0]])
    self.colour=(150, 150, 150)
    physobj.id+=1
    self.length=length
    self.height=height
    def gethitbox(self):
        return self.pos
