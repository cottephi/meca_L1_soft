import os
import Student
from numbers import Number

class Promo:
  def __init__(self, year = "", b_open = True):
    self.s_year = year
    self.s_students = []
    if year != "" :
      if not os.path.isfile(year):
        self.s_promo_file = open(year, "w").close()
      elif b_open:
        self.Open()
    
  def AddStudent(self, student):
    self.s_students.append(student)
    
  def Open(self, promo_name = ""):
    if promo_name == "":
      promo_name = self.s_year
    self.s_promo_file = open(promo_name,"r")
    if os.stat(promo_name).st_size == 0:
        print("Promotion " + self.s_year + " is empty.")
        self.s_promo_file.close()
        return
    lines = self.s_promo_file.readlines()
    if lines[0] != 'students;grades;knowhow\n':
      print("ERROR : promotion file " + promo_name + " has wrong format: \n First line is " + lines[0] + " but should be 'students;grades;knowhow\n'")
      exit(0)
    lines = lines[1:]
    for i in range(0,len(lines)):
      lines[i] = lines[i].split("\n")[0].split(";")
      tmp_student = Student.Student(lines[i][0])
      if lines[i][0] in [ st.GetName() for st in self.s_students ]:
        print("ERROR : " + tmp_student.GetName() + " is already in promotion " + self.s_year + ". Please avoid duplicate names.")
        exit(0)
      marks = lines[i][1].split(",")
      knowhows = lines[i][2].split(",")
      if len(marks) != len(knowhows):
        print("ERROR : promotion file " + promo_name + " has wrong format at line " + str(i) + ": it has " + str(len(marks)) + " marks and " + str(len(knowhows)) + " know-hows. Those two numbers should be equal.")
        exit(0)
      for j in range(0,len(knowhows)):
        marks[j] = marks[j].split("+")
        for mark in marks[j]:
          try:
            val = float(mark)
          except ValueError:
            print("ERROR : promotion file " + promo_name + " has wrong format at line " + str(i) + ": the mark " + mark + " should be a number.")
            exit(0)
        tmp_student.AddKnowhow(knowhows[j], marks[j])
      self.AddStudent(tmp_student)
    self.s_promo_file.close()
    
  def Save(self, year = ""):
    if year == "":
      year = self.s_year
      print("Updating promotion " + year + "...")
    else:
      if os.path.isfile(year):
        bool_ecrase = input("Promotion " + year + " alreasy exists. Do you want to erase it? (y/n) \n")
        while bool_ecrase != "n" and bool_ecrase != "y":
          bool_ecrase = input("Please answer by y or n. \n")
        if bool_ecrase == "n":
          print("ok ciao")
          exit(1)
      print("Saving new promotion " + year + "...")
    self.s_promo_file = open(year,"w")
    self.s_promo_file.write("students;grades;knowhow\n")
    for student in self.s_students:
      line = student.GetName()
      marksline = ";"
      knowhowsline = ";"
      for knowhow in student.GetKnowhows():
        knowhowsline = knowhowsline + knowhow + ","
        for mark in student.GetKnowhowMarks(knowhow):
          marksline = marksline + str(mark) + "+"
        marksline = marksline[:-1]
        marksline = marksline + ","
      knowhowsline = knowhowsline[:-1]
      marksline = marksline[:-1]
      line = line + marksline + knowhowsline + "\n"
      self.s_promo_file.write(line)
    self.s_promo_file.close()
        
  def GetStudent(self, student_name):
    names = self.GetStudentsNames()
    if not student_name in names:
      print("ERROR : " + student_name + " is not in promotion " + self.s_year  +".")
      exit(0)
    return self.s_students[names.index(student_name)]

  def GetStudents(self):
    return self.s_students
    
  def GetStudentsNames(self):
    return [st.GetName() for st in self.s_students]
    
  def GetYear(self):
    return self.s_year
    
  def SetStudents(self,students):
    self.s_students = students
    
  def SetYear(self, year):
    self.s_year = year
    
  def PlotAll(self):
    print("Under construction")
    
  def IsStudent(self, student_name):
    names = self.GetStudentsNames()
    if not student_name in names:
      return False
    else:
      return True
