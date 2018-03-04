import json,urllib.request

class Api():
  def __init__(self, url):
      self.url = url
  def json(self):
      data = urllib.request.urlopen(self.url).read()
      return json.loads(data)
