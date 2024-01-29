import sys, time, traceback
from datetime import date, timedelta, datetime
sys.path.append("C:\\Users\\oto23\\mu_code\\CHH_scripts")
import chh, utils



# version 1.1
branch =              0  # 0 = Austin      1 = San Antonio
SOC_ROC_note =        1
fill_out_note =       1
print_forcura_blurb = 1
ROC =                 0
# TODO dialysis put in program, reasons for wrong answers on cog page,
# TODO ROC supervisory aide visit page,
# TODO add html search on med page for specific class of meds


# SOC FOLDER  PT POC   DRESSING   INFECTION   DVT'S   PAIN   BM   WBAT   FALL RISK   AD
subjectiveExtra =   "Subjective: Pain:    Sleeping:    BM's:
otherInPatientStay= ""
SurgicalSOC =       2'  # 0= no wounds, 1= at least one observable wound, 2= non-observable wounds only
dc_reason =         "Patient met all home health goals and is ready for outpatient therapy
dc_per_patient =    0'
if dc_per_patient:
    dc_reason =     'Per patient request'

visitStartTime =    "
visitEndTime =      "

patientName =       "
MR_not_used =       ""
ptPhone =           "
address1 =          "
address2 =          "
physician =         "  # leave out 'Dr.', 'borick, catlett, dodgin, golderg, heinrich, hyde, manuel, michel, moghimi, nwelue' already loaded
physicianPhone =    ""

caregiverName =     ""
caregiverPhone =    ""
caregiverRltnshp =  ""
# spouse =            "
# spousePhone =       ["

age =               ""
DOB_not_used =      ""
gender =            "  # 'man' or 'woman'
insurance =         "mcr"  "mcrother" "com   yes
previousPatient =   0
pta =               "
CM =                "Cheryl Campbell   Sheri Wariakois

# patient variables
PMH =               ""
PSxH =              ""  # optional (empty str if none)
dm =                '
insulin =           '
diagnosis_3_plus =  0

# allergies =
# pharmacy =
# phone =



side =              ""
joint =             ""
cause =             "DJD"       # {cause} led to ... {effect}
effect =            "T
medDx =             "Aftercare following joint replacement surgery ("+side.upper()+" "+joint.upper()+" "+effect+")"
approach =          ""  # anterior | posteriolateral | posterior  - HIPS only
F2Fdate =           ""
medEventDate =      F2Fdate         # sxDate
dcedFrom =          "  "        # 'cprmc' | 'nwh' | 'sdmc' | 'sdsh' | 'west' are preloaded
sxLocation =        dcedFrom
dcDate =            ""
wbStatus =          ""

evalDate =          "01-12-2024" "yes    # MM-DD-YYYY

physicianFU =       "  # MM-DD-YYYY

physicianOthers =   "PCP - Dr. _____ at 512- ____"

ptFreq =            " "# Dodgin, Heinrich 1w1, 3w1, 2w4; Manuel 1,4,3,2; Michel 1w1, 3w1, 2w3, 'freqName_...' will be reformatted to '1w1, ...'
visitCount =        ""
nurseFreq =         ""
otFreq =            ""
stFreq =            ""
MSWfreq =           ""
HHAfreq =           ""
otherDiscFreqEff =  ""
needToCallMonday =  0

goal =              "Return to"
PTPOCfocus =        "Joint rehab per protocol, gait, balance, transfers, ROM, and strengthening."

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
op_clinic =         "
op_fax =            "

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
depression_dx =     0'
phq2 =              0'  # not used in program
social_isol =       0
psychosocial_factors = "none"
ER_trips =          01"
func_mobility =     "Ind with Equip   Indep


c_rep_3_words =     3' # C0200  how many words correct?
c_year =            3'  # 0 = missed by > 5 years, 1 = 2-5 years off, 2 = one year off, 3 = correct
c_month =           2'   # 0 = missed by > month, 1 = 6 days to 1 month, 2 = accurate within 5 days
c_day_of_week =     1'
c_400_sock =        2'
c_400_blue =        2'
c_400_bed =         2'

ht =                0 # probably not # inches, min = 50
wt =                0 #  probably not # pounds

livingWill =        0
MPOA =              0
MPOAname =          0  # only if MPOA == 1
MPOAphone =         0  # only if MPOA == 1, enter as list
DNR =               0
agencyRCVDcopy =    0

# vaccinations
flu =               '
pna =               0
shingles =          0
covid =             0

# measurements
fall_in_last_3_mo = 0'
tug =               "  # int or str
rom =               ["  # [flex, abd/ext]  ext for knees, abd for hips
mmt =               ["  # [flex, abd/ext]  ext for knees, abd for hips
level_dist =        '
unlevel_dist =      '
num_stairs =        '


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
equipDict = {
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

equipDictOther = {
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
hearing =       0   # 0 = Adequate, 1 = some difficulty, 2 = Increase speaker volume, 3 = absence of useful hearing
vision =        0  # 0 = Adequate, 1 = large print only,2 = limited vision, 3 = highly, 4 = severely
health_lit =    0  # 0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always
delirium =      0'
dialysis =      0      # 1 = hemodialysis, 2 = perotoneal  Still need to code this into the program

side = side.strip() + ' '
joint = joint.strip() + ' '
effect = effect.strip() + ' '
if approach != "":
    approach = approach.strip() + ' '


newMeds =           "blood thinner ____, pain meds ____, stool softeners and laxatives ____, prophylactic antibiotic ____, NSAIDS ____, anti-nausea ____, muscle relaxant ____"
poly_pharm_4_plus = 1
opioid_usage =      1'
antiplatelet =      1'  # aspirin, clopidogrel (Plavix)
anticoagulant =     0'  # Apixaban (Eliquis), Enoxaparin (Lovenox), rivaroxaban (Xarelto), Coumadin, Warfarin, Heparin
antibioticPRO =     0'
antibioticUTI =     0'
UTI =               0'
painPump =          0'
M2030 =             "NA" " # injectable meds 00=ind, 01=dep prep, 02= real-time reminder, 03=unable, NA = no inj meds
meds_chemo =        0'
hypoglycemic_usage =0'  # examples: Ozempic, Actos
endocrine_dx =      0'
cardiac_dx =        1'

medInteraction =    0'
medInterFollowUp =  0'


PLOF = "Able to ambulate in community for five minutes without assistive device."


livingSituation = """Patient lives in a ____ story house with ____ spouse.  Spouse ____ helps with ADL's, IADL's, \
and medication management.  No ____ barriers to learning.  \
No hazards.____ """   # keep 'no hazards' if no stairs, narrow, pets, or cluttered/soiled items

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

Patient tolerated therapy well.
""" "

goals_summary = f"""Patient demonstrates increased strength, balance, ROM and decreased pain which contribute to \
improved transfers, gait, functional mobility, and decreased fall risk.""" "

care_summary = f"""Stengthening, balance, gait, transfers, ROM, safety, infection prevention, DVT prevention."""


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



forcuraBlurb = f"""{patientName} discharged today. Patient reports {pta} ____  \
Thanks for taking great care of our patients.""" "


patient_care_prefs = ""

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
norton = {
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
visual_impairment =  0

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
hospRiskAss = {
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

m1033_comment = "Recent change in meds"
if opioid_usage == 1:
    m1033_comment += ", opioid usage"
if numberOfWounds > 0:
    m1033_comment += ", wound, risk of infection"



# M1800 questions and my default answers, adjust if needed
"
M1800 = "00"  # grooming, 1 = can do it if groom tools within reach, 2 = needs help
M1810 = "00"  # upper body dressing, 1 = can do it handed items, 2 = needs help
M1820 = "00"  # lower body dressing, 1 = can do it handed items, 2 = needs help
M1830 = "00"  # bathing, 2 = intermittent help, 3 = can shower with full-time help, 4 = sponge bathe ind, 5 = sponge bathe dep, 6 = full dep
if painPump == 1:
    M1830 = "05"
M1840 = "00"  # toilet trsfr, 1 = with sup, 2 = unable commode but can use bedpan, 3 = help with bedpan, 4 = full dep
M1845 = "00"  # toilet hygiene, 2 = needs help
M1850 = "01"  # transferring, 2 = able to bear weight and pivot, 3 = unable to bear weight
M1860 = "01"  # ambulation, 1= one-handed device, 2 = two-handed device, 3 = able to amb w/ sup, 4 = wc ind, 5 wc dep, 6 = bed
M1870 = "00"  # feeding, 1 = meal set-up

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
GG0130DC_dict = {"
'A' : '06',  # eating
'B' : '06',  # oral_hyg
'C' : '06',  # toilet hygiene
'E' : '06',  # shower
'F' : '06',  # upper body dressing
'G' : '06',  # lower body dressing
'H' : '06',  # footwear donning/doffing
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
GG0170DC_dict = {"
'A' : '06',  # roll left and right
'B' : '06',  # sit to lying
'C' : '06',  # lying to sitting on EOB
'D' : '06',  # sit to stand
'E' : '06',  # chair/bed-to-chair transfer
'F' : '06',  # toilet transfer
'G' : '06',  # car transfer
'I' : '06',  # walk 10 feet
'J' : '06',  # walk 50 feet w 2 turns
'K' : '06',  # walk 150 feet
'L' : '05',  # walk 10 feet on uneven
'M' : '06',  # 1 step
'N' : '05',  # 4 steps
'O' : '05',  # 12 steps
'P' : '05',  # picking up object
'Q' : '0'  # wheelchair use
}

GG0170DC_wheelchair_dict = {
'R1' : '04',    'R2' : '06',    'RR1' : '1',  # wheel 50 feet with 2 turns, RR1: 1=manual, 2=eletric
'S1' : '04',    'S2' : '06',    'SS1' : '1'   # wheel 150 feet, SS1: 1=manual, 2=electric
}

if GG0170DC_dict['I'] == '88' or GG0170DC_dict['I'] == '10' or GG0170DC_dict['I'] == '09' or GG0170DC_dict['I'] == '07':
    for i in ['J1', 'K1', 'L1']:
        GG0170DC_dict.pop(i)

if GG0170DC_dict['M'] == '88' or GG0170DC_dict['M'] == '10' or GG0170DC_dict['M'] == '09' or GG0170DC_dict['M'] == '07':
    for i in ['N', 'O']:
        GG0170DC_dict.pop(i)



func_impair_factors = f"Recent {effect}with muscle and joint pain, change in meds"
if numberOfWounds > 0:
    func_impair_factors += ", wound precautions"
if opioid_usage == 1:
    func_impair_factors += ", opioid usage"

# BIMS_score= c_rep_3_words + c_year + c_month + c_day_of_week + c_400_sock + c_400_blue + c_400_bed
if branch == 0:
    username = 'jasonschwarz'
elif branch == 1:
    username = 'jasonschwarzpt@gmail.com'

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

'''
# default vital sign parameters
tempHigh = "100.5"  # this will change for pre-loaded physicians
tempLow = 96
pulseHigh = 100
pulseLow = 60
respHigh = 24
respLow = 12
sbpHigh = 170
sbpLow = 100
dbpHigh = 100
dbpLow = 60
o2Low = 90
# if dm == 1: these will be used:
fastBsHigh = 200
fastBsLow = 60
randBsHigh = 200
randBsLow = 60
'''

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
POD7DD = "01-01-2024"
physs = chh.Physicians()
tempHigh, physicianFullName, woundCare, TEDhose = physs.get_phys_details(physician, woundDesc, POD7DD)
vitals = chh.Vitals()





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

# DC report used in 'Communication' note
dc_report = f"""Home Health Discharge REPORT

Patient discharged from all services of Capitol Home Health on {evalDate}.

Reason for discharge: {dc_reason}

Patient and/or caregiver notified of discharge; they verbalized understanding.

Outpatient clinic: {op_clinic}
Outpatient clinic fax numer: {op_fax}
"""




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



# main orders to go on POC:
mainOrders = f"""•
•
Physician orders received. """




# General interventions (everyone admit gets them)
generalInterventions = """Patient

Discussed plan of care and frequency including wound care with patient (and family/caregivers).  \
Therapist and patient in agreement. _____

"""




# HB ortho used on "PT Eval" page
hbOrtho = f"Patient is homebound due to recent {effect} which increases their risk of falls."


# Covid screen used on "PT Eval" page
covidScreen = ""




##### Section 2 of 3 - define functions, initiate webdriver, open browser #####


# define functions

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


print("PTA: " + pta + " CM: " + CM + '\n')
print(forcuraBlurb + '\n')
# print("Wound care on orders: " + woundCare + woundCareCustom + '\n')

if __name__ == "__main__":

    # these 3 lines can be removed once all sections go through utils
    sys.path.append("C:\\users\\oto23\\AppData\\Roaming\\Python\\Python39\\site-packages")
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    # # initiate webdriver
    # # utils.webdriver()


    # # open browser
    # driver = webdriver.Chrome("C:\\Program Files\Google\Chrome\Application\chromedriver")
    # driver.get("https://kinnser.net/login.cfm")
    # userElem = driver.find_element_by_id("username")
    # userElem.send_keys(username)
    # userElem.send_keys(Keys.TAB) # use without password
    # # passElem = driver.find_element_by_id("password")
    # # passElem.send_keys("")
    # # passElem.submit()

    # initiate webdriver
    driver = utils.webdriver_init()

    # open browswer
    utils.open_browswer(driver, username)


    ##### Section 3 of 3 - Autofill forms and pages #####


    #### DC report

    # page = "DC Report"
    # input(f'{patientName} AUTOFILL {page}')
    # try:
    #     driver.find_element_by_id("CallSummary").send_keys(dc_report)

    # except:
    #     utils.autofill_error(page, patientName)

    utils.comm_note(driver, patientName, text=dc_reason)


    ##### 1 Patient Tracking
    page = "Patient Tracking"
    input(f'{patientName} AUTOFILL {page}')

    try:
        driver.find_element_by_id("cTO_timein").send_keys(visitStartTime)  # timeIn
        driver.find_element_by_id("cTO_timeout").send_keys(visitEndTime)  # timeOut

        driver.find_element_by_id("cTO_visitdate").click()  # visitDate
        driver.find_element_by_id("cTO_visitdate").send_keys(evalDate)  # visit date


        #driver.find_element_by_id("M0032_ROC_DT_NA").send_keys(Keys.SPACE)  # ROC button


        # A1110 Language
        '''
        if ROC == 0:
            driver.find_element_by_id("A1110A").send_keys("English")
            driver.find_element_by_id("A1110B_1").send_keys(Keys.SPACE)
        elif ROC == 1:
            print("check language selection")
        '''

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
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page


    ##### 2 Administrative
    page = "Administrative"
    input(f'{patientName} AUTOFILL {page}')

    try:
        driver.find_element_by_id("M0090_INFO_COMPLETED_DT").click()  # assessment date
        driver.find_element_by_id("M0090_INFO_COMPLETED_DT").send_keys(Keys.BACK_SPACE * 8)
        driver.find_element_by_id("M0090_INFO_COMPLETED_DT").send_keys(evalDate)

        # driver.find_element_by_id("M0102_PHYSN_ORDRD_SOCROC_DT_NA").send_keys(Keys.SPACE)

        # driver.find_element_by_id("M0104_PHYSN_RFRL_DT").click()  # MD ordered date
        # driver.find_element_by_id("M0104_PHYSN_RFRL_DT").send_keys(Keys.BACK_SPACE * 8)
        # driver.find_element_by_id("M0104_PHYSN_RFRL_DT").send_keys(dcDate)

        driver.find_element_by_id("M0906_DC_TRAN_DTH_DT").click()  # assessment date
        driver.find_element_by_id("M0906_DC_TRAN_DTH_DT").send_keys(Keys.BACK_SPACE * 8)
        driver.find_element_by_id("M0906_DC_TRAN_DTH_DT").send_keys(evalDate)

        # driver.find_element_by_id("M0110_01").send_keys(Keys.SPACE)  # 'early' episode

        # A1250 Transportation
        driver.find_element_by_id("A1250C").send_keys(Keys.SPACE)

        # ER trips
        if ER_trips == 0:
            driver.find_element_by_id("M2301_00").send_keys(Keys.SPACE)

        # M2410 to which inpatient facility
        driver.find_element_by_id("M2410_NA").send_keys(Keys.SPACE)

        # M2420 Discharge Disposition
        driver.find_element_by_id("M2420_01").send_keys(Keys.SPACE)

        # A2121 Med list to next provider
        # driver.find_element_by_id("A2121_00").send_keys(Keys.SPACE)  # No

        # A2123 Med list to patient
        driver.find_element_by_id("A2123_01").send_keys(Keys.SPACE)  # yes
        driver.find_element_by_id("A2124D").send_keys(Keys.SPACE)  # on paper

    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page


    ##### 3 Vitals
    page = "Vitals"
    pause_to_autofill()
    try:
        # clear form from previous episode:
        linksToClear = [2]
        if previousPatient == 1:
            clearLink()

        # enter patient vitals:
        driver.find_element_by_id("cVS_pulseradical").send_keys(ptPulse)  # pulse
        driver.find_element_by_id("PulseRadicalRegular1").send_keys(Keys.SPACE)  # pulseReg
        driver.find_element_by_id("cVS_temperature").send_keys(ptTemp)  # temp
        driver.find_element_by_id("cVS_respiratory").send_keys(ptRR)  # resp
        driver.find_element_by_id("cVS_bplsitting").send_keys(ptLBP)  # left arm bp, sitting
        driver.find_element_by_id("cVS_bprsitting").send_keys(ptRBP)  # right arm bp, sitting
        # driver.find_element_by_id("cVS_height").send_keys(str(ht) + " inches")  # height
        # driver.find_element_by_id("cVS_weight").send_keys(str(wt) + " lbs")  # weight
        # driver.find_element_by_id("cActual2").send_keys(Keys.SPACE)  # "stated" ht and wt

        # enter vital sign parameters:
        '''
        driver.find_element_by_id("c485np_temphigh").send_keys(tempHigh)  # np_tempHigh
        driver.find_element_by_id("c485np_templow").send_keys(vitals.temp_low)  # np_tempLow
        driver.find_element_by_id("c485np_pulsehigh").send_keys(vitals.pulse_high)  # np_pulsehigh
        driver.find_element_by_id("c485np_pulselow").send_keys(vitals.pulse_low)  # np_pulselow
        driver.find_element_by_id("c485np_resphigh").send_keys(vitals.resp_high)  # np_resphigh
        driver.find_element_by_id("c485np_resplow").send_keys(vitals.resp_low)  # np_resplow
        driver.find_element_by_id("c485np_syshigh").send_keys(vitals.sbp_high)  # np_syshigh
        driver.find_element_by_id("c485np_syslow").send_keys(vitals.sbp_lLow)  # np_syslow
        driver.find_element_by_id("c485np_diashigh").send_keys(vitals.dbp_high)  # np_diashigh
        driver.find_element_by_id("c485NP_DiasLow").send_keys(vitals.dbp_low)  # np_diaslow
        driver.find_element_by_id("c485np_02stat").send_keys(vitals.o2_low)  # np_02stat
        if dm == 1:
            driver.find_element_by_id("c485np_fastbslevelgt").send_keys(vitals.fast_bs_High)
            driver.find_element_by_id("c485np_fastbslevellt").send_keys(vitals.fast_bs_low)
            driver.find_element_by_id("c485np_randombslevelgt").send_keys(vitals.rand_bs_high)
            driver.find_element_by_id("c485np_randombslevellt").send_keys(vitals.rand_bs_low)
        '''
    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page


    ##### 4 Patient History and Prognosis
    page = "Patient History and Prognosis"
    # pause_to_autofill()
    try:
        # clear form from previous episode:
        linksToClear = [1,2,4,8]
        if ROC == 1:
            linksToClear = [1,2]
        if previousPatient == 1:
            clearLink()

        # PMH list with check boxes and comments
        '''
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
        '''

        # Immunizations
        '''
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
        '''
        # Health Screeing
        # nothing to autofill

        # Advanced Directives
        '''
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
        '''
        # surragate decision maker
        '''
        driver.find_element_by_id('hs2').send_keys(Keys.SPACE)  # for pink box
        driver.find_element_by_id('frm_ACPsurrRecordDocumentedNo').send_keys(Keys.SPACE)  # for purple box
        '''

        # patient have a discussion with HHA re advanced care plan or surrogate decision maker
        driver.find_element_by_id('frm_ACPdiscussWithHHAYes').send_keys(Keys.SPACE)

        driver.find_element_by_id('frm_ACPrecordDocumentedNo').send_keys(Keys.SPACE)

        driver.find_element_by_id('frm_ACPsurrRecordDocumentedNo').send_keys(Keys.SPACE)

        # prognosis
        # driver.find_element_by_id('pp3').send_keys(Keys.SPACE)

        # functional limitations
        '''
        driver.find_element_by_id('c485FI_ambulation').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485FI_endurance').send_keys(Keys.SPACE)
        driver.find_element_by_id('c485FI_dyspnea').send_keys(Keys.SPACE)
        if incontinence >= 1:
            driver.find_element_by_id('c485FI_bowelincont').send_keys(Keys.SPACE)
        '''

    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page

    ##### 5 Hearing, Speech, and Vision
    page = "Hearing, Speech, and Vision"

    try:
        # clear form from previous episode:
        linksToClear = [1]
        if previousPatient == 1:
            clearLink()

        # TODO code goes here
        '''
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
        '''
        # B1300 Health Literacy
        if health_lit is not None:
            driver.find_element_by_id(f"B1300_{health_lit}").send_keys(Keys.SPACE)


    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page


    ##### 6 Cog, Mood, Behav
    page = "Cog, Mood, Behav"

    try:
        # clear form from previous episode:
        linksToClear = [1]
        if previousPatient == 1:
            clearLink()

        # Mental status
        '''
        orientation = ['person', 'time', 'place', 'situation']
        for thing in orientation:
            driver.find_element_by_id(f'CA485_MS_{thing}_Ori').send_keys(Keys.SPACE)
        # driver.find_element_by_id('CA485_MS_person_Ori').send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_MS_memoryNoProblems').send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_MS_neuroNoProblems').send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_MS_behavioralAppropriateWNL').send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_MS_moodAppropriateWNL').send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_MS_pyschosocial').send_keys(psychosocial_factors)
        '''

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

        # M1700
        driver.find_element_by_id('M1700_00').send_keys(Keys.SPACE)
        # M1720
        driver.find_element_by_id('M1710_00').send_keys(Keys.SPACE)
        # M1720
        driver.find_element_by_id(f'M1720_0{anxiety}').send_keys(Keys.SPACE)

        # D 0700 Social Isolation
        driver.find_element_by_id(f'D0700_{social_isol}').send_keys(Keys.SPACE)

        # M1740
        driver.find_element_by_id('M1740_BD_NONE').send_keys(Keys.SPACE)
        # M1745
        driver.find_element_by_id('M1745_00').send_keys(Keys.SPACE)

        '''
        if anxiety > 1:
            driver.find_element_by_id('CA485_MS_anxious').send_keys(Keys.SPACE)
        '''

        if cog_impairment == 1:
            driver.find_element_by_id('CA485_MS_forgetful_E').send_keys(Keys.SPACE)
            driver.find_element_by_id('M1700_01').send_keys(Keys.SPACE)
            driver.find_element_by_id('M1710_01').send_keys(Keys.SPACE)
            #driver.find_element_by_id('c485MS_forgetful').send_keys(Keys.SPACE)

    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page


    ##### 7 Pref Cust Rout Act
    page = "Pref Cust Rout Act"

    try:
        # clear form from previous episode:
        linksToClear = [3, 4, 5]
        if previousPatient == 1:
            clearLink()

        # TODO code goes here
        # M2102
        driver.find_element_by_id('M2102_a_00').send_keys(Keys.SPACE)
        driver.find_element_by_id('M2102_c_00').send_keys(Keys.SPACE)
        driver.find_element_by_id('M2102_d_00').send_keys(Keys.SPACE)
        driver.find_element_by_id('M2102_f_00').send_keys(Keys.SPACE)
        '''
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
        '''

    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page


    ##### 8 Enviro Cond
    '''
    page = "Enviro Cond"

    try:
        # clear form from previous episode:
        linksToClear = [1,2,3]
        if previousPatient == 1:
            clearLink()

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


    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page
    '''

    ##### 9 Functional Status
    page = "Functional Status"

    try:
        # clear form from previous episode:
        linksToClear = [1,2,11,12,14]
        if previousPatient == 1:
            clearLink()

        # Activities Permitted:
        '''
        driver.find_element_by_id("c485AP_walker").send_keys(Keys.SPACE)
        driver.find_element_by_id("c485AP_expres").send_keys(Keys.SPACE)
        driver.find_element_by_id("c485AP_tbedchair").send_keys(Keys.SPACE)
        driver.find_element_by_id('c485AP_msother').send_keys(wbStatus)
        if GG0170SOCROC_dict['Q1'] == '1':
            driver.find_element_by_id('c485AP_wheelchair').send_keys(Keys.SPACE)
        '''

        # Musculoskeletal:
        '''
        driver.find_element_by_id("cMSk_weakness").send_keys(Keys.SPACE)  # mskWeakness
        driver.find_element_by_id("cMSk_ambdifficult").send_keys(Keys.SPACE)  # mskAmbDifficult
        driver.find_element_by_id("cMSk_limitmob").send_keys(Keys.SPACE)  # mskLimitMobBox
        driver.find_element_by_id("cMSk_limitedmobdesc").send_keys(f'{side}{joint}')  # mskLimitedMobComment
        driver.find_element_by_id("cMSk_jointstiff").send_keys(Keys.SPACE)  # mskJointStiffBox
        driver.find_element_by_id("cMSk_jointstiffdesc").send_keys(f'{side}{joint}')  # mskJointStiffComment
        driver.find_element_by_id("cMSk_pbalance").send_keys(Keys.SPACE)  # mskPBalance
        driver.find_element_by_id("cMSk_assistdev").send_keys(Keys.SPACE)  # mskAssistDevBox
        driver.find_element_by_id("cMSk_assistdevdesc").send_keys("2 wheel walker")  # mskAssistDevComment
        '''

        # M1800 questions and my default answers:
        driver.find_element_by_id("M1800_" + M1800).send_keys(Keys.SPACE)  # grooming
        driver.find_element_by_id("M1810_" + M1810).send_keys(Keys.SPACE)  # upper body dressing
        driver.find_element_by_id("M1820_" + M1820).send_keys(Keys.SPACE)  # lower body dressing
        driver.find_element_by_id("M1830_" + M1830).send_keys(Keys.SPACE)  # bathing
        driver.find_element_by_id("M1840_" + M1840).send_keys(Keys.SPACE)  # toilet trsfr
        driver.find_element_by_id("M1845_" + M1845).send_keys(Keys.SPACE)  # toilet hygiene
        driver.find_element_by_id("M1850_" + M1850).send_keys(Keys.SPACE)  # transferring
        driver.find_element_by_id("M1860_" + M1860).send_keys(Keys.SPACE)  # ambulation

        # MAHC 10 Risk assessment tool
        '''
        if age == '':
            print('Enter age: (you only get one chance)')
            age = input()
        # TODO  add data validation clause to ensure interger provided for age
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
        '''

    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page




    ##### 10 Func Abilities and Goals
    page =  "Func Abilities and Goals"

    try:

        # GG0100 prior functioning
        '''
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
        '''

        # GG0130 Self Care and my default answers
        for k,v in GG0130DC_dict.items():
            driver.find_element_by_id("GG0130DC_" + k).send_keys(v)

        # GG0170 Mobilty and my default answers
        for k,v in GG0170DC_dict.items():
            driver.find_element_by_id("GG0170DC_" + k).send_keys(v)
        if GG0170DC_dict['Q'] == '1':
            for k,v in GG0170DC_wheelchair_dict.items():
                driver.find_element_by_id("GG0170DC_" + k).send_keys(v)

    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page



    ##### 11 Bladder and Bowel
    page =  "Bladder and Bowel"

    try:
        # clear form from previous episode:
        linksToClear = [1,6]
        if previousPatient == 1:
            clearLink()

        # GU
        '''
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
        '''

        # driver.find_element_by_id('cES_lastBM').send_keys(Keys.SPACE)  # last BM
        driver.find_element_by_id("cES_lastbmdate").click()
        driver.find_element_by_id("cES_lastbmdate").send_keys(Keys.BACK_SPACE * 8)
        driver.find_element_by_id('cES_lastbmdate').send_keys(lastBM)
        driver.find_element_by_id('lbm2').send_keys(Keys.SPACE)  # per pt

        # driver.find_element_by_id('cES_lbmconstipation').send_keys(Keys.SPACE)
        # driver.find_element_by_id('cc2').send_keys(Keys.SPACE)

        # M1600 UTI and prophylactic treatment
        driver.find_element_by_id('M1600_00').send_keys(Keys.SPACE)


        if antibioticUTI == 1:
            driver.find_element_by_id('M1600_NA').send_keys(Keys.SPACE)

        if UTI == 1:
            driver.find_element_by_id('M1600_01').send_keys(Keys.SPACE)


        # M1620 and M1630 bowel incontinence, ostemy
        driver.find_element_by_id('M1620_00').send_keys(Keys.SPACE)
        # driver.find_element_by_id('M1630_00').send_keys(Keys.SPACE)

        # dialysis
        # driver.find_element_by_id('id2').send_keys(Keys.SPACE)


    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page




    ##### 12 Active Diagnosis
    '''
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
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page

    '''

    ##### 13 Health Conditions
    page =  "Health Conditions"

    try:
        # clear form from previous episode:
        linksToClear = [2]
        if previousPatient == 1:
            clearLink()

        #M1033 Risk for hospitalization
        '''
        for key, value in hospRiskAss.items():
            if value == 1:
                driver.find_element_by_id('CA485_M1033_HOSP_RISK_' + key).send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_M1033_COMMENT').send_keys(m1033_comment)
        '''

        # Pain
        '''
        driver.find_element_by_id("cPS_onsetdate").click()  # SOC date
        driver.find_element_by_id("cPS_onsetdate").send_keys(Keys.BACK_SPACE * 8)
        driver.find_element_by_id('cPS_onsetdate').send_keys(medEventDate)
        '''

        # driver.find_element_by_id('cPS_locpain').send_keys(side + joint)
        driver.find_element_by_id('cPS_intpain').send_keys(pain[1])
        # driver.find_element_by_id('cPS_duration').send_keys('constant ____')
        # driver.find_element_by_id('cPS_quality').send_keys('ache, sharp')
        # driver.find_element_by_id('cPS_painworse').send_keys('transfers, end range of motion ____')
        # driver.find_element_by_id('cPS_painbetter').send_keys('rest, position, ice, elevation, gentle ROM, paid meds ____')
        driver.find_element_by_id('cPS_relief').send_keys(pain[0])
        # driver.find_element_by_id('cPS_meds').send_keys('refer to med list')
        # driver.find_element_by_id('cPS_effective').send_keys('good ____')
        driver.find_element_by_id('cPS_adverse').send_keys('none ____')
        driver.find_element_by_id('cPS_goal').send_keys(' or zero pain')

        # J0510 Pain effecting sleep
        driver.find_element_by_id(f'J0510_{pain_Sleep}').send_keys(Keys.SPACE)

        # J0520 Pain interfering with TA (therapeutic activities)
        driver.find_element_by_id(f'J0520_0{pain_TA}').send_keys(Keys.SPACE)

        # J0530 Pain interfering DD (day to day) activities
        driver.find_element_by_id(f'J0530_{pain_DD}').send_keys(Keys.SPACE)



    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page




    ##### 14 Respiratory Status
    page =  "Respiratory Status"

    try:
        # clear form from previous episode:
        linksToClear = [1]

        # if previousPatient == 1:
        #  clearLink()

        clearLink()

        # CTA
        driver.find_element_by_id('cRes_cta').send_keys(Keys.SPACE)
        driver.find_element_by_id('cRes_ctatext').send_keys(lungsounds)

        # driver.find_element_by_id('cRes_wnl').send_keys(Keys.SPACE)  # resp
        driver.find_element_by_id('cRes_o2sat').send_keys(Keys.SPACE)
        driver.find_element_by_id('cRes_o2sattext').send_keys(str(ptO2))
        driver.find_element_by_id('M1400_00').send_keys(Keys.SPACE)

        if equipDict['oxygen'] == 0:
            driver.find_element_by_id('cRes_o2satlist').click()
            driver.find_element_by_id('cRes_o2satlist').send_keys('r')


    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page


    ##### 15 Endocrine
    page =  "Endocrine"

    try:
        # clear form from previous episode:
        linksToClear = [1]
        if previousPatient == 1:
            clearLink()
        '''
        if dm == 1:
            driver.find_element_by_id('d1').send_keys(Keys.SPACE)
        elif dm == 0:
            driver.find_element_by_id('d2').send_keys(Keys.SPACE)
        if dm == 0 and endocrine_dx == 0:
            driver.find_element_by_id('cEndo_wnl').send_keys(Keys.SPACE)

        '''
    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page



    ##### 16 Cardiac Status
    page =  "Cardiac Status"

    try:
        # clear form from previous episode:
        linksToClear = [1]
        if previousPatient == 1:
            clearLink()
        if cardiac_dx == 0:
            driver.find_element_by_id('cCa_wnl').send_keys(Keys.SPACE)  # WNL
        '''
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

        '''
    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page




    ##### 17 Swallowing_Nutritional Status  # M2102_f_01
    page =  "Swallowing_Nutritional Status"

    try:
        # clear form from previous episode:
        linksToClear = [1,2,6]
        if previousPatient == 1:
            clearLink()

        # driver.find_element_by_id('cNu_nuwnl').send_keys(Keys.SPACE)  # WNL
        # driver.find_element_by_id('cNHS_otcmeds').send_keys(Keys.SPACE)  # 3 or more meds

        # K 0520 Nutritional approaches
        driver.find_element_by_id('K0520Z4').send_keys(Keys.SPACE)
        driver.find_element_by_id('K0520Z5').send_keys(Keys.SPACE)
        if dm == 1:
            driver.find_element_by_id('K0520D4').send_keys(Keys.SPACE)
            driver.find_element_by_id('K0520D5').send_keys(Keys.SPACE)

        # M1060 Height and weight
        '''
        driver.find_element_by_id('M1060_HEIGHT_NOT_ASSESSED').send_keys(Keys.SPACE)
        driver.find_element_by_id('M1060_WEIGHT_NOT_ASSESSED').send_keys(Keys.SPACE)
        '''

        # M1870 Feeding or Eating
        driver.find_element_by_id("M1870_" + M1870).send_keys(Keys.SPACE)  # feeding

        # Enter Physician's orders
        # driver.find_element_by_id('c485PO_regulardiet').send_keys(Keys.SPACE)  # regular diet

    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page



    ##### 18 Skin Conditions
    page =  "Skin Conditions"

    try:
        # clear form from previous episode:
        linksToClear = [2]
        if previousPatient == 1:
            clearLink()
        # risk of ulcers?
        '''
        driver.find_element_by_id('CA485_PUIR_riskPressureUlcerInjury_2').send_keys(Keys.SPACE)
        driver.find_element_by_id('CA485_PUIR_riskAssessmentTool').send_keys('Norton Pressure Score')
        driver.find_element_by_id('CA485_PUIR_score').send_keys(norton_score)
        driver.find_element_by_id('CA485_PUIR_comments').send_keys(pressure_sore_risk_comment)
        '''

        # Integumentary Status
        '''
        driver.find_element_by_id('st1').send_keys(Keys.SPACE)  # skin turgor
        driver.find_element_by_id('cIS_skinpinkwnl').send_keys(Keys.SPACE)  # skin color
        driver.find_element_by_id('cIS_warm').send_keys(Keys.SPACE)  # warm
        driver.find_element_by_id('cIS_incision').send_keys(Keys.SPACE)  # incision
        driver.find_element_by_id('iY1').send_keys(Keys.SPACE)  # instructed on infection control
        driver.find_element_by_id('n1').send_keys(Keys.SPACE)  # nails 'good'
        '''

        driver.find_element_by_id('M1306_0').send_keys(Keys.SPACE)  # pressure injury
        # driver.find_element_by_id('M1307_NA').send_keys(Keys.SPACE)
        # driver.find_element_by_id('M1322_00').send_keys(Keys.SPACE)  # stage 1
        driver.find_element_by_id('M1324_NA').send_keys(Keys.SPACE)
        driver.find_element_by_id('M1330_00').send_keys(Keys.SPACE)
        driver.find_element_by_id(f'M1340_0{SurgicalSOC}').send_keys(Keys.SPACE)

        # unclick these options if no wounds
        if numberOfWounds == 0:
            driver.find_element_by_id('cIS_warm').send_keys(Keys.SPACE)  # warm
            driver.find_element_by_id('cIS_incision').send_keys(Keys.SPACE)  # incision


    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page




    ##### 19 Meds
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
        if antiplatelet == 1:
            driver.find_element_by_id('N0415I1').send_keys(Keys.SPACE)
            driver.find_element_by_id('N0415I2').send_keys(Keys.SPACE)
        if hypoglycemic_usage == 1:
            driver.find_element_by_id('N0415J1').send_keys(Keys.SPACE)
            driver.find_element_by_id('N0415J2').send_keys(Keys.SPACE)
        if anticoagulant + antibioticPRO + antibioticUTI + opioid_usage + hypoglycemic_usage + antiplatelet == 0:
            driver.find_element_by_id('N0415Z1').send_keys(Keys.SPACE)

        # M questions
        # driver.find_element_by_id(f'M2001_{medInteraction}').send_keys(Keys.SPACE)  # M2001 Med interaction
        # if medInteraction > 0:
          #  driver.find_element_by_id(f'M2003_0{medInterFollowUp}').send_keys(Keys.SPACE)
        # driver.find_element_by_id('M2010_01').send_keys(Keys.SPACE)  # high risk drug education
        driver.find_element_by_id('M2005_9').send_keys(Keys.SPACE)
        driver.find_element_by_id('M2020_00').send_keys(Keys.SPACE)  # mgmt of oral meds
        # driver.find_element_by_id('M2030_' + M2030).send_keys(Keys.SPACE)  # mgmt of inj meds

    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page


    ##### 20 Spec Trtmts, Procs, and Progs
    page =  "Spec Trtmts, Procs, and Progs"

    try:

        # O0110
        if spec_Trtmts_count == 0:
            driver.find_element_by_id('O0110Z1c').send_keys(Keys.SPACE)
        if cpap == 1:
            driver.find_element_by_id('O0110G1c').send_keys(Keys.SPACE)
            time.sleep(1)
            driver.find_element_by_id('O0110G3c').send_keys(Keys.SPACE)
        if spec_Trtmts['oxygen'] == 1:
            driver.find_element_by_id('O0110C1c').send_keys(Keys.SPACE)
            time.sleep(1)
            driver.find_element_by_id('O0110C2c').send_keys(Keys.SPACE)
        if spec_Trtmts['chemo_IV'] == 1 or spec_Trtmts['chemo_oral'] == 1:
            driver.find_element_by_id('O0110A1c').send_keys(Keys.SPACE)
            time.sleep(1)
            if spec_Trtmts['chemo_IV'] == 1:
                driver.find_element_by_id('O0110A2c').send_keys(Keys.SPACE)
            if spec_Trtmts['chemo_oral'] == 1:
                driver.find_element_by_id('O0110A3c').send_keys(Keys.SPACE)
        if spec_Trtmts['radiation'] == 1:
            driver.find_element_by_id('O0110B1c').send_keys(Keys.SPACE)
        if spec_Trtmts['dialysis'] == 1:
            driver.find_element_by_id('O0110J1c').send_keys(Keys.SPACE)

        # M2200 Therapy Need
        '''
        M2200 = driver.find_element_by_id("M2200_THER_NEED_NUM")
        M2200.send_keys(Keys.BACK_SPACE * 3)
        M2200.send_keys(visitCount)
        '''
        # M 1041
        driver.find_element_by_id('M1041_1').send_keys(Keys.SPACE)
        # M 1046
        if flu:
            driver.find_element_by_id('M1046_03').send_keys(Keys.SPACE)
        else:
            driver.find_element_by_id('M1046_08').send_keys(Keys.SPACE)

        # Randomly placed shingles shot
        '''
        if ROC == 0:
            if shingles == 1:
                driver.find_element_by_id('HasShinglesVac').send_keys(Keys.SPACE)
            elif shingles == 0:
                driver.find_element_by_id('DoesNotHaveShinglesVac').send_keys(Keys.SPACE)
        elif ROC == 1:
            print("check ROC selections")
        '''
        # shingles shot offered?
        driver.find_element_by_id('frm_ShingleOfferedOptionNo').send_keys(Keys.SPACE)
        driver.find_element_by_id('frm_ShingleReceivedOtherOptionNo').send_keys(Keys.SPACE)


    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page


    ##### 21 Orders
    page =  "Orders"

    try:
        # clear form from previous episode:
        linksToClear = [1, 2, 3, 4, 5, 6]
        if previousPatient == 1:
            clearLink()

        # M 2401
        driver.find_element_by_id('M2401_b1').send_keys(Keys.SPACE)  # falls

        if depression_dx:
            driver.find_element_by_id('M2401_c1').send_keys(Keys.SPACE)  # depression
        else:
            driver.find_element_by_id('M2401_cNA').send_keys(Keys.SPACE)

        driver.find_element_by_id('M2401_d1').send_keys(Keys.SPACE)  # pain
        driver.find_element_by_id('M2401_eNA').send_keys(Keys.SPACE)   # prevent pressure ulcers
        driver.find_element_by_id('M2401_fNA').send_keys(Keys.SPACE)   # treat pressure ulcers

        '''
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
        '''
    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page


    ##### 22 Supplies Worksheet
    page = "Supplies Worksheet"

    scroll_up_then_pause()  # pause to finish and inspect page


    ##### 23 Supplies Used This Visit
    page =  "Supplies Used This Visit"

    scroll_up_then_pause()  # pause to finish and inspect page


    ##### 24 PT Evaluation
    page =  "PT Evaluation"
    '''
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
    '''
    # input("Autofill AFTER loading desired template")

    try:
        # Medical Dx and date
        '''
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
        '''
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

        '''
        # Social Support/Safety Hazards
        driver.find_element_by_id("frm_SafetySanHaz13").send_keys(livingSituation)
        '''

        '''
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
        '''

        # Functional Assessment
        '''
        driver.find_element_by_id('frm_FAPTBedMobComments').send_keys(func_impair_factors)
        driver.find_element_by_id('frm_FAPT35').send_keys(func_impair_factors)
        driver.find_element_by_id('frm_FAPT22').send_keys(func_impair_factors)
        # weightbearing status
        driver.find_element_by_id('frm_FAPT40').send_keys(wbStatus)
        '''
        # bed mobility
        driver.find_element_by_id("frm_BMRollingL").send_keys(Keys.SPACE)
        driver.find_element_by_id("frm_BMRollingR").send_keys(Keys.SPACE)
        driver.find_element_by_id('frm_BMRollingALDC').send_keys("Indep")

        # transfer
        driver.find_element_by_id("frm_TransSitStandALDC").send_keys(func_mobility)
        driver.find_element_by_id("frm_TransStandSitALDC").send_keys(func_mobility)
        driver.find_element_by_id("frm_TransBedWCALDC").send_keys("NT")
        driver.find_element_by_id("frm_TransWCBedALDC").send_keys("NT")
        driver.find_element_by_id("frm_TransToiletBSCALDC").send_keys(func_mobility)
        driver.find_element_by_id("frm_TransTubShowerALDC").send_keys(func_mobility)
        driver.find_element_by_id("frm_TransCarVanALDC").send_keys("NT")

        # gait
        driver.find_element_by_id("frm_GaitLevelALDC").send_keys(func_mobility)  # level
        driver.find_element_by_id("frm_GaitLevelAmtDC").send_keys(level_dist)
        driver.find_element_by_id("frm_GaitUnLevelALDC").send_keys('Ind with Equip')  # unlevel
        driver.find_element_by_id("frm_GaitUnLevelAmtDC").send_keys(unlevel_dist)
        driver.find_element_by_id("frm_GaitStepsStairsALDC").send_keys('Ind with Equip')  # steps
        driver.find_element_by_id("frm_GaitStepsStairsAmtDC").send_keys(num_stairs)

        # wheelchair
        driver.find_element_by_id("frm_OtherWCLevelALDC").send_keys("NT")

        # balance
        driver.find_element_by_id("frm_BalanceSitALDC").send_keys(func_mobility)
        driver.find_element_by_id("frm_BalanceStandALDC").send_keys(func_mobility)

        # "Evaluation and Testing Description" blank - subjective
        driver.find_element_by_id("frm_BalanceEvalTestDC").send_keys(subjective)

        # Treatment this visit
        driver.find_element_by_id('frm_trtmntSIV').send_keys(treatment)

        # Functional assessment Continue
        teaching_list = [
        'frm_tHEP',
        'frm_tHEPpt1',
        'frm_tHEPpt2',
        'frm_tSF',
        'frm_tSFpt1',
        'frm_tSFpt2',
        'frm_tSG',
        'frm_tSGpt1',
        'frm_tSGpt2']
        for box in teaching_list:
            driver.find_element_by_id(box).send_keys(Keys.SPACE)

        driver.find_element_by_id("frm_tTitlesTxt").send_keys("Agency handout")

        # Treatment Goals and Plan
        driver.find_element_by_id("frm_GoalsAllMetDC").send_keys(Keys.SPACE)
        driver.find_element_by_id("frm_GoalsSummaryDC").send_keys(goals_summary)

        # add coordination people
        # driver.find_element_by_id('frm_CareCoordName').send_keys(f", Marcy Sanchez, {CM}, {pta}")

        '''
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
        '''
    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page

    ##### 25 Discharge Summary
    page =  "Discharge Summary"
    try:
        date_boxes = [
            'frm_DateCompleted',
            'frm_DischargeDate'
            ]
        for date_box in date_boxes:
            driver.find_element_by_id(date_box).click()  # assessment date
            driver.find_element_by_id(date_box).send_keys(Keys.BACK_SPACE * 8)
            driver.find_element_by_id(date_box).send_keys(evalDate)

        # reason for dc
        driver.find_element_by_id("frm_GoalsMet").send_keys(Keys.SPACE)
        if dc_per_patient:
            driver.find_element_by_id("frm_PerPatFamReq").send_keys(Keys.SPACE)

        # condition at discharge
        driver.find_element_by_id('frm_CurrentStatus').click()
        driver.find_element_by_id('frm_CurrentStatus').send_keys('i')

        driver.find_element_by_id("frm_PhyPsych").send_keys(goals_summary)
        driver.find_element_by_id("frm_services_pt").send_keys(Keys.SPACE)

        driver.find_element_by_id("frm_CareSummary").send_keys(care_summary)

        # Goals Summary
        outcomes = [
        'frm_GoalsMet_GoalsSummary',
        'frm_ImprovedInd',
        'frm_ImprovedCond',
        'frm_ImprovedFunc',
        'frm_ImprovedKnow']
        for outcome in outcomes:
            driver.find_element_by_id(outcome).send_keys(Keys.SPACE)

        # dc info
        dc_info_boxes = [
        'frm_DischargeInsY',
        'frm_DischargeInsPatient',
        'frm_MedFollowupY',
        'frm_MedFollowupPatient',
        'frm_MedFollowupVerbalY',
        'frm_MedFollowupVerbalPatient',
        'frm_MedicationRevY',
        'frm_MedicationRevPatient',
        'frm_ComprehendInstructionsY',
        'frm_ComprehendInstructionsPatient',
        'frm_CallAgencyN',
        'frm_InformedPriorY',
        'frm_InformedPriorPatient',
        'frm_ToPatient',
        'frm_LiveArrangeDCHome',
        'frm_CareCoordDCHomeHealth']  # care coordination
        for box in dc_info_boxes:
            driver.find_element_by_id(box).send_keys(Keys.SPACE)

        driver.find_element_by_id("frm_InfoProvided").send_keys("Continue exercises and safety precautions.")

    except:
        PAE()

    scroll_up_then_pause()  # pause to finish and inspect page

    ##### 26 Aide Supervision
    page =  "Aide Supervision "
    try:
        driver.find_element_by_id("frm_sDate").click()  # assessment date
        driver.find_element_by_id("frm_sDate").send_keys(Keys.BACK_SPACE * 8)
        driver.find_element_by_id("frm_sDate").send_keys(evalDate)

        driver.find_element_by_id("frm_start_time").send_keys(visitStartTime)  # timeIn
        driver.find_element_by_id("frm_end_time").send_keys(visitEndTime)  # timeOut

        driver.find_element_by_id("frm_cPresentNo").send_keys(Keys.SPACE)

        qualities = [
        'frm_ddlNotify',
        'frm_ddlDuty',
        'frm_ddlCooperative',
        'frm_ddlCourteous',
        'frm_ddlMantainsComm',
        'frm_ddlFollowInstructions',
        'frm_ddlDemonstratesComp',
        'frm_ddlDocument',
        'frm_ddlNeeds',
        'frm_ddlAdherence',
        'frm_ddlComplies',
        'frm_ddlHonors']
        for quality in qualities:
            driver.find_element_by_id(quality).click()
            driver.find_element_by_id(quality).send_keys('e')

        driver.find_element_by_id('frm_chgs').send_keys("Continue plan of care.")

    except:
        PAE()
        input('<Enter> to acknowledge')

    # scroll_up_then_pause()

    ##### 27 NB Aide Supervision
    page =  "NB Aide Supervision (separate note)"
    input('<Enter> when NB note open')
    try:
        driver.find_element_by_id("frm_sDate").click()  # assessment date
        driver.find_element_by_id("frm_sDate").send_keys(Keys.BACK_SPACE * 8)
        driver.find_element_by_id("frm_sDate").send_keys(evalDate)

        driver.find_element_by_id("frm_start_time").send_keys(visitStartTime)  # timeIn
        driver.find_element_by_id("frm_end_time").send_keys(visitEndTime)  # timeOut

        driver.find_element_by_id("frm_cPresentNo").send_keys(Keys.SPACE)

        qualities = [
        'frm_ddlNotify',
        'frm_ddlDuty',
        'frm_ddlCooperative',
        'frm_ddlCourteous',
        'frm_ddlMantainsComm',
        'frm_ddlFollowInstructions',
        'frm_ddlDemonstratesComp',
        'frm_ddlDocument',
        'frm_ddlNeeds',
        'frm_ddlAdherence',
        'frm_ddlComplies',
        'frm_ddlHonors']
        for quality in qualities:
            driver.find_element_by_id(quality).click()
            driver.find_element_by_id(quality).send_keys('e')

        driver.find_element_by_id('frm_chgs').send_keys("Continue plan of care.")

    except:
        PAE()
        input('<Enter> to acknowledge')

    print('Good-bye and good luck.\n')
    print("PTA: " + pta + " CM: " + CM + '\n')
    print(forcuraBlurb + '\n')
    # print("Wound care on orders: " + woundCare + woundCareCustom + '\n')

