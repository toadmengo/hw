import requests
import json
from bs4 import BeautifulSoup
import csv
from logininfo import canvasToken

def dateformat(date):
    time = date.split('T')
    date = time[0].split('-')
    time = date[1] + ' ' + date[2]
    return time

csv_file = open('assignments.csv', 'w')
csv_writer= csv.writer(csv_file)
csv_writer.writerow(['course', 'assignment', 'startdate', 'duedate'])

token = canvasToken
url = 'https://canvas.instructure.com/api/v1/courses/?'

param = {'access_token': token}
r = requests.get(url, params=param)
class_list = r.json()


classID=[]
assignmentlists=[]
for course in class_list:
    coursewords = course['name'].split(' ')
    coursename=coursewords[0] + " " + coursewords[1]
    if len(coursewords[2])==1:
        coursename=coursename + " " + coursewords[2]

    cID=course['id']
    assignmenturl = f'https://canvas.instructure.com/api/v1/courses/{cID}/assignments?'
    ar = requests.get(assignmenturl, params=param)
    assignments=ar.json()
    for assignment in assignments:
        duedate = assignment['due_at']
        if duedate == None:
            due = 'NA'
        else:
            due = dateformat(duedate)
        startdate = assignment['unlock_at']
        if startdate == None:
            start = 'NA'
        else:
            start=dateformat(startdate)
        assign = assignment['name']
        csv_writer.writerow([coursename, assign, start, due])
        
csv_file.close()

    





