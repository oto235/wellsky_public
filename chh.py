class Vitals:
    # default vital sign parameters
    temp_high = "100.5"
    temp_low = 96
    pulse_high = 100
    pulse_low = 60
    resp_high = 24
    resp_low = 12
    sbp_high = 170
    sbp_lLow = 100
    dbp_high = 100
    dbp_low = 60
    o2_low = 90
    # if dm == 1: these will be used:
    fast_bs_High = 200
    fast_bs_low = 60
    rand_bs_high = 200
    rand_bs_low = 60


class Physicians:
    def __init__(self):
        self.tempHigh = Vitals.temp_high
        self.physicianFullName = ""
        self.woundCare = ""
        self.TEDhose = "TED hose _____ x 2 weeks. May take off at night."
        self.freq = ""
        self.visit_count = "???"
        self.pa = ""

    def get_phys_details(self, physician: str, woundDesc: str, POD7DD: str, day: str):
        
        # preprocess 'day' to line up with dictionary keys
        if 'sun' in day.lower():
            day = 'sun'
        elif 'mon' in day.lower():
            day = 'mon'
        elif 'tue' in day.lower():
            day = 'tue'
        elif 'wed' in day.lower():
            day = 'wed'
        elif 'thu' in day.lower():
            day = 'thu'
        elif 'fri' in day.lower():
            day = 'fri'
        elif 'sat' in day.lower():
            day = 'sat'
        else: 
            print("Something not right with 'day'.")
        
        # example physician 
        if "bannister" in physician.lower():
            self.tempHigh = "101.5"
            self.physicianFullName = 'Sir Roger Bannister'
            self.TEDhose = "TED hose x 2 weeks. May take off at night."

            freq_Bannister = {"sun" : "4w1, 3w1, 2w1",
                             "mon" : "4w1, 3w1, 2w1",
                             "tue" : "4w1, 3w1, 2w1",
                             "wed" : "3w3",
                             "thu" : "2w1, 4w1, 3w1, 2w1",
                             "fri" : "1w1, 4w1, 3w1, 2w1",
                             "sat" : "1w1, 4w1, 3w1, 2w1"
                             }

            try:
                self.freq = freq_Bannister[day]
            except:
                self.freq = "1w1, UNK"
                print("You need to manually enter PT POC")
            
            if 'aquacel' in woundDesc.lower() or 'mepilex' in woundDesc.lower():
                self.woundCare = f"""Aquacel or Mepilex - leave in place for 7 days then remove and replace with \
second Aquacel or Mepilex.  Report any drainage to provider. Post op day 7 is {POD7DD}. ____"""
            elif 'prevena' in woundDesc.lower():
                self.woundCare = f"""Prevena wound vac - leave for 7 days and replace with Aquacel or Mepilex. Report \
any drainage to provider. Post op day 7 is {POD7DD}. ____"""
            elif 'pico' in woundDesc.lower():
                self.woundCare = f"""PICO wound vac - cut tubing/disconnect box at 7 days and cover stump with a \
tegaderm UNLESS saturated with drainage, water or sweat then change to Aquacel or Mepilex. Leave PICO dressing in \
place until surgeon follow up appt. Report any drainage to provider. Post op day 7 is {POD7DD}. ____"""
            else:
                self. woundCare = """Add custom wound care here ____ """

        

        else:
            self.woundCare = 'Monitor wound(s) for abnormalities. ____ '
            print('Following physician not loaded into program.')
            self.physicianFullName = physician
            self.freq = "1w1, UNK"

        try:
            freq_split = self.freq.split()
            count_int = 0
            for term in freq_split:
                count_int += int(term[0]) * int(term[2])
            self.visit_count = ("000" + str(count_int))[-3:]

        except:
            self.visit_count = "???"

        return self.tempHigh, self.physicianFullName, self.woundCare, self.TEDhose, self.freq, self.visit_count
