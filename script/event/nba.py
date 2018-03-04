import utility.time as now
import utility.request as request

class Games():
  def __init__(self, data):
    self.team = data[0]
    self.dateRange = data[1]

  def data(self):
    EST = now.Zone(-5,False,'EST')
    currentDate = now.datetime.now(EST).strftime('%Y-%m-%d')
    offsetDate = now.timedelta(days = int(self.dateRange) + 1)
    prevDate = now.datetime.strptime(str(now.datetime.now(EST) - offsetDate)[:10], '%Y-%m-%d')
    nextDate = now.datetime.strptime(str(now.datetime.now(EST) + offsetDate)[:10], '%Y-%m-%d')

    year = int(now.datetime.now(EST).strftime('%Y'))
    month = int(now.datetime.now(EST).strftime('%m'))
    monthIndex = month

    # Map season indices 0-7 to months September to April
    if month >= 1 and month < 5:
        year = year - 1
        monthIndex = month + 3
    elif month >= 5 and month < 9:
        year = year - 1
        monthIndex = 7
    else:
        monthIndex = month - 9



    output = request.Api('http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/' + str(year) + '/league/00_full_schedule.json').json()

    def schedule(monthIndex):
        listObj = []

        for i in range(0, len(output['lscd'][monthIndex]['mscd']['g'])):
            arena = output['lscd'][monthIndex]['mscd']['g'][i]['an']
            city = output['lscd'][monthIndex]['mscd']['g'][i]['ac']
            state = output['lscd'][monthIndex]['mscd']['g'][i]['as']
            home = output['lscd'][monthIndex]['mscd']['g'][i]['h']
            visitor = output['lscd'][monthIndex]['mscd']['g'][i]['v']
            easternTimeZone = output['lscd'][monthIndex]['mscd']['g'][i]['etm']
            date = output['lscd'][monthIndex]['mscd']['g'][i]['gdte']
            dateValue = now.datetime.strptime(date, '%Y-%m-%d')

            if (self.team == visitor['ta'] or self.team == home['ta']) and dateValue > prevDate and dateValue < nextDate:
                dataObj = {
                  'arena': arena,
                  'city': city,
                  'state': state,
                  'date': date,
                  'etz': easternTimeZone[11:],
                  'vtn': visitor['tn'],
                  'vre': visitor['re'],
                  'vtc': visitor['tc'],
                  'vta': visitor['ta'],
                  'vs': visitor['s'],
                  'htn': home['tn'],
                  'hre': home['re'],
                  'htc': home['tc'],
                  'hta': home['ta'],
                  'hs': home['s'],
                }

                listObj.append(dataObj)

        return listObj

    if monthIndex > 0:
      # Display games from previous month and current month
      scheduleObj = schedule(monthIndex - 1)
      scheduleObj.extend(schedule(monthIndex))
      return scheduleObj
    else:
      return schedule(monthIndex)
