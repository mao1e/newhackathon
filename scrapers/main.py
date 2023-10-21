import requests
from selenium import webdriver
from selenium.common import ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException, \
    JavascriptException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

start_time = time.time()

# Set up website object
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.ratemyprofessors.com/search/professors/1967")

def create_button(path):
    try:
        button = driver.find_element(By.XPATH, path)
    except NoSuchElementException:  # if the button is not on screen
        print("Button is not on screen.", path)
        return None
    else:
        return button


def click_button(path):
    try:
        button = create_button(path)
        button.click()
    except ElementClickInterceptedException:  # if the button is blocked by another element
        print("Button is blocked by another element.", button)
    except ElementNotInteractableException:  # if the button cannot be clicked
        print("Button is not clickable.", button)
    except AttributeError as e:
        print(f"An AttributeError occurred: {e}")


def scroll_to_button(path):
    try:
        button = create_button(path)
        driver.execute_script("arguments[0].scrollIntoView();", button)
        scroll_position = int(driver.execute_script("return window.pageYOffset;")) - 200
        driver.execute_script("window.scrollTo(0, " + str(scroll_position) + ");")
        return True
    except NoSuchElementException:
        print("Could not scroll.")
    except JavascriptException:
        print("Could not scroll.")
    return False


# Element for each button
cookie = "//button[text()='Close']"
ad = "//a[@id='bx-close-inside-1177612']"
show = "//button[text()='Show More']"


click_button(cookie)
click_button(ad)


# Clicks show more until there is no more
#limiter = 0
hasShowButton = True
while hasShowButton:
    time.sleep(1)
    if scroll_to_button(show):
        click_button(show)
    else:
        time.sleep(10)
        click_button(ad)
        hasShowButton = scroll_to_button(show)
    #limiter += 1
    #if limiter == 10:
    #    break


end_time = time.time()

# Set up BeautifulSoup
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")


# Create a list for all the elements
ratings = []
firstNames = []
lastNames = []
difficulties = []
real_difficulties = []

# Extract ratings, names and difficulties from the provided HTML
additional_ratings = soup.find_all('div', class_='CardNumRating__CardNumRatingNumber-sc-17t4b9u-2')
for rating in additional_ratings:
    ratings.append(rating.text)

additional_names = soup.find_all('div', class_='CardName__StyledCardName-sc-1gyrgim-0 cJdVEK')
for name in additional_names:
    name = name.text
    firstSpace = name.find(' ')
    lastSpace = name.rindex(' ')
    firstName = name[0:firstSpace].lower()
    lastName = name[lastSpace+1:len(name)].lower()
    firstNames.append(firstName)
    lastNames.append(lastName)

additional_difficulties = soup.find_all('div', class_='CardFeedback__CardFeedbackNumber-lq6nix-2 hroXqf')
i = 0  # Separate difficulties into two array because they have the same id
for difficulty in additional_difficulties:
    if i % 2 == 0:
        difficulties.append(difficulty.text)
    else:
        real_difficulties.append(difficulty.text)
    i += 1

# Record the data into a csv file
df = pd.DataFrame({'Rating': ratings, 'First Name': firstNames, 'Last Name': lastNames, 'Difficulty': real_difficulties})
df.to_csv('RMPSCRAPE.csv', index=False, encoding='utf-8')


print(ratings)
print(firstNames)
print(lastNames)
print(difficulties)
print(real_difficulties)
print(len(ratings))
print(end_time - start_time)


