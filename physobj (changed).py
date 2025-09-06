from math import *
from sys import _current_frames
from matrix import *

def angvector(angle):
  return Vector([[cos(radians(angle)), sin(radians(angle))], [-sin(radians(angle)), cos(radians(angle))]])
def check_bounds(list, vel):
  #within_bounds is true unless proved otherwise
  within_bounds=True
  try:
    if (vel[0][0]<list[0][0]):
      within_bounds=False
  except:
    pass
  try:
    if (vel[0][0]>list[0][1]):
      within_bounds=False
  except:
    pass
  try:
    if (vel[0][1]<list[1][0]):
      within_bounds=False
  except:
    pass
  try:
    if (vel[0][1]>list[1][1]):
      within_bounds=False
  except:
    pass
  return within_bounds
def check_state(list, state):
  within_bounds=True
  try:
    if not (state>list[0] and state<list[1]):
      within_bounds=False
  except:
    pass
  return within_bounds

class item():
  image_sets=[
    [5, ["BreadB.png", "Bread SpecialB.png"], [54, 34]],
    [1, ["Life4.png"], [27, 27]],
    [5, ["Bread.png", "Bread Special.png"], [27, 17]],
    [1, ["Finish flag.png"], [364, 296]]
  ]
  def create_hitbox(self, pos, width, height):
    x, y = pos[0][0], pos[0][1]
    self.hitbox=Vector([[x, y], [x+width, y], [x+width, y+height], [x, y+height]])
  def __init__(self, pos, type):
    self.pos=pos
    self.offset=Vector([[0, 0]])
    self.type=type
    self.id=["Collectible", self.type]
    if self.type==3:
      self.draw_hitbox=True
    else:
      self.draw_hitbox=False
    self.mobile=False
    self.collision_response=False
    self.image_counter=0
    self.image=pygame.image.load("images/"+str(item.image_sets[self.type][1][self.image_counter]))
    self.frame_duration=item.image_sets[self.type][0]
    dimensions=item.image_sets[self.type][2]
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

class physobj():
  id=1
  #[[minx, maxx, miny, maxy], [frames] OR
  #[[minx, maxx, miny, maxy], [tileset]
  #For gingerbread man [left, right, up, down], [frames]
  #"none" for False, True for True, "any" for either option.
  image_sets=[[[["none", True, "any", "any"], ["Gingerbread man running1.png", "Gingerbread man running2.png", "Gingerbread man running3.png"]],
               [["any", "any", "any", "any"], ["Gingerbread man idle.png"]]],
              [[["any", "any"], [["Rock reflect.png", "Rock triangle left.png", "Rock triangle right.png"]]]],
              [[["any", "any"], [["Ice Cube.png", "Ice cube triangle left.png", "Ice cube triangle right.png"]]]],
              [[["any", "any"], ["House roof2.png"]]],
              [[["any", "any"], ["House bottom2.png"]]],
              [[["any", "any"], ["Bakery top.png"]]],
              [[["any", "any"], ["Bakery bottom.png"]]],
              [[["any", "any"], ["Candy cane.png"]]],
              [[["any", "any"], [["Alien jelly.png", "Alien jelly.png", "Alien jelly.png"]]]]
             ]
  def __init__(self, hitbox, mass, image_set):
    self.pos=hitbox
    self.collision_response=True
    self.bounciness=1
    self.offset=Vector([[0, 0]])
    self.friction=1
    if image_set>=0:
      #self.limits=physobj.image_sets[image_set][0]
      #self.frames=physobj.image_sets[image_set][1]
      self.images=physobj.image_sets[image_set]
      self.has_image=True
      self.draw_hitbox=True
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
    #if self.id[1]==1:
      #print(self.acceleration)
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
      #self.calc_aforces()
      #self.velocity+=self.acceleration
      #self.rotation+=self.rotational_acceleration
      self.pos+=self.velocity
      #self.pos=(angvector(self.rotation)*(self.pos-self.pivot))+self.pivot
      self.pivot = self.pos.cofmass()
      self.aforces=[]
  def set_frames(self, limits, frames):
    self.limits=limits
    self.frames=frames
  def find_frame(self):
    self.calc_aforces()
    for i in range(len(self.images)):
      #If there are 4 conditions (over 2), it must be a player.
      if len(self.images[i][0])>2:
        current_frame_matches=True
        #Left
        current_condition=self.images[i][0][0]
        if current_condition=="any":
          #If any value is accepted, it's valid.
          pass
        else:
          if self.find_force("c_left")=="none":
            if current_condition=="none":
              #If not found, and none expected, it's valid.
              pass
            else:
              #If none found, yet one expected, not valid.
              current_frame_matches=False
          else:
            #If one expected, and one found, it's valid.
            if current_condition==True:
              pass
            else:
              #If one expected, and none found, not valid.
              current_frame_matches=False
        #Right
        current_condition=self.images[i][0][1]
        if current_condition=="any":
          #If any value is accepted, it's valid.
          pass
        else:
          if self.find_force("c_right")=="none":
            if current_condition=="none":
              #If not found, and none expected, it's valid.
              pass
            else:
              #If none found, yet one expected, not valid.
              current_frame_matches=False
          else:
            #If one expected, and one found, it's valid.
            if current_condition==True:
              pass
            else:
              #If one expected, and none found, not valid.
              current_frame_matches=False
        #Up
        current_condition=self.images[i][0][2]
        if current_condition=="any":
          #If any value is accepted, it's valid.
          pass
        else:
          if self.find_force("c_up")=="none":
            if current_condition=="none":
              #If not found, and none expected, it's valid.
              pass
            else:
              #If none found, yet one expected, not valid.
              current_frame_matches=False
          else:
            #If one expected, and one found, it's valid.
            if current_condition==True:
              pass
            else:
              #If one expected, and none found, not valid.
              current_frame_matches=False
        #Down
        current_condition=self.images[i][0][3]
        if current_condition=="any":
          #If any value is accepted, it's valid.
          pass
        else:
          if self.find_force("c_down")=="none":
            if current_condition=="none":
              #If not found, and none expected, it's valid.
              pass
            else:
              #If none found, yet one expected, not valid.
              current_frame_matches=False
          else:
            #If one expected, and one found, it's valid.
            if current_condition==True:
              pass
            else:
              #If one expected, and none found, not valid.
              current_frame_matches=False
        #within_bounds=check_bounds(self.images[i][0], self.velocity)
      else:
        within_bounds=check_state(self.images[i][0], self.velocity)
      if within_bounds:
        if self.current_frame[0]==i:
          if self.current_frame[1]<len(self.images[i][1])-1:
            self.current_frame[1]+=1
          else:
            self.current_frame[1]=0
        else:
          self.current_frame=[i, 0]
    if type(self.images[self.current_frame[0]][1][self.current_frame[1]])!=list:
      self.image=pygame.image.load("images/"+str(self.images[self.current_frame[0]][1][self.current_frame[1]]))
    else:
      self.image=[]
      for i in range(len(self.images[self.current_frame[0]][1][self.current_frame[1]])):
        self.image.append(pygame.image.load("images/"+str(self.images[self.current_frame[0]][1][self.current_frame[1]][i])))
  def translation(self, amount):
    self.pos+=amount
    self.pivot=self.pos.cofmass()
  def rotate(self, amount):
    self.pos=angvector(amount)*self.pos

class player(physobj):
  def __init__(self, hitbox, mass, image_set):
    self.pos=hitbox
    self.collision_response=True
    self.bounciness=1
    self.offset=Vector([[0, 0]])
    self.friction=1
    if image_set>=0:
      #self.limits=physobj.image_sets[image_set][0]
      #self.frames=physobj.image_sets[image_set][1]
      self.images=physobj.image_sets[image_set]
      self.has_image=True
      self.draw_hitbox=True
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

class bigwall(physobj):
  def __init__(self, hitbox, mass, image_set, length, height):
    self.pos=hitbox
    if image_set>=0:
      #self.limits=physobj.image_sets[image_set][0]
      #self.frames=physobj.image_sets[image_set][1]
      self.images=physobj.image_sets[image_set]
      self.has_image=True
      self.draw_hitbox=True
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
