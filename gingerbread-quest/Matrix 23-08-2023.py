from math import *
import pygame, sys

def neg_pos_square(x):
  if x<0:
    return (x**2)*-1
  else:
    return (x**2)

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
    #if Vector.tick%5==0:
    #  print(angle)
    #Vector.tick+=1
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
  
  

  #Indices of the minimum and maximum points onto an axis.
  #And the steps say in which direction the "forward hull" is.
  def find_hull(self, p):
    smallest_self, biggest_self = [self.getc(0).projscalar(p), 0], [self.getc(0).projscalar(p), 0]
    l_self=len(self)
    for i in range(l_self):
      proj_scalar=self.getc(i).projscalar(p)
      if proj_scalar<smallest_self[0]:
        smallest_self=[proj_scalar, i]
      if proj_scalar>biggest_self[0]:
        biggest_self=[proj_scalar, i]
    normal=Vector([[-p[0][1], p[0][0]]])
    left=self.getc((smallest_self[1]-1)%l_self)
    right=self.getc((smallest_self[1]+1)%l_self)
    if (right-right.proj(p)).projscalar(normal)>=(left-left.proj(p)).projscalar(normal):
      step=1
    else:
      step=-1
    return smallest_self[1], biggest_self[1], step
        
  def collision(a, b, vel):
    ovel=vel
    #Creates the normal
    if vel.magnitude()>0:
      p=Vector([[-vel[0][1], vel[0][0]]])
    else:
      return [False, Vector([[0, 0]])]

    l_a, l_b = len(a), len(b)
    proj=a.getc(0).projscalar(p)
    smallest_a=[proj, 0]
    biggest_a=[proj, 0]
    for i in range(l_a):
      proj=a.getc(i).projscalar(p)
      if proj<smallest_a[0]:
        smallest_a=[proj, i]
      if proj>biggest_a[0]:
        biggest_a=[proj, i]
    proj=b.getc(0).projscalar(p)
    smallest_b=[proj, 0]
    biggest_b=[proj, 0]
    for i in range(l_b):
      proj=b.getc(i).projscalar(p)
      if proj<smallest_b[0]:
        smallest_b=[proj, i]
      if proj>biggest_b[0]:
        biggest_b=[proj, i]
    left_gap_a = a.getc((smallest_a[1]-1)%l_a)-(a.getc((smallest_a[1]-1)%l_a).proj(p))
    right_gap_a = a.getc((smallest_a[1]+1)%l_a)-(a.getc((smallest_a[1]+1)%l_a).proj(p))
    if right_gap_a.projscalar(vel)>left_gap_a.projscalar(vel):
      step_a=1
    else:
      step_a=-1
    left_gap_b = b.getc((smallest_a[1]-1)%l_b)-(b.getc((smallest_b[1]-1)%l_b).proj(p))
    right_gap_b = b.getc((smallest_a[1]+1)%l_b)-(b.getc((smallest_b[1]+1)%l_b).proj(p))
    if right_gap_b.projscalar(vel)>left_gap_b.projscalar(vel):
      step_b=1
    else:
      step_b=-1

    #ca, cb are currenta, currentb
    ca=smallest_a[1]
    cb=smallest_b[1]
    valid_gaps=0
    while (ca<biggest_a[1]) and (cb<biggest_b[1]):
      ca_proj=a.getc(ca%l_a).projscalar(vel)
      cb_proj=b.getc(cb%l_b).projscalar(vel)
      if ca_proj<cb_proj:
        if cb_proj<a.getc((ca+step_a)%l_a).projscalar(vel):
          check=True
          a1, a2 = a.getc(ca%l_a), a.getc((ca+step_a)%l_a)
          b2 = b.getc(cb%l_b)
          b1 = b2-vel
          source="b"
        else:
          check=False
          source="b"
          ca+=1
      elif cb_proj<ca_proj:
        if ca_proj<b.getc((cb+step_b)%l_b).projscalar(vel):
          check=True
          a1 = a.getc(ca%l_a)
          a2 = a1+vel
          b1, b2 = b.getc(cb%l_b), b.getc((cb+step_b)%l_b)
          source="a"
        else:
          check=False
          source="a"
          cb+=1

      if check:
        try:
          ma=(a2[0][1]-a1[0][1])/(a2[0][0]-a1[0][0])
        except:
          ma="error"
        try:
          mb=(b2[0][1]-b1[0][1])/(b2[0][0]-b1[0][0])
        except:
          mb="error"
        try:
          mp=(pl[0][1])/(p[0][0])
        except:
          mp="error"
        if ma=="error" and mb=="error":
          if a1[0][0]==b1[0][0]:
            if source=="a":
              if vel[0][1]>0:
                if b1[0][1]<b2[0][1]:
                  intersection=b1
                  gap=[intersection-a1, intersection]
                  valid_gap=True
                else:
                  intersection=b2
                  gap=[intersection-a1, intersection]
                  valid_gap=True
              elif vel[0][1]<0:
                if b1[0][1]>b2[0][1]:
                  intersection=b1
                  gap=[intersection-a1, intersection]
                  valid_gap=True
                else:
                  intersection=b2
                  gap=[intersection-a1, intersection]
                  valid_gap=True
              else:
                valid_gap=False
            elif source=="b":
              if vel[0][1]>0:
                if a1[0][1]<a2[0][1]:
                  intersection=a1
                  gap=[b2-intersection, intersection]
                  valid_gap=True
                else:
                  intersection=a2
                  gap=[b2-intersection, intersection]
                  valid_gap=True
              elif vel[0][1]<0:
                if b1[0][1]>b2[0][1]:
                  intersection=a1
                  gap=[b2-intersection, intersection]
                  valid_gap=True
                else:
                  intersection=a2
                  gap=[b2-intersection, intersection]
                  valid_gap=True
              else:
                valid_gap=False
              #if (b1-a1).projscalar(vel)<(b2-a1).projscalar(vel):
              #  gap=[b1-a1, b1]
              #else:
              #  gap=[b2-a1, b2]
            #elif source=="b":
            #  if (b1-a2).projscalar(vel)<(b1-a1).projscalar(vel):
            #    gap=[b1-a2, a2]
            #  else:
            #    gap=[b1-a1, a1]
          else:
            valid_gap=False
        elif ma=="error":
          valid_gap=True
          x=a1[0][0]
          y=mb*x + b1[0][1] - mb*b1[0][0]
          intersection=Vector([[x, y]])
          if source=="a":
            gap=[intersection-a1, intersection]
          elif source=="b":
            gap=[b1-intersection, intersection]
        elif mb=="error":
          valid_gap=True
          x=b1[0][0]
          y=ma*x + a1[0][1] - ma*a1[0][0]
          intersection=Vector([[x, y]])
          if source=="a":
            gap=[intersection-a1, intersection]
          elif source=="b":
            gap=[b2-intersection, intersection]
        elif ma-mb==0:
          #Parallel, so will never meet.
          valid_gap=False
        else:
          x=(b1[0][1] + ma*a1[0][0] - a1[0][1] - mb*b1[0][0])/(ma-mb)
          y=ma*x + a1[0][1] - ma*a1[0][0]
          intersection=Vector([[x, y]])
          if source=="a":
            gap=[intersection-a1, intersection]
          elif source=="b":
            gap-[b2-intersection, intersection]
          valid_gap=True
      else:
        valid_gap=False
      #print("Valid - ", valid_gap)
      if valid_gap:
        valid_gaps+=1
        try:
          if gap[0].proj(vel)<smallest[0].proj(vel):
            smallest=gap
        except:
          smallest=gap
        try:
          if gap[0].projscalar(vel)>biggest[0].projscalar(vel):
            biggest=gap
        except:
          biggest=gap
    print("Valids - ",valid_gaps)
    try:
      if biggest.projscalar(vel)>=1:
        return [True, smallest]
      else:
        return [False, smallest]
    except:
      return [False]

  #Takes 2 matrices, designed for 2 physobj/char's positions.
  def collision(self, b, vel):
    l_self, l_b=len(self), len(b)
    collision=True
    smallest_self, biggest_self, smallest_b, biggest_b=[], [], [], []
    
    for i in range(l_self+l_b):
      #Creates the normal
      if i<l_self:
        side=self.getc((i+1)%l_self)-self.getc((i)%l_self)
        p=Vector([[-side[0][1], side[0][0]]])
      else:
        side=b.getc((i+1-l_self)%l_b)-b.getc((i-l_self)%l_b)
        p=Vector([[-side[0][1], side[0][0]]])
      #Checks for smallest and biggest in self
      smallest_self.append(self.getc(0).projscalar(p))
      biggest_self.append(self.getc(0).projscalar(p))
      for j in range(l_self):
        proj_scalar=self.getc(j).projscalar(p)
        if proj_scalar<smallest_self[i]:
          smallest_self[i]=proj_scalar
        if proj_scalar>biggest_self[i]:
          biggest_self[i]=proj_scalar
      #Checks fro smallest and biggest in b
      smallest_b.append(b.getc(0).projscalar(p))
      biggest_b.append(b.getc(0).projscalar(p))
      for j in range(l_b):
        proj_scalar=b.getc(j).projscalar(p)
        if proj_scalar<smallest_b[i]:
          smallest_b[i]=proj_scalar
        if proj_scalar>biggest_b[i]:
          biggest_b[i]=proj_scalar

      #MTV_1d=interval_MTV(smallest_self[i], biggest_self[i], smallest_b[i], biggest_b[i])
      #if MTV_1d!=False:
      #  try:
      #    if abs(MTV_1d)<minimum_magnitude:
      #      minimum_magnitude=abs(MTV_1d)
      #      MTV=MTV_1d*p
      #  except:
      #    minimum_magnitude=MTV_1d
      #    MTV=minimum_magnitude*p
      #else:
      #  collision=False

      MTV_1d=interval_MTV(smallest_self[i], biggest_self[i], smallest_b[i], biggest_b[i])
      if MTV_1d[0]!=False:
        MTV_check=MTV_1d[0]*p
        if MTV_check.dot(vel)<0:
          try:
            if abs(MTV_1d)<minimum_magnitude:
              minimum_magnitude=abs(MTV_1d)
              MTV=MTV_check
          except:
            minimum_magnitude=MTV_1d[0]
            MTV=minimum_magnitude*p
            contact=MTV_1d[1]*p
      else:
        collision=False

    if collision:
      return [collision, MTV, contact]
      #return [collision, -1*smallest_gap[0]]
    else:
      return [collision]

  def line_collision(p1, p2, l1, l2, l3, l4):
    #aq, bq and cq are a, b and c in the quadratic
    #print("1 - ",(l3[0][1]+l2[0][1]-l1[0][1]-l4[0][1]))
    #print("2 - ",(p2[0][0]+l2[0][0]-p1[0][0]-l4[0][0]))
    aq=(l3[0][1]+l2[0][1]-l1[0][1]-l4[0][1])*(p2[0][0]+l2[0][0]-p1[0][0]-l4[0][0])
    #print("a1 - ",aq)
    aq=aq-((p2[0][1]+l2[0][1]-p1[0][1]-l4[0][1])*(l3[0][0]+l2[0][0]-l1[0][0]-l4[0][0]))
    #aq=(p2[0][0]+l2[0][0]-p1[0][0]-l4[0][0])-(p2[0][1]+l2[0][1]-p1[0][1]-l4[0][1])
    #print("a2 - ",aq)
    bq=(l1[0][1]-l2[0][1])*(p2[0][0]+l2[0][0]-p1[0][0]-l4[0][0])
    bq+=(p1[0][0]-l2[0][0])*(l3[0][1]+l2[0][1]-l1[0][1]-l4[0][1])
    bq-=(p1[0][1]-l2[0][1])*(l3[0][0]+l2[0][0]-l1[0][0]-l4[0][0])
    bq-=(l1[0][0]-l2[0][0])*(p2[0][1]+l2[0][1]-p1[0][1]-l4[0][1])
    #print("b - ",bq)
    cq=(l1[0][1]-l2[0][1])*(p1[0][0]-l2[0][0])-(p1[0][1]-l2[0][1])*(l1[0][0]-l2[0][0])
    #print("c - ",cq)
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
