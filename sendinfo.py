import csv
import requests

url = 'http://toadmengo.pythonanywhere.com/addfrompython'
def main():
    with open('assignments+.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                duetimes = row[3].split("-")
                startimes = row[2].split("-")
                data = {'course': row[0], 'name': row[1], 'syear': startimes[0], 'smonth': startimes[1], 'sday': startimes[2], 'dyear': duetimes[0], 'dmonth': duetimes[1], 'dday': duetimes[2]}
                r = requests.post(url, data = data)
                print(r)
