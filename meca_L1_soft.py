import glob
import sys
import string
import os
import re
import shutil
import math
import time
from subprocess import call
from datetime import datetime
from datetime import timedelta

import source/promo.py
import source/student.py

def GetCurrentPromoName():
  CurrDate =  time.strftime("%x").split("/")
  if float(CurrDate[0]) > 8:     #Si on est après août
    return CurrDate[2] + "-" + str(int(CurrDate[2])+1)
  

if __name__ == '__main__':
  exit(1)
