# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 18:15:59 2022 at Grenoble École de Management (Grenoble, France)

@author: tim565
"""
import time
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

employeeCountsInput = input("Insert y to add number of employees, insert n for no number of employees then press enter:")
if employeeCountsInput == "y":
    employeeCounts = input("Use this format: 10-49_50-199_200%2B; emplyeeCounts: ")
    url = url + "&employeeCounts=" + employeeCounts

print("Full url:", url)
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
print("Info: Cookie button clicked \nInfo: Ready to start search")

"""
TODO: next steps
"""
company_name_list = []
company_plz_city_list = []
company_description_list = []

"""
Clean and close
"""
time.sleep(10)
print("Info: Timer out, quitting website...")
driver.quit()
print("--- Company Register Finished --- (Code: 0) ")