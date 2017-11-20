#Class promotion, able to store students 

import os
import Student
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import shutil
from numbers import Number

class Promo: #Creator of the class
  def __init__(self, year = "", b_open = True):
    self.s_year = year #name of the class (could use something other than the year, but it is the most obvious choice)
    self.s_students = [] #list of objects Student)
    if year != "" : #if the name is precised, check if the promo already exists. If it does, opens it (unless precises otherwise), otherwise creates an empty one
      if not os.path.isdir(year):
        os.mkdir(year)
        self.s_promo_file = open(year + os.sep + year, "w")
        self.s_promo_file.write('students;grades;dates;knowhow\n')
        self.s_promo_file.close()
      elif b_open:
        self.Open()

  def Remove(self):#removes the class folder entierely, including backups
    shutil.rmtree(self.s_year)  
  
  def AddStudent(self, student):#adds a student to the current student list. With all its grades and knowhows, if any
    self.s_students.append(student)
    
  def Open(self, promo_name = "", File = False):#opens the class from its file
    if promo_name == "":#if no name is given, use the name of the promotion
      promo_name = self.s_year
      File = False
    if File:#Is used when specifying a file that is not in the directory containing all the promotions. promo_name should then be the path to the file.
      self.s_promo_file = open(promo_name,"r")
      if os.stat(promo_name).st_size == 0:
          print("Promotion " + self.s_year + " is empty.")
          self.s_promo_file.close()
          return "empty"
    else:#open promotion file
      self.s_promo_file = open(promo_name + os.sep + promo_name,"r")
      if os.stat(promo_name + os.sep + promo_name).st_size == 0:
          print("Promotion " + self.s_year + " is empty.")
          self.s_promo_file.close()
          exit(1)
          return "empty"
#will check if the file has correct format, then read line by line by separating the main objects, then the knowhows, then the marks and dates
    lines = self.s_promo_file.readlines()
    if lines[0] != 'students;grades;dates;knowhow\n':
      if lines[0] == 'students;knowhow\n' and File:#if file is list of student and list of knowhows
        for i in range(1,len(lines)):
          if lines[i] == "\n":#skip empty lines
            continue
          l = lines[i].split("\n")[0].split(";")
          if len(l) != 2:
            print("ERROR : wrong format at line " + str(i))
          if l[0] == "":
            continue
          tmp_student = Student.Student(l[0])
          if l[0] in [ st.GetName() for st in self.s_students ]:
            print("ERROR : " + tmp_student.GetName() + " is already in promotion " + self.s_year + ". Please avoid duplicate names.")
            exit(0)
          for j in range(1,len(lines)):
            if lines[j] == "\n":#skip empty lines
              continue
            l = lines[j].split("\n")[0].split(";")
            if len(l) != 2:
              print("ERROR : wrong format at line " + str(j))
            if l[1] == "":
              continue
            if tmp_student.IsKnowhow(l[1]):
              print("ERROR : duplicate knowhow name " + l[1] + ".")
              exit(0)
            tmp_student.AddKnowhow(l[1])
          self.AddStudent(tmp_student)
        self.s_promo_file.close()
        return
      else:
        print("ERROR : promotion file " + promo_name + " has wrong format: \n First line is " + lines[0] + " but should be 'students;grades;dates;knowhow'")
        exit(0)
        
    #if normal first line format
    for i in range(1,len(lines)):
      if lines[i] == "\n":#skip empty lines
        continue
      lines[i] = lines[i].split("\n")[0].split(";")
      if len(lines[i]) != 4:
        print("ERROR : wrong format at line " + str(i))
        exit(0)
      #object Student to fill
      tmp_student = Student.Student(lines[i][0])
      #Is two students have the same name, stops.
      if lines[i][0] in [ st.GetName() for st in self.s_students ]:
        print("ERROR : " + tmp_student.GetName() + " is already in promotion " + self.s_year + ". Please avoid duplicate names.")
        exit(0)
      #if no knowhows in this line, save student to promo and continue to next line
      if len(lines[i][3]) == 0:
        self.AddStudent(tmp_student)
        continue
      #removes blanks in grades and dates
      marks = lines[i][1].replace(" ","").split(",")
      dates = lines[i][2].replace(" ","").split(",")
      knowhows = lines[i][3].split(",")
      #checks if the number of knowhows matches the number of gradess and dates
      if len(marks) != len(knowhows) or len(marks) != len(dates) or len(knowhows) != len(dates):
        print("ERROR : promotion file " + promo_name + " has wrong format at line " + str(i) + ": it has " + str(len(marks)) + " marks, " + str(len(dates)) + " and " + str(len(knowhows)) + " knowhows. Those three numbers should be equal.")
        exit(0)
      #splits the grades of a given knowhow. Idem for the dates.
      rec_marks = [] #will contain a list of pairs (grade, date)
      for j in range(0,len(knowhows)):
        #if no grades for this knowhow, save knowhow to student and continue to next knowhow
        if len(marks[j]) == 0:
          tmp_student.AddKnowhow(knowhows[j])
          continue
        marks[j] = marks[j].split("+")
        dates[j] = dates[j].split("+")
        #check if dates have correct format, and pairs marks and dates
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
        #add the knowhow and the corresponding grades and dates to the current student
        tmp_student.AddKnowhow(knowhows[j], rec_marks)
        rec_marks = []
      #Add current student to promotion
      self.AddStudent(tmp_student)
    self.s_promo_file.close()
    
    
  #Save the promotion to a file specified by the argument year. If not specified, updates the current promotion file. Creates a backup of the new promotion, keeps up to 5 backups.
  def Save(self, year = ""):
    if year == "":
      year = self.s_year
      print("Updating promotion " + year + "...")
    else:
      if os.path.isdir(year):
        bool_ecrase = input("Promotion " + year + " already exists. Do you want to erase it? (y/n) \n")
        while bool_ecrase != "n" and bool_ecrase != "y":
          bool_ecrase = input("Please answer by y or n. \n")
        if bool_ecrase == "n":
          print("ok ciao")
          exit(1)
      print("Saving new promotion " + year + "...")
        
    self.s_promo_file = open(year + os.sep + year,"w")
    self.s_promo_file.write("students;grades;dates;knowhow\n")
    if len(self.s_students) == 0:
      self.s_promo_file.close()
      return
    for student in self.s_students:
      line = student.GetName()
      marksline = ";"
      datesline = ";"
      knowhowsline = ";"
      if len(student.GetKnowhows()) == 0:
        line = line + marksline + datesline + knowhowsline + "\n"
        self.s_promo_file.write(line)
        self.s_promo_file.close()
        return
      for knowhow in student.GetKnowhows():
        knowhowsline = knowhowsline + knowhow + ","
        if len(student.GetKnowhowMarks(knowhow)[0]) == 0:
          continue
        for mark in student.GetKnowhowMarks(knowhow):
          marksline = marksline + str(mark[0]) + "+"
          datesline = datesline + str(mark[1].day) + os.sep + str(mark[1].month) + os.sep + str(mark[1].year) + "+"
        marksline = marksline[:-1]
        marksline = marksline + ","
        datesline = datesline[:-1]
        datesline = datesline + ","
      knowhowsline = knowhowsline[:-1]
      if marksline != ";":
        marksline = marksline[:-1]
        datesline = datesline[:-1]
      line = line + marksline + datesline + knowhowsline + "\n"
      self.s_promo_file.write(line)
    self.s_promo_file.close()
    
    #backs up
    if not os.path.isdir(year + os.sep + "backup"):
      os.mkdir(year + os.sep + "backup")
    for i in range(1,6):
      if not os.path.isfile(year + os.sep + "backup" + os.sep + year + "_" + str(i)):
        shutil.copy(year + os.sep + year,year + os.sep + "backup" + os.sep + year + "_" + str(i))
        return
    os.remove(year + os.sep + "backup" + os.sep + year + "_1")
    for i in range(2,6):
      shutil.move(year + os.sep + "backup" + os.sep + year + "_" + str(i), year + os.sep + "backup" + os.sep + year + "_" + str(i-1))
    shutil.copy(year + os.sep + year,year + os.sep + "backup" + os.sep + year + "_5")
        
      
  #Accessors and modifiers
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
      if not os.path.isdir(self.s_year + os.sep + student.GetName()):
        os.mkdir(self.s_year + os.sep + student.GetName())
      mean = student.GetMean()
      print(student.GetName())
      for mark in mean:
        print("  " + mark + " : " + str(mean[mark]))
      for knowhow in student.GetKnowhows():
        dates = []
        marks = []
        if len(student.GetKnowhowMarks(knowhow)[0]) == 0:
          continue
        for mark in student.GetKnowhowMarks(knowhow):
          dates.append(mark[1])
          marks.append(mark[0])
        plt.title(student.GetName() + " : " + knowhow)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.gca().set_ylim([-1,21])
        print(max(dates))
        plt.gca().set_xlim([min(dates) - datetime.timedelta(days=1),max(dates) + datetime.timedelta(days=1)])
        plt.plot(dates, marks, 'ro')
        plt.gcf().autofmt_xdate()
        plt.savefig(self.s_year + os.sep + student.GetName() + os.sep + knowhow + ".pdf")
        plt.close()
        print("Plotted " + self.s_year + os.sep + student.GetName() + os.sep + knowhow + ".pdf")
    
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
      
