# -*- coding: utf-8 -*-

"""
Created on Mon Oct  3 18:15:59 2022 at Grenoble École de Management (Grenoble, France)

@author: tim565
"""
import time
import datetime
import csv
import math
from selenium import webdriver
from selenium.webdriver.common.by import By


# Class variables
company_data_list = []
get_variables = ""

def removeHtmlTags(item):
    for a in range(len(item)):
        if item[a] == "<" and item[a+1] == "e" and item[a+2] == "m" and item[a+3] == ">":
            item = item[:a] + item[(a+4):]
            break
    for a in range(len(item)):
        if item[a] == "<" and item[a+1] == "/" and item[a+2] == "e" and item[a+3] == "m" and item[a+4] == ">":
            item = item[:a] + item[(a+5):]
            break
    for a in range(len(item)):
        if item[a] == "&" and item[a+1] == "a" and item[a+2] == "m" and item[a+3] == "p":
            item = item[:a-1] + item[(a+5):]
            break
    for a in range(len(item)):
        if item[a] == ";":
            item = item[:a] + "," + item[a:]
            break
    return item

def getCountry(item):
    country = item[:2]
    return country

def getPlz(item):
    plz = item[3:8]
    return plz

def getCity(item):
    city = item[9:]
    return city

# --- 1. INPUTS --- 1. INPUTS --- 1. INPUTS --- 1. INPUTS --- 1. INPUTS --- 1. INPUTS --- 1. INPUTS --- 1. INPUTS --- 1. INPUTS
"""
The user needs to specify parameters for the search in the database. 
The parameter 'q' is the only mandatory, it specifies a word for the search engine. All other params are optional. 
"""
print("--- Company Register Started ---")
q = input("q: ")
get_variables = "?q=" + q

siteNumberInput = input("Insert y to add a number of site to start from, then press enter: ")
if siteNumberInput == "y":
    siteNumber = int(input("Site number: ") or "0")

locationLinkInput = input("Insert y to add a link for the location [exclude & signs], then press enter: ")
if locationLinkInput == "y":
    locationLink = input("Link for location: ")
    get_variables = "?q=" + q + "&" + locationLink

employeeCountsInput = input("Insert y to add number of employees, insert n for no number of employees then press enter: ")
if employeeCountsInput == "y":
    employeeCounts = input("Use this format: 10-49_50-199_200%2B; emplyeeCounts: ")
    get_variables = get_variables + "&employeeCounts=" + employeeCounts

print("HTTP GET variables:", get_variables)
printout = input("Insert y if you would like to print all companies in terminal: ")
input("Press enter to start company search")
# --- 1. END INPUTS --- 1. END INPUTS --- 1. END INPUTS --- 1. END INPUTS --- 1. END INPUTS --- 1. END INPUTS --- 1. END INPUTS

# --- 2. GET NUM_OF_COMPANIES --- 2. GET NUM_OF_COMPANIES --- 2. GET NUM_OF_COMPANIES --- 2. GET NUM_OF_COMPANIES --- 2. GET NUM_OF_COMPANIES
driver = webdriver.Firefox()
driver.get(str("https://www.wlw.de/de/suche/"+get_variables))
print("Info: Loading website...")
time.sleep(5)

# Remove cookie button
btn_cookie = driver.find_element(By.ID, "CybotCookiebotDialogFooterButtonAcceptAll")
btn_cookie.click()
print("Info: Cookie button clicked \nInfo: Searching for companies...")

total_num_of_companies_with_text = driver.find_element(By.XPATH, "//a[@class='search-tab-link search-tabs-supplier-link active']").get_attribute("innerHTML")
total_num_of_companies = ""
for i in range(len(total_num_of_companies_with_text)):
    if total_num_of_companies_with_text[i] == "0" or total_num_of_companies_with_text[i] == "1" or total_num_of_companies_with_text[i] == "2" or total_num_of_companies_with_text[i] == "3" or total_num_of_companies_with_text[i] == "4" or total_num_of_companies_with_text[i] == "5" or total_num_of_companies_with_text[i] == "6" or total_num_of_companies_with_text[i] == "7" or total_num_of_companies_with_text[i] == "8" or total_num_of_companies_with_text[i] == "9":
        total_num_of_companies = total_num_of_companies + total_num_of_companies_with_text[i]
num_of_companies_rest = str(int(total_num_of_companies)%30)
total_num_of_sites = str(math.trunc(int(total_num_of_companies)/30))
print("Info: Total number of sites in this search: ", total_num_of_sites, ", rest: ", num_of_companies_rest)
driver.quit()
# --- 2. END GET NUM_OF_COMPANIES --- 2. END GET NUM_OF_COMPANIES --- 2. END GET NUM_OF_COMPANIES --- 2. END GET NUM_OF_COMPANIES

# --- 3. ITERATE THROUGH SITES --- 3. ITERATE THROUGH SITES --- 3. ITERATE THROUGH SITES --- 3. ITERATE THROUGH SITES ---
for i in range(int(total_num_of_sites)):
    i = i + siteNumber

    # Start webdriver and wait 5 seconds until the website has load and the cookie button popped up
    driver = webdriver.Firefox()
    driver.get(str("https://www.wlw.de/de/suche/page/"+str(i+1)+"/"+get_variables))
    print("Info: Loading website...")
    time.sleep(5)

    # Remove cookie button
    btn_cookie = driver.find_element(By.ID, "CybotCookiebotDialogFooterButtonAcceptAll")
    btn_cookie.click()
    print("Info: Cookie button clicked \nInfo: Searching for companies...")

    # Iterate through list with 30 (default) items
    for i in range(30):
        path_company_name = "//div[@class='flex flex-col gap-y-2']/div[" + str(i+1) + "]//a[@class='company-title-link']/span"
        path_company_plz_city = "//div[@class='flex flex-col gap-y-2']/div[" + str(i+1) + "]//div[@class='address']"

        company_name = driver.find_element(By.XPATH, path_company_name).get_attribute("innerHTML")
        company_plz_city = driver.find_element(By.XPATH, path_company_plz_city).get_attribute("innerHTML")
        # --- 3.1 Remove html items left in strings --- 3.1 Remove html items left in strings --- 3.1 Remove html items left in strings
        company_name = removeHtmlTags(company_name)
        company_plz_city = removeHtmlTags(company_plz_city)
        # --- 3.1 END Remove html items left in strings --- 3.1 END Remove html items left in strings --- 3.1 END Remove html items left in strings

        if printout == "y":
            print("Output Nr: ",i,", Name: ",company_name,", Plz-City: ",company_plz_city)
        company_data_list.append([company_name, getCountry(company_plz_city), getPlz(company_plz_city), getCity(company_plz_city)])
    driver.quit()


    header = ["company_name", "company_country", "company_plz", "company_city"]
    file_name = str(datetime.datetime.now())
    with open(file_name+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(header)
        writer.writerows(company_data_list)
# --- 3. END ITERATE THROUGH SITES --- 3. END ITERATE THROUGH SITES --- 3. END ITERATE THROUGH SITES --- 3. END ITERATE THROUGH SITES ---

# --- 4. OUTPUTS --- 4. OUTPUTS --- 4. OUTPUTS --- 4. OUTPUTS --- 4. OUTPUTS --- 4. OUTPUTS --- 4. OUTPUTS --- 4. OUTPUTS ---
# Store results in .csv file
header = ["company_name", "company_country", "company_plz", "company_city"]
file_name = input("Enter a name for the .csv to store results: ")
with open(file_name+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(header)
    writer.writerows(company_data_list)

time.sleep(10)
print("Info: Timer out, quitting website...")
print("--- Company Register Finished --- (Code: 0) ")
# --- 4. END OUTPUTS --- 4. END OUTPUTS --- 4. END OUTPUTS --- 4. END OUTPUTS --- 4. END OUTPUTS --- 4. END OUTPUTS --- 4. END OUTPUTS ---
