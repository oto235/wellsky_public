import traceback, sys, time
import hidden_vars
# add file path for selenium depending on installation
sys.path.append(hidden_vars.filepath_selenium)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
sys.path.append(hidden_vars.filepath_CHH)
import chh


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
def general_interventions():
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

# enter a date, click on box, delete anything there, enter new date
def enter_date(driver, id, date):
    driver.find_element_by_id(id).click()
    driver.find_element_by_id(id).send_keys(Keys.BACK_SPACE * 8)
    driver.find_element_by_id(id).send_keys(date)

# Clear previous entries from previous episode/visit
def clear_link(driver, linksToClear):
    for i in range(len(linksToClear)):
        driver.find_element_by_id('clearLink' + str(linksToClear[i])).click()
    input("<Enter> when all sections cleared and ready to autofill page")

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

# Page 2 of EMR
def administrative(driver, patientName, evalDate, dcDate, medDx):
    page = "Administrative"
    input(f'{patientName} AUTOFILL {page}')
    try:
        # driver.find_element_by_id("M0090_INFO_COMPLETED_DT").click()  # assessment date
        # driver.find_element_by_id("M0090_INFO_COMPLETED_DT").send_keys(Keys.BACK_SPACE * 8)
        # driver.find_element_by_id("M0090_INFO_COMPLETED_DT").send_keys(evalDate)
        
        # assessment date
        enter_date(driver, "M0090_INFO_COMPLETED_DT", evalDate)

        driver.find_element_by_id("M0102_PHYSN_ORDRD_SOCROC_DT_NA").send_keys(Keys.SPACE)

        driver.find_element_by_id("M0104_PHYSN_RFRL_DT").click()  # MD ordered date
        driver.find_element_by_id("M0104_PHYSN_RFRL_DT").send_keys(Keys.BACK_SPACE * 8)
        driver.find_element_by_id("M0104_PHYSN_RFRL_DT").send_keys(dcDate)

        driver.find_element_by_id("M0110_01").send_keys(Keys.SPACE)  # 'early' episode

        # A1250 Transportation
        driver.find_element_by_id("A1250C").send_keys(Keys.SPACE)

        # M1000 Inpatient Facilities DC'ed from
        driver.find_element_by_id("M1000_DC_IPPS_14_DA").send_keys(Keys.SPACE)  # M1000 in-patient stay

        # M1005 Inpatient DC date
        driver.find_element_by_id("M1005_INP_DISCHARGE_DT").click()  # M1005 InP dc date
        driver.find_element_by_id("M1005_INP_DISCHARGE_DT").send_keys(Keys.BACK_SPACE * 8)
        driver.find_element_by_id("M1005_INP_DISCHARGE_DT").send_keys(dcDate)

        # M1005 why inpatient stay
        driver.find_element_by_id("c_m1005comment").send_keys(medDx)  # M1005comment

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page
    
# Page 3 of EMR
def vitals(driver, previousPatient, ptPulse, ptTemp, ptRR, ptLBP, ptRBP, ht, wt, 
           tempHigh, chh_vitals, dm, patientName):
    page = "Vitals"
    pause_to_autofill(page)

    try:
        # clear form from previous episode:
        linksToClear = [2]
        if previousPatient == 1:
            clear_link(driver, linksToClear)

        # enter patient vitals:
        driver.find_element_by_id("cVS_pulseradical").send_keys(ptPulse)  # pulse
        driver.find_element_by_id("PulseRadicalRegular1").send_keys(Keys.SPACE)  # pulseReg
        driver.find_element_by_id("cVS_temperature").send_keys(ptTemp)  # temp
        driver.find_element_by_id("cVS_respiratory").send_keys(ptRR)  # resp
        driver.find_element_by_id("cVS_bplsitting").send_keys(ptLBP)  # left arm bp, sitting
        driver.find_element_by_id("cVS_bprsitting").send_keys(ptRBP)  # right arm bp, sitting
        driver.find_element_by_id("cVS_height").send_keys(str(ht) + " inches")  # height
        driver.find_element_by_id("cVS_weight").send_keys(str(wt) + " lbs")  # weight
        driver.find_element_by_id("cActual2").send_keys(Keys.SPACE)  # "stated" ht and wt

        # enter vital sign parameters:
        driver.find_element_by_id("c485np_temphigh").send_keys(tempHigh)  # np_tempHigh
        driver.find_element_by_id("c485np_templow").send_keys(chh_vitals.temp_low)  # np_tempLow
        driver.find_element_by_id("c485np_pulsehigh").send_keys(chh_vitals.pulse_high)  # np_pulsehigh
        driver.find_element_by_id("c485np_pulselow").send_keys(chh_vitals.pulse_low)  # np_pulselow
        driver.find_element_by_id("c485np_resphigh").send_keys(chh_vitals.resp_high)  # np_resphigh
        driver.find_element_by_id("c485np_resplow").send_keys(chh_vitals.resp_low)  # np_resplow
        driver.find_element_by_id("c485np_syshigh").send_keys(chh_vitals.sbp_high)  # np_syshigh
        driver.find_element_by_id("c485np_syslow").send_keys(chh_vitals.sbp_lLow)  # np_syslow
        driver.find_element_by_id("c485np_diashigh").send_keys(chh_vitals.dbp_high)  # np_diashigh
        driver.find_element_by_id("c485NP_DiasLow").send_keys(chh_vitals.dbp_low)  # np_diaslow
        driver.find_element_by_id("c485np_02stat").send_keys(chh_vitals.o2_low)  # np_02stat
        if dm == 1:
            driver.find_element_by_id("c485np_fastbslevelgt").send_keys(chh_vitals.fast_bs_High)
            driver.find_element_by_id("c485np_fastbslevellt").send_keys(chh_vitals.fast_bs_low)
            driver.find_element_by_id("c485np_randombslevelgt").send_keys(chh_vitals.rand_bs_high)
            driver.find_element_by_id("c485np_randombslevellt").send_keys(chh_vitals.rand_bs_low)

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 4 of EMR
def patient_history_and_prognosis(driver, ROC, previousPatient, side, joint, effect, PMHfull,
                                  PSxH, incontinence, PMH, pna, flu, covid, livingWill, 
                                  agencyRCVDcopy, MPOA, DNR, MPOAname, MPOAphone, patientName):
    page = "Patient History and Prognosis"
    # pause_to_autofill()
    try:
        # clear form from previous episode:
        linksToClear = [1,2,4,8]
        if ROC == 1:
            linksToClear = [1,2]
        if previousPatient == 1:
            clear_link(driver, linksToClear)

        # PMH list with check boxes and comments
        driver.find_element_by_id("cMH_osteoarthritis").send_keys(Keys.SPACE)  # OA
        driver.find_element_by_id("cMH_osteoarthritissites").send_keys(f'{side}{joint}')

        if 'TKR' in effect or 'THR' in effect or 'replacement' in effect:
            driver.find_element_by_id("cMH_jointreplacement").send_keys(Keys.SPACE)  # jointReplacementBox
            driver.find_element_by_id("cMH_joint").send_keys(f'{side}{joint}')  # jointReplacmentComment

        driver.find_element_by_id("cMH_other").send_keys(Keys.SPACE)  # 'other'
        driver.find_element_by_id("cMH_otherdetails").send_keys(PMHfull)  # 'other' comments

        if PSxH != '':
            driver.find_element_by_id('cMH_surghistory').send_keys(Keys.SPACE)  # past sx hx
            driver.find_element_by_id('cMH_surghistorydetails').send_keys(PSxH)  # pas sx hx comments

        if incontinence >= 1:
            driver.find_element_by_id('cMH_urinaryincont').send_keys(Keys.SPACE)

        if "HTN" in PMH:
            driver.find_element_by_id("cMH_htn").send_keys(Keys.SPACE)

        # Immunizations
        if pna == 1:
            driver.find_element_by_id('pY').send_keys(Keys.SPACE)
        elif pna == 0:
            driver.find_element_by_id('pN').send_keys(Keys.SPACE)
        if flu == 1:
            driver.find_element_by_id('fY').send_keys(Keys.SPACE)
        elif flu == 0:
            driver.find_element_by_id('fN').send_keys(Keys.SPACE)
        if covid == 1:
            driver.find_element_by_id('add1Y').send_keys(Keys.SPACE)
            driver.find_element_by_id('cImm_add1info').send_keys('COVID')

        # Health Screeing
        # nothing to autofill

        # Advanced Directives
        if livingWill == 1 or MPOA == 1 or DNR == 1:
            driver.find_element_by_id('phad1').send_keys(Keys.SPACE)
            time.sleep(1)
            if agencyRCVDcopy == 1:
                driver.find_element_by_id('cofaa1').send_keys(Keys.SPACE)  # for pink box
            if agencyRCVDcopy == 0:
                driver.find_element_by_id('cofaa2').send_keys(Keys.SPACE)  # for pink box
        if DNR == 1:
            driver.find_element_by_id('addnr').send_keys(Keys.SPACE)
            # driver.find_element_by_id('pd0').send_keys(Keys.SPACE)  # can't find this on webpage
        if DNR == 0:
            pass
            # driver.find_element_by_id('pd1').send_keys(Keys.SPACE)
        if livingWill == 1:
            driver.find_element_by_id('adlw').send_keys(Keys.SPACE)
        if MPOA == 1:
            driver.find_element_by_id('admpoa').send_keys(Keys.SPACE)
            driver.find_element_by_id('admpoan').send_keys(MPOAname)
            driver.find_element_by_id('admpoap1').send_keys(MPOAphone[0])
            driver.find_element_by_id('admpoap2').send_keys(MPOAphone[1])
            driver.find_element_by_id('admpoap3').send_keys(MPOAphone[2])

        if livingWill == 0 and MPOA == 0 and DNR == 0:
            driver.find_element_by_id('phad2').send_keys(Keys.SPACE)  # pink box first question

        if agencyRCVDcopy == 1:
            driver.find_element_by_id('frm_ACPrecordDocumentedYes').send_keys(Keys.SPACE)  # for purple box
        if agencyRCVDcopy == 0:
            driver.find_element_by_id('frm_ACPrecordDocumentedNo').send_keys(Keys.SPACE)  # for purple box

        # surragate decision maker
        driver.find_element_by_id('hs2').send_keys(Keys.SPACE)  # for pink box
        driver.find_element_by_id('frm_ACPsurrRecordDocumentedNo').send_keys(Keys.SPACE)  # for purple box

        # patient provided written/verbal info re advance directives
        driver.find_element_by_id('pwpwvi1').send_keys(Keys.SPACE)

        # prognosis
        driver.find_element_by_id('pp3').send_keys(Keys.SPACE)

        # functional limitations
        driver.find_element_by_id('c485FI_ambulation').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485FI_endurance').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485FI_dyspnea').send_keys(Keys.SPACE)
        if incontinence >= 1:
            driver.find_element_by_id('c485FI_bowelincont').send_keys(Keys.SPACE)

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 5 of EMR
def hearing_speech_vision(driver, previousPatient, hearing, ROC, vision, 
                          health_lit, patientName):
    page = "Hearing, Speech, and Vision"

    try:
        # clear form from previous episode:
        linksToClear = [1]
        if previousPatient == 1:
            clear_link(driver, linksToClear)

        driver.find_element_by_id('cSS_wnl').send_keys(Keys.SPACE)  # eyes
        driver.find_element_by_id('cSS_nosewnl').send_keys(Keys.SPACE)  # nose
        # B0200 Hearing
        if hearing is not None:
            if ROC == 0:
                driver.find_element_by_id(f"B0200_0{hearing}").send_keys(Keys.SPACE)
            elif ROC ==1:
                print("check ROC selections on this page")
            if hearing == 0:
                driver.find_element_by_id("cSS_earswnl").send_keys(Keys.SPACE)
        # B1000 Vision
        if vision is not None:
            driver.find_element_by_id(f"B1000_0{vision}").send_keys(Keys.SPACE)
        # B1300 Health Literacy
        if health_lit is not None:
            driver.find_element_by_id(f"B1300_{health_lit}").send_keys(Keys.SPACE)

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 6 of EMR
def cog_mood_behav(driver, previousPatient, psychosocial_factors, c_rep_3_words, c_year,
                   c_month, c_day_of_week, c_400_sock, c_400_blue, c_400_bed, delirium,
                   social_isol, anxiety, cog_impairment, patientName):    
    page = "Cog, Mood, Behav"

    try:
        # clear form from previous episode:
        linksToClear = [1]
        if previousPatient == 1:
            clear_link(driver, linksToClear)

        # Mental status
        orientation = ['person', 'time', 'place', 'situation']
        for thing in orientation:
            driver.find_element_by_id(f'CA485_MS_{thing}_Ori').send_keys(Keys.SPACE)
        # driver.find_element_by_id('CA485_MS_person_Ori').send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_MS_memoryNoProblems').send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_MS_neuroNoProblems').send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_MS_behavioralAppropriateWNL').send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_MS_moodAppropriateWNL').send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_MS_pyschosocial').send_keys(psychosocial_factors)

        # C0100
        driver.find_element_by_id('CC0100_01').send_keys(Keys.SPACE)

        # C0200
        driver.find_element_by_id(f'CC0200_0{c_rep_3_words}').send_keys(Keys.SPACE)

        # C0300
        driver.find_element_by_id(f'CC0300A_0{c_year}').send_keys(Keys.SPACE)
        driver.find_element_by_id(f'CC0300B_0{c_month}').send_keys(Keys.SPACE)
        driver.find_element_by_id(f'CC0300C_0{c_day_of_week}').send_keys(Keys.SPACE)

        # C0400
        driver.find_element_by_id(f'CC0400A_0{c_400_sock}').send_keys(Keys.SPACE)
        driver.find_element_by_id(f'CC0400B_0{c_400_blue}').send_keys(Keys.SPACE)
        driver.find_element_by_id(f'CC0400C_0{c_400_bed}').send_keys(Keys.SPACE)

        # C0500 - it is autocalculated

        # C1310
        if delirium == 0:
            driver.find_element_by_id('CC1310A_0').send_keys(Keys.SPACE)
            driver.find_element_by_id('CC1310B_0').send_keys(Keys.SPACE)
            driver.find_element_by_id('CC1310C_0').send_keys(Keys.SPACE)
            driver.find_element_by_id('CC1310D_0').send_keys(Keys.SPACE)

        # D 0700 Social Isolation
        driver.find_element_by_id(f'D0700_{social_isol}').send_keys(Keys.SPACE)

        # M questions
        driver.find_element_by_id('M1700_00').send_keys(Keys.SPACE)
        driver.find_element_by_id('M1710_00').send_keys(Keys.SPACE)
        driver.find_element_by_id(f'M1720_0{anxiety}').send_keys(Keys.SPACE)
        driver.find_element_by_id('M1740_BD_NONE').send_keys(Keys.SPACE)
        driver.find_element_by_id('M1745_00').send_keys(Keys.SPACE)

        if anxiety > 1:
            driver.find_element_by_id('CA485_MS_anxious').send_keys(Keys.SPACE)

        if cog_impairment == 1:
            driver.find_element_by_id('CA485_MS_forgetful_E').send_keys(Keys.SPACE)
            driver.find_element_by_id('M1700_01').send_keys(Keys.SPACE)
            driver.find_element_by_id('M1710_01').send_keys(Keys.SPACE)
            #driver.find_element_by_id('c485MS_forgetful').send_keys(Keys.SPACE)

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 7 of EMR
def pref_cust_rout_act(driver, previousPatient, patient_care_prefs, patientName):
    page = "Pref Cust Rout Act"

    try:
        # clear form from previous episode:
        linksToClear = [3, 4, 5]
        if previousPatient == 1:
            clear_link(driver, linksToClear)

        driver.find_element_by_id('M2102_f_00').send_keys(Keys.SPACE)

        # types of assistance
        driver.find_element_by_id('cToF_adlfamily').send_keys(Keys.SPACE)
        driver.find_element_by_id('cTof_iadlfamily').send_keys(Keys.SPACE)
        driver.find_element_by_id('cTof_psychfamily').send_keys(Keys.SPACE)
        driver.find_element_by_id('cToF_assistfamily').send_keys(Keys.SPACE)
        driver.find_element_by_id('cToF_financefamily').send_keys(Keys.SPACE)

        driver.find_element_by_id('cSA_names').send_keys('family/friends')

        driver.find_element_by_id('ca2').send_keys(Keys.SPACE)
        driver.find_element_by_id('ca4').send_keys(Keys.SPACE)
        driver.find_element_by_id('ca6').send_keys(Keys.SPACE)
        driver.find_element_by_id('ca8').send_keys(Keys.SPACE)
        driver.find_element_by_id('ca10').send_keys(Keys.SPACE)
        driver.find_element_by_id('financialAssist3').send_keys(Keys.SPACE)

        driver.find_element_by_id('frm_patientCarePreferences').send_keys(patient_care_prefs)

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 8 of EMR
def enviro_cond(driver, previousPatient, anticoagulant, livingSituation, equipDict, 
                patientName):
    page = "Enviro Cond"

    try:
        # clear form from previous episode:
        linksToClear = [1,2,3]
        if previousPatient == 1:
            clear_link(driver, linksToClear)

        # Safety measures
        if anticoagulant == 1:
            driver.find_element_by_id('c485SM_anticoagulant').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485SM_pathclear').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485SM_standardpos').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485SM_emergplan').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485SM_ambulation').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485SM_fall').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485SM_adls').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485SM_devices').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485SM_safetymeasures').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485SM_mobsafety').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485SM_dmesafety').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485SM_displan').send_keys(Keys.SPACE)

        driver.find_element_by_id('c485SM_riskcode').send_keys('III')
        driver.find_element_by_id('c485SM_disastercode').send_keys('LOW')

        # Safety/sanitation hazards affecting patient
        if 'no hazards' in livingSituation.lower():
            driver.find_element_by_id('cSH_nohazards').send_keys(Keys.SPACE)
        if 'stairs' in livingSituation.lower():
            driver.find_element_by_id('cSH_stairs').send_keys(Keys.SPACE)
        if 'narrow' in livingSituation.lower():
            driver.find_element_by_id('cSH_walkway').send_keys(Keys.SPACE)
        if 'cluttered' in livingSituation.lower() or 'soiled' in livingSituation.lower():
            driver.find_element_by_id('cSH_soiledarea').send_keys(Keys.SPACE)
        if 'rug' in livingSituation.lower():
            driver.find_element_by_id('cSH_otherdetails').send_keys('rugs ')
        if 'pet' in livingSituation.lower():
            driver.find_element_by_id('cSH_otherdetails').send_keys('pet(s) ')

        # Fire Assessment for Patients with Oxygen
        if equipDict['oxygen'] == 0:
            driver.find_element_by_id('cFA_isuseoxygen').send_keys(Keys.SPACE)
        elif equipDict['oxygen'] ==1:
            driver.find_element_by_id('c485SM_o2').send_keys(Keys.SPACE)
            driver.find_element_by_id('c485EMan_suppliesdmeprov').send_keys("Oxygen")

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 9 of EMR
def functional_status(driver, previousPatient, wbStatus, GG0170SOCROC_dict, side, joint,
                      M1800_dict, age, diagnosis_3_plus, fall_in_last_3_mo, visual_impairment,
                      environmental_hzds, poly_pharm_4_plus, cog_impairment, incontinence,
                      tug, equipDict, equipDictOther, catheterType, patientName):
    page = "Functional Status"

    try:
        # clear form from previous episode:
        linksToClear = [1,2,11,12,14]
        if previousPatient == 1:
            clear_link(driver, linksToClear)

        # Activities Permitted:
        driver.find_element_by_id("c485AP_walker").send_keys(Keys.SPACE)
        driver.find_element_by_id("c485AP_expres").send_keys(Keys.SPACE)
        driver.find_element_by_id("c485AP_tbedchair").send_keys(Keys.SPACE)
        driver.find_element_by_id('c485AP_msother').send_keys(wbStatus)
        if GG0170SOCROC_dict['Q1'] == '1':
            driver.find_element_by_id('c485AP_wheelchair').send_keys(Keys.SPACE)

        # Musculoskeletal:
        driver.find_element_by_id("cMSk_weakness").send_keys(Keys.SPACE)  # mskWeakness
        driver.find_element_by_id("cMSk_ambdifficult").send_keys(Keys.SPACE)  # mskAmbDifficult
        driver.find_element_by_id("cMSk_limitmob").send_keys(Keys.SPACE)  # mskLimitMobBox
        driver.find_element_by_id("cMSk_limitedmobdesc").send_keys(f'{side}{joint}')  # mskLimitedMobComment
        driver.find_element_by_id("cMSk_jointstiff").send_keys(Keys.SPACE)  # mskJointStiffBox
        driver.find_element_by_id("cMSk_jointstiffdesc").send_keys(f'{side}{joint}')  # mskJointStiffComment
        driver.find_element_by_id("cMSk_pbalance").send_keys(Keys.SPACE)  # mskPBalance
        driver.find_element_by_id("cMSk_assistdev").send_keys(Keys.SPACE)  # mskAssistDevBox
        driver.find_element_by_id("cMSk_assistdevdesc").send_keys("2 wheel walker")  # mskAssistDevComment

        # M1800 questions and my default answers:
        driver.find_element_by_id("M1800_" + M1800_dict['M1800']).send_keys(Keys.SPACE)  # grooming
        driver.find_element_by_id("M1810_" + M1800_dict['M1810']).send_keys(Keys.SPACE)  # upper body dressing
        driver.find_element_by_id("M1820_" + M1800_dict['M1820']).send_keys(Keys.SPACE)  # lower body dressing
        driver.find_element_by_id("M1830_" + M1800_dict['M1830']).send_keys(Keys.SPACE)  # bathing
        driver.find_element_by_id("M1840_" + M1800_dict['M1840']).send_keys(Keys.SPACE)  # toilet trsfr
        driver.find_element_by_id("M1845_" + M1800_dict['M1845']).send_keys(Keys.SPACE)  # toilet hygiene
        driver.find_element_by_id("M1850_" + M1800_dict['M1850']).send_keys(Keys.SPACE)  # transferring
        driver.find_element_by_id("M1860_" + M1800_dict['M1860']).send_keys(Keys.SPACE)  # ambulation

        # MAHC 10 Risk assessment tool
        if age == '':
            print('Enter age: (you only get one chance)')
            age = input()
        if int(age) >= 65:
            driver.find_element_by_id("a1").send_keys(Keys.SPACE)
        else:
            driver.find_element_by_id("a2").send_keys(Keys.SPACE)

        if diagnosis_3_plus == 1:
            driver.find_element_by_id('m1').send_keys(Keys.SPACE)
        else:
            driver.find_element_by_id('m2').send_keys(Keys.SPACE)

        if fall_in_last_3_mo == 1:
            driver.find_element_by_id('c1').send_keys(Keys.SPACE)
        else:
            driver.find_element_by_id('c2').send_keys(Keys.SPACE)

        if visual_impairment > 0:
            driver.find_element_by_id('r1').send_keys(Keys.SPACE)
        else:
            driver.find_element_by_id('r2').send_keys(Keys.SPACE)

        if environmental_hzds == 1:
            driver.find_element_by_id('j1').send_keys(Keys.SPACE)
        else:
            driver.find_element_by_id('j2').send_keys(Keys.SPACE)

        if poly_pharm_4_plus == 1:
            driver.find_element_by_id('n1').send_keys(Keys.SPACE)
        else:
            driver.find_element_by_id('n2').send_keys(Keys.SPACE)

        if cog_impairment == 1:
            driver.find_element_by_id('e1').send_keys(Keys.SPACE)
        else:
            driver.find_element_by_id('e2').send_keys(Keys.SPACE)

        if int(incontinence) >= 1:
            driver.find_element_by_id("k1").send_keys(Keys.SPACE)
        if int(incontinence) == 0:
            driver.find_element_by_id("k2").send_keys(Keys.SPACE)

        driver.find_element_by_id("s1").send_keys(Keys.SPACE)  # impaired funcational mobility
        driver.find_element_by_id("d1").send_keys(Keys.SPACE)  # pain affecting level of function

        # TUG test
        driver.find_element_by_id("cTUGseconds").send_keys(tug)

        # DME checkboxes
        for key, value in equipDict.items():
            if value == 1:
                driver.find_element_by_id("c485EMan_" + key).send_keys(Keys.SPACE)

        # DME other comment box
        for key, value in equipDictOther.items():
            if value == 1:
                dme = str(key).replace('_', ' ')
                driver.find_element_by_id("c485EMan_dmeother").send_keys(f'{dme}, ')

        # Supplies
        driver.find_element_by_id("c485EMan_abds").send_keys(Keys.SPACE)
        driver.find_element_by_id("c485EMan_gauzepads").send_keys(Keys.SPACE)
        driver.find_element_by_id("c485EMan_acewrap").send_keys(Keys.SPACE)
        driver.find_element_by_id("c485EMan_suppliesdress").send_keys(Keys.SPACE)
        driver.find_element_by_id("c485EMan_tape").send_keys(Keys.SPACE)
        driver.find_element_by_id("c485EMan_alcoholpads").send_keys(Keys.SPACE)
        driver.find_element_by_id("c485EMan_exgloves").send_keys(Keys.SPACE)
        if catheterType.lower() == 'foley':
            driver.find_element_by_id("c485EMan_foleycath").send_keys(Keys.SPACE)

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 10 of EMR
def func_abilities_and_goals(driver, cog_impairment, priorWalker, priorWheelchair, 
                             priorMotorized, GG0130SOCROC_dict, GG0170SOCROC_dict,
                             GG0170SOCROC_wheelchair_dict, patientName):
    page =  "Func Abilities and Goals"

    try:

        # GG0100 prior functioning
        driver.find_element_by_id('GG0100_A').send_keys(3)  # prior self care
        driver.find_element_by_id('GG0100_B').send_keys(3)  # prior indoor
        driver.find_element_by_id('GG0100_C').send_keys(3)  # prior stairs
        driver.find_element_by_id('GG0100_D').send_keys(3)  # prior cog
        if cog_impairment == 1:
            driver.find_element_by_id('GG0100_D').send_keys(2)

        # GG0110 prior device
        driver.find_element_by_id('GG0110_Z').send_keys(Keys.SPACE)  # Z: none
        if priorWalker == 1:
            driver.find_element_by_id('GG0110_D').send_keys(Keys.SPACE)  # D: walker
        if priorWheelchair == 1:
            driver.find_element_by_id('GG0110_A').send_keys(Keys.SPACE)  # A: wheelchair
        if priorMotorized == 1:
            driver.find_element_by_id('GG0110_B').send_keys(Keys.SPACE)  # B: motorized wheelchair or scooter

        # GG0130 Self Care and my default answers
        for k,v in GG0130SOCROC_dict.items():
            driver.find_element_by_id("GG0130SOCROC_" + k).send_keys(v)

        # GG0170 Mobilty and my default answers
        for k,v in GG0170SOCROC_dict.items():
            driver.find_element_by_id("GG0170SOCROC_" + k).send_keys(v)
        if GG0170SOCROC_dict['Q1'] == '1':
            for k,v in GG0170SOCROC_wheelchair_dict.items():
                driver.find_element_by_id("GG0170SOCROC_" + k).send_keys(v)

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 11 of EMR
def bladder_and_bowel(driver, previousPatient, incontinence, catheterType, 
                      antibioticUTI, cathChanged, lastBM, UTI, patientName):
    page =  "Bladder and Bowel"

    try:
        # clear form from previous episode:
        linksToClear = [1,6]
        if previousPatient == 1:
            clear_link(driver, linksToClear)

        # GU
        if incontinence >= 1:
            driver.find_element_by_id('cES_incont').send_keys(Keys.SPACE)
            driver.find_element_by_id('M1610_01').send_keys(Keys.SPACE)

        elif incontinence == 0:
            driver.find_element_by_id('cES_wnl').send_keys(Keys.SPACE)
            driver.find_element_by_id('M1610_00').send_keys(Keys.SPACE)

        if catheterType != '':
            driver.find_element_by_id('cES_catheter').send_keys(Keys.SPACE)
            driver.find_element_by_id('cES_catheterlist').click()
            driver.find_element_by_id('cES_catheterlist').send_keys(catheterType[0])
            driver.find_element_by_id('cES_catheterchanged').click()
            driver.find_element_by_id('cES_catheterchanged').send_keys(cathChanged)
            driver.find_element_by_id('M1610_02').send_keys(Keys.SPACE)

        driver.find_element_by_id('cES_lastBM').send_keys(Keys.SPACE)  # last BM
        driver.find_element_by_id("cES_lastbmdate").click()
        driver.find_element_by_id("cES_lastbmdate").send_keys(Keys.BACK_SPACE * 8)
        driver.find_element_by_id('cES_lastbmdate').send_keys(lastBM)
        driver.find_element_by_id('lbm2').send_keys(Keys.SPACE)  # per pt
        driver.find_element_by_id('cES_lbmconstipation').send_keys(Keys.SPACE)
        driver.find_element_by_id('cc2').send_keys(Keys.SPACE)

        # M1600 UTI and prophylactic treatment
        driver.find_element_by_id('M1600_00').send_keys(Keys.SPACE)

        if antibioticUTI == 1:
            driver.find_element_by_id('M1600_NA').send_keys(Keys.SPACE)

        if UTI == 1:
            driver.find_element_by_id('M1600_01').send_keys(Keys.SPACE)


        # M1620 and M1630 bowel incontinence, ostemy
        driver.find_element_by_id('M1620_00').send_keys(Keys.SPACE)
        driver.find_element_by_id('M1630_00').send_keys(Keys.SPACE)

        # dialysis
        driver.find_element_by_id('id2').send_keys(Keys.SPACE)


    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page


# Page 12 of EMR
def active_dx(driver, PMH, dm, patientName):

    page =  "Active Diagnosis"

    try:

        # M1028 None box - above DM and PVD in case either = 1
        driver.find_element_by_id("M1028_ACTV_DIAG_NOA_D").send_keys(Keys.SPACE)

        # PVD clause for M1028:
        if 'pvd' in PMH.lower():
            driver.find_element_by_id("M1028_ACTV_DIAG_PVD_PAD_D").send_keys(Keys.SPACE)

        # DM clause for M1028:
        if dm == 1:
            driver.find_element_by_id("M1028_ACTV_DIAG_DM_D").send_keys(Keys.SPACE)   # M1028

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 13 of EMR
def health_conditions(driver, previousPatient, hospRiskAss, m1033_comment, medEventDate, 
                      side, joint, pain, pain_Sleep, pain_TA, pain_DD, patientName):
    page =  "Health Conditions"

    try:
        # clear form from previous episode:
        linksToClear = [2]
        if previousPatient == 1:
            clear_link(driver, linksToClear)

        #M1033 Risk for hospitalization
        for key, value in hospRiskAss.items():
            if value == 1:
                driver.find_element_by_id('CA485_M1033_HOSP_RISK_' + key).send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_M1033_COMMENT').send_keys(m1033_comment)

        # Pain
        driver.find_element_by_id("cPS_onsetdate").click()  # SOC date
        driver.find_element_by_id("cPS_onsetdate").send_keys(Keys.BACK_SPACE * 8)
        driver.find_element_by_id('cPS_onsetdate').send_keys(medEventDate)

        driver.find_element_by_id('cPS_locpain').send_keys(side + joint)
        driver.find_element_by_id('cPS_intpain').send_keys(pain[1])
        driver.find_element_by_id('cPS_duration').send_keys('constant ____')
        driver.find_element_by_id('cPS_quality').send_keys('ache, sharp')
        driver.find_element_by_id('cPS_painworse').send_keys('transfers, end range of motion ____')
        driver.find_element_by_id('cPS_painbetter').send_keys('rest, position, ice, elevation, gentle ROM, paid meds ____')
        driver.find_element_by_id('cPS_relief').send_keys(pain[0])
        driver.find_element_by_id('cPS_meds').send_keys('refer to med list')
        driver.find_element_by_id('cPS_effective').send_keys('good ____')
        driver.find_element_by_id('cPS_adverse').send_keys('constipation ____')
        driver.find_element_by_id('cPS_goal').send_keys('zero pain')

        # J0510 Pain effecting sleep
        driver.find_element_by_id(f'J0510_{pain_Sleep}').send_keys(Keys.SPACE)

        # J0520 Pain interfering with TA (therapeutic activities)
        driver.find_element_by_id(f'J0520_0{pain_TA}').send_keys(Keys.SPACE)

        # J0530 Pain interfering DD (day to day) activities
        driver.find_element_by_id(f'J0530_{pain_DD}').send_keys(Keys.SPACE)

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 14 of EMR
def respitory_status(driver, previousPatient, lungsounds, ptO2, equipDict, 
                     patientName):    
    page =  "Respiratory Status"

    try:
        # clear form from previous episode:
        linksToClear = [1]
        if previousPatient == 1:
            clear_link(driver, linksToClear)

        # CTA
        driver.find_element_by_id('cRes_cta').send_keys(Keys.SPACE)
        driver.find_element_by_id('cRes_ctatext').send_keys(lungsounds)

        # driver.find_element_by_id('cRes_wnl').send_keys(Keys.SPACE)  # resp
        driver.find_element_by_id('cRes_o2sat').send_keys(Keys.SPACE)
        driver.find_element_by_id('cRes_o2sattext').send_keys(str(ptO2))
        driver.find_element_by_id('M1400_02').send_keys(Keys.SPACE)

        if equipDict['oxygen'] == 0:
            driver.find_element_by_id('cRes_o2satlist').click()
            driver.find_element_by_id('cRes_o2satlist').send_keys('r')


    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 15 of EMR
def endocrine(driver, previousPatient, dm, endocrine_dx, patientName):
    page =  "Endocrine"

    try:
        # clear form from previous episode:
        linksToClear = [1]
        if previousPatient == 1:
            clear_link(driver, linksToClear)

        if dm == 1:
            driver.find_element_by_id('d1').send_keys(Keys.SPACE)
        elif dm == 0:
            driver.find_element_by_id('d2').send_keys(Keys.SPACE)
        if dm == 0 and endocrine_dx == 0:
            driver.find_element_by_id('cEndo_wnl').send_keys(Keys.SPACE)


    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 16 of EMR
def cardiac_status(driver, previousPatient, cardiac_dx, side, joint, patientName):
    page =  "Cardiac Status"

    try:
        # clear form from previous episode:
        linksToClear = [1]
        if previousPatient == 1:
            clear_link(driver, linksToClear)
        if cardiac_dx == 0:
            driver.find_element_by_id('cCa_wnl').send_keys(Keys.SPACE)  # WNL

        driver.find_element_by_id('cCa_chestpain').send_keys(Keys.SPACE)
        driver.find_element_by_id('cCa_chestpaindesc').send_keys('denies')

        driver.find_element_by_id('cCa_dizziness').send_keys(Keys.SPACE)
        driver.find_element_by_id('cCa_dizzineesdesc').send_keys('denies')

        driver.find_element_by_id('cCa_edema').send_keys(Keys.SPACE)
        driver.find_element_by_id('cCa_edema1').send_keys(f'{side}{joint}')

        driver.find_element_by_id('cCa_neckvein').send_keys(Keys.SPACE)
        driver.find_element_by_id('cCa_neckveindesc').send_keys('none')

        driver.find_element_by_id('cCa_peripheral').send_keys(Keys.SPACE)  # peripheral pulses
        driver.find_element_by_id('cCa_peripheraldesc').send_keys('regular')

        driver.find_element_by_id('cCa_caprefill').send_keys(Keys.SPACE)
        driver.find_element_by_id('cr1').send_keys(Keys.SPACE)


    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 17 of EMR
def swallowing_nutritional_status(driver, previousPatient, numberOfWounds, M1800_dict, 
                                  patientName):
    page =  "Swallowing_Nutritional Status"

    try:
        # clear form from previous episode:
        linksToClear = [1,2,6]
        if previousPatient == 1:
            clear_link(driver, linksToClear)

        # driver.find_element_by_id('cNu_nuwnl').send_keys(Keys.SPACE)  # WNL
        driver.find_element_by_id('cNHS_otcmeds').send_keys(Keys.SPACE)  # 3 or more meds
        if numberOfWounds > 0:
            driver.find_element_by_id('cNHS_openwound').send_keys(Keys.SPACE)  # open wound

        # K 0520 Nutritional approaches
        driver.find_element_by_id('K0520Z1').send_keys(Keys.SPACE)
        if dm == 1:
            driver.find_element_by_id('K0520D1').send_keys(Keys.SPACE)

        # M1060 Height and weight
        driver.find_element_by_id('M1060_HEIGHT_NOT_ASSESSED').send_keys(Keys.SPACE)
        driver.find_element_by_id('M1060_WEIGHT_NOT_ASSESSED').send_keys(Keys.SPACE)

        # M1870 Feeding or Eating
        driver.find_element_by_id("M1870_" + M1800_dict['M1870']).send_keys(Keys.SPACE)  # feeding

        # Enter Physician's orders
        driver.find_element_by_id('c485PO_regulardiet').send_keys(Keys.SPACE)  # regular diet

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause()  # pause to finish and inspect page

# Page 18 of EMR
def skin_conditions(driver, previousPatient, norton_score, pressure_sore_risk_comment, 
                    SurgicalSOC, numberOfWounds, patientName):

    page =  "Skin Conditions"

    try:
        # clear form from previous episode:
        linksToClear = [2]
        if previousPatient == 1:
            clear_link(driver, linksToClear)
        # risk of ulcers?
        driver.find_element_by_id('CA485_PUIR_riskPressureUlcerInjury_2').send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_PUIR_riskAssessmentTool').send_keys('Norton Pressure Score')
        driver.find_element_by_id('CA485_PUIR_score').send_keys(norton_score)
        driver.find_element_by_id('CA485_PUIR_comments').send_keys(pressure_sore_risk_comment)

        # Integumentary Status
        driver.find_element_by_id('st1').send_keys(Keys.SPACE)  # skin turgor
        driver.find_element_by_id('cIS_skinpinkwnl').send_keys(Keys.SPACE)  # skin color
        driver.find_element_by_id('cIS_warm').send_keys(Keys.SPACE)  # warm
        driver.find_element_by_id('cIS_incision').send_keys(Keys.SPACE)  # incision
        driver.find_element_by_id('iY1').send_keys(Keys.SPACE)  # instructed on infection control
        driver.find_element_by_id('n1').send_keys(Keys.SPACE)  # nails 'good'

        driver.find_element_by_id('M1306_0').send_keys(Keys.SPACE)  # pressure injury
        driver.find_element_by_id('M1322_00').send_keys(Keys.SPACE)  # stage 1
        driver.find_element_by_id('M1324_NA').send_keys(Keys.SPACE)
        driver.find_element_by_id('M1330_00').send_keys(Keys.SPACE)
        driver.find_element_by_id(f'M1340_0{SurgicalSOC}').send_keys(Keys.SPACE)

        # unclick these options if no wounds
        if numberOfWounds == 0:
            driver.find_element_by_id('cIS_warm').send_keys(Keys.SPACE)  # warm
            driver.find_element_by_id('cIS_incision').send_keys(Keys.SPACE)  # incision

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 19 of EMR
def meds(driver, anticoagulant, antibioticPRO, antibioticUTI, opioid_usage, hypoglycemic_usage, 
         antiplatelet, medInteraction, medInterFollowUp, M2030, patientName):
    page =  "Meds"

    try:

        # N0415
        if anticoagulant == 1:
            driver.find_element_by_id('N0415E1').send_keys(Keys.SPACE)
            driver.find_element_by_id('N0415E2').send_keys(Keys.SPACE)
        if antibioticPRO ==1 or antibioticUTI == 1:
            driver.find_element_by_id('N0415F1').send_keys(Keys.SPACE)
            driver.find_element_by_id('N0415F2').send_keys(Keys.SPACE)
        if opioid_usage == 1:
            driver.find_element_by_id('N0415H1').send_keys(Keys.SPACE)
            driver.find_element_by_id('N0415H2').send_keys(Keys.SPACE)
        if hypoglycemic_usage == 1:
            driver.find_element_by_id('N0415J1').send_keys(Keys.SPACE)
            driver.find_element_by_id('N0415J2').send_keys(Keys.SPACE)
        if antiplatelet == 1:
            driver.find_element_by_id('N0415I1').send_keys(Keys.SPACE)
            driver.find_element_by_id('N0415I2').send_keys(Keys.SPACE)
        if anticoagulant + antibioticPRO + antibioticUTI + opioid_usage + hypoglycemic_usage + antiplatelet == 0:
            driver.find_element_by_id('N0415Z1').send_keys(Keys.SPACE)

        # M questions
        driver.find_element_by_id(f'M2001_{medInteraction}').send_keys(Keys.SPACE)  # M2001 Med interaction
        if medInteraction > 0:
            driver.find_element_by_id(f'M2003_0{medInterFollowUp}').send_keys(Keys.SPACE)
        driver.find_element_by_id('M2010_01').send_keys(Keys.SPACE)  # high risk drug education
        driver.find_element_by_id('M2020_03').send_keys(Keys.SPACE)  # mgmt of oral meds
        driver.find_element_by_id('M2030_' + M2030).send_keys(Keys.SPACE)  # mgmt of inj meds

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 20 of EMR
def spec_tx_procs_and_progs(driver, spec_Trtmts_count, cpap, spec_Trtmts, visitCount, ROC, 
                            shingles, patientName):
    page =  "Spec Trtmts, Procs, and Progs"

    try:

        # O0110
        if spec_Trtmts_count == 0:
            driver.find_element_by_id('O0110Z1a').send_keys(Keys.SPACE)
        if cpap == 1:
            driver.find_element_by_id('O0110G1a').send_keys(Keys.SPACE)
            time.sleep(1)
            driver.find_element_by_id('O0110G3a').send_keys(Keys.SPACE)
        if spec_Trtmts['oxygen'] == 1:
            driver.find_element_by_id('O0110C1a').send_keys(Keys.SPACE)
            time.sleep(1)
            driver.find_element_by_id('O0110C2a').send_keys(Keys.SPACE)
        if spec_Trtmts['chemo_IV'] == 1 or spec_Trtmts['chemo_oral'] == 1:
            driver.find_element_by_id('O0110A1a').send_keys(Keys.SPACE)
            time.sleep(1)
            if spec_Trtmts['chemo_IV'] == 1:
                driver.find_element_by_id('O0110A2a').send_keys(Keys.SPACE)
            if spec_Trtmts['chemo_oral'] == 1:
                driver.find_element_by_id('O0110A3a').send_keys(Keys.SPACE)
        if spec_Trtmts['radiation'] == 1:
            driver.find_element_by_id('O0110B1a').send_keys(Keys.SPACE)
        if spec_Trtmts['dialysis'] == 1:
            driver.find_element_by_id('O0110J1a').send_keys(Keys.SPACE)

        # M2200 Therapy Need
        M2200 = driver.find_element_by_id("M2200_THER_NEED_NUM")
        M2200.send_keys(Keys.BACK_SPACE * 3)
        M2200.send_keys(visitCount)

        # Randomly placed shingles shot
        if ROC == 0:
            if shingles == 1:
                driver.find_element_by_id('HasShinglesVac').send_keys(Keys.SPACE)
            elif shingles == 0:
                driver.find_element_by_id('DoesNotHaveShinglesVac').send_keys(Keys.SPACE)
        elif ROC == 1:
            print("check ROC selections")

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page
    
# Page 21 of EMR
def orders(driver, previousPatient, ptFreq, nurseFreq, otFreq, stFreq, MSWfreq, HHAfreq, 
           mainOrders, diagnosis_3_plus, ROC, relevantMedHx, generalInterventions, 
           POCapproval, PTPOCfocus, physicianFU, patientName):
    page =  "Orders"

    try:
        # clear form from previous episode:
        linksToClear = [1, 2, 3, 4, 5, 6]
        if previousPatient == 1:
            clear_link(driver, linksToClear)

        # order frequency
        driver.find_element_by_id("c485ODT_ptfreq").send_keys(ptFreq)
        driver.find_element_by_id("c485ODT_snfreq").send_keys(nurseFreq)
        driver.find_element_by_id("c485ODT_otfreq").send_keys(otFreq)
        driver.find_element_by_id("c485ODT_ltfreq").send_keys(stFreq)
        driver.find_element_by_id("c485ODT_mswfreq").send_keys(MSWfreq)
        driver.find_element_by_id("c485ODT_hhafreq").send_keys(HHAfreq)

        # main orders
        driver.find_element_by_id("c485ODT_addorders").send_keys(mainOrders)

        # rehab potential - 'good'
        driver.find_element_by_id('cpt485RP_gachgoals').send_keys(Keys.SPACE)

        # discharge plans
        driver.find_element_by_id('cpt485DP_medstable').send_keys(Keys.SPACE)
        driver.find_element_by_id('cpt485DP_indhelp').send_keys(Keys.SPACE)
        driver.find_element_by_id('cpt485DP_discaregiver').send_keys(Keys.SPACE)
        driver.find_element_by_id('cpt485DP_discareself').send_keys(Keys.SPACE)
        driver.find_element_by_id('cpt485DP_caremanage').send_keys(Keys.SPACE)
        driver.find_element_by_id('cpt485DP_disgoalsmet').send_keys(Keys.SPACE)

        # patient strengths
        driver.find_element_by_id('cPStr_mlearner').send_keys(Keys.SPACE)
        if diagnosis_3_plus == 0:
            driver.find_element_by_id('cPStr_abmultdiag').send_keys(Keys.SPACE)

        # Conclusions:
        driver.find_element_by_id('cPStr_interneed').send_keys(Keys.SPACE)
        driver.find_element_by_id('cPStr_instneed').send_keys(Keys.SPACE)

        # skilled intervention
        if ROC == 0:
            driver.find_element_by_id("cSInt_assessment").send_keys(f"{relevantMedHx} \n\n {generalInterventions}")
            driver.find_element_by_id("cSInt_respinter").send_keys(Keys.SPACE)
            driver.find_element_by_id("cSInt_vupt").send_keys(Keys.SPACE)
            driver.find_element_by_id('cSInt_rdpt').send_keys(Keys.SPACE)
            driver.find_element_by_id('cSInt_rftpt').send_keys(Keys.SPACE)
            # title of teaching tool
            driver.find_element_by_id("cSInt_titletool").send_keys('agency handout')
            # progress to goals
            driver.find_element_by_id("cSInt_proggoals").send_keys('25%')
            # name (conferenced with)
            driver.find_element_by_id("cSInt_confname").send_keys('Jason Schwarz')
            # regarding
            driver.find_element_by_id("cSInt_regarding").send_keys('P.T. POC')
            # Physician contacted RE:
            driver.find_element_by_id('cSInt_physcontact').send_keys(POCapproval)
             # order changes:
            driver.find_element_by_id('cSInt_ordchanges').send_keys('none ____')
             # plans for next visit
            driver.find_element_by_id("cSInt_nvisitplans").send_keys(PTPOCfocus)
            # next physician appt
            driver.find_element_by_id("cSInt_nvisidate").click()
            driver.find_element_by_id("cSInt_nvisidate").send_keys(Keys.BACK_SPACE * 8)
            driver.find_element_by_id("cSInt_nvisidate").send_keys(physicianFU)
            # discharge planning
            driver.find_element_by_id("cSInt_dplanning").send_keys('yes')

        elif ROC == 1:
            driver.find_element_by_id("cptSInt_assinstperform").send_keys(f"{relevantMedHx} \n\n {generalInterventions}")
            driver.find_element_by_id("cptSInt_tolwell").send_keys(Keys.SPACE)
            driver.find_element_by_id("cptSInt_respinter").send_keys(Keys.SPACE)
            driver.find_element_by_id("cptSInt_vupt").send_keys(Keys.SPACE)
            driver.find_element_by_id('cptSInt_rdpt').send_keys(Keys.SPACE)
            driver.find_element_by_id('cptSInt_rftpt').send_keys(Keys.SPACE)
            driver.find_element_by_id("cptSInt_titletool").send_keys('agency handout')
            driver.find_element_by_id("cptSInt_proggoals").send_keys('25%')
            driver.find_element_by_id("cptSInt_confname").send_keys('Jason Schwarz')
            driver.find_element_by_id("cptSInt_regarding").send_keys('P.T. POC')
            driver.find_element_by_id('cptSInt_physcontact').send_keys(POCapproval)
            driver.find_element_by_id('cptSInt_ordchanges').send_keys('none ____')
            driver.find_element_by_id("cptSInt_nvisitplans").send_keys(PTPOCfocus)
            driver.find_element_by_id("cptSInt_nvisidate").click()
            driver.find_element_by_id("cptSInt_nvisidate").send_keys(Keys.BACK_SPACE * 8)
            driver.find_element_by_id("cptSInt_nvisidate").send_keys(physicianFU)
            driver.find_element_by_id("cptSInt_dplanning").send_keys('yes')

    except:
        autofill_error(page, patientName)

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 22 of EMR
def supplpies_worksheet(driver):
    page = "Supplies Worksheet"

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 23 of EMR
def supplies_used_this_visit(driver):
    page =  "Supplies Used This Visit"

    scroll_up_then_pause(driver, page)  # pause to finish and inspect page

# Page 24 of EMR
def pt_evaluation(driver, ROC, relevantMedHx, hbOrtho, covidScreen, livingSituation, subjective, 
                  treatment, pta, CM, forcuraBlurb, woundCare, woundCareCustom, medDx, 
                  medEventDate, evalDate, PLOF, goal, dm, joint, approach, numberOfWounds, 
                  opioid_usage, anticoagulant, spec_Trtmts, woundDesc, side, SurgicalSOC, 
                  rom, mmt, GG0170SOCROC_dict, func_impair_factors, wbStatus, woundLocation, 
                  woundCareProvided, woundCareTolerance, woundDescIndiv, patientName):

    page =  "PT Evaluation"

    if ROC == 1:
        input("press Enter to print stuff")
        print("relavent md hx")
        print(relevantMedHx)
        print("homebound reason")
        print(hbOrtho, covidScreen)
        print("living situation")
        print(livingSituation)
        print("subjective and extra")
        print(subjective)
        print("treatment")
        print(treatment)
        print("PTA: " + pta + " CM: " + CM + '\n')
        print(forcuraBlurb + '\n')
        print("Wound care on orders: " + woundCare + woundCareCustom + '\n')
        input("pressing Enter again will run normal program")

    input("Autofill AFTER loading desired template")

    try:
        # Medical Dx and date
        driver.find_element_by_id('frm_MedDiagText').send_keys(medDx)

        driver.find_element_by_id("frm_MedDiagOEDate").click()  # Med Dx date (sx date)
        driver.find_element_by_id("frm_MedDiagOEDate").send_keys(Keys.BACK_SPACE * 8)
        driver.find_element_by_id("frm_MedDiagOEDate").send_keys(medEventDate)

        # PT date
        driver.find_element_by_id("frm_PTDiagOEDate").click()  # PT Dx date (eval date)
        driver.find_element_by_id("frm_PTDiagOEDate").send_keys(Keys.BACK_SPACE * 8)
        driver.find_element_by_id("frm_PTDiagOEDate").send_keys(evalDate)

        # Rel Med Hx free text box
        driver.find_element_by_id('frm_RlvntMedHist').send_keys(relevantMedHx)

        # PLOF free text box
        driver.find_element_by_id('frm_PriorLevelFunc').send_keys(PLOF)

        # Patient goals free rext box
        driver.find_element_by_id('frm_PatientGoals').send_keys(goal)

        # Precautions
        driver.find_element_by_id('frm_PatientPrecautions').send_keys('Universal, Falls')
        if dm == 1:
            driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Diabetic')
        if 'hip' in joint and 'posterio' in approach.lower():
            driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Posterior Hip')
        if 'back' in joint:
            driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Spinal')
        if numberOfWounds > 0:
            driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Wound')
        if opioid_usage == 1:
            driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Opioids')
        if anticoagulant == 1:
            driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Anticoagulation')
        if spec_Trtmts['oxygen'] == 1:
            driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Oxygen')

        # Homebound section:
        input('<Enter> for Homebound status')
        HB = driver.find_element_by_id("cHo_homebound_cY").send_keys(Keys.SPACE)

        input('<Enter> to fill out the rest')
        # Criteria 1
        driver.find_element_by_id("cHo_homebound_crit1Part1").send_keys(Keys.SPACE)  # HBcrit1Part1
        driver.find_element_by_id("cHo_homebound_crit1Part2").send_keys(Keys.SPACE)  # HBcrit1Part2
        driver.find_element_by_id("cHo_homebound_crit1Part2_specify").send_keys(hbOrtho)  # HBcrit1Specify

        # Criteria 2
        driver.find_element_by_id("cHo_homebound_crit2Part1").send_keys(Keys.SPACE)  # HBcrit2Part1
        driver.find_element_by_id("cHo_homebound_crit2Part2").send_keys(Keys.SPACE)  # HBcrit2Part2
        driver.find_element_by_id("cHo_homebound_crit2Part2_specify").send_keys(hbOrtho, covidScreen)  # HBcrit2Specify

        # Social Support/Safety Hazards
        driver.find_element_by_id("frm_SafetySanHaz13").send_keys(livingSituation)

        # Subjective Info
        driver.find_element_by_id("frm_SubInfo").send_keys(subjective)

        # Physical Assessment
        driver.find_element_by_id("frm_PhyAsmtSkin").send_keys(woundDesc)
        if SurgicalSOC >= 1:
            driver.find_element_by_id('frm_PhyAsmtCoordination').send_keys(f"Decreased around {side}{joint}")
            driver.find_element_by_id('frm_PhyAsmtSensation').send_keys(f"Abnormal around {side}{joint}")
            driver.find_element_by_id('frm_PhyAsmtEdemaLocText').send_keys(side + joint)

        # add ROM and MMT
        if joint.strip() == 'knee' and side.strip() == 'left':
            driver.find_element_by_id('frm_ROM94').send_keys(rom[0])  # flexion
            driver.find_element_by_id('frm_ROM98').click()
            driver.find_element_by_id('frm_ROM98').send_keys(Keys.BACK_SPACE * 3)
            driver.find_element_by_id('frm_ROM98').send_keys(rom[1])  # ext
            driver.find_element_by_id('frm_ROM96').send_keys(mmt[0])  # flexion mmt
            driver.find_element_by_id('frm_ROM100').click()
            driver.find_element_by_id('frm_ROM100').send_keys(Keys.BACK_SPACE * 2)
            driver.find_element_by_id('frm_ROM100').send_keys(mmt[1])  # ext mmt

        if joint.strip() == 'knee' and side.strip() == 'right':
            driver.find_element_by_id('frm_ROM93').send_keys(rom[0])  # flexion
            driver.find_element_by_id('frm_ROM97').click()
            driver.find_element_by_id('frm_ROM97').send_keys(Keys.BACK_SPACE * 3)
            driver.find_element_by_id('frm_ROM97').send_keys(rom[1])  # ext
            driver.find_element_by_id('frm_ROM95').send_keys(mmt[0])  # flexion mmt
            driver.find_element_by_id('frm_ROM99').click()
            driver.find_element_by_id('frm_ROM99').send_keys(Keys.BACK_SPACE * 2)
            driver.find_element_by_id('frm_ROM99').send_keys(mmt[1])  # ext mmt

        if joint.strip() == 'hip' and side.strip() == 'left':
            # rom
            driver.find_element_by_id('frm_ROM70').send_keys(rom[0])  # flexion rom
            driver.find_element_by_id('frm_ROM74').click()
            driver.find_element_by_id('frm_ROM74').send_keys(Keys.BACK_SPACE * 3)  # erase extension autofill
            driver.find_element_by_id('frm_ROM78').send_keys(rom[1])  # abd rom
            driver.find_element_by_id('frm_ROM82').click()
            driver.find_element_by_id('frm_ROM82').send_keys(Keys.BACK_SPACE * 3)  # erase adduction autofill
            # mmt
            driver.find_element_by_id('frm_ROM72').send_keys(mmt[0])  # flexion mmt
            driver.find_element_by_id('frm_ROM76').click()
            driver.find_element_by_id('frm_ROM76').send_keys(Keys.BACK_SPACE * 3)  # erase extension mmt autofill
            driver.find_element_by_id('frm_ROM80').send_keys(mmt[1])  # abd mmt
            driver.find_element_by_id('frm_ROM84').click()
            driver.find_element_by_id('frm_ROM84').send_keys(Keys.BACK_SPACE * 3)  # erase adduction mmt autofill

        if joint.strip() == 'hip' and side.strip() == 'right':
            # rom
            driver.find_element_by_id('frm_ROM69').send_keys(rom[0])  # flexion rom
            driver.find_element_by_id('frm_ROM73').click()
            driver.find_element_by_id('frm_ROM73').send_keys(Keys.BACK_SPACE * 3)  # erase extension autofill
            driver.find_element_by_id('frm_ROM77').send_keys(rom[1])  # abd rom
            driver.find_element_by_id('frm_ROM81').click()
            driver.find_element_by_id('frm_ROM81').send_keys(Keys.BACK_SPACE * 3)  # erase adduction autofill
            # mmt
            driver.find_element_by_id('frm_ROM71').send_keys(mmt[0])  # flexion mmt
            driver.find_element_by_id('frm_ROM75').click()
            driver.find_element_by_id('frm_ROM75').send_keys(Keys.BACK_SPACE * 3)  # erase extension mmt autofill
            driver.find_element_by_id('frm_ROM79').send_keys(mmt[1])  # abd mmt
            driver.find_element_by_id('frm_ROM83').click()
            driver.find_element_by_id('frm_ROM83').send_keys(Keys.BACK_SPACE * 3)  # erase adduction mmt autofill

        if GG0170SOCROC_dict['Q1'] == '1':  # wheelchair use is True
            driver.find_element_by_id('frm_FAPT36').send_keys("CGA")        # Level ground assistance
            driver.find_element_by_id('frm_FAPT37').send_keys("Mod A x 1")  # Unlevel ground assistance
            driver.find_element_by_id('frm_FAPT38').send_keys("CGA")        # Maneuvering assistance
            driver.find_element_by_id('frm_FAPT39').send_keys(func_impair_factors)


        # Functional Assessment
        driver.find_element_by_id('frm_FAPTBedMobComments').send_keys(func_impair_factors)
        driver.find_element_by_id('frm_FAPT35').send_keys(func_impair_factors)
        driver.find_element_by_id('frm_FAPT22').send_keys(func_impair_factors)
        # weightbearing status
        driver.find_element_by_id('frm_FAPT40').send_keys(wbStatus)

        # add coordination people
        driver.find_element_by_id('frm_CareCoordName').send_keys(f", Marcy Sanchez, {CM}, {pta}")

        # treatment provided
        driver.find_element_by_id('frm_TrtmntPlanComments1').send_keys(treatment)

        if numberOfWounds != 0:
            for i in range(numberOfWounds):
                woundNumber = str(i + 1)
                input("Click 'Add (Another) Wound' then <Enter> when ready to autofill 'Wound " + woundNumber + "'")
                driver.find_element_by_id(f'frm_wound{woundNumber}Location').send_keys(woundLocation[i])  # Location
                driver.find_element_by_id(f'frm_wound{woundNumber}Type').click()
                driver.find_element_by_id(f'frm_wound{woundNumber}Type').send_keys("su")  # type - surgical
                driver.find_element_by_id(f'frm_wound{woundNumber}PresentOnAdmission').click()  # present on admission
                driver.find_element_by_id(f'frm_wound{woundNumber}Treatment').send_keys(woundCareProvided[i])
                driver.find_element_by_id(f'frm_wound{woundNumber}PatientResponseToTreatment').send_keys(woundCareTolerance[i])
                driver.find_element_by_id(f'frm_wound{woundNumber}AdditionalInformation').send_keys(woundDescIndiv[i])
                input("Finish this wound, click 'Save Wound', then <Enter> to continue")

    except:
        autofill_error(page, patientName)
        input('<Enter> to acknowledge')

# used for testing functions
if __name__ == "__main__":
    
    driver = webdriver_init()
    open_browswer(driver, username='user_name')
    
