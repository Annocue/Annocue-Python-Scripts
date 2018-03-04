import json
import utility.request as request
import utility.directory as directory

path = directory.Relative('../config-python-scripts/config.json').path()
stockApiKey = json.load(open(path))['stockApiKey']

class Prices:
  def __init__(self, data):
      self.stock = data if type(data) is list else [data]

  def data(self):
      listObj = []

      for i in range(0, len(self.stock)):
          output = request.Api('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + self.stock[i] + '&apikey=' + stockApiKey).json()
          lastRefresh = output['Meta Data']['3. Last Refreshed']
          stockDetails = output['Time Series (Daily)'][lastRefresh]

          dataObj = {
            'stock': self.stock[i].upper(),
            'date': lastRefresh,
            'open': stockDetails['1. open'],
            'high': stockDetails['2. high'],
            'low': stockDetails['3. low'],
            'adjusted': stockDetails['5. adjusted close'],
            'volume': stockDetails['6. volume'],
            'dividend': stockDetails['7. dividend amount'],
            'split': stockDetails['8. split coefficient'],
          }

          listObj.append(dataObj)

      return listObj
