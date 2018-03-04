import json
import utility.request as request
import utility.directory as directory

path = directory.Relative('../config-python-scripts/config.json').path()
forecastApiKey = json.load(open(path))['forecastApiKey']

class Days:
    def __init__(self, data):
        cityNameArray = data[0].lower().split(' ')
        cityNameArrayCapitalized = list(map(lambda x: x.capitalize(), cityNameArray))
        self.cityUnder = '_'.join(cityNameArrayCapitalized)
        self.citySpace = ' '.join(cityNameArrayCapitalized)
        self.state = data[1].upper()
        self.dateRange = int(data[2])

    def data(self):
        output = request.Api('http://api.wunderground.com/api/' + forecastApiKey + '/forecast10day/q/' + self.state + '/' + self.cityUnder + '.json').json()

        forecastDate = output['forecast']['txt_forecast']['date']
        forecastDay = output['forecast']['txt_forecast']['forecastday']

        listObj = []
        metaObj = {
          'city': self.citySpace,
          'state': self.state,
          'time': forecastDate,
        }
        listObj.append(metaObj)

        forecastDays = len(forecastDay)
        if (self.dateRange >= 0 and self.dateRange < 20):
            forecastDays = self.dateRange * 2

        for i in range(0, forecastDays):
            dataObj = {
              'day': forecastDay[i]['title'],
              'celsius': forecastDay[i]['fcttext_metric'],
              'fahrenheit': forecastDay[i]['fcttext'],
              'icon': forecastDay[i]['icon'],
              'iconUrl': forecastDay[i]['icon_url']
            }
            listObj.append(dataObj)

        return listObj
