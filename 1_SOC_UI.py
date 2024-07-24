import sys, copy
from datetime import timedelta, datetime
import hidden_vars, chh, utils
sys.path.append(hidden_vars.filepath_CHH)


# change

branch =              0  # 0 = Austin      1 = San Antonio
SOC_ROC_note =        1
fill_out_note =       1
print_forcura_blurb = 1
ROC =                 0


# SOC FOLDER  PT POC   DRESSING   INFECTION   DVT'S   PAIN   BM   WBAT   FALL RISK   AD
subjectiveExtra =   "Passing gas, no BM since
otherInPatientStay= ""
SurgicalSOC =       2'   # 0= no wounds, 1= at least one observable wound, 2= non-observable wounds only

# my variables
myTemp =            ""
myTempTime =        ""
visitStartTime =    "
visitEndTime =      "
evalDate =          "07-18-2024" "    # MM-DD-YYYY

patientName =       "
MR_not_used =       "
ptPhone =           "
address1 =          "
address2 =          "
physician =         "
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
CM =                "Cheryl Campbell

pta =               "
previousPatient =   '

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
approach =          ""  "# anterior | posterolateral | posterior  - HIPS only
F2Fdate =           "
medEventDate =      F2Fdate"          # sxDate
dcedFrom =          "          # 'cprmc' | 'nwh' | 'sdmc' | 'sdsh' | 'west' are preloaded
sxLocation =        dcedFrom"
dcDate =            "
wbStatus =          "

physicianFU =       "  # MM-DD-YYYY

physicianOthers =   "PCP - Dr. _____ at 512-

# ptFreq =            "
# visitCount =        "
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
pain_Sleep =        4'  # 0 = NA, 1 = Rarely or none, 2 = Occasionally, 3 = Frequently, 4 = Near constant, 8 = Unable to answer
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
cog_impairment =    0'  # safety & behavior issues - M1740, M1745
anxiety =           0123'  # 0= none, 1= not daily, 2 = daily, 3 = all the time

phq2 = {'
'little_interest' : 0,
'hopeless' :        0   }
social_isol =       0'
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
MPOAname =          "
MPOAphone =         ["
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
woundCareTolerance =["N/A"]
woundCareCustom =   ""
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

# if oxygen == 1:
DME_co_name = "

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
hypoglycemic_usage =0'  # examples: Ozempic, Actos, Mounjaro, Jardiance
endocrine_dx =      0'
cardiac_dx =        1'

medInteraction =    0'
medInterFollowUp =  0'


PLOF = "Able to ambulate in community for five minutes without assistive device.

num_of_stairs = '

livingSituation = f"""Patient lives with: {num_of_stairs} stairs, ____ spouse, no hazards. ____ \
Spouse ____ helps with ADL's, IADL's, and medication management. \
No ____ barriers to learning. """  " # keep 'no hazards' if no stairs, narrow, pets, or cluttered/soiled items

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

Patient tolerated therapy well. ____
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


patient_care_prefs = "none.

# Braden dict.
braden = {
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

m1033_comment = "Recent change in meds, fall risk
if opioid_usage == 1:
    m1033_comment += ", opioid usage"
if numberOfWounds > 0:
    m1033_comment += ", wound, risk of infection"


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
if num_of_stairs < 12:
    GG0170SOCROC_dict['O2'] = '10'

if num_of_stairs < 4:
    GG0170SOCROC_dict['N1'] = '10'
    GG0170SOCROC_dict['N2'] = '10'


GG0170SOCROC_wheelchair_dict = {
'R1' : '04',    'R2' : '06',    'RR1' : '1',  # wheel 50 feet with 2 turns, RR1: 1=manual, 2=eletric
'S1' : '04',    'S2' : '06',    'SS1' : '1'   # wheel 150 feet, SS1: 1=manual, 2=electric
}

if GG0170SOCROC_dict['I1'] == '88' or GG0170SOCROC_dict['I1'] == '10' or GG0170SOCROC_dict['I1'] == '09' or GG0170SOCROC_dict['I1'] == '07':
    for i in ['J1', 'K1', 'L1']:
        GG0170SOCROC_dict.pop(i)

if GG0170SOCROC_dict['M1'] == '88' or GG0170SOCROC_dict['M1'] == '10' or GG0170SOCROC_dict['M1'] == '09' or GG0170SOCROC_dict['M1'] == '07':
    for i in ['N1', 'O1']:
        try:
            GG0170SOCROC_dict.pop(i)
        except:
            pass

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


# pressure_sore_risk_comment = "Low Risk"
# if norton_score < 19:
#     pressure_sore_risk_comment = "Medium Risk"
# if norton_score < 14:
#     pressure_sore_risk_comment = "High Risk"
# if norton_score < 10:
#     pressure_sore_risk_comment = "Very High Risk"





















##################################################################
###########     Program below; change with caution!     ##########
##################################################################


##### Section 1 of 2 - variable manipulation for later uses #####




# # reformat preloaded phone numbers
# if physicianPhone.lstrip().startswith('ph'):
#     extra1, extra2, physicianPhoneTemp = physicianPhone.partition('_')
#     physicianPhone = physicianPhoneTemp.replace('_', '-')


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

eval_date_obj = datetime.strptime(evalDate, "%m-%d-%Y")
day = eval_date_obj.strftime('%A')  # eval date day of week

physs = chh.Physicians()
tempHigh, physicianFullName, woundCare, TEDhose, freq_auto, visit_count_auto = physs.get_phys_details(physician, woundDesc, POD7DD, day)
chh_vitals = chh.Vitals()



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

ptPOC = copy.deepcopy(ptFreq)

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

# adjust this
if "none" in psychosocial_factors:
    psychosocial_factors = ""
psychosocial_factors += livingSituation

# main orders
mainOrders = utils.main_orders(medDx, otherdisciplines, tempHigh, woundCare, woundCareCustom, side, joint,
                               effect, wbStatus, jointOrders, TEDhose, painPumpBlurb, painPumpOrders)

# General interventions (everyone admitted gets them, no input needed)
generalInterventions = utils.general_interventions()

# # home bound status for ortho patients
# hbOrtho = utils.hb_ortho(effect)

# covid screen blurb
covidScreen = utils.covid_screen(myTempTime, myTemp, ptTemp, CV19ss, CV19contact, CV19travel)


