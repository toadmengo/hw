import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time
from logininfo import *

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver=webdriver.Chrome(PATH)
driver.minimize_window()
driver.get("https://apps.canvas.uw.edu/wayf")

driver.find_element_by_id("login").click()

def uwLogin():
    user = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "weblogin_netid"))
    )
    user.send_keys(netID)
    password = driver.find_element_by_id("weblogin_password")
    password.send_keys(uwpass)
    password.send_keys(Keys.RETURN)

uwLogin()

driver.get('https://www.webassign.net/washington/login.html')
driver.find_element_by_id("loginbtn").click()

with open('assignments.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    try:
        dashboard = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "js-student-myAssignmentsWrapper"))
        )
        assigns= dashboard.find_elements_by_tag_name('li')
        course= 'MATH 126'
        startdate='NA'
        for assign in assigns:
            assignment = assign.find_element_by_class_name('css-4qmd1n').text
            due = assign.find_element_by_class_name('css-atykpv').text
            duedate = due.split(',')[1]
            duedate = duedate[1:]
            writer.writerow([course, assignment, startdate, duedate])

    finally:
        driver.quit()

