# Import necessary packages
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
from selenium.webdriver.common.by import By

# Set up the Selenium webdriver
browser = webdriver.Chrome()
browser.get("https://www.linkedin.com")

print("Set up the Selenium webdriver")

# Log in to LinkedIn
username = "sandumijayasekara@gmail.com"
password = "Sandumi@0915"
print("Log in to LinkedIn")

browser.find_element(By.ID,'session_key').send_keys(username)
browser.find_element(By.ID,'session_password').send_keys(password)
browser.find_element(By.CLASS_NAME,'sign-in-form__submit-button').click()

print("Search for RPA jobs and filter the results")
# Search for RPA jobs and filter the results
search_term = "RPA"
job_listings = []

time.sleep(10) 
browser.find_element(By.XPATH,'//*[@id="global-nav-typeahead"]/input').send_keys(search_term)
browser.find_element(By.XPATH,'//*[@id="global-nav-typeahead"]/input').submit()

browser.find_element(By.CSS_SELECTOR,'button.artdeco-dropdown__trigger--placement-top').click()
time.sleep(2)  # Allow time for dropdown to appear
browser.find_element(By.XPATH,'//span[text()="Date Posted"]').click()

# Scrape the job listings
soup = BeautifulSoup(browser.page_source, 'html.parser')

for listing in soup.find_all('li', {'class': 'jobs-search-results__list-item'}):
    title = listing.find('h3', {'class': 'job-card-search__title'}).get_text().strip()
    desc = listing.find('div', {'class': 'job-card-search__description'}).get_text().strip()
    apply_link = listing.find('a', {'class': 'job-card-search__link-wrapper'}).get('href')
    
    job_listings.append({'Title': title, 'Description': desc, 'Link': apply_link})

# Store the scraped data in an Excel file
df = pd.DataFrame(job_listings)
df.to_excel('rpa_jobs.xlsx', index=False)

# Send the Excel file as an email attachment
from_email = "sandumijayasekara@gmail.com"
to_email = "sandumijayasekara@gmail.com"
password = "1QAZ2wsx@1993"

msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = "RPA Job Listings"

part = MIMEBase('application', "octet-stream")
part.set_payload(open("rpa_jobs.xlsx", "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="rpa_jobs.xlsx"')

msg.attach(part)

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.login(from_email, password)
smtpObj.sendmail(from_email, to_email, msg.as_string())
smtpObj.quit()
