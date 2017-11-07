import os
import Student
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import shutil
from numbers import Number

class Promo:
  def __init__(self, year = "", b_open = True):
    self.s_year = year
    self.s_students = []
    if year != "" :
      if not os.path.isdir(year):
        os.mkdir(year)
        self.s_promo_file = open(year + "/" + year, "w")
        self.s_promo_file.write('students;grades;dates;knowhow\n')
        self.s_promo_file.close()
      elif b_open:
        self.Open()

  def Remove(self):
    shutil.rmtree(self.s_year)  
  
  def AddStudent(self, student):
    self.s_students.append(student)
    
  def Open(self, promo_name = "", File = False):
    if promo_name == "":
      promo_name = self.s_year
      File = False
    if File:
      self.s_promo_file = open(promo_name,"r")
      if os.stat(promo_name).st_size == 0:
          print("Promotion " + self.s_year + " is empty.")
          self.s_promo_file.close()
          return
    else:
      self.s_promo_file = open(promo_name + "/" + promo_name,"r")
      if os.stat(promo_name + "/" + promo_name).st_size == 0:
          print("Promotion " + self.s_year + " is empty.")
          self.s_promo_file.close()
          return
    lines = self.s_promo_file.readlines()
    if lines[0] != 'students;grades;dates;knowhow\n':
      print("ERROR : promotion file " + promo_name + " has wrong format: \n First line is " + lines[0] + " but should be 'students;grades;dates;knowhow\n'")
      exit(0)
    lines = lines[1:]
    for i in range(0,len(lines)):
      if lines[i] == "\n":
        continue
      lines[i] = lines[i].split("\n")[0].split(";")
      tmp_student = Student.Student(lines[i][0])
      if lines[i][0] in [ st.GetName() for st in self.s_students ]:
        print("ERROR : " + tmp_student.GetName() + " is already in promotion " + self.s_year + ". Please avoid duplicate names.")
        exit(0)
      marks = lines[i][1].replace(" ","").split(",")
      dates = lines[i][2].replace(" ","").split(",")
      knowhows = lines[i][3].split(",")
      if len(marks) != len(knowhows) or len(marks) != len(dates) or len(knowhows) != len(dates):
        print("ERROR : promotion file " + promo_name + " has wrong format at line " + str(i) + ": it has " + str(len(marks)) + " marks, " + str(len(dates)) + " and " + str(len(knowhows)) + " know-hows. Those three numbers should be equal.")
        exit(0)
      rec_marks = []
      for j in range(0,len(knowhows)):
        marks[j] = marks[j].split("+")
        dates[j] = dates[j].split("+")
        for mark, mydate in zip(marks[j], dates[j]):
          if "/" not in mydate:
            print("ERROR : " + mydate + " has wrong format. Please use day/month/year")
            exit(0)
          date = mydate.split("/")
          if len(date) != 3:
            print("ERROR : " + date + " has wrong format. Please use day/month/year")
            exit(0)
          day = int(date[0])
          month = int(date[1])
          year = int(date[2])
          if day > 31 or month > 12:
            print("ERROR : " + date + " has wrong format. Please use day/month/year")
            exit(0)
          try:
            val = float(mark)
          except ValueError:
            print("ERROR : promotion file " + promo_name + " has wrong format at line " + str(i+1) + ": the mark " + mark + " should be a number.")
            exit(0)
          try:
            val = datetime.date(year, month, day)
          except ValueError:
            print("ERROR : promotion file " + promo_name + " has wrong format at line " + str(i+1) + ": the date " + mydate + " is not a valid date format.")
            exit(0)
          rec_marks.append([mark,datetime.date(year, month, day)])
        tmp_student.AddKnowhow(knowhows[j], rec_marks)
        rec_marks = []
      self.AddStudent(tmp_student)
    self.s_promo_file.close()
    
  def Save(self, year = ""):
    if year == "":
      year = self.s_year
      print("Updating promotion " + year + "...")
    else:
      if os.path.isdir(year):
        bool_ecrase = input("Promotion " + year + " alreasy exists. Do you want to erase it? (y/n) \n")
        while bool_ecrase != "n" and bool_ecrase != "y":
          bool_ecrase = input("Please answer by y or n. \n")
        if bool_ecrase == "n":
          print("ok ciao")
          exit(1)
      print("Saving new promotion " + year + "...")
    self.s_promo_file = open(year + "/" + year,"w")
    self.s_promo_file.write("students;grades;dates;knowhow\n")
    for student in self.s_students:
      line = student.GetName()
      marksline = ";"
      datesline = ";"
      knowhowsline = ";"
      for knowhow in student.GetKnowhows():
        knowhowsline = knowhowsline + knowhow + ","
        for mark in student.GetKnowhowMarks(knowhow):
          marksline = marksline + str(mark[0]) + "+"
          datesline = datesline + str(mark[1].day) + "/" + str(mark[1].month) + "/" + str(mark[1].year) + "+"
        marksline = marksline[:-1]
        marksline = marksline + ","
        datesline = datesline[:-1]
        datesline = datesline + ","
      knowhowsline = knowhowsline[:-1]
      marksline = marksline[:-1]
      datesline = datesline[:-1]
      line = line + marksline + datesline + knowhowsline + "\n"
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
    for student in self.s_students:
      mean = student.GetMean()
      print(student.GetName())
      for mark in mean:
        print("  " + mark + " : " + str(mean[mark]))
      for knowhow in student.GetKnowhows():
        dates = []
        marks = []
        for mark in student.GetKnowhowMarks(knowhow):
          dates.append(mark[1])
          marks.append(mark[0])
        plt.title(student.GetName() + " : " + knowhow)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.gca().set_ylim([0,20])
        plt.plot(dates, marks, 'ro')
        plt.gcf().autofmt_xdate()
        plt.savefig(self.s_year + "/" + student.GetName() + "_" + knowhow + ".pdf")
        plt.close()
        print("Plotted ./" + self.s_year + "/" + student.GetName() + "_" + knowhow + ".pdf")
    
  def IsStudent(self, student_name):
    names = self.GetStudentsNames()
    if not student_name in names:
      return False
    else:
      return True
      
  def AddPromotion(self, promo2):
    for student2 in promo2.GetStudents():
      if not self.IsStudent(student2.GetName()):
        self.AddStudent(student2)
        continue
      for knowhow2 in student2.GetKnowhows():
        if not self.GetStudent(student2.GetName()).IsKnowhow(knowhow2):
          self.GetStudent(student2.GetName()).AddKnowhow(knowhow2)
          continue
        self.GetStudent(student2.GetName()).AddMark(knowhow2, student2.GetKnowhowMarks(knowhow2))
      
