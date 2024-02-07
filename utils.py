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

# 1 
def patient_tracking(driver, patientName, visitStartTime, visitEndTime, evalDate, ROC, insurance, 
                           caregiverName, caregiverRltnshp, caregiverPhone):
    page = "Patient Tracking"
    input(f'{patientName} AUTOFILL {page}')
    try:
        driver.find_element_by_id("cTO_timein").send_keys(visitStartTime)  # timeIn
        driver.find_element_by_id("cTO_timeout").send_keys(visitEndTime)  # timeOut

        driver.find_element_by_id("cTO_visitdate").click()  # visitDate
        driver.find_element_by_id("cTO_visitdate").send_keys(evalDate)  # visit date


        #driver.find_element_by_id("M0032_ROC_DT_NA").send_keys(Keys.SPACE)  # ROC button


        # A1110 Language
        if ROC == 0:
            driver.find_element_by_id("A1110A").send_keys("English")
            driver.find_element_by_id("A1110B_1").send_keys(Keys.SPACE)
        elif ROC == 1:
            print("check language selection")

        if insurance == 'mcr':
            driver.find_element_by_id('M0150_CPAY_MCARE_FFS').send_keys(Keys.SPACE)
        elif insurance == 'mcrother':
            driver.find_element_by_id('M0150_CPAY_MCARE_HMO').send_keys(Keys.SPACE)
        elif insurance == 'com':
            driver.find_element_by_id('M0150_CPAY_PRIV_INS').send_keys(Keys.SPACE)

        enterCGinfo = input("Enter 'Emergency Contact'? yes or <enter>: ")
        if 'y' in enterCGinfo.lower():
            try:
                driver.find_element_by_id('cEC_ContactName').send_keys(caregiverName)
                driver.find_element_by_id('cEC_ContactRelationship').send_keys(caregiverRltnshp)
                driver.find_element_by_id('cEC_EmergencyPhoneA').send_keys(caregiverPhone[0])
                driver.find_element_by_id('cEC_EmergencyPhoneB').send_keys(caregiverPhone[1])
                driver.find_element_by_id('cEC_EmergencyPhoneC').send_keys(caregiverPhone[2])
            except:
                print("You need to manually enter contact info. Something is not right with it.")

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page



if __name__ == "__main__":
    
    
    driver = webdriver_init()
    open_browswer(driver, username='user_name')
    
