class promo:
  def __init__(self, name):
    self.name = name
    self.knowhows = {}
    
  def addsknowhow(self, knowhow):
    self.knowhows.append(knowhow)
