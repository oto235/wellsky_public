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


#### example physicians listed below
class Physicians:
    def __init__(self):
        self.tempHigh = Vitals.temp_high
        self.physicianFullName = ""
        self.woundCare = ""
        self.TEDhose = "TED hose _____ x 2 weeks. May take off at night."

    def get_phys_details(self, physician: str, woundDesc: str, POD7DD: str):

        if physician.lower() == "bannister":
            self.tempHigh = "101"
            self.physicianFullName = 'Roger Bannister'
            self.TEDhose = "TED hose bilaterally daily: 24 hrs/day x 4 weeks on the operative side and for 2 weeks on \
the non-operative side."
            # freqSatBannister_1w1_4w1_3w1_2w1
            # freqSunBannister_4w1_3w1_2w1
            # phBannister_512_555_5555
            self.woundCare = """PA will remove sutures/staples, unless MD appointment is over two weeks post \
op, then PT/PTA may remove at 14 days post-op. If dermabond present, do not remove at the time of primary dressing removal. \
Allow dermabond to fall off naturally.
ABD to be removed at FIRST visit.
____ If hip, apply steri-strips, xeroform, gauze and tape. \
____ If knee, apply steri-strips.
____ When Silverlon is present, leave on until post-op day 12-14, unless it is 55% \
saturated, remove and apply xeroform, gauze, and tape. ____ """

        elif physician.lower() == "prefontaine":
            self.tempHigh = "101.5"
            self.physicianFullName = 'Steve Prefontaine'
            self.TEDhose = "TED hose x 2 weeks. May take off at night."
            # freqSatPre_1w1_4w1_3w1_2w1
            # freqSunPre_4w1_3w1_2w1
            # phPre_512_555_0000
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

        return self.tempHigh, self.physicianFullName, self.woundCare, self.TEDhose
