import os

class Relative():
  def __init__(self, relativePath):
      self.relativePath = relativePath
  def path(self):
      return os.path.join(os.getcwd(), self.relativePath)
