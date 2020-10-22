import csv
from bs4 import BeautifulSoup
import requests
from requests_html import HTML, HTMLSession

csv_file= open('assignments.csv', 'a')
csv_writer= csv.writer(csv_file)

session = HTMLSession()
r = session.get("https://courses.cs.washington.edu/courses/cse142/20au/calendar.html")
assignmentlist=[]
releasedlist=[]

days = r.html.find('.day')
for day in days:
    assignmentscol = day.find('.assignments', first=True)
    try:
        assignments = assignmentscol.find('.rect', first=True)
        words = assignments.text.split(' ')
        if words[2] != 'released':
            date= day.find('.date', first= True).text
            date = date[5:] + ' ' + date[0:3]
            link= assignments.attrs['href']
            course='CSE 142'
            assignname= words[0] + ' ' + words[1]
            assignmentlist.append([course, assignname , 'NA', date])
        elif words[2] == 'released':
            releasedlist.append([assignments.text, date])
    except:
        pass
for released in releasedlist:
    words = released[0].split(' ')
    for assign in assignmentlist:
        check = assign[1].split(' ')
        if check[0] == words[0] and check[1] == words[1]:
            assign[2] = released[1]

for assign in assignmentlist:
    csv_writer.writerow(assign)

csv_file.close()
