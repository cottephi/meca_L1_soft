import glob
import sys
import os
import time
import Student
import Promo
import getopt
import datetime
import shutil
from numbers import Number

#Returns the name of the promotion corresponding to current date. Like, if today is 09/12/2017, the returned name will be 2017-2018. Changes in August.
def GetCurrentPromoName():
  CurrMonth =  time.strftime("%m")
  CurrYear =  time.strftime("%Y")
  if int(CurrMonth) > 8:
    return str(CurrYear) + "-" + str(int(CurrYear)+1)
  else:
    return str(int(CurrYear)+1) + "-" + str(int(CurrYear)+2)
    
#Needs details
def usage():
  print("Unrecognized arguments")
  print(" -h for help (=this message)")
  print(" -n to create a new promotion")
  print(" -p to plot the promotion")
  print(" -u to update the promotion")
  print(" -f [FILE_NAME] to use a file (as new promotion or as update)")
  print(" -s to specify a student (not compatible with -f)")
  print(" -k to specify a knowhow (not compatible with -f)")
  print(" -m to specify a grade. Format to use : 10.5-20/11/2017 12-22/11/2017 etc... Will add the grade 10.5 at the date 20 nov. 2017 and the grade 12 at the date 22 nov. 2017. (not compatible with -f)")
  print(" -y to specify the promotion. The name can be whatever you want.")
  
#main function
def main(argv):

  #Booleans to ID the arguments
  create_new = False
  promo_name = ""
  plot_opt = False
  add_opt = False
  update_opt = False
  file_opt = False
  file_arg = ""
  student_opt = False
  student_arg = ""
  knowhow_opt = False
  knowhow_arg = ""
  mark_opt = False
  mark_arg = ""
  year_opt = False
  
  #Read the arguments
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hnpuf:s:k:m:y:", [])
  except getopt.GetoptError as err:
    print(str(err))
    usage()
    exit(0)
  for opt, arg in opts:
    if opt == "-h":
      usage()
      exit(1)
    elif opt == "-n":
      create_new = True
    elif opt == "-p":
      plot_opt = True
    elif opt == "-u":
      update_opt = True
    elif opt == "-f":
      file_opt = True
      if not os.path.isfile(arg):
        print("ERROR : file " + arg + " not found")
        exit(0)
      file_arg = os.path.abspath(arg)
    elif opt == "-s":
      student_opt = True
      student_arg = arg
      print(student_arg)
    elif opt == "-k":
      knowhow_opt = True
      knowhow_arg = arg
    elif opt == "-m":
      mark_opt = True
      mark_arg = arg
    elif opt == "-y":
      year_opt = True
      promo_name = arg
    else:
      usage()
      exit(0)
      
  if not create_new and not plot_opt and not update_opt and not file_opt and not student_opt and not knowhow_opt and not mark_opt and not year_opt:
    usage()
    exit(0)
  if not os.path.isdir("promos"):
    print("ERROR: promos directory not found")
    exit(0)
    
#  /////////////////////////////////
  os.chdir("promos")
#  /////////////////////////////////

  promotion = Promo.Promo()

  #if -n option was specified : create new promotion
  if create_new:
    if not year_opt: #if promotion name was not specified (-y option)
      promo_name = str(input("Please indicate the name of the promotion you want to create (write current to use " +  GetCurrentPromoName() + ") \n"))
    if promo_name == "":
      print("Can not have empty name")
      exit(0)
    if promo_name == "current":
      promo_name = GetCurrentPromoName()
    if os.path.isdir(promo_name): #if promotion is already in promo/ directory
      erase = input("Promotion " + promo_name + " already exists, do you want to erase it? (y/n) \n")
      while erase != "y" and erase != "n":
        erase = input("Please answer by y or n \n")
      if erase == "n":
        print("Ok ciao")
        exit(1)
      shutil.rmtree(promo_name)
      print("Deleted promotion " + promo_name)
    if file_opt: #if -f option is specified, try to create promotion from file
      print("Creating new promotion from file " + file_arg + "...")
      promotion = Promo.Promo(promo_name, False)
      promotion.Open(file_arg, True)
      promotion.Save()
      if plot_opt:
        promotion.PlotAll()
    else:#else creates an empty promotion
      print("Creating empty promotion " + promo_name + "...")
      promotion = Promo.Promo(promo_name)
      if plot_opt:
        print("ERROR : can not plot an empty promotion")
        exit(0)
    exit(1)
  
  #if -y option was specified, tries to open the corresponding promotion
  if year_opt:
    if not os.path.isdir(promo_name): #if the specified promotion is not in promo/ directory, proposes to create it
      bool_create = input("Promotion " + promo_name + " does not exist. Do you want to create it? (y/n)\n")
      while create != "y" and create != "n":
        bool_create = input("Please answer by y or n \n")
      if bool_create == "n":
        print("Ok ciao")
        exit(1)
      print("Creating " + promo_name + "...")
      promotion = Promo.Promo(promo_name)
    else:
      print("Opening " + promo_name + "...")
      promotion = Promo.Promo(promo_name)
  
  #if no specified name, tries the current year as name
  else:
    promo_name = GetCurrentPromoName()
    if not os.path.isdir(promo_name):#if promotion not found, proposes to create it
      bool_create = input("Promotion of current year does not exist. Do you want to create it? (y/n)\n")
      while bool_create != "n" and bool_create != "y":
        bool_create = input("Please answer by y or n\n")
      if bool_create == "n":
        print("Ok ciao")
        exit(1)
      print("Creating " + promo_name + "...")
      promotion = Promo.Promo(promo_name)
    else:
      print("Opening promotion " + promo_name + "...")
      promotion = Promo.Promo(promo_name)
    
#  /////////////////////////////////

  #Should make the soft do something : modifiy the promotion or plot it.
  if not update_opt and not plot_opt:
    print("Please do something! Update or plot the promotion, but do not make me waste my time!")
    exit(0)
  
  #if -u option was used
  if update_opt:
    if not student_opt and not knowhow_opt and not file_opt:#need something to update : a student, a knowhow or a file to update from
      print("You need something to update : a student, a knowhow or an input file?")
      exit(0)
    if file_opt and (student_opt or knowhow_opt):#if file was specified, but also student or knowhow then the soft does not know which to use
      print("I can not guess wether you want to use student/kowhow or file to update the promotion.")
      exit(0)
    if not file_opt and student_opt and not knowhow_opt:#if only student was specified, it will be added to the promotion if not already in it. If it is already in it, you need to tell the soft what to do
      if promotion.IsStudent(student_arg):
        print("You need to tell me what to do to " + student_arg + " (use -k option to specify knowhow it and -m option to add a grade).")
        exit(0)
    if not file_opt and student_opt and knowhow_opt and not mark_opt:#if a kowhow is specified, but not a grade, will add the knowhow to a student. If the knowhow already exists, you need to add a grade
      if promotion.GetStudent(student_arg).IsKnowhow(knowhow_arg):
        print("You need to tell me which grade to add to knowhow " + knowhow_arg + " to student " + student_arg + ". Use -m option.")
        exit(0)
      
    if not file_opt:#if no file specified : update according to -s, -k and -m options.Add student and/or knowhow if not existant
      if not promotion.IsStudent(student_arg):
        bool_add = input("Student " + student_arg + " is not in promotion " + promo_name + ", do you want to add him/her? (y/n) \n")
        while bool_add != "y" and bool_add != "n":
          bool_add = input("Please answer by y or n \n")
        if bool_add == "n":
          print("Ok ciao")
          exit(1)
        print("Adding student " + student_arg + " to promotion " + promo_name + "...")
        promotion.AddStudent(Student.Student(student_arg))
        
      if knowhow_opt:#if knowhow was specified  
        if not promotion.GetStudent(student_arg).IsKnowhow(knowhow_arg):
          bool_add = input("Knowhow " + knowhow_arg + " is not a knowhow of student " + student_arg + ", do you want to add it? (y/n) \n")
          while bool_add != "y" and bool_add != "n":
            bool_add = input("Please answer by y or n \n")
          if bool_add == "n":
            print("Ok ciao")
            exit(1)
          print("Adding knowhow " + knowhow_arg + " to student " + student_arg + "...")
          promotion.GetStudent(student_arg).AddKnowhow(knowhow_arg)
        
        if mark_opt:#if grade was specified
          print("Adding grade " + mark_arg + " to " + student_arg + "\'s knowhow " + knowhow_arg + "...")
          mark_arg = mark_arg.split(" ")
          for i in range(0,len(mark_arg)):
            if mark_arg[i] == "" or "-" not in mark_arg[i]:
              print("ERROR : " + mark_arg[i] + " has wrong format. Should be \"mark1-date1 mark2-date2 etc...\"")
              exit(0)
            mark_arg[i] = mark_arg[i].split("-")
            if len(mark_arg[i]) != 2:
              print("ERROR : " + mark_arg[i] + " has wrong format. Should be \"mark1-date1 mark2-date2 etc...\"")
              exit(0)
            if "/" not in mark_arg[i][1]:
              print("ERROR : " + mark_arg[i][1] + " has wrong format. Please use day/month/year")
              exit(0)
            date = mark_arg[i][1].split("/")
            if len(date) != 3:
              print("ERROR : " + date + " has wrong format. Please use day/month/year")
              exit(0)
            day = int(date[0])
            month = int(date[1])
            year = int(date[2])
            if day > 31 or month > 12:
              print("ERROR : " + date + " has wrong format. Please use day/month/year")
              exit(0)
            mark_arg[i][1] = datetime.date(year,month,day)
          promotion.GetStudent(student_arg).AddMark(knowhow_arg, mark_arg)

    #if input file was specified
    if file_opt:
      tmp_promotion = Promo.Promo("tmp",False)
      tmp_promotion.Open(file_arg, True)
      promotion.AddPromotion(tmp_promotion)
      tmp_promotion.Remove()
  
  #if plot was specified
  if plot_opt:
    promotion.PlotAll()  
  
  if update_opt:
    promotion.Save()
    
  exit(1)
    
if __name__ == '__main__':
  if len(sys.argv) == 1:
    usage()
    exit(0)
  main(sys.argv[1:])
