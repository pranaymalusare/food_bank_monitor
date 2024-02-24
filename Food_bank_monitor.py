from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import yagmail
import os

def send_email():
    sender = os.getenv('MY_EMAIL')
    password = os.getenv('MY_PASSWORD')
    receiver = os.getenv('MY_RECEIVER')  
    subject = 'Food Bank Booking Open!'
    body = 'The food bank booking is now open. Visit the site to book.'
    yag = yagmail.SMTP(user=sender, password=password)

    try:
        yag.send(to=receiver, subject=subject, contents=body)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_food_bank_open():
    url = 'https://outlook.office365.com/owa/calendar/SMUCommunityFoodRoom@smuhalifax.onmicrosoft.com/bookings/'

    try:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        while True:
            dates = driver.find_elements(By.XPATH, "//div[@class='date circle']")
            if dates:  # Check if date elements are present
                for date in dates:
                    if "bookable" in date.get_attribute("class"):
                        print(f"Bookable date found: {date.text}")
                        send_email()
            else:
                print("No slots available at the moment.")

            time.sleep(60)  # Check every minute

    except Exception as e:
        print(f"Error checking the site: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    check_food_bank_open()
