#Class to handle a single student, its knowhows and the corresponding grades. The name has no particular format restriction. The knowhows and the grade are handled by a dictionnary. The keys are the knowhows names, the items are, for each knowhow, a list of pairs grade-date, date being the date at which the grade was given to the student.


from numbers import Number
import datetime

class Student:
  def __init__(self, name = ""):#Creator, initiating name of the student and a knowohws dictionnary
    self.s_name = name
    self.s_knowhows = {}
    
  def AddKnowhow(self, knowhow, marks = [[]]):#Add a knowhow, possiblty without grades yet. If with grades, those must be a list of pairs.
    self.s_knowhows[knowhow] = marks
   
  def AddMark(self, knowhow, marks):#Adds a grade-date pair to a given knowhow
    new_marks = []
    old_marks = []
    if not self.IsKnowhow(knowhow):
      print("ERROR : " + knowhow + " is not a knowhow of student " + self.s_name + ".")
      exit(0)
    if not type(marks) is list:#"marks" should always be a list
      print("ERROR : grades-dates should be passed as a list to AddMark")
      exit(0)
    if type(marks[0]) is list:#if the first item is a list, expect it and the other items to be [grade,date]. Will exit with error otherwise.
      for mark in marks:
        if not type(mark) is list:
          print("ERROR : wrong input type in AddMark")
          exit(0)
        if len(mark) != 2:
          print("ERROR : grade-date pair should be of size 2")
          exit(0)
        try:#expects first item to be grade, ie a number.
          val = float(mark[0])
        except ValueError:
          print("ERROR : can not add the non-number mark " + mark[0] + " to konw-how " + knowhow + " to student " + self.s_name + ".")
          exit(0)
        if float(mark[0]) > 20 or float(mark[0]) < 0:
          print("ERROR : grades should be between 0 and 20")
          exit(0)
        if not  type(mark[1]) is datetime.date:#expects second item to be a datetime.date object
          print("ERROR : " + date + " must be datetime.date object.")
          exit(0)
      if self.s_knowhows[knowhow] = "":
        new_marks = marks
      else:
        old_marks = self.s_knowhows[knowhow]
        new_marks = old_marks + marks
    else:#if first item of marks is not a list, then marks is assumed to be a grade-date pair.
      try:
        val = float(marks[0])
      except ValueError:
        print("ERROR : can not add the non-number mark " + marks + " to kowhow " + knowhow + " to student " + self.s_name + ".")
        exit(0)
      if not  type(mark[1]) is datetime.date:
        print("ERROR : " + date + " must be datetime.date object.")
        exit(0)
      if self.s_knowhows[knowhow] = "":
        new_marks = marks
      else:
        new_marks = self.s_knowhows[knowhow]
        new_marks.append(marks)
    self.s_knowhows[knowhow] = new_marks
    
#Accessor and modifiers

  def GetName(self):
    return self.s_name
    
  def GetKnowhowMarks(self, knowhow):
    if not knowhow in self.s_knowhows:
      print("ERROR : knowhow " + knowhow + " is not in " + self.s_name + "\'s list of knowhows")
      exit(0)
    return self.s_knowhows[knowhow]
   
  def GetKnowhows(self):
    return self.s_knowhows
    
  #computes the means of each knowhows, as a dic whose keys are the knowhows and the items the means. Can specify one knowhow in inupt to have only its mean.
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
        
    
  def IsKnowhow(self, knowhow):#check if knowhow is in knowhows list
    if not knowhow in self.s_knowhows:
      return False
    else:
      return True
