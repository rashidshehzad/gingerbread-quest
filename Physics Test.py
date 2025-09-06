import pygame, sys
from pygame.locals import QUIT
import time
import copy
from math import sin, cos, radians, degrees

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Hello World!')


class Vector():
    # def __init__(self, list):
    #     self.vector = []
    #     if list[0] == "Ø":
    #         rows = list[1]
    #         columns = list[2]
    #     else:
    #         rows = len(list)
    #         columns = len(list[0])
    #     #To make sure elements aren't made into NoneType, but instead Int.
    #     for i in range(rows):
    #         self.vector.append([])
    #         for j in range(columns):
    #             if list[0] == "Ø":
    #                 self.vector[i].append(0)
    #             else:
    #                 self.vector[i].append(float(list[i][j]))

    def __init__(self, list):
        self.vector = list

    #def getvector(self):
    #  return self.vector
    def __add__(self, b):
      result = []
      
      for i in range(len(self.vector)):
        result.append([])
        for j in range(len(self.vector[0])):
          if len(self.vector[0]) == len(b.vector[0]):
            #print("b - ",b.vector)
            #print("self - ",self.vector)
            #print("i - ",i,"j - ",j)
            result[i].append(self.vector[i][j]+b.vector[i][j])
          else:
            result[i].append(self.vector[i][j]+b.vector[i][0])
      return Vector(result)

    def __sub__(self, b):
      result = []
      
      for i in range(len(self.vector)):
        result.append([])
        for j in range(len(self.vector[0])):
          if len(self.vector[0]) == len(b.vector[0]):
            #print("b - ",b.vector)
            #print("self - ",self.vector)
            #print("i - ",i,"j - ",j)
            result[i].append(self.vector[i][j]-b.vector[i][j])
          else:
            result[i].append(self.vector[i][j]-b.vector[i][0])
      return Vector(result)

    def rowtotal(self, row):
        rowtotal = 0
        for i in range(len(self.vector[row])):
            rowtotal += self.vector[row][i]
        return rowtotal

    def columntotal(self, column):
        columntotal = 0
        for i in range(len(self.vector)):
            columntotal += self.vector[i][column]
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

    def gettuple(self):
        temp = []
        for i in range(len(self.vector)):
            temp.append(self.vector[i][0])
        return tuple(temp)

    def getlist(self):
        return self.vector

    def __rmul__(self, left):
      if not isinstance(left, Vector):
        return self * left
      else:
        return left*self

    def __mul__(self, right):
      if isinstance(right, Vector):
        answer=[]
        for i in range(len(self.vector)):
          answer.append([])
          for j in range(len(right[0])):
            total=0
            for k in range(len(right.vector)):
              total=total+(float(self[i][k])*float(right[k][j]))
            answer[i].append(total)
      else:
        answer=[]
        for i in range(len(self.vector)):
          answer.append([])
          for j in range(len(self[0])):
            answer[i].append(float(self[i][j])*float(right))
      return Vector(answer)

    def __str__(self):
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

    #def getcentroid(self):

def determinant(a, b):
  return a[0][0]*b[1][0] - a[1][0]*b[0][0]

def shift(initial, shift):
  result=copy.deepcopy(initial.vector)
  for i in range(len(result)):
    for j in range(len(result[0])):
      result[i][j]=initial.vector[i][j]+shift.vector[i][0]
  return Vector(result)

def angvector(angle):
  #Original  - 
  #return Vector([[cos(angle), -sin(angle)], [sin(angle), cos(angle)]])
  #Radians - 
  return Vector([[cos(radians(angle)), -sin(radians(angle))], [sin(radians(angle)), cos(radians(angle))]])


# a = vector([[0, 1], [2, 3]])
# print(a.vector)
# print(type(a))


class physobj():
  # def __init__(self, pos, rotation, velocity, colour):
  def __init__(self, pos: Vector, rotation: Vector, velocity: Vector, pivot: Vector, colour: tuple):
    self.pos = pos
    self.rotation = rotation
    if len(velocity[0])==1:
      for i in range(len(self.pos[0])):
        velocity.vector[0].append(velocity[0][0])
        velocity.vector[1].append(velocity[1][0])
    self.velocity = velocity
    self.pivot = pivot
    self.colour = colour
    #aforces is the forces affecting it.
    self.aforces=[]
    print(self.pos)
    #print(self.rotation, "type self.rotation - ", type(self.rotation))
    #print(self.pos, "self.pos - ", type(self.pos))

  def move(self):
    temppos=shift(self.pos, -1*self.pivot)
    self.pos = shift((self.rotation * temppos), self.pivot)+self.velocity
    self.pivot=self.pivot+self.velocity

  def draw(self):
    points = []
    #print("self.pos - ", self.pos)
    for i in range(len(self.pos[0])):
      points.append((self.pos[0][i], self.pos[1][i]))
      pygame.draw.line(screen, (34,139,34), points[i], (self.pivot[0][0], self.pivot[1][0]))
    #print("Len of points: ", len(points))
    pygame.draw.polygon(screen, self.colour, points)
    pygame.draw.circle(screen, (30,144,255), self.pivot.gettuple(), 5)


def getline(a, b):
    dy = b.vector[0][0] - a.vector[0][0]
    dx = b.vector[1][0] - b.vector[1][0]
    m = dy / dx
    c = b.vector[0][0] - (b.vector[1][0] * m)
    return m, c


frames = 100
#objects = [[vector([[150, 200, 220], [200, 270, 150]]), (255, 192, 203)]]
#self, pos: Vector, rotation: Vector, velocity: Vector, pivot: Vector, colour: tuple
objects = [
  # physobj(vector([[150, 200, 220], [200, 270, 150]]), angvector(2),
  # vector([[5], [2]]), (255, 192, 203))
  #300, 150 -> 200, 220
  physobj(Vector([[150, 200, 220], [200, 270, 150]]), angvector(-5),
          Vector([[2], [3]]), Vector([[150], [200]]), (255, 192, 203)),
  physobj(Vector([[280, 320, 320, 280], [170, 170, 130, 130]]), angvector(8),
          Vector([[0], [0]]), Vector([[300], [150]]), (136, 8, 8))
]

for i in range(frames):
  screen.fill((0,0,1))
  for j in range(len(objects)):
      objects[j].move()
      objects[j].draw()
  pygame.display.update()
  #print("Hello.")
  time.sleep(0.05)

loop = False
while loop:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
