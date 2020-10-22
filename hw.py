import smtplib
from email.message import EmailMessage
import calendar

from logininfo import *
import canvas2
import Webassign
import CSE142
import organize
from organize import urgentassigns, assignmentlist

message=''
for assign in urgentassigns:
    message = message + assign[0] + ': ' + assign[1] + ' is due ' + str(assign[3]) + ', ' + str(calendar.day_name[assign[3].weekday()]) +'\n'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(gmail1, passw)
server.sendmail(gmail1,
    'toddmeng@uw.edu',
    message)
print('email sent!')

server.close()