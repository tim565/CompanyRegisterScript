# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 18:15:59 2022 at Grenoble École de Management (Grenoble, France)

@author: tim565
"""
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

"""
The user needs to specify parameters for the search in the database. 
The parameter 'q' is the only mandatory, it specifies a word for the search engine. All other params are optional. 
"""
print("--- Company Register Started ---")
q = input("q: ")
url = "https://www.wlw.de/de/suche?q=" + q

locationInput = input("Insert y to add a location, insert n for no location, then press enter: ")
if locationInput == "y":
    locationCountry = "DE"
    url = url + "&locationCountry=" + locationCountry
    locationKind = "other"
    url = url + "&locationKind=" + locationKind

    locationLatitude = input("locationLatitude: ")
    url = url + "&locationLatitude=" + locationLatitude
    locationLongitude = input("locationLongitude: ")
    url = url + "&locationLongitude=" + locationLongitude

    locationName = input("locationName: ")
    url = url + "&locationName=" + locationName + ",%20Deutschland"

    locationRadius = input("locationRadiusInput: ")
    url = url + "&locationRadius=" + locationRadius + "km"

supplierTypesInput = input("Insert y to add a supplier type, insert n for no supplier type, then press enter: ")
if supplierTypesInput == "y":
    supplierTypes = input("Use one or more of these: Hersteller_Händler_Dienstleister_Großhändler; supplierTypes: ")
    url = url + "&supplierTypes=" + supplierTypes

employeeCountsInput = input("Insert y to add number of employees, insert n for no number of employees then press enter: ")
if employeeCountsInput == "y":
    employeeCounts = input("Use this format: 10-49_50-199_200%2B; emplyeeCounts: ")
    url = url + "&employeeCounts=" + employeeCounts

print("Full url:", url)
printout = input("Insert y if you would like to print all companies in terminal: ")
input("Press enter to start company search")

"""
After the search params are entered and the URL is generated, the script uses selenium to access the website. 
"""
# Start webdriver and wait 5 seconds until the website has load and the cookie button popped up
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(url)
print("Info: Loading website...")
time.sleep(5)

# Remove cookie button
btn_cookie = driver.find_element(By.ID, "CybotCookiebotDialogFooterButtonAcceptAll")
btn_cookie.click()
print("Info: Cookie button clicked \nInfo: Searching for companies...")

# TODO: specify page number before iterating (by change in the URL)

# Iterate through list with 30 (default) items
company_data_list = []
for i in range(30):
    # TODO: currently only full sites with 30 items can be accessed; check for next item and break if necessary
    path_company_name = "//div[@class='flex flex-col']/div[" + str(i+1) + "]/a[@class='company-title-link']"
    path_company_plz_city = "//div[@class='flex flex-col']/div[" + str(i+1) + "]//div[@class='address']"
    path_company_description = "//div[@class='flex flex-col']/div[" + str(i+1) + "]/div[@class='description']"

    company_name = driver.find_element(By.XPATH, path_company_name).get_attribute("innerHTML")
    company_plz_city = driver.find_element(By.XPATH, path_company_plz_city).get_attribute("innerHTML")
    company_description = driver.find_element(By.XPATH, path_company_description).get_attribute("innerHTML")
    # TODO: filter out <em>q</em> and &amp that are set by website
    company_data_list.append([company_name, company_plz_city, company_description])

if printout == "y":
    for i in range(len(company_data_list)):
        print(i, ": ", company_data_list[i])

# Store results in .csv file
header = ["company_name", "company_plz_city", "company_description"]
file_name = input("Enter a name for the .csv to store results: ")
with open(file_name+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(header)
    writer.writerows(company_data_list)


"""
Clean and close
"""
time.sleep(10)
print("Info: Timer out, quitting website...")
driver.quit()
print("--- Company Register Finished --- (Code: 0) ")