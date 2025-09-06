#Imports modules in lines 18-19
#Class Vector declared on line 63.
#Includes operator overloading on lines 70 to 137
#dot product lines 163-165. determinant on lines 214-216.
#Polyinertia used to calculate the rotational inertia of a polygon (such as player hitbox).

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
import pygame, sys
#Solves a quadratic equation.
#I copied this from fotino.me so it would work with the collision algorithm.
def solve_quadratic(a, b, c):
  if abs(a)<=0:
    if abs(b)<=0:
      if abs(c)<=0:
        return [0] #There is no equation, so infinitely many solutions. Pick smallest one
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
#Finds the overlap between 2 intervals.
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
#Returns a boolean value IF there is an overlap between 2 intervals.
def interval(a_min, a_max, b_min, b_max):
  #a_right and a_left are the 2 posible MTV directions
  a_right=b_max-a_min
  a_left=a_max-b_min
  if a_right<0 or a_left<0:
    return False
  elif a_right<a_left:
    return 1
  else:
    return -1

class Vector():
  tick=0
  def __init__(self, list):
    self.vector = list
    #self.polygons is a dummy value.
    self.polygons=["HELLO!"]
  #Adds either an integer or another matrix to the vector.
  def __add__(self, b):
    rtype="Float"
    if isinstance(b, Vector):
      rtype="Vector"
    result = []
    for i in range(len(self.vector)):
      result.append([])
      for j in range(len(self.vector[0])):
        #If the object is an integer, it is added to the current element.
        if rtype=="Float":
          result[i].append(self.vector[i][j]+b)
        #If it's a matrix, both current elements are added.
        else:
          result[i].append(self.vector[i][j]+b.vector[0][j])
    return Vector(result)
  #Subtraction is the same as addition, but negative.      
  def __sub__(self, b):
    rtype="Float"
    if isinstance(b, Vector):
      rtype="Vector"
    result = []
    for i in range(len(self.vector)):
      result.append([])
      for j in range(len(self.vector[0])):
        if rtype=="Float":
          result[i].append(self.vector[i][j]-b)
        else:
          result[i].append(self.vector[i][j]-b.vector[0][j])
    return Vector(result)
  #Returns the number of rows in the vector.
  def __len__(self):
    return len(self.vector)
  #Returns a specific item. Example of operator overloading.
  def __getitem__(self, index):
    return self.vector[index]
  #Sets a particular element to have a certain value.
  def __setitem__(self, index, item):
    self.vector[index] = item
  #Fixes the order of operations if one of the arguaments is a number.
  def __rmul__(self, left):
    if not isinstance(left, Vector):
      return self * left
  #Multiplication function.
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
    return temp
  #Returns the matrix as a string.
  def __str__(self):
    return str(self.vector)
  #Returns a version of the vector where all elements are positive.
  def abs(self):
    for i in range(len(self.vector)):
      for j in range(len(self.vector[i])):
        abs_vector[i][j]=abs(self.vector[i][j])
    return abs_vector
  #Returns the total of all elements in that row. Useful when multiplying.
  def rowtotal(self, row):
    rowtotal = 0
    for i in range(len(self.vector)):
      rowtotal += self.vector[i][row]
      return rowtotal
  #Sum of all elements in a particular column.
  def columntotal(self, column):
    columntotal = 0
    for i in range(len(self.vector[0])):
      columntotal += self.vector[column][i]
    return columntotal
  #Calculates the vector's magnitude.
  def magnitude(self):
    total = 0
    for i in range(len(self.vector)):
      for j in range(len(self.vector[0])):
        total += self.vector[i][j]**2
    return total**0.5
  #Returns the dot product of two 2 by 2 matrices.
  def dot(self, b):
    return (self[0][0]*b[0][0])+(self[0][1]*b[0][1])
  #Creates a new matrix object  
  def gettuple(self, column):
    temp = []
    for i in range(len(self.vector[column])):
      temp.append(self.vector[column][i])
    return tuple(temp)
  #Returns the matrix in list form.
  def getlist(self):
    return self.vector
  #Returns the row as a list.
  def getrow(self, index):
    ans = []
    for i in range(len(self.vector[0])):
        ans.append(self.vector[index][i])
    return ans
  #Returns the column as a list.
  def getcolumn(self, column):
    ans = []
    for i in range(len(self.vector)):
      ans.append(self.vector[i][index])
    return ans
  #For testing purposes, draws the matrix as a polygon.
  def draw(self, pivot, colour):
    points = []
    for i in range(len(self.vector)):
      points.append((self.vector[i][0], self.vector[i][1]))
      pygame.draw.line(screen, (34,139,34), points[i], (pivot[0][0], pivot[0][1]))
    if len(points)>2:
      pygame.draw.polygon(screen, colour, points)
    pygame.draw.circle(screen, (30,144,255), pivot.gettuple(0), 5)
  #Returns a specific column as its own matrix.
  def getc(self, c):
    return Vector([self.vector[c]])
  #Allows the matrix to be multiplied by flipping its dimensions.
  def transpose(self):
    answer=[]
    for i in range(len(self.vector[0])):
      answer.append([])
      for j in range(len(self.vector)):
        answer[i].append(self[j][i])
    return Vector(answer)
  #Turns the dummy array polygons into a list of matrices.
  #This splits the matrix into other matrices representing triangles.
  def polygonate(self):
    polygons=[]
    for i in range(len(self.vector)-1):
      polygons.append(Vector([self.vector[0], self.vector[i], self.vector[i+1]]))
    return polygons
  #Returns the determinant of two 1 by 2 vectors.
  def determinant(self, b):
    return self[0][0]*b[1][0] - a[1][0]*b[0][0]
    
  def shift(self, shift):
    result=copy.deepcopy(self.vector)
    for i in range(len(result)):
      for j in range(len(result[0])):
        result[i][j]=self.vector[i][j]+shift.vector[i][0]
    return Vector(result)
  #Projects a vector onto another vector.
  def proj(self, b):
    mult=((self.transpose()*b)[0][0])/(b.magnitude()**2)*b
    return mult
  #Returns the scalar value required for a vector projection.
  def projscalar(self, b):
    #print("proj - ",self, b)
    return ((self.transpose()*b)[0][0])/(b.magnitude()**2)
  #Keeps the vector's direction, but shrinks it to magnitude 1.
  def normalise(self):
    return (1/self.magnitude())*self
  #Used to find the rotational inertia of a right-angled triangle
  def trinertia(h, w, density):
    inertia=density*((h*(w**3))/4 + ((h**3)*w)/12)
    return inertia
  #Area of a triangle with inputs height and width.
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
  #Finds the rotational inertia of a polygon.
  def polynertia(shape, mass):
    #Splits the shape into individual triangles.
    polygons=shape.polygonate()
    inertias=[]
    cm=Vector.cofmass(shape)
    #Sets up the trinertias.
    area=0
    for polygon in polygons:
      #Each polygon's initial inertia is calculated, then offset.
      v1=polygon.getc(1)-polygon.getc(0)
      v2=polygon.getc(2)-polygon.getc(0)
      p4=polygon.getc(0)+v1.proj(v2)
      h=(p4-polygon.getc(2)).magnitude()
      w1=(p4-polygon.getc(0)).magnitude()
      w2=(polygon.getc(1)-p4).magnitude()
      a1, a2=Vector.triarea(h, w1), Vector.triarea(h, w2)
      neg2=1
      if Vector.projscalar(v1, v2)>1:
        a2=a2*-1
        neg2=-1
      #The following information is added to the list 'inertias' for each triangle
      #Point of inertia, height, w1, w2, total area, negativity of second triangle
      inertias.append([p4, h, w1, w2, (a1+a2), neg2])
      area+=(a1+a2)
    inertia=0
    density=mass/area
    #Inertia = Inertia(centre of mass) + mass*distance**2
    for i in range(len(inertias)):
      tmass=inertias[i][4]*density
      p4, h, w1, w2, neg2=inertias[i][0], inertias[i][1], inertias[i][2], inertias[i][3], inertias[i][5]
      t1, t2=Vector.trinertia(h, w1, density), Vector.trinertia(h, w2, density)
      distance=(inertias[i][0]-cm).magnitude()
      inertia+=(inertias[i][0]+(tmass*distance**2))[0][0]
    return inertia
  #Converts the line between 2 points into a gradient and a y intercept.
  def getline(a, b):
    dy = b.vector[0][0] - a.vector[0][0]
    dx = b.vector[1][0] - b.vector[1][0]
    m = dy / dx
    c = b.vector[0][0] - (b.vector[1][0] * m)
    return m, c
  #Finds the angle between the vector and a second 2 by 1 vector.
  def angle(self, b):
    x1, y1 = self[0][0], self[0][1]
    x2, y2 = b[0][0], b[0][1]
    angle = degrees(atan2(x1*y2-y1*x2,x1*x2+y1*y2))
    return angle
  #The following static methods are for operations this class would need.
  #Returns the moment/torque of a force impacting a position from a centre.
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

  def line_collision(p1, p2, l1, l2, l3, l4):
    #aq, bq and cq are a, b and c in the quadratic
    aq=(l3[0][1]+l2[0][1]-l1[0][1]-l4[0][1])*(p2[0][0]+l2[0][0]-p1[0][0]-l4[0][0])
    aq=aq-((p2[0][1]+l2[0][1]-p1[0][1]-l4[0][1])*(l3[0][0]+l2[0][0]-l1[0][0]-l4[0][0]))
    bq=(l1[0][1]-l2[0][1])*(p2[0][0]+l2[0][0]-p1[0][0]-l4[0][0])
    bq+=(p1[0][0]-l2[0][0])*(l3[0][1]+l2[0][1]-l1[0][1]-l4[0][1])
    bq-=(p1[0][1]-l2[0][1])*(l3[0][0]+l2[0][0]-l1[0][0]-l4[0][0])
    bq-=(l1[0][0]-l2[0][0])*(p2[0][1]+l2[0][1]-p1[0][1]-l4[0][1])
    cq=(l1[0][1]-l2[0][1])*(p1[0][0]-l2[0][0])-(p1[0][1]-l2[0][1])*(l1[0][0]-l2[0][0])
    t1_temp=solve_quadratic(aq, bq, cq)
    point_collision="none"
    for k in range(len(t1_temp)):
      t1=t1_temp[k]
      if (t1>=0 and t1<=1):
        intersection=p1+t1*(p2-p1)
        at=l1+t1*(l3-l1)
        bt=l2+t1*(l4-l2)
        if abs(bt[0][0]-at[0][0])>0:
          t2=(intersection[0][0]-at[0][0])/(bt[0][0]-at[0][0])
        elif abs(bt[0][1]-at[0][1])>0:
          t2=(intersection[0][1]-at[0][1])/(bt[0][1]-at[0][1])
        else:
          t2="none"
        if t2!="none":
          if (t2>=0 and t2<=1):
            if point_collision=="none":
              point_collision=[intersection, [at, bt], t1]
            else:
              if t1<=point_collision[2]:
                point_collision=[intersection, [at, bt], t1]
    return point_collision

  def collision(a1, a2, b1, b2):
    l_a, l_b = len(a1), len(b1)
    final_collision="none"
    for i in range(l_a):
      p1=a1.getc(i)
      p2=a2.getc(i)
      for j in range(l_b):
        l1=b1.getc(j)
        l2=b1.getc((j+1)%l_b)
        l3=b2.getc(j)
        l4=b2.getc((j+1)%l_b)
        point_collision=p1.line_collision(p2, l1, l2, l3, l4)
        if point_collision!="none":
          if final_collision=="none":
            final_collision=[True, point_collision[0], point_collision[1], point_collision[2]]
          else:
            if point_collision[2]<final_collision[3]:
              final_collision=[True, point_collision[0], point_collision[1], point_collision[2]]
    #Intersection, both edges, time
    return final_collision
