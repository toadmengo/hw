from flask import Flask, redirect, url_for, render_template, session, flash, request
import csv
from datetime import date
import datetime
import calendar

todlist=[]
tomlist=[]
today= date.today()
tod = today.day
with open('assignments+.csv') as csvfile:
    reader = csv.reader(csvfile)
    id = 0
    for row in reader:
        if row:
            times = row[3].split("-")
            row[3] = datetime.date(int(times[0]), int(times[1]), int(times[2]))
            startimes = row[2].split("-")
            row[2] = datetime.date(int(startimes[0]), int(startimes[1]), int(startimes[2]))
            if row[3].month == today.month:
                day = int(times[2])
                row.append(day)
                if today >= row[2] and today <= row[3]:
                    row.append(1)
                else:
                    row.append(0) 
                row.append(str(id))
                todlist.append(row)
            if row[3].month == today.month+1 or row[3].month == today.month-11:
                day = int(times[2])
                row.append(day)
                if today >= row[2] and today <= row[3]:
                    row.append(1)
                else:
                    row.append(0) 
                row.append(str(id))
                tomlist.append(row)
            id += 1

datelist=[]
monthrange = calendar.monthrange(today.year, today.month)[1]
for i in range(monthrange):
    datelist.append([datetime.date(today.year, today.month, i+1), i+1])
month = calendar.month_name[today.month]

tomdatelist=[]
if today.month!=12:
    tommonthrange = calendar.monthrange(today.year, today.month+1)[1]
    tommonth = calendar.month_name[today.month+1]
else:
    tommonthrange = calendar.monthrange(today.year+1, today.month-11)[1]
    tommonth = calendar.month_name[today.month-11]
for i in range(tommonthrange):
    try:
        tomdatelist.append([datetime.date(today.year, today.month+1, i+1), i+1])
    except:
        tomdatelist.append([datetime.date(today.year+1, today.month-11, i+1), i+1])


app = Flask(__name__)
app.secret_key = "biden2020" 

@app.route("/", methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':      
        change = False
        for i in todlist:
            try:
                status = request.form[f"{i[6]}"]
                change = True
                print(i, status) ### post method of checkbox switches the status of the assignment
            except:
                pass
        if change:
            flash("Changes marked", "info")
        return redirect(url_for("home"))

    gap = calendar.monthrange(today.year, today.month)[0]-1
    return render_template("firstmonth.html", assignmentlist= todlist, datelist = datelist, gap = gap, today= tod, month = month)

@app.route("/next", methods = ['POST', 'GET'])
def next():
    if request.method == 'POST':      
        change = False
        for i in tomlist:
            try:
                status = request.form[f"{i[6]}"]
                change = True
                print(i, status) ### post method of checkbox switches the status of the assignment
            except:
                pass
        if change:
            flash("Changes marked", "info")
        return redirect(url_for("next"))

    if today.month != 12:
        gap = calendar.monthrange(today.year, today.month+1)[0]-1
    else:
        gap = calendar.monthrange(today.year+1, today.month-11)[0]-1
    return render_template("nextmonth.html", assignmentlist= tomlist, datelist = tomdatelist, gap = gap, today= -1, month = tommonth)

if __name__ == "__main__":
    app.run(debug=True)