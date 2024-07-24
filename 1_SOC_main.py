import utils, hidden_vars
import sys
from selenium.webdriver.common.by import By
sys.path.append(hidden_vars.filepath_patients)
from bs4 import BeautifulSoup as bs

# insert file name here
import patient_specific_filename as pt


# TODO GOALS!
# TODO FLU shot should only answer if it applies to Oct 1 - March 31

# Get apropriate username
if pt.branch == 0:
    username = hidden_vars.username_austin
elif pt.branch == 1:
    username = hidden_vars.username_san_antonio

####### variable manipulation #######

# check for cog impairments
cog_impairments_set = {'Alzheimer', 'CVA', 'stroke', 'TBI', 'Lewy', 'Huntington',
                       'Parkinson', 'dementia'}

dxs = ' '.join([pt.PMH, pt.medDx, pt.cause, pt.effect])
for cog_dx in cog_impairments_set:
    if cog_dx.lower() in dxs.lower():
        pt.cog_impairment = 1

# pressure scores
pt.pressure_sore_risk_comment = "Low Risk"
if pt.norton_score < 19:
    pt.pressure_sore_risk_comment = "Medium Risk"
if pt.norton_score < 14:
    pt.pressure_sore_risk_comment = "High Risk"
if pt.norton_score < 10:
    pt.pressure_sore_risk_comment = "Very High Risk"



# home bound status for ortho patients
pt.hbOrtho = utils.hb_ortho(pt.effect)

####### end #######

print("PTA: " + pt.pta + " CM: " + pt.CM + '\n')
print(pt.forcuraBlurb + '\n')
print("Wound care on orders: " + pt.woundCare + pt.woundCareCustom + '\n')

# initiate webdriver
driver = utils.webdriver_init()

# open browswer
utils.open_browswer(driver, username)

print("Please navigate to a comm note or a SOC page.")
input("Press <enter> when ready to autofill.")

fill_another_page = True
while fill_another_page == True:
    h1 = ""
    h2 = ""
    h3 = ""

    try:
        h1 = driver.find_element(By.CSS_SELECTOR, "h1").text
    except:
        answer = input("h1 not found in html code. <enter> to try again. 'goals' to enter goals.")
        if answer == "goals":
            utils.enter_goals(driver, pt.evalDate, pt.ptPOC)

    #### fill out SOC ROC report
    if h1 == "Patient Communication":
        utils.comm_note(driver, pt.patientName, text=pt.SOCrocReport)
        print("Please navigate to a SOC page. Recommended: 'Patient Tracking'.")
        input("Press <enter> when ready to autofill.")

    ##### Pull h3 heading to find page
    elif "Start of Care" in h1:
        try:
            h3 = driver.find_element(By.CSS_SELECTOR, "h3").text
        except:
            input("h3 not found in html code. <enter> to try again.")

        ##### 1 Patient Tracking
        if h3 == "Patient Tracking":
            utils.patient_tracking(driver, h3, pt.patientName, pt.visitStartTime, pt.visitEndTime, pt.evalDate, pt.ROC,
                                pt.insurance, pt.caregiverName, pt.caregiverRltnshp, pt.caregiverPhone)

        ##### 2 Administrative
        elif h3 == "Administrative":
            utils.administrative(driver, h3, pt.patientName, pt.evalDate, pt.dcDate, pt.medDx, pt.SurgicalSOC)

        ##### 3 Vitals
        elif h3 == "Vitals":
            pass

        ##### All pages are competed, but not publicly available

        else:
            print("h3 = " + str(h3))
            input("Nothing was autofilled. <enter> to try again.")

    else:
        answer = input("Please click on a valid page to fill out and press <enter>. Or <exit>")
        if answer == "exit":
            fill_another_page = False
            driver.quit()
input("<enter> when ready to close browser.")
print('Good-bye and good luck.\n')
print("PTA: " + pt.pta + " CM: " + pt.CM + '\n')
print(pt.forcuraBlurb + '\n')
print("Wound care on orders: " + pt.woundCare + pt.woundCareCustom + '\n')

