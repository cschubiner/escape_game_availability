import json

def get_score(month, day, time, spots, dayName):
    s = 0
    if (month == 'July' and day >= 5 and day <= 21) or (month == 'August' and day >= 14 and day <= 25):
        s -=100000
    if time < 12:
        s -= 500000

    if dayName == 'Friday' or dayName == 'Saturday':
        s += 500

    s += 1000*spots
    s += -10*day
    s -= time
    return s

dates = None
with open('room_escape_dates.json','r') as j:
    dates = json.load(j)

dList = list()
for dateStr in dates:
    if 'Today' in dateStr or 'Tomorrow' in dateStr:
        continue

    month, dayNum = dateStr.split(',')[1].split()
    dayNum = int(dayNum)
    dayName = dateStr.split(',')[0].strip()
    for time in dates[dateStr]:
        eventTime = time['eventTime']
        timeNum = int(eventTime.split(':')[0])
        if 'PM' in eventTime and timeNum != 12:
            timeNum += 12
        spots = int(time['available'])
        dList.append((get_score(month, dayNum, timeNum, spots, dayName), dateStr + ' at ' + eventTime, month, dayNum, timeNum, spots))

dSet = set()
for t in sorted(dList, reverse=True)[:20]:
    score, dateStr, month, dayNum, timeNum, spots = t
    dSet.add((month, dayNum))
    if len(dSet) > 6:
        break
    print dayNum, t[1]
    # print 'ZZ', t
