from numbers import Number

class Student:
  def __init__(self, name = ""):
    self.s_name = name
    self.s_knowhows = {}
    
  def AddKnowhow(self, knowhow, marks = ""):
    self.s_knowhows[knowhow] = marks
   
  def AddMark(self, knowhow, marks):
    if not self.IsKnowhow(knowhow):
      print("ERROR : " + knowhow + " is not a knowhow of student " + self.s_name + ".")
      exit(0)
    if type(marks) is list:
      for mark in marks:
        try:
          val = float(mark)
        except ValueError:
          print("ERROR : can not add the non-number mark " + mark + " to konw-how " + knowhow + "to student " + self.s_name + ".")
          exit(0)
      old_marks = self.s_knowhows[knowhow]
      new_marks = old_marks + marks
    else:
      try:
        val = float(marks)
      except ValueError:
        print("ERROR : can not add the non-number mark " + marks + " to konw-how " + knowhow + "to student " + self.s_name + ".")
        exit(0)
      new_marks = self.s_knowhows[knowhow]
      new_marks.append(marks)
    self.s_knowhows[knowhow] = new_marks
    
  def GetName(self):
    return self.s_name
    
  def GetKnowhowMarks(self, knowhow):
    if not knowhow in self.s_knowhows:
      print("ERROR : knowhow " + knowhow + " is not in " + self.s_name + "\'s list of knowhows")
      exit(0)
    return self.s_knowhows[knowhow]
   
  def GetKnowhows(self):
    return self.s_knowhows
    
  def IsKnowhow(self, knowhow):
    if not knowhow in self.s_knowhows:
      return False
    else:
      return True
