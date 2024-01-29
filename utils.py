# utils
import traceback, sys
sys.path.append("C:\\users\\oto23\\AppData\\Roaming\\Python\\Python39\\site-packages")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def webdriver_init():
    driver = webdriver.Chrome("C:\\Program Files\Google\Chrome\Application\chromedriver")
    return driver

def open_browswer(driver, username):
    driver.get("https://kinnser.net/login.cfm")
    userElem = driver.find_element_by_id("username")
    userElem.send_keys(username)
    userElem.send_keys(Keys.TAB)

def autofill_error(page, patientName):
    print(f"***** {page} AUTOFILL ERROR *****")
    errorFile = open(f'{patientName}_{page}_error_file', 'w')
    errorFile.write(traceback.format_exc())
    errorFile.close()
    print('Traceback written to file.')

def pause_to_autofill(page):
    input(f"AUTOFILL {page}.")

def scroll_up_then_pause(driver, page):
    driver.find_element_by_tag_name('html').send_keys(Keys.HOME)
    input(f"'Save & Cont' {page}.")
    driver.find_element_by_id("oasisSaveContinueButton").click()  # 'save and continue'

def clearLink():
    for i in range(len(linksToClear)):
        driver.find_element_by_id('clearLink' + str(linksToClear[i])).click()
    input("<Enter> when all sections cleared and ready to autofill page")

# dummy function to test f strings
def funct(patientName, page):
    print(f'here we have {patientName} on page {page}')


def comm_note(driver, patientName, text):
    page = "Comm note"
    input(f'{patientName} AUTOFILL {page}')
    try:
        driver.find_element_by_id("CallSummary").send_keys(text)
    except:
        autofill_error(page, patientName)





if __name__ == "__main__":
    
    
    driver = webdriver_init()
    open_browswer(driver, username='user_name')
    
