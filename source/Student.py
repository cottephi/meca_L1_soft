from numbers import Number
import datetime

class Student:
  def __init__(self, name = ""):
    self.s_name = name
    self.s_knowhows = {}
    
  def AddKnowhow(self, knowhow, marks = [[]]):
    self.s_knowhows[knowhow] = marks
   
  def AddMark(self, knowhow, marks):
    if not self.IsKnowhow(knowhow):
      print("ERROR : " + knowhow + " is not a knowhow of student " + self.s_name + ".")
      exit(0)
    if type(marks) is list:
      if type(marks[0]) is list:
        for mark in marks:
          try:
            val = float(mark[0])
          except ValueError:
            print("ERROR : can not add the non-number mark " + mark[0] + " to konw-how " + knowhow + " to student " + self.s_name + ".")
            exit(0)
          if not  type(mark[1]) is datetime.date:
            print("ERROR : " + date + " must be datetime.date object.")
            exit(0)
        old_marks = self.s_knowhows[knowhow]
        new_marks = old_marks + marks
      else:
        try:
          val = float(marks[0])
        except ValueError:
          print("ERROR : can not add the non-number mark " + marks + " to konw-how " + knowhow + " to student " + self.s_name + ".")
          exit(0)
        if not  type(mark[1]) is datetime.date:
          print("ERROR : " + date + " must be datetime.date object.")
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
    
  def GetMean(self, knowhow = ""):
    mean = {}
    if knowhow == "":
      for knowhow in self.s_knowhows:
        mean[knowhow] = 0
        marks = 0
        for mark in self.s_knowhows[knowhow]:
          mean[knowhow] = float(mean[knowhow]) + float(mark[0])
          marks = marks + 1
        mean[knowhow] = mean[knowhow]/marks
    else:
      marks = 0
      if not IsKnowhow(knowhow):
        print("ERROR : knowhow " + " is not in " + self.s_name + "\'s list of knowhows")
        exit(0)
      for mark in self.s_knowhows[knowhow]:
        mean[knowhow] = float(mean[knowhow]) + float(mark[0])
        marks = marks + 1
      mean[knowhow] = mean[knowhow]/marks
    return mean
        
    
  def IsKnowhow(self, knowhow):
    if not knowhow in self.s_knowhows:
      return False
    else:
      return True
