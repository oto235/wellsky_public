import sys, time, traceback
from datetime import date, timedelta, datetime
import hidden_vars
sys.path.append(hidden_vars.filepath_CHH)
import chh, utils

branch =              0  # 0 = Austin      1 = San Antonio
SOC_ROC_note =        1
fill_out_note =       1
print_forcura_blurb = 1
ROC =                 0


# SOC FOLDER  PT POC   DRESSING   INFECTION   DVT'S   PAIN   BM   WBAT   FALL RISK   AD
subjectiveExtra =   "Passing gas, no BM since
otherInPatientStay= "
SurgicalSOC =       2'   # 0= no wounds, 1= at least one observable wound, 2= non-observable wounds only

# my variables
myTemp =            "
myTempTime =        "
visitStartTime =    "
visitEndTime =      "
evalDate =          "03-03-2024" "    # MM-DD-YYYY

patientName =       "
MR_not_used =       "
ptPhone =           "
address1 =          "
address2 =          "
physician =         "  # leave out 'Dr.', 'borick, catlett, dodgin, golderg, heinrich, hyde, manuel, michel, moghimi, nwelue' already loaded
physicianPhone =    "

caregiverName =     "
caregiverPhone =    ["
caregiverRltnshp =  "
# spouse =            "
# spousePhone =       ["

age =               "
DOB_not_used =      "
gender =            "  # 'man' or 'woman'
insurance =         "mcr"  "mcrother" "com
previousPatient =   '
pta =               "
CM =                "Cheryl Campbell   Sheri Wariakois

# patient variables
PMH =               "
PSxH =              "  # optional (empty str if none)
dm =                '
insulin =           '
diagnosis_3_plus =  '

# allergies =
# pharmacy =
# phone =



side =              "
joint =             "
cause =             "DJD       # {cause} led to ... {effect}
effect =            "T
medDx =             "Aftercare following joint replacement surgery ("+side.upper()+" "+joint.upper()+" "+effect+")" "
approach =          ""  "# anterior | posteriolateral | posterior  - HIPS only
F2Fdate =           "
medEventDate =      F2Fdate"          # sxDate
dcedFrom =          "          # 'cprmc' | 'nwh' | 'sdmc' | 'sdsh' | 'west' are preloaded
sxLocation =        dcedFrom"
dcDate =            "
wbStatus =          "

physicianFU =       "  # MM-DD-YYYY

physicianOthers =   "PCP - Dr. _____ at 512- ____

ptFreq =            " # Dodgin, Heinrich 1w1, 3w1, 2w4; Manuel 1,4,3,2; Michel 1w1, 3w1, 2w3, 'freqName_...' will be reformatted to '1w1, ...'
visitCount =        "
nurseFreq =         ""
otFreq =            ""
stFreq =            ""
MSWfreq =           ""
HHAfreq =           ""
otherDiscFreqEff =  ""
needToCallMonday =  0'

goal =              "Return to
PTPOCfocus =        "Joint rehab per protocol, gait, balance, transfers, ROM, and strengthening.

# Patient vitals - any integer
ptTemp =            "
ptPulse =           '
ptO2 =              '
ptLBP =             "
ptRBP =             "
ptRR =              '
pain =              "
capRefill =         "good
lastBM =            "  # MM-DD-YYYY
lungsounds =        "upper, lower lobes
pain_Sleep =        '  # 0 = NA, 1 = Rarely or none, 2 = Occasionally, 3 = Frequently, 4 = Near constant, 8 = Unable to answer
pain_TA =           4'  # 0 = NA, 1 = Rarely or none, 2 = Occasionally, 3 = Frequently, 4 = Near constant, 8 = Unable to answer
pain_DD =           4'  # 1,2,3,4,8 options only (no 0)


# COVID Screen
fmTemp =            ""
cgTemp =            ""
# N | Y  if Y, then explain:
CV19ss =            "N"
CV19contact =       "N"
CV19travel =        "N"

# additional questions
cpap =              0'
incontinence =      0123'  # 0= none, 1=once a day linen change, 2= multiple linen changes, 3= near constant moisture
catheterType =      ""  # optional, 'foley' or 'suprapubic'
cathChanged =       ""  # optional, MM-DD-YYYY
cog_impairment =    0'
anxiety =           0123'  # 0= none, 1= not daily, 2 = daily, 3 = all the time

phq2 =              0'  # not used in program
social_isol =       '
psychosocial_factors = "none

c_rep_3_words =     0123' # C0200  how many words correct?
c_year =            0123'  # 0 = missed by > 5 years, 1 = 2-5 years off, 2 = one year off, 3 = correct
c_month =           012'   # 0 = missed by > month, 1 = 6 days to 1 month, 2 = accurate within 5 days
c_day_of_week =     01'
c_400_sock =        012'
c_400_blue =        012'
c_400_bed =         012'

ht =                '  # inches, min = 50
wt =                '  # pounds

livingWill =        '
MPOA =              '
MPOAname =          "  # only if MPOA == 1
MPOAphone =         ["  # only if MPOA == 1, enter as list
DNR =               '
agencyRCVDcopy =    '

# vaccinations
flu =               '
pna =               '
shingles =          '
covid =             '

# measurements
fall_in_last_3_mo = 0'
tug =               "  # int or str
rom =               ["  # [flex, abd/ext]  ext for knees, abd for hips
mmt =               ["  # [flex, abd/ext]  ext for knees, abd for hips

# wounds
# DRESSING and desciption, enter none if none, 'pico', 'prevena', 'aquacel', 'mepilex' generate specific woundCare wording
woundLocation =     [side + " " + joint]      # make empty list for no wounds
woundSoiled =       ["  # percentage
woundLength =       ['  # optional, int in cm
woundCovering =     ["PICO wound vac | PREVENA wound vac | Aquacel | Mepilex | steri-strips  #  use one of these listed, describe if not found
woundAherence =     ["well"]"
periwoundSkin =     ["normal tone"]"
numberOfWounds =    len(woundLocation)
woundCareProvided = ["none"]"
woundCareTolerance =["N/A"]"
woundCareCustom =   "
# woundCareCustom will be added to end of wound care blurb in forcura, comm note, and orders

woundDesc = ""
woundDescIndiv = [] " # make this a list of individual wound descriptions. It will be concatonated to a single string 'woundDesc'
woundDescLen = len(woundDescIndiv)
if woundDescLen == 0:
    for i in range(numberOfWounds):  # take out his loop and use list above to customize
        woundDescIndiv.append(f"""{woundLocation[i].title()} surgical incision covered by {woundCovering[i]}, \
{woundSoiled[i]}% soiled, {woundAherence[i]} adhered to skin, periwound: {periwoundSkin[i]}.""")

woundDesc = " ".join(woundDescIndiv)

if numberOfWounds == 0:
    woundDesc = "No wounds."

# equipment - use 0 or 1
equipDict = {"
'bedcommode':   0,
'cane':         0,
'etoiletseat':  0,
'grabbars':     0,
'hosbed':       0,
'nebulizer':    0,
'oxygen':       0,
'tubbench':     0,
'walker':       1,
'wheelchair':   0   }

equipDictOther = {"
'bed_rail':         0,
'cervical_brace':   0,
'grabber':          0,
'knee_immobilizer': 0,
'lumbar_brace':     0,
'rollator':         0,
'sock_helper':      0,
'shower_chair':     0
}


#### to fill out immediately after visit ####\
# if unsure, leave empty string
hearing =       0123'   # 0 = Adequate, 1 = some difficulty, 2 = Increase speaker volume, 3 = absence of useful hearing
vision =        01234'  # 0 = Adequate, 1 = large print only,2 = limited vision, 3 = highly, 4 = severely
health_lit =    01234'  # 0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always
delirium =      0'
dialysis =      0'      # 1 = hemodialysis, 2 = perotoneal  Still need to code this into the program

side = side.strip() + ' '
joint = joint.strip() + ' '
effect = effect.strip() + ' '
if approach != "":
    approach = approach.strip() + ' '


newMeds =           "blood thinner ____, pain meds ____, stool softeners and laxatives ____, prophylactic antibiotic ____, NSAIDS ____, anti-nausea ____, muscle relaxant ____
poly_pharm_4_plus = 1'
opioid_usage =      1'
antiplatelet =      1'  # aspirin, clopidogrel (Plavix)
anticoagulant =     0'  # Apixaban (Eliquis), Enoxaparin (Lovenox), rivaroxaban (Xarelto), Coumadin, Warfarin, Heparin
antibioticPRO =     0'
antibioticUTI =     0'
UTI =               0'
painPump =          0'
M2030 =             "NA" " # injectable meds 00=ind, 01=dep prep, 02= real-time reminder, 03=unable, NA = no inj meds
meds_chemo =        0'
hypoglycemic_usage =0'  # examples: Ozempic, Actos, Mounjaro
endocrine_dx =      0'
cardiac_dx =        1'

medInteraction =    0'
medInterFollowUp =  0'


PLOF = "Able to ambulate in community for five minutes without assistive device.


livingSituation = """Patient lives in a ____ story house with ____ spouse.  Spouse ____ helps with ADL's, IADL's, \
and medication management.  No ____ barriers to learning.  \
No hazards.____ """  " # keep 'no hazards' if no stairs, narrow, pets, or cluttered/soiled items

subjective = f"""Patient found ____ alert and agreeable to therapy.  Pain currently at {pain[1]}. Best is {pain[0]}. \
Worst is {pain[2]}. {subjectiveExtra}""" "


treatment = f"""Instructed patient in safe transfers, using 1-2 hands on ____ stable surface, and \
focusing on controlling movements.  Verbal cueing improved and reinforced safety.

Instructed patient in balance activities times ____ minutes. Losses of balance: ____.  \
Cueing improved safety.

TUG: {tug} seconds.

Instructed patient in gait training focusing on safe gait, appropriate heel to toe sequence, \
appropriate step length using ____ .  Cueing improved gait form.

Instructed patient in therapeutic exercises times ten reps including ____.  \
Cueing required to improve form with ____.

Patient tolerated therapy well. ____<move this section down to Treatment...>____
""" "

if ptFreq.lstrip().startswith('freq'):
    extra1, extra2, freqTemp = ptFreq.partition('_')
    ptFreq = freqTemp.replace('_', ', ')

painPumpBlurb = ""
painPumpOrders = ""
if painPump == 1:
    painPumpBlurb = "Pain pump present."
    painPumpOrders = "Home health clinician may remove pain pump catheter once medication is fully dispensed or upon MD/patient request. Apply Band-Aid or similar dressing if needed."

catheterBlurb = ""
if catheterType != "":
    catheterBlurb = f'{catheterType.upper()} catheter present.'

# date manipulation
medEventDateObject = datetime.strptime(medEventDate, "%m-%d-%Y")
medEventDateDay = medEventDateObject.strftime("%A")
POD7Object = medEventDateObject + timedelta(7)
POD7DD = POD7Object.strftime("%m-%d-%Y, %A")

# forcura blurbs have woundCare "added" at the very end of program
forcuraBlurb = f"""Good day team, patient {patientName}. {cause} led to \
{approach}{side}{joint}{effect}performed by Dr. {physician} on {medEventDate}, {medEventDateDay}. \
{woundDesc} Last BM: {lastBM}. PT POC: {ptFreq} to focus on {PTPOCfocus} ____ \
Lives in ____ {painPumpBlurb} {catheterBlurb}""" "

if SurgicalSOC == 0:
    forcuraBlurb = f"""Good day team, patient {patientName}. {cause} led to \
{approach}{side}{joint}{effect} on {medEventDate}. Followed by Dr. {physician}. \
{woundDesc} Last BM: {lastBM}. PT POC: {ptFreq} to focus on {effect} rehab including {PTPOCfocus}. ____ \
Lives in ____ {painPumpBlurb} {catheterBlurb}""" "


patient_care_prefs = "

# Braden dict.
braden = {"
'sensory':   4,  #                                                            3= some sensory impairment, 4= no sensory impairment
'moisture':  4 - incontinence,  #
'activity':  4,  # 1= bedfast,                  2= chairfast, NWB,            3= walks occassional short, 4= walks every 2 hours
'mobility':  3,  # 1= completely immobile,      2= occasional slight changes, 3= frequent slight changes, 4= frequent major changes
'nutrition': 3,  # 1= never eats complete meal, 2= rarely eats complete meal, 3= eats half+ of each meal, 4= eats most of every meal
'friction' : 2   # 1= mod to max assist,        2= min assist,                3= no assist
}
braden_score = 0
for k,v in braden.items():
    braden_score += v

# Norton Pressue
norton = {'
'physical_condition':   4,  # 4 = Good, 3 = fair, 2 = poor, 1 = very bad
'mental_condition':     4,  # 4 = Alert, 3 = apathetic, 2 = confused, 1 = stuporous
'activity':             4,  # 4 = Ambulant, 3 = walk with help, 2 = chairbound, 1 = bedfast
'mobility':             4,  # 4 = full, 3 = slightly impaired, 2 = very limited, 1 = immobile
'incontinence':         4 - incontinence
}
norton_score = 0
for k,v in norton.items():
    norton_score += v

# remaining MAHC items on ADL's page
visual_impairment =  012'

# Special Treatments, Procedures, and Programs
spec_Trtmts = {'
'chemo_IV':         0,
'chemo_oral':       0,
'radiation':        0,
'oxygen':           equipDict['oxygen'],
'suctioning':       0,
'tracheostomy_care':0,
'invase_mech_vent': 0,
'nn_invase_mch_vnt':cpap,
'cpap':             cpap,
'IV_meds':          0,
'transfusions':     0,
'dialysis':         dialysis,
'IV_access':        0  # central, PICC, port
}

spec_Trtmts_count = 0
for k,v in spec_Trtmts.items():
    spec_Trtmts_count += v

# M1033 hospital risk assessment
hospRiskAss = {"
'HSTRY_FALLS':      0,  # 1 History of falls (2 or more falls - or any fall with an injury - in the past 12 months)
'UNINT_WGHTLOSS':   0,  # 2 Unintentional weight loss of a total of 10 pounds or more in the past 12 months
'MULT_HOSPZTN':     0,  # 3 Multiple hospitalizations (2 or more) in the past 6 months
'MULT_EMERG_VISIT': 0,  # 4 Multiple emergency department visits (2 or more) in the past 6 months
'RCNT_DCLN':        0,  # 5 Decline in mental, emotional, or behavioral status in the past 3 months
'COMPLIANCE':       0,  # 6 Reported or observed history of difficulty complying with any medical instructions (for example, medications, diet, exercise) in the past 3 months
'5PLUS_MDCTN':      1,  # 7 Currently taking 5 or more medications
'EXHAUSTION':       1,  # 8 Currently reports exhaustion
'OTHR':             1,  # 9 Other risk(s) not listed in 1-8
'NONE_ABOVE':       0   # 10 None of the above (this will wipe all others out)
}

m1033_comment = "Recent change in meds
if opioid_usage == 1:
    m1033_comment += ", opioid usage"
if numberOfWounds > 0:
    m1033_comment += ", wound, risk of infection"


# # M1800 questions and my default answers, adjust if needed
# "
# M1800 = "02"  # grooming, 1 = can do it if groom tools within reach, 2 = needs help
# M1810 = "02"  # upper body dressing, 1 = can do it handed items, 2 = needs help
# M1820 = "02"  # lower body dressing, 1 = can do it handed items, 2 = needs help
# M1830 = "03"  # bathing, 2 = intermittent help, 3 = can shower with full-time help, 4 = sponge bathe ind, 5 = sponge bathe dep, 6 = full dep
# if painPump == 1:
#     M1830 = "05"
# M1840 = "01"  # toilet trsfr, 1 = with sup, 2 = unable commode but can use bedpan, 3 = help with bedpan, 4 = full dep
# M1845 = "02"  # toilet hygiene, 2 = needs help
# M1850 = "02"  # transferring, 2 = able to bear weight and pivot, 3 = unable to bear weight
# M1860 = "03"  # ambulation, 1= one-handed device, 2 = two-handed device, 3 = able to amb w/ sup, 4 = wc ind, 5 wc dep, 6 = bed
# M1870 = "01"  # feeding, 1 = meal set-up

# M1800 questions and my default answers, adjust if needed
M1800_dict = {'
'M1800':    "02",  # grooming, 1 = can do it if groom tools within reach, 2 = needs help
'M1810':    "02",  # upper body dressing, 1 = can do it handed items, 2 = needs help
'M1820':    "02",  # lower body dressing, 1 = can do it handed items, 2 = needs help
'M1830':    "03",  # bathing, 2 = intermittent help, 3 = can shower with full-time help, 4 = sponge bathe ind, 5 = sponge bathe dep, 6 = full dep
'M1840':    "01",  # toilet trsfr, 1 = with sup, 2 = unable commode but can use bedpan, 3 = help with bedpan, 4 = full dep
'M1845':    "02",  # toilet hygiene, 2 = needs help
'M1850':    "02",  # transferring, 2 = able to bear weight and pivot, 3 = unable to bear weight
'M1860':    "03",  # ambulation, 1= one-handed device, 2 = two-handed device, 3 = able to amb w/ sup, 4 = wc ind, 5 wc dep, 6 = bed
'M1870':    "01"  # feeding, 1 = meal set-up
}
if painPump == 1:
    M1800_dict['M1830'] = "05"


# prior use of device, default is "none"
"
priorWalker = 0
priorWheelchair = 0
priorMotorized = 0


# GG0130 - Self Care and my default answers
# 06 = ind
# 05 = setup
# 04 = sup
# 03 = helper < 0.5
# 02 = helper > 0.5
# 01 = helper = 1
# not attempted:
# 07 = patient refused
# 09 = N/A, not done prior
# 10 = enviro limits
# 88 = med/safety concern
GG0130SOCROC_dict = {"
'A1' : '05',    'A2' : '06',   # eating
'B1' : '04',    'B2' : '06',   # oral_hyg
'C1' : '03',    'C2' : '05',   # toilet hygiene
'E1' : '03',    'E2' : '05',   # shower
'F1' : '04',    'F2' : '06',   # upper body dressing
'G1' : '03',    'G2' : '05',   # lower body dressing
'H1' : '03',    'H2' : '05'    # footwear donning/doffing
}


# GG0170 - mobility with my default answers, adjust if needed
# 06 = ind
# 05 = setup
# 04 = sup
# 03 = helper < 0.5
# 02 = helper > 0.5
# 01 = helper = 1
# not attempted:
# 07 = patient refused
# 09 = N/A, not done prior
# 10 = enviro limits
# 88 = med/safety concern
GG0170SOCROC_dict = {"
'A1' : '04',    'A2' : '06',  # roll left and right
'B1' : '04',    'B2' : '06',  # sit to lying
'C1' : '04',    'C2' : '06',  # lying to sitting on EOB
'D1' : '03',    'D2' : '06',  # sit to stand
'E1' : '03',    'E2' : '05',  # chair/bed-to-chair transfer
'F1' : '03',    'F2' : '05',  # toilet transfer
'G1' : '03',    'G2' : '05',  # car transfer
'I1' : '04',    'I2' : '06',  # walk 10 feet
'J1' : '04',    'J2' : '06',  # walk 50 feet w 2 turns
'K1' : '04',    'K2' : '06',  # walk 150 feet
'L1' : '03',    'L2' : '05',  # walk 10 feet on uneven
'M1' : '04',    'M2' : '06',  # 1 step
'N1' : '88',    'N2' : '06',  # 4 steps
                'O2' : '05',  # 12 steps
'P1' : '03',    'P2' : '05',  # picking up object
'Q1' : '0'  # wheelchair use
}

GG0170SOCROC_wheelchair_dict = {
'R1' : '04',    'R2' : '06',    'RR1' : '1',  # wheel 50 feet with 2 turns, RR1: 1=manual, 2=eletric
'S1' : '04',    'S2' : '06',    'SS1' : '1'   # wheel 150 feet, SS1: 1=manual, 2=electric
}

if GG0170SOCROC_dict['I1'] == '88' or GG0170SOCROC_dict['I1'] == '10' or GG0170SOCROC_dict['I1'] == '09' or GG0170SOCROC_dict['I1'] == '07':
    for i in ['J1', 'K1', 'L1']:
        GG0170SOCROC_dict.pop(i)

if GG0170SOCROC_dict['M1'] == '88' or GG0170SOCROC_dict['M1'] == '10' or GG0170SOCROC_dict['M1'] == '09' or GG0170SOCROC_dict['M1'] == '07':
    for i in ['N1', 'O1']:
        GG0170SOCROC_dict.pop(i)


func_impair_factors = f"Recent {effect}with muscle and joint pain, change in meds
if numberOfWounds > 0:
    func_impair_factors += ", wound precautions"
if opioid_usage == 1:
    func_impair_factors += ", opioid usage"

# BIMS_score= c_rep_3_words + c_year + c_month + c_day_of_week + c_400_sock + c_400_blue + c_400_bed

# Get apropriate username
if branch == 0:
    username = hidden_vars.username_austin
elif branch == 1:
    username = hidden_vars.username_san_antonio

pressure_sore_risk_comment = "Low Risk"
if norton_score < 19:
    pressure_sore_risk_comment = "Medium Risk"
if norton_score < 14:
    pressure_sore_risk_comment = "High Risk"
if norton_score < 10:
    pressure_sore_risk_comment = "Very High Risk"





















##################################################################
###########     Program below; change with caution!     ##########
##################################################################


##### Section 1 fo 3 - variable manipulation for later uses #####


# reformat preloaded phone numbers
if physicianPhone.lstrip().startswith('ph'):
    extra1, extra2, physicianPhoneTemp = physicianPhone.partition('_')
    physicianPhone = physicianPhoneTemp.replace('_', '-')


# MAHC item
if 'no hazards' in livingSituation.lower():
    environmental_hzds = 0
else:
    environmental_hzds = 1

# preloaded hospitals
if sxLocation.lower() == 'sdmc':
    sxLocation = "St. David's Medical Center"
elif sxLocation.lower() == 'nwh':
    sxLocation = "Northwest Hills Surgical Hospital"
elif sxLocation.lower() == 'west':
    sxLocation = "Westlake Surgery Center"
elif sxLocation.lower() == 'cprmc':
    sxLocation = "Cedar Park Regional Medical Center"
elif sxLocation.lower() == 'sdsh':
    sxLocation = "St. David's Surgical Hospital"

if dcedFrom.lower() == 'sdmc':
    dcedFrom = "St. David's Medical Center"
elif dcedFrom.lower() == 'nwh':
    dcedFrom = "Northwest Hills Surgical Hospital"
elif dcedFrom.lower() == 'west':
    dcedFrom = "Westlake Surgery Center"
elif dcedFrom.lower() == 'cprmc':
    dcedFrom = "Cedar Park Regional Medical Center"
elif dcedFrom.lower() == 'sdsh':
    dcedFrom = "St. David's Surgical Hospital"


# correct spellings
if 'aqaucel' in woundDesc.lower():
    woundDesc.replace('aqaucel', 'aquacel')

physs = chh.Physicians()
tempHigh, physicianFullName, woundCare, TEDhose = physs.get_phys_details(physician, woundDesc, POD7DD)
chh_vitals = chh.Vitals()


'''
# preloaded physicians

### borick
# freqBorick_1w1_unk
# phBorick_512_244_0766

### catlett
# freqSatCatlett_1w1_3w1_2w4
# freqSunCatlett_4w1_2w4
# phCatlett_512_476_2830

### dodgin
# freqSatDodgin_1w1_3w1_2w1
# freqSunDodgin_4w1_3w1
# phDodgin_512_476_2830

### gerken
# freqSatGerken_1w1_3w1_2w1
# freqSunGerken_3w2
# phGerken_210_874_3359

### goldberg
# freqSatGoldberg_1w1_4w1_3w1_2w1
# freqSunGoldberg_4w1_3w1_2w1
# phGoldberg_512_856_1000

### gordon
# freqSatGordon_1w1_3w1_2w1
# freqSunGordon_3w2
# phGordon_210_390_0008

### heinrich
# freqSatHeinrich_1w1_4w1_3w1_2w1
# freqSunHeinrich_4w1_3w1_2w1
# phHeinrich_512_476_2830

### hurt
# freqHurt 6 visits in first 14 days
# phHurt_512_856_1000

### hyde
# phHyde_512_346_4933

### manuel
# freqSatManuel_1w1_4w1_3w1_2w1
# freqSunManuel_4w1_3w1_2w1
# phManuel_737_202_2500

### michel
# freqMichel_1w1_3w1_2w3
# phMichel_512_454_4561

### millican
# freqSatMillican_1w1_3w1_2w1
# freqSunMillican_3w2
# phMillican_210_692_7400

### moghimi
# phMoghimi_512_476_2830
# MA = "Payton"
# freqSatMoghimi_1w1_3w1_2w4
# freqSunMoghimi_3w1_2w4

### moore
# phMoore_512_894_2294

### nwelue
# phNwelue_210_804_5400	

'''

if numberOfWounds == 0:
    woundCare = "None - no wounds."

# POC stuff
if needToCallMonday == 0:
    POCapproval = f'Dr. {physicianFullName} protocol'
    orthoProtocol = POCapproval
elif needToCallMonday == 1:
    POCapproval = 'will call Monday morning'
    orthoProtocol = 'none.'
else:
    POCapproval = '____'


otherdisciplines = ""
if nurseFreq != "":
    if "declined" in nurseFreq:
        otherdisciplines += f"{nurseFreq}"
    else:
        nurseFreq = f"{nurseFreq} effective week of {otherDiscFreqEff}"
        otherdisciplines += "Nursing eval ordered. ____ "
if otFreq != "":
    if "declined" in otFreq:
        otherdisciplines += f"{otFreq}"
    else:
        otFreq = f"{otFreq} effective week of {otherDiscFreqEff}"
        otherdisciplines += "OT eval ordered. ____ "
if ptFreq != "":
    ptFreq = f"{ptFreq} effective {evalDate}"
if stFreq != "":
    if "declined" in stFreq:
        otherdisciplines += f"{stFreq}"
    else:
        stFreq = f"{stFreq} effective week of {otherDiscFreqEff}"
        otherdisciplines += "ST eval ordered. ____ "
if MSWfreq != "":
    if "declined" in MSWfreq:
        otherdisciplines += f"{MSWfreq}"
    else:
        MSWfreq = f"{MSWfreq} effective week of {otherDiscFreqEff}"
        otherdisciplines += "MSW eval ordered. ____ "
if HHAfreq != "":
    if "declined" in HHAfreq:
        otherdisciplines += f"{HHAfreq}"
    else:
        HHAfreq = f"{HHAfreq} effective week of {otherDiscFreqEff}"
        otherdisciplines += "HHA ordered. ____ "


if otherdisciplines == "":
    otherdisciplines = """To avoid duplication of services, no other disciplines ordered at this time."""


# adjust PMH incluing adding DM, incontinence if not already in:
PMHfull = PMH
if dm == 1 and 'dm' not in PMH.lower() and 'diabetes' not in PMH.lower():
    PMHfull += ', DM'
if incontinence >= 1 and 'incontinence' not in PMH.lower():
    PMHfull += ', incontinence'


# to help with puncuation with PMHfull and PSxH
if PSxH != "":
    signifMedHx = f"Significant medical history includes: {PMHfull}, {PSxH}."
if PSxH == "":
    signifMedHx = f"Significant medical history includes: {PMHfull}."


# relevant medical hx used in 'Orders...' and 'PT Eval...'
relevantMedHx = f"""{cause} led to {approach}{side}{joint}{effect}performed by \
Dr. {physicianFullName} on {medEventDate} at {sxLocation}. Patient discharged home on {dcDate}. New medications are: \
{newMeds} {signifMedHx} {otherInPatientStay} {painPumpBlurb} {catheterBlurb}"""

if SurgicalSOC == 0:
    effect = effect.strip()
    relevantMedHx = f"""{cause.title()} on {medEventDate} led to {approach}{side}{joint}{effect}. Assessed by \
Dr. {physicianFullName}. {otherInPatientStay} Patient discharged home on {dcDate}. New medications are: \
{newMeds} {signifMedHx} {painPumpBlurb} {catheterBlurb}"""

if painPumpBlurb != "":
    painPumpBlurb = f"\n{painPumpBlurb}\n"
if catheterBlurb != "":
    catheterBlurb = f"\n{catheterBlurb}\n"

# for SOC ROC comm note
SOCrocReport = utils.SOC_ROC_report(age, gender, approach, side, joint, effect, relevantMedHx, woundDesc,
                   physicianFullName, physicianPhone, physicianOthers, F2Fdate,
                   orthoProtocol, POCapproval, dcedFrom, nurseFreq, ptFreq,
                   otFreq, stFreq, MSWfreq, HHAfreq, woundCare, woundCareCustom,
                   PTPOCfocus)


# joint specific clause for main orders
if joint.strip() == 'knee':
    jointOrders = """KNEE ROM goals: For total and partial knee arthroplasty: ROM goal \
for flexion: ~90 degrees and 0 degrees extension by 2-weeks post op. ____
"""
elif joint.strip() == 'back' or joint.strip() == 'spine' or joint.strip() == 'lumbar':
    jointOrders = """NO Bending, Twisting, or Lifting over 10 pounds. ____
"""
elif joint.strip() == 'hip' and 'posterio' in approach.lower():
    jointOrders = """POSTERIOR HIP PRECAUTIONS: No hip flexion > 90 degrees, no adduction \
past midline, and no internal rotation past neutral. ____
"""
elif joint.strip() == 'hip' and 'anterior' in approach.lower():
    jointOrders = """Anterior hip surgery: No hip precautions. ____
"""
else:
    jointOrders = '____no joint orders____'


# main orders
mainOrders = utils.main_orders(medDx, otherdisciplines, tempHigh, woundCare, woundCareCustom, side, joint,
                               effect, wbStatus, jointOrders, TEDhose, painPumpBlurb, painPumpOrders)

# General interventions (everyone admitted gets them, no input needed)
generalInterventions = utils.general_interventions()

# home bound status for ortho patients
hbOrtho = utils.hb_ortho(effect)

# covid screen blurb
covidScreen = utils.covid_screen(myTempTime, myTemp, ptTemp, CV19ss, CV19contact, CV19travel)

##### Section 2 of 3 - define functions, initiate webdriver, open browser #####


# define functions
# these can be removed once all is migrated to utils.py
def PAE():
    print(f"***** {page} AUTOFILL ERROR *****")
    errorFile = open(f'{patientName}_{page}_error_file', 'w')
    errorFile.write(traceback.format_exc())
    errorFile.close()
    print('Traceback written to file.')

def pause_to_autofill():
    input(f"AUTOFILL {page}.")

def scroll_up_then_pause():
    driver.find_element_by_tag_name('html').send_keys(Keys.HOME)
    input(f"'Save & Cont' {page}.")
    driver.find_element_by_id("oasisSaveContinueButton").click()  # 'save and continue'

def clearLink():
    for i in range(len(linksToClear)):
        driver.find_element_by_id('clearLink' + str(linksToClear[i])).click()
    input("<Enter> when all sections cleared and ready to autofill page")




if __name__ == "__main__":
    print("PTA: " + pta + " CM: " + CM + '\n')
    print(forcuraBlurb + '\n')
    print("Wound care on orders: " + woundCare + woundCareCustom + '\n')

    # the next 3 lines can be removed once all sections go through utils.py
    sys.path.append(hidden_vars.filepath_selenium)
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    # initiate webdriver
    driver = utils.webdriver_init(hidden_vars.filepath_webdriver)

    # open browswer
    utils.open_browswer(driver, username)


    ##### Section 3 of 3 - Autofill forms and pages #####


    #### fill out SOC ROC report
    utils.comm_note(driver, patientName, text=SOCrocReport)


    ##### 1 Patient Tracking
    utils.patient_tracking(driver, patientName, visitStartTime, visitEndTime, evalDate, ROC,
                           insurance, caregiverName, caregiverRltnshp, caregiverPhone)


    ##### 2 Administrative
    utils.administrative(driver, patientName, evalDate, dcDate, medDx)


    ##### 3 Vitals
    utils.vitals(driver, previousPatient, ptPulse, ptTemp, ptRR, ptLBP, ptRBP, ht, wt,
                tempHigh, chh_vitals, dm, patientName)


    ##### 4 Patient History and Prognosis
    utils.patient_history_and_prognosis(driver, ROC, previousPatient, side, joint, effect, PMHfull,
                                        PSxH, incontinence, PMH, pna, flu, covid, livingWill,
                                        agencyRCVDcopy, MPOA, DNR, MPOAname, MPOAphone, patientName)


    ##### 5 Hearing, Speech, and Vision
    utils.hearing_speech_vision(driver, previousPatient, hearing, ROC, vision,
                                health_lit, patientName)


    ##### 6 Cog, Mood, Behav
    utils.cog_mood_behav(driver, previousPatient, psychosocial_factors, c_rep_3_words, c_year,
                        c_month, c_day_of_week, c_400_sock, c_400_blue, c_400_bed, delirium,
                        social_isol, anxiety, cog_impairment, patientName)


    ##### 7 Pref Cust Rout Act
    utils.pref_cust_rout_act(driver, previousPatient, patient_care_prefs, patientName)


    ##### 8 Enviro Cond
    utils.enviro_cond(driver, previousPatient, anticoagulant, livingSituation, equipDict,
                      patientName)



    ##### 9 Functional Status
    utils.functional_status(driver, previousPatient, wbStatus, GG0170SOCROC_dict, side, joint,
                      M1800_dict, age, diagnosis_3_plus, fall_in_last_3_mo, visual_impairment,
                      environmental_hzds, poly_pharm_4_plus, cog_impairment, incontinence,
                      tug, equipDict, equipDictOther, catheterType, patientName)

    
    ##### 10 Func Abilities and Goals
    utils.func_abilities_and_goals(driver, cog_impairment, priorWalker, priorWheelchair, 
                             priorMotorized, GG0130SOCROC_dict, GG0170SOCROC_dict,
                             GG0170SOCROC_wheelchair_dict, patientName)

    # page =  "Func Abilities and Goals"

    # try:

    #     # GG0100 prior functioning
    #     driver.find_element_by_id('GG0100_A').send_keys(3)  # prior self care
    #     driver.find_element_by_id('GG0100_B').send_keys(3)  # prior indoor
    #     driver.find_element_by_id('GG0100_C').send_keys(3)  # prior stairs
    #     driver.find_element_by_id('GG0100_D').send_keys(3)  # prior cog
    #     if cog_impairment == 1:
    #         driver.find_element_by_id('GG0100_D').send_keys(2)

    #     # GG0110 prior device
    #     driver.find_element_by_id('GG0110_Z').send_keys(Keys.SPACE)  # Z: none
    #     if priorWalker == 1:
    #         driver.find_element_by_id('GG0110_D').send_keys(Keys.SPACE)  # D: walker
    #     if priorWheelchair == 1:
    #         driver.find_element_by_id('GG0110_A').send_keys(Keys.SPACE)  # A: wheelchair
    #     if priorMotorized == 1:
    #         driver.find_element_by_id('GG0110_B').send_keys(Keys.SPACE)  # B: motorized wheelchair or scooter

    #     # GG0130 Self Care and my default answers
    #     for k,v in GG0130SOCROC_dict.items():
    #         driver.find_element_by_id("GG0130SOCROC_" + k).send_keys(v)

    #     # GG0170 Mobilty and my default answers
    #     for k,v in GG0170SOCROC_dict.items():
    #         driver.find_element_by_id("GG0170SOCROC_" + k).send_keys(v)
    #     if GG0170SOCROC_dict['Q1'] == '1':
    #         for k,v in GG0170SOCROC_wheelchair_dict.items():
    #             driver.find_element_by_id("GG0170SOCROC_" + k).send_keys(v)

    # except:
    #     PAE()

    # scroll_up_then_pause()  # pause to finish and inspect page



    ##### 11 Bladder and Bowel
    utils.bladder_and_bowel(driver, previousPatient, incontinence, catheterType, 
                      antibioticUTI, cathChanged, lastBM, UTI, patientName)

    # page =  "Bladder and Bowel"

    # try:
    #     # clear form from previous episode:
    #     linksToClear = [1,6]
    #     if previousPatient == 1:
    #         clearLink()

    #     # GU
    #     if incontinence >= 1:
    #         driver.find_element_by_id('cES_incont').send_keys(Keys.SPACE)
    #         driver.find_element_by_id('M1610_01').send_keys(Keys.SPACE)

    #     elif incontinence == 0:
    #         driver.find_element_by_id('cES_wnl').send_keys(Keys.SPACE)
    #         driver.find_element_by_id('M1610_00').send_keys(Keys.SPACE)

    #     if catheterType != '':
    #         driver.find_element_by_id('cES_catheter').send_keys(Keys.SPACE)
    #         driver.find_element_by_id('cES_catheterlist').click()
    #         driver.find_element_by_id('cES_catheterlist').send_keys(catheterType[0])
    #         driver.find_element_by_id('cES_catheterchanged').click()
    #         driver.find_element_by_id('cES_catheterchanged').send_keys(cathChanged)
    #         driver.find_element_by_id('M1610_02').send_keys(Keys.SPACE)

    #     driver.find_element_by_id('cES_lastBM').send_keys(Keys.SPACE)  # last BM
    #     driver.find_element_by_id("cES_lastbmdate").click()
    #     driver.find_element_by_id("cES_lastbmdate").send_keys(Keys.BACK_SPACE * 8)
    #     driver.find_element_by_id('cES_lastbmdate').send_keys(lastBM)
    #     driver.find_element_by_id('lbm2').send_keys(Keys.SPACE)  # per pt
    #     driver.find_element_by_id('cES_lbmconstipation').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cc2').send_keys(Keys.SPACE)

    #     # M1600 UTI and prophylactic treatment
    #     driver.find_element_by_id('M1600_00').send_keys(Keys.SPACE)


    #     if antibioticUTI == 1:
    #         driver.find_element_by_id('M1600_NA').send_keys(Keys.SPACE)

    #     if UTI == 1:
    #         driver.find_element_by_id('M1600_01').send_keys(Keys.SPACE)


    #     # M1620 and M1630 bowel incontinence, ostemy
    #     driver.find_element_by_id('M1620_00').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('M1630_00').send_keys(Keys.SPACE)

    #     # dialysis
    #     driver.find_element_by_id('id2').send_keys(Keys.SPACE)


    # except:
    #     PAE()

    # scroll_up_then_pause()  # pause to finish and inspect page




    ##### 12 Active Diagnosis
    utils.active_dx(driver, PMH, dm, patientName)

    # page =  "Active Diagnosis"

    # try:

    #     # M1028 None box - above DM and PVD in case either = 1
    #     driver.find_element_by_id("M1028_ACTV_DIAG_NOA_D").send_keys(Keys.SPACE)

    #     # PVD clause for M1028:
    #     if 'pvd' in PMH.lower():
    #         driver.find_element_by_id("M1028_ACTV_DIAG_PVD_PAD_D").send_keys(Keys.SPACE)

    #     # DM clause for M1028:
    #     if dm == 1:
    #         driver.find_element_by_id("M1028_ACTV_DIAG_DM_D").send_keys(Keys.SPACE)   # M1028

    # except:
    #     PAE()

    # scroll_up_then_pause()  # pause to finish and inspect page



    ##### 13 Health Conditions
    utils.health_conditions(driver, previousPatient, hospRiskAss, m1033_comment, medEventDate, 
                      side, joint, pain, pain_Sleep, pain_TA, pain_DD, patientName)

    # page =  "Health Conditions"

    # try:
    #     # clear form from previous episode:
    #     linksToClear = [2]
    #     if previousPatient == 1:
    #         clearLink()

    #     #M1033 Risk for hospitalization
    #     for key, value in hospRiskAss.items():
    #         if value == 1:
    #             driver.find_element_by_id('CA485_M1033_HOSP_RISK_' + key).send_keys(Keys.SPACE)
    #     driver.find_element_by_id('CA485_M1033_COMMENT').send_keys(m1033_comment)

    #     # Pain
    #     driver.find_element_by_id("cPS_onsetdate").click()  # SOC date
    #     driver.find_element_by_id("cPS_onsetdate").send_keys(Keys.BACK_SPACE * 8)
    #     driver.find_element_by_id('cPS_onsetdate').send_keys(medEventDate)

    #     driver.find_element_by_id('cPS_locpain').send_keys(side + joint)
    #     driver.find_element_by_id('cPS_intpain').send_keys(pain[1])
    #     driver.find_element_by_id('cPS_duration').send_keys('constant ____')
    #     driver.find_element_by_id('cPS_quality').send_keys('ache, sharp')
    #     driver.find_element_by_id('cPS_painworse').send_keys('transfers, end range of motion ____')
    #     driver.find_element_by_id('cPS_painbetter').send_keys('rest, position, ice, elevation, gentle ROM, paid meds ____')
    #     driver.find_element_by_id('cPS_relief').send_keys(pain[0])
    #     driver.find_element_by_id('cPS_meds').send_keys('refer to med list')
    #     driver.find_element_by_id('cPS_effective').send_keys('good ____')
    #     driver.find_element_by_id('cPS_adverse').send_keys('constipation ____')
    #     driver.find_element_by_id('cPS_goal').send_keys('zero pain')

    #     # J0510 Pain effecting sleep
    #     driver.find_element_by_id(f'J0510_{pain_Sleep}').send_keys(Keys.SPACE)

    #     # J0520 Pain interfering with TA (therapeutic activities)
    #     driver.find_element_by_id(f'J0520_0{pain_TA}').send_keys(Keys.SPACE)

    #     # J0530 Pain interfering DD (day to day) activities
    #     driver.find_element_by_id(f'J0530_{pain_DD}').send_keys(Keys.SPACE)

    # except:
    #     PAE()

    # scroll_up_then_pause()  # pause to finish and inspect page


    ##### 14 Respiratory Status
    utils.respitory_status(driver, previousPatient, lungsounds, ptO2, equipDict, 
                     patientName)

    # page =  "Respiratory Status"

    # try:
    #     # clear form from previous episode:
    #     linksToClear = [1]
    #     if previousPatient == 1:
    #         clearLink()

    #     # CTA
    #     driver.find_element_by_id('cRes_cta').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cRes_ctatext').send_keys(lungsounds)

    #     # driver.find_element_by_id('cRes_wnl').send_keys(Keys.SPACE)  # resp
    #     driver.find_element_by_id('cRes_o2sat').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cRes_o2sattext').send_keys(str(ptO2))
    #     driver.find_element_by_id('M1400_02').send_keys(Keys.SPACE)

    #     if equipDict['oxygen'] == 0:
    #         driver.find_element_by_id('cRes_o2satlist').click()
    #         driver.find_element_by_id('cRes_o2satlist').send_keys('r')


    # except:
    #     PAE()

    # scroll_up_then_pause()  # pause to finish and inspect page


    ##### 15 Endocrine
    utils.endocrine(driver, previousPatient, dm, endocrine_dx, patientName)

    # page =  "Endocrine"

    # try:
    #     # clear form from previous episode:
    #     linksToClear = [1]
    #     if previousPatient == 1:
    #         clearLink()

    #     if dm == 1:
    #         driver.find_element_by_id('d1').send_keys(Keys.SPACE)
    #     elif dm == 0:
    #         driver.find_element_by_id('d2').send_keys(Keys.SPACE)
    #     if dm == 0 and endocrine_dx == 0:
    #         driver.find_element_by_id('cEndo_wnl').send_keys(Keys.SPACE)


    # except:
    #     PAE()

    # scroll_up_then_pause()  # pause to finish and inspect page



    ##### 16 Cardiac Status
    utils.cardiac_status(driver, previousPatient, cardiac_dx, side, joint, patientName)

    # page =  "Cardiac Status"

    # try:
    #     # clear form from previous episode:
    #     linksToClear = [1]
    #     if previousPatient == 1:
    #         clearLink()
    #     if cardiac_dx == 0:
    #         driver.find_element_by_id('cCa_wnl').send_keys(Keys.SPACE)  # WNL

    #     driver.find_element_by_id('cCa_chestpain').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cCa_chestpaindesc').send_keys('denies')

    #     driver.find_element_by_id('cCa_dizziness').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cCa_dizzineesdesc').send_keys('denies')

    #     driver.find_element_by_id('cCa_edema').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cCa_edema1').send_keys(f'{side}{joint}')

    #     driver.find_element_by_id('cCa_neckvein').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cCa_neckveindesc').send_keys('none')

    #     driver.find_element_by_id('cCa_peripheral').send_keys(Keys.SPACE)  # peripheral pulses
    #     driver.find_element_by_id('cCa_peripheraldesc').send_keys('regular')

    #     driver.find_element_by_id('cCa_caprefill').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cr1').send_keys(Keys.SPACE)


    # except:
    #     PAE()

    # scroll_up_then_pause()  # pause to finish and inspect page


    ##### 17 Swallowing_Nutritional Status  # M2102_f_01
    utils.swallowing_nutritional_status(driver, previousPatient, numberOfWounds, M1800_dict, 
                                  patientName)

    # page =  "Swallowing_Nutritional Status"

    # try:
    #     # clear form from previous episode:
    #     linksToClear = [1,2,6]
    #     if previousPatient == 1:
    #         clearLink()

    #     # driver.find_element_by_id('cNu_nuwnl').send_keys(Keys.SPACE)  # WNL
    #     driver.find_element_by_id('cNHS_otcmeds').send_keys(Keys.SPACE)  # 3 or more meds
    #     if numberOfWounds > 0:
    #         driver.find_element_by_id('cNHS_openwound').send_keys(Keys.SPACE)  # open wound

    #     # K 0520 Nutritional approaches
    #     driver.find_element_by_id('K0520Z1').send_keys(Keys.SPACE)
    #     if dm == 1:
    #         driver.find_element_by_id('K0520D1').send_keys(Keys.SPACE)

    #     # M1060 Height and weight
    #     driver.find_element_by_id('M1060_HEIGHT_NOT_ASSESSED').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('M1060_WEIGHT_NOT_ASSESSED').send_keys(Keys.SPACE)

    #     # M1870 Feeding or Eating
    #     driver.find_element_by_id("M1870_" + M1800_dict['M1870']).send_keys(Keys.SPACE)  # feeding

    #     # Enter Physician's orders
    #     driver.find_element_by_id('c485PO_regulardiet').send_keys(Keys.SPACE)  # regular diet

    # except:
    #     PAE()

    # scroll_up_then_pause()  # pause to finish and inspect page



    ##### 18 Skin Conditions
    utils.skin_conditions(driver, previousPatient, norton_score, pressure_sore_risk_comment, 
                    SurgicalSOC, numberOfWounds, patientName)

    # page =  "Skin Conditions"

    # try:
    #     # clear form from previous episode:
    #     linksToClear = [2]
    #     if previousPatient == 1:
    #         clearLink()
    #     # risk of ulcers?
    #     driver.find_element_by_id('CA485_PUIR_riskPressureUlcerInjury_2').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('CA485_PUIR_riskAssessmentTool').send_keys('Norton Pressure Score')
    #     driver.find_element_by_id('CA485_PUIR_score').send_keys(norton_score)
    #     driver.find_element_by_id('CA485_PUIR_comments').send_keys(pressure_sore_risk_comment)

    #     # Integumentary Status
    #     driver.find_element_by_id('st1').send_keys(Keys.SPACE)  # skin turgor
    #     driver.find_element_by_id('cIS_skinpinkwnl').send_keys(Keys.SPACE)  # skin color
    #     driver.find_element_by_id('cIS_warm').send_keys(Keys.SPACE)  # warm
    #     driver.find_element_by_id('cIS_incision').send_keys(Keys.SPACE)  # incision
    #     driver.find_element_by_id('iY1').send_keys(Keys.SPACE)  # instructed on infection control
    #     driver.find_element_by_id('n1').send_keys(Keys.SPACE)  # nails 'good'

    #     driver.find_element_by_id('M1306_0').send_keys(Keys.SPACE)  # pressure injury
    #     driver.find_element_by_id('M1322_00').send_keys(Keys.SPACE)  # stage 1
    #     driver.find_element_by_id('M1324_NA').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('M1330_00').send_keys(Keys.SPACE)
    #     driver.find_element_by_id(f'M1340_0{SurgicalSOC}').send_keys(Keys.SPACE)

    #     # unclick these options if no wounds
    #     if numberOfWounds == 0:
    #         driver.find_element_by_id('cIS_warm').send_keys(Keys.SPACE)  # warm
    #         driver.find_element_by_id('cIS_incision').send_keys(Keys.SPACE)  # incision


    # except:
    #     PAE()

    # scroll_up_then_pause()  # pause to finish and inspect page




    ##### 19 Meds
    utils.meds(driver, anticoagulant, antibioticPRO, antibioticUTI, opioid_usage, hypoglycemic_usage, 
         antiplatelet, medInteraction, medInterFollowUp, M2030, patientName)

    # page =  "Meds"

    # try:

    #     # N0415
    #     if anticoagulant == 1:
    #         driver.find_element_by_id('N0415E1').send_keys(Keys.SPACE)
    #         driver.find_element_by_id('N0415E2').send_keys(Keys.SPACE)
    #     if antibioticPRO ==1 or antibioticUTI == 1:
    #         driver.find_element_by_id('N0415F1').send_keys(Keys.SPACE)
    #         driver.find_element_by_id('N0415F2').send_keys(Keys.SPACE)
    #     if opioid_usage == 1:
    #         driver.find_element_by_id('N0415H1').send_keys(Keys.SPACE)
    #         driver.find_element_by_id('N0415H2').send_keys(Keys.SPACE)
    #     if hypoglycemic_usage == 1:
    #         driver.find_element_by_id('N0415J1').send_keys(Keys.SPACE)
    #         driver.find_element_by_id('N0415J2').send_keys(Keys.SPACE)
    #     if antiplatelet == 1:
    #         driver.find_element_by_id('N0415I1').send_keys(Keys.SPACE)
    #         driver.find_element_by_id('N0415I2').send_keys(Keys.SPACE)
    #     if anticoagulant + antibioticPRO + antibioticUTI + opioid_usage + hypoglycemic_usage + antiplatelet == 0:
    #         driver.find_element_by_id('N0415Z1').send_keys(Keys.SPACE)

    #     # M questions
    #     driver.find_element_by_id(f'M2001_{medInteraction}').send_keys(Keys.SPACE)  # M2001 Med interaction
    #     if medInteraction > 0:
    #         driver.find_element_by_id(f'M2003_0{medInterFollowUp}').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('M2010_01').send_keys(Keys.SPACE)  # high risk drug education
    #     driver.find_element_by_id('M2020_03').send_keys(Keys.SPACE)  # mgmt of oral meds
    #     driver.find_element_by_id('M2030_' + M2030).send_keys(Keys.SPACE)  # mgmt of inj meds

    # except:
    #     PAE()

    # scroll_up_then_pause()  # pause to finish and inspect page


    ##### 20 Spec Trtmts, Procs, and Progs
    utils.spec_tx_procs_and_progs(driver, spec_Trtmts_count, cpap, spec_Trtmts, visitCount, ROC, 
                            shingles, patientName)

    # page =  "Spec Trtmts, Procs, and Progs"

    # try:

    #     # O0110
    #     if spec_Trtmts_count == 0:
    #         driver.find_element_by_id('O0110Z1a').send_keys(Keys.SPACE)
    #     if cpap == 1:
    #         driver.find_element_by_id('O0110G1a').send_keys(Keys.SPACE)
    #         time.sleep(1)
    #         driver.find_element_by_id('O0110G3a').send_keys(Keys.SPACE)
    #     if spec_Trtmts['oxygen'] == 1:
    #         driver.find_element_by_id('O0110C1a').send_keys(Keys.SPACE)
    #         time.sleep(1)
    #         driver.find_element_by_id('O0110C2a').send_keys(Keys.SPACE)
    #     if spec_Trtmts['chemo_IV'] == 1 or spec_Trtmts['chemo_oral'] == 1:
    #         driver.find_element_by_id('O0110A1a').send_keys(Keys.SPACE)
    #         time.sleep(1)
    #         if spec_Trtmts['chemo_IV'] == 1:
    #             driver.find_element_by_id('O0110A2a').send_keys(Keys.SPACE)
    #         if spec_Trtmts['chemo_oral'] == 1:
    #             driver.find_element_by_id('O0110A3a').send_keys(Keys.SPACE)
    #     if spec_Trtmts['radiation'] == 1:
    #         driver.find_element_by_id('O0110B1a').send_keys(Keys.SPACE)
    #     if spec_Trtmts['dialysis'] == 1:
    #         driver.find_element_by_id('O0110J1a').send_keys(Keys.SPACE)

    #     # M2200 Therapy Need
    #     M2200 = driver.find_element_by_id("M2200_THER_NEED_NUM")
    #     M2200.send_keys(Keys.BACK_SPACE * 3)
    #     M2200.send_keys(visitCount)

    #     # Randomly placed shingles shot
    #     if ROC == 0:
    #         if shingles == 1:
    #             driver.find_element_by_id('HasShinglesVac').send_keys(Keys.SPACE)
    #         elif shingles == 0:
    #             driver.find_element_by_id('DoesNotHaveShinglesVac').send_keys(Keys.SPACE)
    #     elif ROC == 1:
    #         print("check ROC selections")

    # except:
    #     PAE()

    # scroll_up_then_pause()  # pause to finish and inspect page


    ##### 21 Orders
    utils.orders(driver, previousPatient, ptFreq, nurseFreq, otFreq, stFreq, MSWfreq, HHAfreq, 
           mainOrders, diagnosis_3_plus, ROC, relevantMedHx, generalInterventions, 
           POCapproval, PTPOCfocus, physicianFU, patientName)
           
    # page =  "Orders"

    # try:
    #     # clear form from previous episode:
    #     linksToClear = [1, 2, 3, 4, 5, 6]
    #     if previousPatient == 1:
    #         clearLink()

    #     # order frequency
    #     driver.find_element_by_id("c485ODT_ptfreq").send_keys(ptFreq)
    #     driver.find_element_by_id("c485ODT_snfreq").send_keys(nurseFreq)
    #     driver.find_element_by_id("c485ODT_otfreq").send_keys(otFreq)
    #     driver.find_element_by_id("c485ODT_ltfreq").send_keys(stFreq)
    #     driver.find_element_by_id("c485ODT_mswfreq").send_keys(MSWfreq)
    #     driver.find_element_by_id("c485ODT_hhafreq").send_keys(HHAfreq)

    #     # main orders
    #     driver.find_element_by_id("c485ODT_addorders").send_keys(mainOrders)

    #     # rehab potential - 'good'
    #     driver.find_element_by_id('cpt485RP_gachgoals').send_keys(Keys.SPACE)

    #     # discharge plans
    #     driver.find_element_by_id('cpt485DP_medstable').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cpt485DP_indhelp').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cpt485DP_discaregiver').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cpt485DP_discareself').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cpt485DP_caremanage').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cpt485DP_disgoalsmet').send_keys(Keys.SPACE)

    #     # patient strengths
    #     driver.find_element_by_id('cPStr_mlearner').send_keys(Keys.SPACE)
    #     if diagnosis_3_plus == 0:
    #         driver.find_element_by_id('cPStr_abmultdiag').send_keys(Keys.SPACE)

    #     # Conclusions:
    #     driver.find_element_by_id('cPStr_interneed').send_keys(Keys.SPACE)
    #     driver.find_element_by_id('cPStr_instneed').send_keys(Keys.SPACE)

    #     # skilled intervention
    #     if ROC == 0:
    #         driver.find_element_by_id("cSInt_assessment").send_keys(f"{relevantMedHx} \n\n {generalInterventions}")
    #         driver.find_element_by_id("cSInt_respinter").send_keys(Keys.SPACE)
    #         driver.find_element_by_id("cSInt_vupt").send_keys(Keys.SPACE)
    #         driver.find_element_by_id('cSInt_rdpt').send_keys(Keys.SPACE)
    #         driver.find_element_by_id('cSInt_rftpt').send_keys(Keys.SPACE)
    #         # title of teaching tool
    #         driver.find_element_by_id("cSInt_titletool").send_keys('agency handout')
    #         # progress to goals
    #         driver.find_element_by_id("cSInt_proggoals").send_keys('25%')
    #         # name (conferenced with)
    #         driver.find_element_by_id("cSInt_confname").send_keys('Jason Schwarz')
    #         # regarding
    #         driver.find_element_by_id("cSInt_regarding").send_keys('P.T. POC')
    #         # Physician contacted RE:
    #         driver.find_element_by_id('cSInt_physcontact').send_keys(POCapproval)
    #          # order changes:
    #         driver.find_element_by_id('cSInt_ordchanges').send_keys('none ____')
    #          # plans for next visit
    #         driver.find_element_by_id("cSInt_nvisitplans").send_keys(PTPOCfocus)
    #         # next physician appt
    #         driver.find_element_by_id("cSInt_nvisidate").click()
    #         driver.find_element_by_id("cSInt_nvisidate").send_keys(Keys.BACK_SPACE * 8)
    #         driver.find_element_by_id("cSInt_nvisidate").send_keys(physicianFU)
    #         # discharge planning
    #         driver.find_element_by_id("cSInt_dplanning").send_keys('yes')

    #     elif ROC == 1:
    #         driver.find_element_by_id("cptSInt_assinstperform").send_keys(f"{relevantMedHx} \n\n {generalInterventions}")
    #         driver.find_element_by_id("cptSInt_tolwell").send_keys(Keys.SPACE)
    #         driver.find_element_by_id("cptSInt_respinter").send_keys(Keys.SPACE)
    #         driver.find_element_by_id("cptSInt_vupt").send_keys(Keys.SPACE)
    #         driver.find_element_by_id('cptSInt_rdpt').send_keys(Keys.SPACE)
    #         driver.find_element_by_id('cptSInt_rftpt').send_keys(Keys.SPACE)
    #         driver.find_element_by_id("cptSInt_titletool").send_keys('agency handout')
    #         driver.find_element_by_id("cptSInt_proggoals").send_keys('25%')
    #         driver.find_element_by_id("cptSInt_confname").send_keys('Jason Schwarz')
    #         driver.find_element_by_id("cptSInt_regarding").send_keys('P.T. POC')
    #         driver.find_element_by_id('cptSInt_physcontact').send_keys(POCapproval)
    #         driver.find_element_by_id('cptSInt_ordchanges').send_keys('none ____')
    #         driver.find_element_by_id("cptSInt_nvisitplans").send_keys(PTPOCfocus)
    #         driver.find_element_by_id("cptSInt_nvisidate").click()
    #         driver.find_element_by_id("cptSInt_nvisidate").send_keys(Keys.BACK_SPACE * 8)
    #         driver.find_element_by_id("cptSInt_nvisidate").send_keys(physicianFU)
    #         driver.find_element_by_id("cptSInt_dplanning").send_keys('yes')

    # except:
    #     PAE()

    # scroll_up_then_pause()  # pause to finish and inspect page


    ##### 22 Supplies Worksheet
    utils.supplpies_worksheet(driver)

    # page = "Supplies Worksheet"

    # scroll_up_then_pause()  # pause to finish and inspect page


    ##### 23 Supplies Used This Visit
    utils.supplies_used_this_visit(driver)

    # page =  "Supplies Used This Visit"

    # scroll_up_then_pause()  # pause to finish and inspect page


    ##### 24 PT Evaluation
    utils.pt_evaluation(driver, ROC, relevantMedHx, hbOrtho, covidScreen, livingSituation, subjective, 
                  treatment, pta, CM, forcuraBlurb, woundCare, woundCareCustom, medDx, 
                  medEventDate, evalDate, PLOF, goal, dm, joint, approach, numberOfWounds, 
                  opioid_usage, anticoagulant, spec_Trtmts, woundDesc, side, SurgicalSOC, 
                  rom, mmt, GG0170SOCROC_dict, func_impair_factors, wbStatus, woundLocation, 
                  woundCareProvided, woundCareTolerance, woundDescIndiv, patientName)

    # page =  "PT Evaluation"

    # if ROC == 1:
    #     input("press Enter to print stuff")
    #     print("relavent md hx")
    #     print(relevantMedHx)
    #     print("homebound reason")
    #     print(hbOrtho, covidScreen)
    #     print("living situation")
    #     print(livingSituation)
    #     print("subjective and extra")
    #     print(subjective)
    #     print("treatment")
    #     print(treatment)
    #     print("PTA: " + pta + " CM: " + CM + '\n')
    #     print(forcuraBlurb + '\n')
    #     print("Wound care on orders: " + woundCare + woundCareCustom + '\n')
    #     input("pressing Enter again will run normal program")

    # input("Autofill AFTER loading desired template")

    # try:
    #     # Medical Dx and date
    #     driver.find_element_by_id('frm_MedDiagText').send_keys(medDx)

    #     driver.find_element_by_id("frm_MedDiagOEDate").click()  # Med Dx date (sx date)
    #     driver.find_element_by_id("frm_MedDiagOEDate").send_keys(Keys.BACK_SPACE * 8)
    #     driver.find_element_by_id("frm_MedDiagOEDate").send_keys(medEventDate)

    #     # PT date
    #     driver.find_element_by_id("frm_PTDiagOEDate").click()  # PT Dx date (eval date)
    #     driver.find_element_by_id("frm_PTDiagOEDate").send_keys(Keys.BACK_SPACE * 8)
    #     driver.find_element_by_id("frm_PTDiagOEDate").send_keys(evalDate)

    #     # Rel Med Hx free text box
    #     driver.find_element_by_id('frm_RlvntMedHist').send_keys(relevantMedHx)

    #     # PLOF free text box
    #     driver.find_element_by_id('frm_PriorLevelFunc').send_keys(PLOF)

    #     # Patient goals free rext box
    #     driver.find_element_by_id('frm_PatientGoals').send_keys(goal)

    #     # Precautions
    #     driver.find_element_by_id('frm_PatientPrecautions').send_keys('Universal, Falls')
    #     if dm == 1:
    #         driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Diabetic')
    #     if 'hip' in joint and 'posterio' in approach.lower():
    #         driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Posterior Hip')
    #     if 'back' in joint:
    #         driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Spinal')
    #     if numberOfWounds > 0:
    #         driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Wound')
    #     if opioid_usage == 1:
    #         driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Opioids')
    #     if anticoagulant == 1:
    #         driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Anticoagulation')
    #     if spec_Trtmts['oxygen'] == 1:
    #         driver.find_element_by_id('frm_PatientPrecautions').send_keys(', Oxygen')

    #     # Homebound section:
    #     input('<Enter> for Homebound status')
    #     HB = driver.find_element_by_id("cHo_homebound_cY").send_keys(Keys.SPACE)

    #     input('<Enter> to fill out the rest')
    #     # Criteria 1
    #     driver.find_element_by_id("cHo_homebound_crit1Part1").send_keys(Keys.SPACE)  # HBcrit1Part1
    #     driver.find_element_by_id("cHo_homebound_crit1Part2").send_keys(Keys.SPACE)  # HBcrit1Part2
    #     driver.find_element_by_id("cHo_homebound_crit1Part2_specify").send_keys(hbOrtho)  # HBcrit1Specify

    #     # Criteria 2
    #     driver.find_element_by_id("cHo_homebound_crit2Part1").send_keys(Keys.SPACE)  # HBcrit2Part1
    #     driver.find_element_by_id("cHo_homebound_crit2Part2").send_keys(Keys.SPACE)  # HBcrit2Part2
    #     driver.find_element_by_id("cHo_homebound_crit2Part2_specify").send_keys(hbOrtho, covidScreen)  # HBcrit2Specify

    #     # Social Support/Safety Hazards
    #     driver.find_element_by_id("frm_SafetySanHaz13").send_keys(livingSituation)

    #     # Subjective Info
    #     driver.find_element_by_id("frm_SubInfo").send_keys(subjective)

    #     # Physical Assessment
    #     driver.find_element_by_id("frm_PhyAsmtSkin").send_keys(woundDesc)
    #     if SurgicalSOC >= 1:
    #         driver.find_element_by_id('frm_PhyAsmtCoordination').send_keys(f"Decreased around {side}{joint}")
    #         driver.find_element_by_id('frm_PhyAsmtSensation').send_keys(f"Abnormal around {side}{joint}")
    #         driver.find_element_by_id('frm_PhyAsmtEdemaLocText').send_keys(side + joint)

    #     # add ROM and MMT
    #     if joint.strip() == 'knee' and side.strip() == 'left':
    #         driver.find_element_by_id('frm_ROM94').send_keys(rom[0])  # flexion
    #         driver.find_element_by_id('frm_ROM98').click()
    #         driver.find_element_by_id('frm_ROM98').send_keys(Keys.BACK_SPACE * 3)
    #         driver.find_element_by_id('frm_ROM98').send_keys(rom[1])  # ext
    #         driver.find_element_by_id('frm_ROM96').send_keys(mmt[0])  # flexion mmt
    #         driver.find_element_by_id('frm_ROM100').click()
    #         driver.find_element_by_id('frm_ROM100').send_keys(Keys.BACK_SPACE * 2)
    #         driver.find_element_by_id('frm_ROM100').send_keys(mmt[1])  # ext mmt

    #     if joint.strip() == 'knee' and side.strip() == 'right':
    #         driver.find_element_by_id('frm_ROM93').send_keys(rom[0])  # flexion
    #         driver.find_element_by_id('frm_ROM97').click()
    #         driver.find_element_by_id('frm_ROM97').send_keys(Keys.BACK_SPACE * 3)
    #         driver.find_element_by_id('frm_ROM97').send_keys(rom[1])  # ext
    #         driver.find_element_by_id('frm_ROM95').send_keys(mmt[0])  # flexion mmt
    #         driver.find_element_by_id('frm_ROM99').click()
    #         driver.find_element_by_id('frm_ROM99').send_keys(Keys.BACK_SPACE * 2)
    #         driver.find_element_by_id('frm_ROM99').send_keys(mmt[1])  # ext mmt

    #     if joint.strip() == 'hip' and side.strip() == 'left':
    #         # rom
    #         driver.find_element_by_id('frm_ROM70').send_keys(rom[0])  # flexion rom
    #         driver.find_element_by_id('frm_ROM74').click()
    #         driver.find_element_by_id('frm_ROM74').send_keys(Keys.BACK_SPACE * 3)  # erase extension autofill
    #         driver.find_element_by_id('frm_ROM78').send_keys(rom[1])  # abd rom
    #         driver.find_element_by_id('frm_ROM82').click()
    #         driver.find_element_by_id('frm_ROM82').send_keys(Keys.BACK_SPACE * 3)  # erase adduction autofill
    #         # mmt
    #         driver.find_element_by_id('frm_ROM72').send_keys(mmt[0])  # flexion mmt
    #         driver.find_element_by_id('frm_ROM76').click()
    #         driver.find_element_by_id('frm_ROM76').send_keys(Keys.BACK_SPACE * 3)  # erase extension mmt autofill
    #         driver.find_element_by_id('frm_ROM80').send_keys(mmt[1])  # abd mmt
    #         driver.find_element_by_id('frm_ROM84').click()
    #         driver.find_element_by_id('frm_ROM84').send_keys(Keys.BACK_SPACE * 3)  # erase adduction mmt autofill

    #     if joint.strip() == 'hip' and side.strip() == 'right':
    #         # rom
    #         driver.find_element_by_id('frm_ROM69').send_keys(rom[0])  # flexion rom
    #         driver.find_element_by_id('frm_ROM73').click()
    #         driver.find_element_by_id('frm_ROM73').send_keys(Keys.BACK_SPACE * 3)  # erase extension autofill
    #         driver.find_element_by_id('frm_ROM77').send_keys(rom[1])  # abd rom
    #         driver.find_element_by_id('frm_ROM81').click()
    #         driver.find_element_by_id('frm_ROM81').send_keys(Keys.BACK_SPACE * 3)  # erase adduction autofill
    #         # mmt
    #         driver.find_element_by_id('frm_ROM71').send_keys(mmt[0])  # flexion mmt
    #         driver.find_element_by_id('frm_ROM75').click()
    #         driver.find_element_by_id('frm_ROM75').send_keys(Keys.BACK_SPACE * 3)  # erase extension mmt autofill
    #         driver.find_element_by_id('frm_ROM79').send_keys(mmt[1])  # abd mmt
    #         driver.find_element_by_id('frm_ROM83').click()
    #         driver.find_element_by_id('frm_ROM83').send_keys(Keys.BACK_SPACE * 3)  # erase adduction mmt autofill

    #     if GG0170SOCROC_dict['Q1'] == '1':  # wheelchair use is True
    #         driver.find_element_by_id('frm_FAPT36').send_keys("CGA")        # Level ground assistance
    #         driver.find_element_by_id('frm_FAPT37').send_keys("Mod A x 1")  # Unlevel ground assistance
    #         driver.find_element_by_id('frm_FAPT38').send_keys("CGA")        # Maneuvering assistance
    #         driver.find_element_by_id('frm_FAPT39').send_keys(func_impair_factors)


    #     # Functional Assessment
    #     driver.find_element_by_id('frm_FAPTBedMobComments').send_keys(func_impair_factors)
    #     driver.find_element_by_id('frm_FAPT35').send_keys(func_impair_factors)
    #     driver.find_element_by_id('frm_FAPT22').send_keys(func_impair_factors)
    #     # weightbearing status
    #     driver.find_element_by_id('frm_FAPT40').send_keys(wbStatus)

    #     # add coordination people
    #     driver.find_element_by_id('frm_CareCoordName').send_keys(f", Marcy Sanchez, {CM}, {pta}")

    #     # treatment provided
    #     driver.find_element_by_id('frm_TrtmntPlanComments1').send_keys(treatment)

    #     if numberOfWounds != 0:
    #         for i in range(numberOfWounds):
    #             woundNumber = str(i + 1)
    #             input("Click 'Add (Another) Wound' then <Enter> when ready to autofill 'Wound " + woundNumber + "'")
    #             driver.find_element_by_id(f'frm_wound{woundNumber}Location').send_keys(woundLocation[i])  # Location
    #             driver.find_element_by_id(f'frm_wound{woundNumber}Type').click()
    #             driver.find_element_by_id(f'frm_wound{woundNumber}Type').send_keys("su")  # type - surgical
    #             driver.find_element_by_id(f'frm_wound{woundNumber}PresentOnAdmission').click()  # present on admission
    #             driver.find_element_by_id(f'frm_wound{woundNumber}Treatment').send_keys(woundCareProvided[i])
    #             driver.find_element_by_id(f'frm_wound{woundNumber}PatientResponseToTreatment').send_keys(woundCareTolerance[i])
    #             driver.find_element_by_id(f'frm_wound{woundNumber}AdditionalInformation').send_keys(woundDescIndiv[i])
    #             input("Finish this wound, click 'Save Wound', then <Enter> to continue")

    # except:
    #     PAE()
    #     input('<Enter> to acknowledge')

    print('Good-bye and good luck.\n')
    print("PTA: " + pta + " CM: " + CM + '\n')
    print(forcuraBlurb + '\n')
    print("Wound care on orders: " + woundCare + woundCareCustom + '\n')
