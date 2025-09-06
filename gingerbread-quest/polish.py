def operation(a, b, o):
  if o=="+":
    return a+b
  elif o=="-":
    return a-b
  elif o=="*":
    return a*b
  elif o=="/":
    return a/b
  elif o=="^":
    return a**b

class stack():
  def __init__(self, stack, end):
    self.stack=stack
    self.pointer=end
    self.len=len(self.stack)

  def append(self, element):
    if self.pointer<self.len-1:
      self.pointer+=1
      self.stack[self.pointer]=element

  def remove(self, items):
    for p in range(items):
      if self.pointer>-1:
        self.stack[self.pointer]=""
        self.pointer-=1

  def getpointer(self):
    return self.pointer

  def getpointed(self):
    try:
      return self.stack[self.pointer]
    except:
      return "N/A"

  def __getitem__(self, index):
    return self.stack[index]

def genempty(length):
  empty=[]
  for i in range(length):
    empty.append("")
  return empty

class postfix():
  #Takes polish notation as an input
  def __init__(self, polish):
    self.polish=polish

  def get_element(self, element):
    return self.polish[element]

  def calculate(self, substitution):
    plength=(len(self.polish)//2)+3
    postfix=stack(genempty(plength), -1)
    for i in range(len(self.polish)):
      if self.polish[i]=="x":
        postfix.append(substitution)
      else:
        postfix.append(self.polish[i])
      if isinstance(postfix.getpointed(), str):
        if postfix.getpointed()=="N/A":
          postfix.remove(1)
        else:
          cpos=postfix.getpointer()
          result=operation(postfix[cpos-2], postfix[cpos-1], postfix[cpos])
          postfix.remove(3)
          postfix.append(result)
    return postfix[0]

class f():
  def __init__(self, func):
    self.func=postfix(func)
  def get_element(self, element):
    return self.func.get_element(element)
  def output(self, input):
    return self.func.calculate(input)
