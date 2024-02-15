import traceback, sys
import hidden_vars
# add file path for selenium depending on installation
sys.path.append(hidden_vars.filepath_selenium)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Initialize webdriver.
def webdriver_init(filepath_webdriver):
    driver = webdriver.Chrome(filepath_webdriver)
    return driver

# Open browser (Chrome) and insert username. Password is manually entered. 
def open_browswer(driver, username):
    driver.get("https://kinnser.net/login.cfm")
    userElem = driver.find_element_by_id("username")
    userElem.send_keys(username)
    userElem.send_keys(Keys.TAB)

# Gracefully handle errors when filling out EMR pages and write message to file for review.
def autofill_error(page, patientName):
    print(f"***** {page} AUTOFILL ERROR *****")
    errorFile = open(f'{patientName}_{page}_error_file', 'w')
    errorFile.write(traceback.format_exc())
    errorFile.close()
    print('Traceback written to file.')

# Use this when a pause is needed when filling out an EMR page.
def pause_to_autofill(page):
    input(f"AUTOFILL {page}.")

# Scroll to top of page to prompt clinician to review page before saving and continuing.
# Use at "end" of EMR page.
def scroll_up_then_pause(driver, page):
    driver.find_element_by_tag_name('html').send_keys(Keys.HOME)
    input(f"'Save & Cont' {page}.")
    driver.find_element_by_id("oasisSaveContinueButton").click()  # 'save and continue'

# Clear previous entries. Mostly used when seeing a previous patient
def clearLink(linksToClear):
    for i in range(len(linksToClear)):
        driver.find_element_by_id('clearLink' + str(linksToClear[i])).click()
    input("<Enter> when all sections cleared and ready to autofill page")

# dummy function to test f strings
def funct(patientName, page):
    print(f'here we have {patientName} on page {page}')

# Create the SOC/ROC report to go in the comm note
def SOC_ROC_report(age, gender, approach, side, joint, effect, relevantMedHx, woundDesc,
                   physicianFullName, physicianPhone, physicianOthers, F2Fdate,
                   orthoProtocol, POCapproval, dcedFrom, nurseFreq, ptFreq,
                   otFreq, stFreq, MSWfreq, HHAfreq, woundCare, woundCareCustom, 
                   PTPOCfocus):
    string = f"""SOC/ROC REPORT

PT Admitted {age} yr old {gender} with primary Dx: {approach}{side}{joint}{effect}

Relevant medical history: {relevantMedHx}

Wound/Incision: {woundDesc}

PCP/Following Doctors and phone numbers:
Following: Dr {physicianFullName} at {physicianPhone}
{physicianOthers}

Telehealth Candidate: no

Additional Risk Information or special instructions: none

Last MD F2F visit: {F2Fdate}

Ortho Protocol: {orthoProtocol} ____

Which MD was called to approve POC: {POCapproval}

Name of who POC was reported to? (RN/MA/PA): {POCapproval}

Was POC approved? {POCapproval}

Name of facility patient discharged from: {dcedFrom}

Frequency and Duration:

SN:  {nurseFreq}
PT:  {ptFreq}
OT:  {otFreq}
ST:  {stFreq}
MSW: {MSWfreq}
HHA: {HHAfreq}

Wound care: {woundCare} {woundCareCustom}

PT interventions, reason for home care, plan for next visit : ____ {PTPOCfocus}

Coordinated care with: reviewed calendar and plan of care with patient. Contacted scheduler, case manager, and next clinician.
"""
    return string

# Paste comm note into text box for any comm note (SOC or DC)
def comm_note(driver, patientName, text):
    page = "Comm note"
    input(f'{patientName} AUTOFILL {page}')
    try:
        driver.find_element_by_id("CallSummary").send_keys(text)
    except:
        autofill_error(page, patientName)

# Generate general interventions; everyone admitted gets them.
def general_inteventions():
    string = """Patient was identified with 2+ forms of ID: DOB, name, and ____ caregiver \
confirmation. Patient agreed w/ provision of HHC. Consents signed for care.

P.T. performed whole body assessment.  VS, BM’s ______ WNL; action taken: ____ \
Edema present at and around impairment site. Signs/sx of UTI ____ not present.

P.T. completed medication reconciliation and instructed patient on new and/or current medication \
list. Patient was ___ able to verbalize actions, side effects, and correct schedule/dosages of \
his/her meds.

Instructed patient regarding home health care, infection control measures, advanced directives. \
Advised patient to have emergency plan including evacuation and sheltering location.

Instructed patient when to call home health agency versus emergency services (911).

Instructed patient to monitor for signs and symptoms of infection and blood clots.

Instructed patient how to manage pain with medications listed in chart and non-pharmaceutical \
methods and to monitor signs of symptoms of adverse reactions including constipation.

Instructed patient in fall risk mitigation and home safety including using prescribed assistive \
device, getting help from caregiver when unsafe, using appropriate lighting, wearing appropriate \
foot coverings, using non-slip mats in bathrooms, ______ removing non-secured rugs.

Discussed plan of care and frequency including wound care with patient (and family/caregivers).  \
Therapist and patient in agreement. _____

"""
    return string

# Generate homebound statement for ortho patients
def hb_ortho(effect):
    string = f"Patient is homebound due to recent {effect}, \
unsteady and unsafe ambulation, very poor balance, weakness, and abnormal transfers.  \
Patient is at high risk for falls with serious injury due to surgery and requires assistance of \
2 wheel walker and of another person with all transfers/ambulation and when leaving the \
home for medically necessary appointments.\n\n"
    return string

# Generate covid screen blurb
def covid_screen(myTempTime, myTemp, ptTemp, CV19ss, CV19contact, CV19travel):
    string = f"""COVID 19 Screening Requirements:
** TIME OF SCREENING: _{myTempTime}_

SCREENING OF CLINICIAN:
Clinician Temperature prior to entry in the home/facility: _{myTemp}_
    N  Fever or signs/symptoms of a respiratory infection such as cough, shortness of breath, \
sore throat, chills, repeated shaking with chills, muscle pain, headache, or a new onset of \
loss sense of taste or smell?
    N  Has clinician had contact in the last 14 days with someone who has a confirmed diagnosis \
of COVID-19, is under investigation for COVID-19 or is ill with the symptoms above?
    N  Traveled within the previous 14 days to an area with sustained community transmission?

SCREENING OF CLIENT AND FAMILIES PRIOR TO HOME VISIT:
Agency staff must communicate with the client before a scheduled visit, \
either by telephone, text message, or video conference, and conduct the \
same screen listed above and document screening:
Patient Temperature _{ptTemp}_ \

    {CV19ss} Fever or signs/symptoms of a respiratory infection such as cough, shortness \
of breath, sore throat, chills, repeated shaking with chills, muscle pain, headache, or a new \
onset of loss sense of taste or smell?
    {CV19contact} Has patient/anyone in the home had contact in the last 14 days with \
someone who has a confirmed diagnosis of COVID-19, is under investigation for COVID-19 or is \
ill with symptoms described above?
    {CV19travel} Traveled within the previous 14 days to an area with sustained community \
transmission?"""
    return string

# Generate main orders
def main_orders(medDx, otherdisciplines, tempHigh, woundCare, woundCareCustom, side, joint, effect, 
                wbStatus, jointOrders, TEDhose, painPumpBlurb, painPumpOrders): 
    string = f"""•
•
Physician orders received. Admit patient to home health care for diagnosis of {medDx}.
•      Skilled Nurse for assessment, education on disease processes, medications, and safety.
•      PT OT ST -  Therapy to evaluate and Treat/ perform home safety evaluation - Develop \
discipline specific Plan of Care.

Clinician to perform complete system assessment.  Assess cardio-pulmonary, GU/GI, nutrition, \
pain management, musculoskeletal, circulatory, neurological, hydration, skin integrity, \
assess medication compliance and effectiveness, clinician can pre-fill medication box as \
needed if patient/caregiver unable or refuses to do. Clinician to assess response to treatment \
regimen, s/s of adverse effects of disease process, need for adjustment in response to \
medication regimen, and need for adjustment in POC.  Report abnormal finding to health care \
provider.
Clinician to inform the patient/caregivers on infection control including COVID-19 and \
measures to prevent the spread of the disease.

HHA will provide PPE to be used by patient/caregiver during the HHA visit upon request.
Clinicians will utilize infection control.
Clinician to provide education for s/s of COVID-19 and how to protect themselves and family \
members.  Avoid crowds or areas with a concentration of high traffic. Mild respiratory \
symptom may want to get tested, or self-quarantine 10-14 days, stay home and avoid sick \
individuals, wash hands, clean all high touch surfaces. Moderate to severe symptoms including \
shortness of breath and fevers, seek medical attention or go the hospital or ER.

 {otherdisciplines} ____

•Home Health Agency to HOLD patient's services on admitted to inpatient facility and resume \
care upon discharge. Clinician frequency 1W1 resume home health care.
Agency to discharge patient while in an inpatient facility at end of certification and may \
readmit post d/c for inpatient facility, assess health care needs 1w1.

•Clinicians to assess oxygen saturation via Pulse Oximetry PRN for symptoms of SOB. Report \
Pulse Oximetry reading < 90% to MD.

• Agency may accept orders from on-call physician and any other consulting physician, \
ancillary PA, and NP identified as providing care for patient.

Generic equivalent care supplies may be substituted for all current and future orders.

•Home Health Care may recertify patient for consecutive 60-day episode bases on patient \
medical necessity extending from current certification to include all new, changed orders, \
diagnosis, exacerbations of disease process, medication, and knowledge deficit of patient \
and-or caregiver and-or lack of willing, able caregiver to provide essential care.

DISCHARGE: Clinician to discharge patient from home health services when all goals are met, \
is no longer homebound, patient or MD requests discharge, patient's insurance changes (agency \
to re-admit under new policy if patient in agreement), or if patient moves out of service area.

MEDICATIONS: SN or therapist to teach on new and high-risk medications, action and side \
effects and when to notify Capitol Home Health / MD re: ineffective or adverse reactions to \
medications.

Home health clinician to develop personalized emergency plan with patient.

PAIN:
Home health clinician to assess and monitor patient's pain level and related vital signs, \
recommend pain medication(s) as ordered only, educate and-or implement non-pharmacological \
measures to reduce pain (e.g. ice, heat, massage, relaxation, meditation) unless \
contraindicated (eg. no heat with active cancer or RA).  Notify physician due to unrelieved \
pain above 6 on 0-10 pain scale.

GENERAL WOUND/INCISION CARE:
If blisters form around wound, notify surgeon. Sutures or staples will be removed by provider \
in office.  Report any drainage to surgeon. If wound is questionable in any way, take a \
picture of wound and send to surgeon then upload to chart.

Home health clinician to instruct the patient on signs and symptoms of wound infection to \
report to physician including increased temperature above {tempHigh}, chills, \
increase in drainage, foul odor, redness, unrelieved pain above 6 on 0-10 scale, and any \
other significant changes.

Home health clinician to evaluate wound(s) at each dressing change and PRN for signs and symptoms \
of infection. Report to physician increased temperature above {tempHigh}, \
chills, increase in drainage, foul odor, redness, unrelieved pain above 6 on 0-10 scale, and \
any other significant changes.

SPECIFIC WOUND/INCISION CARE:
{woundCare} {woundCareCustom}

PT TREATMENT:
Physical therapy treatment to focus on rehab of {side}{joint}{effect} including the following interventions:

Physical therapist to teach and perform on patient: {wbStatus}, ____, transfers, gait, balance, \
bed mobility, stairs and steps, home safety, assistive devices including walkers and canes as \
appropriate, therapeutic exercises to all affected body regions, establish and upgrade HEP, \
passive, active, ____ and active assisted range of motion, manual therapy, muscle re-education, and \
non-pharmaceutical modalities for pain control.

{jointOrders}
Utilize standard agency vital signs, notify provider for temperature >{tempHigh}. ___
Provider follow-up at 2 weeks post op.  Call surgeon if no BM after 5 days. {TEDhose}
{painPumpBlurb} {painPumpOrders}"""
    return string

# Page 1 of EMR 
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

# TODO Pages 2-24 of EMR after successful testing of Page 1 of EMR and other changes 
# TODO Testing will occur 2-17-24
    
# used for testing functions
if __name__ == "__main__":
    
    driver = webdriver_init()
    open_browswer(driver, username='user_name')
    
