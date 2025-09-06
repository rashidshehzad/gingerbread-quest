import pygame, sys
from pygame.locals import QUIT
import time
import copy
from math import *

#from matrix import *
#from physics import *

global width
width=10

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Hello World!')

#a=Vector([[3, -2]])
#b=Vector([[1, 7]])
#print("A's angle with b - ",a.angle(b))

class Vector():
  tick=0
  def __init__(self, list):
    self.vector = list
    self.polygons=["HELLO!"]

    #def getvector(self):
    #  return self.vector
  def __add__(self, b):
    rtype="Float"
    if isinstance(b, Vector):
      rtype="Vector"
      if len(self.vector)<len(b.vector):
        return b+self
    result = []
    for i in range(len(self.vector)):
      result.append([])
      for j in range(len(self.vector[0])):
        if rtype=="Float":
          result[i].append(self.vector[i][j]+b)
        else:
          #Why was it [0][j] for b?
          result[i].append(self.vector[i][j]+b.vector[0][j])
    return Vector(result)
      
  def __sub__(self, b):
    rtype="Float"
    if isinstance(b, Vector):
      rtype="Vector"
      if len(self.vector)<len(b.vector):
        return b+self
    result = []
    for i in range(len(self.vector)):
      result.append([])
      for j in range(len(self.vector[0])):
        if rtype=="Float":
          result[i].append(self.vector[i][j]-b)
        else:
          result[i].append(self.vector[i][j]-b.vector[0][j])
    return Vector(result)

  def __len__(self):
    return len(self.vector)
      
  def rowtotal(self, row):
    rowtotal = 0
    for i in range(len(self.vector)):
      rowtotal += self.vector[i][row]
      return rowtotal

  def columntotal(self, column):
    columntotal = 0
    for i in range(len(self.vector[0])):
      columntotal += self.vector[column][i]
    return columntotal

  def __getitem__(self, index):
    return self.vector[index]

  def __setitem__(self, index, item):
    self.vector[index] = item

  def magnitude(self):
    total = 0
    for i in range(len(self.vector)):
      for j in range(len(self.vector[0])):
        total += self.vector[i][j]**2
    return total**0.5

  def gettuple(self, column):
    temp = []
    for i in range(len(self.vector[column])):
      temp.append(self.vector[column][i])
    return tuple(temp)

  def getlist(self):
    return self.vector

  def __rmul__(self, left):
    if not isinstance(left, Vector):
      return self * left
    #else:
    #  return left*self

  def __mul__(self, right):
    if isinstance(right, Vector):
      answer=[]
      for i in range(len(right.vector)):
        answer.append([])
        for j in range(len(self.vector[0])):
          total=0
          for k in range(len(self.vector)):
            try:
              total+=self.vector[k][j]*right.vector[i][k]
            except:
              print("ERROR2!")
              print("i - ", i, "j - ", j, "k - ", k)
          answer[i].append(total)
    else:
      answer=[]
      for i in range(len(self.vector)):
        answer.append([])
        for j in range(len(self[0])):
          answer[i].append(float(self[i][j])*float(right))

    temp=Vector(answer)
    #print("M - ", temp)
    return temp

  def __str__(self):
    #print("V - ",self.vector)
    #print(self.vector)
    return str(self.vector)

  def getrow(self, index):
    ans = []
    for i in range(len(self.vector[0])):
        ans.append(self.vector[index][i])
    return ans

  def getcolumn(self, column):
    ans = []
    for i in range(len(self.vector)):
      ans.append(self.vector[i][index])
    return ans

  def draw(self, pivot, colour):
    points = []
    #print("self.pos - ", self.pos)
    for i in range(len(self.vector)):
      points.append((self.vector[i][0], self.vector[i][1]))
      pygame.draw.line(screen, (34,139,34), points[i], (pivot[0][0], pivot[0][1]))
    #print("Len of points: ", len(points))
    if len(points)>2:
      pygame.draw.polygon(screen, colour, points)
    pygame.draw.circle(screen, (30,144,255), pivot.gettuple(0), 5)

  def polygonate(self):
    polygons=[]
    for i in range(len(self.vector)-1):
      polygons.append(Vector([self.vector[0], self.vector[i], self.vector[i+1]]))
    return polygons

  def getc(self, c):
    return Vector([self.vector[c]])

  def transpose(self):
    answer=[]
    for i in range(len(self.vector[0])):
      answer.append([])
      for j in range(len(self.vector)):
        answer[i].append(self[j][i])
    return Vector(answer)


  def polygonate(self):
    polygons=[]
    for i in range(len(self.vector)-1):
      polygons.append(Vector([self.vector[0], self.vector[i], self.vector[i+1]]))
    return polygons



  def determinant(self, b):
    return self[0][0]*b[1][0] - a[1][0]*b[0][0]

  def det(self, b):
    return (self[0]*b[1])-(b[0]*self[1])
    
  def shift(self, shift):
    result=copy.deepcopy(self.vector)
    for i in range(len(result)):
      for j in range(len(result[0])):
        result[i][j]=self.vector[i][j]+shift.vector[i][0]
    return Vector(result)

  def proj(self, b):
    mult=((self.transpose()*b)[0][0])/(b.magnitude()**2)*b
    return mult

  def projscalar(self, b):
    #print("proj - ",self, b)
    return ((self.transpose()*b)[0][0])/(b.magnitude()**2)

  def normalise(self):
    return (1/self.magnitude())*self
    

  #Used to find the rotational inertia of a right-angled triangle
  def trinertia(h, w, density):
    inertia=density*((h*(w**3))/4 + ((h**3)*w)/12)
    return inertia

  def triarea(h, w):
    area=h*w/2
    return area
  #The centre of a triangle is the sum of its points divided by 3.
  def cofmass(self):
    total=Vector([[0, 0]])
    for i in range(len(self.vector)):
      total=total+self.getc(i)
    cm=(1/len(self.vector))*total
    return cm
  def polynertia(shape, mass):
    polygons=shape.polygonate()
    inertias=[]
    cm=Vector.cofmass(shape)
    #Sets up the trinertias.
    area=0
    for polygon in polygons:
      v1=polygon.getc(1)-polygon.getc(0)
      v2=polygon.getc(2)-polygon.getc(0)
      p4=polygon.getc(0)+v1.proj(v2)
      h=(p4-polygon.getc(2)).magnitude()
      w1=(p4-polygon.getc(0)).magnitude()
      w2=(polygon.getc(1)-p4).magnitude()
      #t1, t2=trinertia(h, w1, d), trinertia(h, w2, d)
      a1, a2=Vector.triarea(h, w1), Vector.triarea(h, w2)
      neg2=1
      if Vector.projscalar(v1, v2)>1:
        #t2=t2*-1
        a2=a2*-1
        neg2=-1
      #Inertia, point of inertia, triangle's area, centre of mass of triangle
      #cm=(1/3)*(polygon.getc(0)+polygon.getc(1)+polygon.getc(2))

      #Point of inertia, height, w1, w2, total area, negativity of second triangle
      inertias.append([p4, h, w1, w2, (a1+a2), neg2])
      area+=(a1+a2)
    inertia=0
    density=mass/area
    #I = I(cm) + md^2

    for i in range(len(inertias)):
      tmass=inertias[i][4]*density
      p4, h, w1, w2, neg2=inertias[i][0], inertias[i][1], inertias[i][2], inertias[i][3], inertias[i][5]
      t1, t2=Vector.trinertia(h, w1, density), Vector.trinertia(h, w2, density)
      distance=(inertias[i][0]-cm).magnitude()
      #distance=(inertias[i][1]-polygons[0][0])/magnitude()
      inertia+=(inertias[i][0]+(tmass*distance**2))[0][0]
    return inertia

  def getline(a, b):
    dy = b.vector[0][0] - a.vector[0][0]
    dx = b.vector[1][0] - b.vector[1][0]
    m = dy / dx
    c = b.vector[0][0] - (b.vector[1][0] * m)
    return m, c


  #This one works, but can't tell if it's negative.
  #def angle(self, b):
  #  top=(self.transpose()*b)[0][0]
  #  #print("top - ",top)
  #  bottom=self.magnitude()*b.magnitude()
  #  angle=degrees(acos(top/bottom))
  #  if Vector.tick%3==0:
  #    print(angle)
  #  Vector.tick+=1
  #  return angle

  def angle(self, b):
    x1, y1 = self[0][0], self[0][1]
    x2, y2 = b[0][0], b[0][1]
    angle = degrees(atan2(x1*y2-y1*x2,x1*x2+y1*y2))
    if Vector.tick%5==0:
      print(angle)
    Vector.tick+=1
    return angle

  @staticmethod
  def torque(force, centre, contact):
    arm_length=(contact-centre)
    d=arm_length.magnitude()
    angle=arm_length.angle(force)
    return sin(radians(angle))*d*force.magnitude()

  @staticmethod
  def torque_angular_acceleration(torque, rotational_inertia):
    return torque/rotational_inertia

  @staticmethod
  def calculate_polynertia_rotational_acceleration(shape, mass, force, contact):
    centre_of_mass=Vector.cofmass(shape)
    rotational_inertia=shape.polynertia(mass)
    torque=Vector.torque(force, centre_of_mass, contact)
    return torque/rotational_inertia

  @staticmethod
  def calculate_rotational_acceleration(shape, rotational_inertia, mass, force, contact):
    centre_of_mass=Vector.cofmass(shape)
    torque=Vector.torque(force, centre_of_mass, contact)
    return torque/rotational_inertia

  def find_min_max_projscalars(self, p):
    min_max_self=[[self[0].projscalar(p), 0], [self[1].projscalar(p), 1]]
    for j in range(2, l_self):
      scalar=self[j].projscalar(p)
      if scalar<min_max_self[0][0]:
        min_max_self[0]=[scalar, i]
      if scalar>min_max_self[1][0]:
        min_max_self[1]=[scalar, i]
    return min_max_self

  def find_min_max_projections(self, p):
    min_max_self=[[self[0].projscalar(p), 0], [self[1].projscalar(p), 1]]
    #centre=self.cofmass()
    for j in range(2, l_self):
      scalar=(self[j]).projscalar(p)
      if scalar<min_max_self[0][0]:
        min_max_self[0]=[scalar, i]
      if scalar>min_max_self[1][0]:
        min_max_self[1]=[scalar, i]
    #Returns the projected vectors instead of their scalars.
    #[[projected vector, index in list, projscalar]]
    min_max_self=[[min_max_self[0][0]*self[min_max_self[0][1]], min_max_self[0][1], min_max_self[0][0]], [min_max_self[1][0]*self[min_max_self[1][1]], min_max_self[1][1], min_max_self[1][0]]]
    return min_max_self

  def draw(self, colour):
    pivot=self.cofmass()
    points = []
    for i in range(len(self.vector)):
      points.append((self.vector[i][0], self.vector[i][1]))
      pygame.draw.line(screen, (34,139,34), points[i], (pivot[0][0], pivot[0][1]), )
    if len(points)>2:
      pygame.draw.polygon(screen, colour, points)
    pygame.draw.circle(screen, (30,144,255), pivot.gettuple(0), 5)
  
  #Takes 2 matrices, designed for 2 physobj/char's positions.
  def collision(self, b):
    l_self, l_b=len(self), len(b)
    collision=True
    for i in range(l_self):
      side_self=[self.getc((i)%l_self), self.getc((i+1)%l_self)]
      gap=side_self[1]-side_self[0]
      #print("Gap - ",gap)
      normal=Vector([[-gap[0][1], gap[0][0]]])
      p=20*normal
      #print("p - ",p)
      #Projscalar is the scalar needed to turn b into self.
      #biggest = [projscalar, index]
      biggest=[self.getc(0).projscalar(p), 0]
      for j in range(l_self):
        if self.getc(j).projscalar(p)>biggest[0]:
          biggest=[self.getc(j).projscalar(p), j]
      smallest=[b.getc(0).projscalar(p), 0]
      for j in range(l_b):
        if b.getc(j).projscalar(p)<smallest[0]:
          smallest=[b.getc(j).projscalar(p), j]
      gap=smallest[0]-biggest[0]
      screen.fill((0,0,1))
      self.draw((34,139,34))
      b.draw((34,139,34))
      pygame.draw.line(screen, (178, 102, 255), (0, 0), p.gettuple(0), 3)
      pygame.draw.line(screen, (178, 102, 255), (biggest[0]*p).gettuple(0), self.gettuple(biggest[1]), 3)
      pygame.draw.line(screen, (178, 102, 255), (smallest[0]*p).gettuple(0), b.gettuple(smallest[1]), 3)
      pygame.display.update()
      time.sleep(5)
      if gap>0:
        collision=False
      try:
        if gap<smallest_gap[0] and abs(gap)<abs(smallest_gap[0]):
          #gap's value, index of max point of self, index of min point of b
          smallest_gap=[gap, biggest[1], smallest[1]]
      except:
        smallest_gap=[gap, biggest[1], smallest[1]]
    if collision:
      return [True, smallest_gap]
    else:
      return [False]

b=Vector([[10, 10], [40, 10], [40, 40], [10, 40]])
a=Vector([[50, 50], [81, 19], [81, 50]])
print(a.collision(b))
