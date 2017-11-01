import glob
import sys
import os
import time
import Student
import Promo
import getopt
from numbers import Number

def GetCurrentPromoName():
  CurrMonth =  time.strftime("%m")
  CurrYear =  time.strftime("%Y")
  if int(CurrMonth) > 8:     #Si on est après août
    return str(CurrYear) + "-" + str(int(CurrYear)+1)
  else:
    return str(int(CurrYear)+1) + "-" + str(int(CurrYear)+2)

def usage():
  print("Unrecognized arguments")
  
def main(argv):

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

  if create_new:
    if not year_opt:
      promo_name = input("Please indicate the name of the promotion you want to create \n")
    if promo_name == "":
      print("Can not have empty name")
      exit(0)
    if os.path.isfile(promo_name):
      erase = input("Promotion " + promo_name + "already exists, do you want to erase it? (y/n) \n")
      while erase != "y" and erase != "n":
        erase = input("Please answer by y or n \n")
      if erase == "n":
        print("Ok ciao")
        exit(1)
      os.remove(promo_name)
      print("Deleted promotion " + promo_name)
    if file_opt:
      print("Creating new promotion from file " + file_arg + "...")
      promotion = Promo.Promo(promo_name)
      promotion.Open(file_arg)
      promotion.Save()
      if plot_opt:
        promotion.PlotAll()
    else:
      print("Creating empty promotion " + promo_name + "...")
      promotion = Promo.Promo(promo_name)
      if plot_opt:
        print("ERROR : can not plot an empty promotion")
        exit(0)
    exit(1)
      
  if year_opt:
    if not os.path.isfile(promo_name):
      bool_create = input("Promotion " + promo_name + " does not exist. Do you want to create it? (y/n)\n")
      while create != "y" and create != "n":
        bool_create = input("Please answer by y or n \n")
      if bool_create == "n":
        print("Ok ciao")
        exit(1)
    print("Creating " + promo_name + "...")
    promotion = Promo.Promo(promo_name)
    exit(1)
  else:
    promo_name = GetCurrentPromoName()
    if not os.path.isfile(promo_name):
      bool_create = input("Promotion of current year does not exist. Do you want to create it? (y/n)\n")
      while bool_create != "n" and bool_create != "y":
        bool_create = input("Please answer by y or n\n")
      if bool_create == "n":
        print("Ok ciao")
        exit(1)
      print("Creating " + promo_name + "...")
      promotion = Promo.Promo(promo_name)
      exit(1)
    else:
      print("Opening promotion " + promo_name + "...")
      promotion = Promo.Promo(promo_name)
    
#  /////////////////////////////////

  if not update_opt and not plot_opt:
    print("Please do something! Update or plot the promotion, but do not make me waste my time!")
    exit(0)

  if update_opt:
    if not student_opt and not file_opt:
      print("You need something to update : a student or an input file?")
      exit(0)
    if file_opt and student_opt:
      print("I can not guess wether you want to use student " + student_arg + " or file " + file_arg + " to update the promotion.")
      exit(0)
    if not file_opt and student_opt and not knowhow_opt:
      print("You need to tell me which knowhow to update for " + student_arg + " (use -k option to specify it and -m option to add a grade).")
      exit(0)
    if not file_opt and student_opt and knowhow_opt and not mark_opt:
      print("You need to tell me which grade to add to knowhow " + knowhow_arg + " to student " + student_arg + ". Use -m option.")
      exit(0)
      
    if not promotion.IsStudent(student_arg):
      bool_add = input("Student " + student_arg + " is not in promotion " + promo_name + ", do you want to add him/her?")
      while bool_add != "y" and bool_add != "n":
        bool_add = input("Please answer by y or n")
      if bool_add == "n":
        print("Ok ciao")
        exit(1)
      print("Adding student " + student_arg + " to promotion " + promo_name + "...")
      promotion.AddStudent(Student.Student(student_arg))
      
    if not promotion.GetStudent(student_arg).IsKnowhow(knowhow_arg):
      bool_add = input("Knowhow " + knowhow_arg + " is not a knowhow of student " + student_arg + ", do you want to add it?")
      while bool_add != "y" and bool_add != "n":
        bool_add = input("Please answer by y or n")
      if bool_add == "n":
        print("Ok ciao")
        exit(1)
      print("Adding knowhow " + knowhow_arg + " to student " + student_arg + "...")
      promotion.GetStudent(student_arg).AddKnowhow(knowhow_arg)
      
    print("Adding grade " + mark_arg + " to " + student_arg + "\'s knowhow " + knowhow_arg + "...")
    promotion.GetStudent(student_arg).AddMark(knowhow_arg, mark_arg)
  
  if plot_opt:
    promotion.PlotAll()  
      
  promotion.Save()
    

  exit(1)
    
if __name__ == '__main__':
  if len(sys.argv) == 1:
    usage()
    exit(0)
  main(sys.argv[1:])
