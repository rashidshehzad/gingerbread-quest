from math import *
import pygame, sys

def neg_pos_square(x):
  if x<0:
    return (x**2)*-1
  else:
    return (x**2)

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

  def dot(self, b):
    return (self[0][0]*b[0][0])+(self[0][1]*b[0][1])
  
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
  def cofmass(shape):
    total=Vector([[0, 0]])
    for i in range(len(shape.vector)):
      total=total+shape.getc(i)
    cm=(1/len(shape.vector))*total
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
  
  #Takes 2 matrices, designed for 2 physobj/char's positions.
  def collision(self, b):
    l_self, l_b=len(self), len(b)
    collision=True
    smallest_self, biggest_self, smallest_b, biggest_b=[], [], [], []
    #gap stores gaps between edges to find the shortest one
    gap=[]
    for i in range(l_self+l_b):
      #Creates the normal
      if i<l_self:
        side=self.getc((i+1)%l_self)-self.getc((i)%l_self)
        p=Vector([[-side[0][1], side[0][0]]])
      else:
        side=b.getc((i+1-l_self)%l_b)-b.getc((i-l_self)%l_b)
        p=Vector([[-side[0][1], side[0][0]]])
      #Checks for smallest and biggest in self
      smallest_self.append([self.getc(0).projscalar(p), 0])
      biggest_self.append([self.getc(0).projscalar(p), 0])
      for j in range(l_self):
        proj_scalar=self.getc(j).projscalar(p)
        if proj_scalar<smallest_self[i][0]:
          smallest_self[i]=[proj_scalar, j]
        if proj_scalar>biggest_self[i][0]:
          biggest_self[i]=[proj_scalar, j]
      smallest_b.append([b.getc(0).projscalar(p), 0])
      biggest_b.append([b.getc(0).projscalar(p), 0])
      for j in range(l_b):
        proj_scalar=b.getc(j).projscalar(p)
        if proj_scalar<smallest_b[i][0]:
          smallest_b[i]=[proj_scalar, j]
        if proj_scalar>biggest_b[i][0]:
          biggest_b[i]=[proj_scalar, j]

      #smallest[i][0]>biggext_b[i][0] or biggest_self[i][0]<smallest_b[i][0]
      if biggest_b[i][0]<smallest_self[i][0] or smallest_b[i][0]>biggest_self[i][0]:
        collision=False
      else:
        gap.append([biggest_b[i][0]-smallest_self[i][0], smallest_self[i][1], biggest_b[i][1]])

    #Finds the smallest gap
    for i in range(len(gap)):
      try:
        if gap[i][0]<smallest[i][0]:
          smallest=gap[i]
      except:
        smallest=gap[0]

    if collision:
      return [collision, smallest[0], smallest[1], smallest[2]]
    else:
      return [collision]
