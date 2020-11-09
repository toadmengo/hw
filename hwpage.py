from flask import Flask, redirect, url_for, render_template, session, flash, request
import csv
from datetime import date
import datetime
import calendar
from flask_sqlalchemy import SQLAlchemy

todlist=[]
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

            day = int(times[2])
            row.append(day)
            if today >= row[2] and today <= row[3]:
                row.append(1)
            else:
                row.append(0) 
            row.append(str(id))
            todlist.append(row)

            id += 1


app = Flask(__name__)
app.secret_key = "biden2020" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class assignments(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    course = db.Column(db.String(100))
    name = db.Column(db.String(300))
    startdate = db.Column(db.Date)
    duedate = db.Column(db.Date)
    status = db.Column(db.Integer)

    
    def __init__(self, course, name, startdate, duedate, status):
        self.course = course
        self.name = name
        self.startdate = startdate
        self.duedate = duedate
        self.status = status



@app.route("/")
def home():
    return redirect(url_for("first"))

@app.route("/first", methods = ['POST', 'GET'])
def first():

    today= date.today()
    tod = today.day

    datelist=[]
    monthrange = calendar.monthrange(today.year, today.month)[1]
    for i in range(monthrange):
        datelist.append([datetime.date(today.year, today.month, i+1), i+1])
    month = calendar.month_name[today.month]

    tomdatelist=[]
    if today.month!=12:
        tommonthrange = calendar.monthrange(today.year, today.month+1)[1]
        tommonth = calendar.month_name[today.month+1]
        nextmonth = datetime.date(today.year, today.month+1, 1)
    else:
        tommonthrange = calendar.monthrange(today.year+1, today.month-11)[1]
        tommonth = calendar.month_name[today.month-11]
        nextmonth = datetime.date(today.year+1, today.month-11, 1)

    for i in range(tommonthrange):
        try:
            tomdatelist.append([datetime.date(today.year, today.month+1, i+1), i+1])
        except:
            tomdatelist.append([datetime.date(today.year+1, today.month-11, i+1), i+1])

    for i in todlist:
        foundassignment = assignments.query.filter_by(name=i[1]).first()
        if not foundassignment:
            print('added!')
            newassign = assignments(i[0], i[1], i[2], i[3], i[5])
            db.session.add(newassign)
            db.session.commit()

    if request.method == 'POST':      
        change = False
        assi = assignments.query.all()
        for i in assi:
            try:
                status = request.form[f"{i._id}"]
                change = True
                changestatus = True
                print('change')
            except:
                changestatus=False
                pass
            
            if changestatus: ### post method of checkbox switches the status of the assignment
                foundassignment = assignments.query.filter_by(name=i.name).first()
                if foundassignment:
                    print('changed!')
                    foundassignment.status = status
                    db.session.commit()
                else:
                    print('added!')
                    newassign = assignments(i[0], i[1], i[2], i[3], status)
                    db.session.add(newassign)
                    db.session.commit()
                    
        if change:
            flash("Changes marked", "info")
            
        return redirect(url_for("first"))

    gap = calendar.monthrange(today.year, today.month)[0]-1
    qry = assignments.query.all()
    return render_template("firstmonth.html", assignmentlist= qry, datelist = datelist, gap = gap, today= tod, month = month, todaymonth = today.month)

@app.route("/view")
def view():
    return render_template("view.html", values = assignments.query.all())

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
    db.create_all()
    app.run(debug=True)