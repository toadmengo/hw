import csv
import datetime

assignmentlist=[]
sortlist=[]
urgentassigns=[]

def convertMonth(month):
    if month == 'Oct':
        return 10
    elif month == 'Nov':
        return 11
    elif month == 'Dec':
        return 12
    elif month == 'NA':
        return 1
    else:
        return int(month)
        
with open('assignments.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        assignmentlist.append(row)

for row in assignmentlist:
    stdate = row['startdate'].split(" ")
    if len(stdate)>1: 
        stdate[0] = convertMonth(stdate[0])
        stdate[1] = int(stdate[1])
    else:
        stdate= [1,1]
    ddate = row['duedate'].split(" ")
    if len(ddate)>1:
        ddate[0] = convertMonth(ddate[0])
        ddate[1] = int(ddate[1])
    else:
        ddate=[1,1]
    sortlist.append([row['course'], row['assignment'], datetime.date(2020, stdate[0], stdate[1]), datetime.date(2020, ddate[0], ddate[1])])

for i in range(len(sortlist)):
    for i in range(len(sortlist)-1):
        if sortlist[i][3]>sortlist[i+1][3]:
            temp = sortlist[i+1]
            sortlist[i+1] = sortlist[i]
            sortlist[i] = temp
            temp = assignmentlist[i+1]
            assignmentlist[i+1] = assignmentlist[i]
            assignmentlist[i] = temp

with open('assignments+.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for row in sortlist:
        writer.writerow(row)

now=datetime.date.today()
for row in sortlist:
    if (row[3]-now <= datetime.timedelta(7) and row[3]-now >= datetime.timedelta()):
        urgentassigns.append(row)






