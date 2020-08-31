from datetime import datetime, timedelta

FEETS_TO_METER = 0.3048             # ratio feets to meter
FPM_TO_MS = FEETS_TO_METER / 60     # ratio fpm to m/s
KNOTS_TO_MS = 0.5144                # ratio knots to m/s
KPH_TO_MS = 0.27778                 # ratio kph to m/s
HPM_TO_DEGS = 180 / 60              # ratio between half turn per minute and degrees/s


def parseAngle(dddmmhht):
    return float(dddmmhht[:3]) + float(dddmmhht[3:]) / 60


def createTimestamp(time_string, reference_timestamp=None):
    if time_string[-1] == "z":
        dd = int(time_string[0:2])
        hh = int(time_string[2:4])
        mm = int(time_string[4:6])

        result = datetime(reference_timestamp.year,
                          reference_timestamp.month,
                          dd,
                          hh, mm, 0)

        if result > reference_timestamp + timedelta(days=14):
            # shift timestamp to previous month
            result = (result.replace(day=1) - timedelta(days=5)).replace(day=result.day)
        elif result < reference_timestamp - timedelta(days=14):
            # shift timestamp to next month
            result = (result.replace(day=28) + timedelta(days=5)).replace(day=result.day)
    else:
        hh = int(time_string[0:2])
        mm = int(time_string[2:4])
        ss = int(time_string[4:6])

        result = datetime(reference_timestamp.year,
                          reference_timestamp.month,
                          reference_timestamp.day,
                          hh, mm, ss)

        if result > reference_timestamp + timedelta(hours=12):
            # shift timestamp to previous day
            result -= timedelta(days=1)
        elif result < reference_timestamp - timedelta(hours=12):
            # shift timestamp to next day
            result += timedelta(days=1)

    return result

aprssymtypes=[ 
	"/z", 			# 0 = ?
	"/'", 			# 1 = (moto-)glider (most frequent)
	"/'", 			# 2 = tow plane (often)
	"/X", 			# 3 = helicopter (often)
	"/g", 			# 4 = parachute (rare but seen - often mixed with drop plane)
	"\\^", 			# 5 = drop plane (seen)
	"/g", 			# 6 = hang-glider (rare but seen)
	"/g", 			# 7 = para-glider (rare but seen)
	"\\^",	 		# 8 = powered aircraft (often)
	"/^", 			# 9 = jet aircraft (rare but seen)
	"/z", 			# A = UFO (people set for fun)
	"/O", 			# B = balloon (seen once)
	"/O", 			# C = airship (seen once)
	"/'", 			# D = UAV (drones, can become very common)
	"/z", 			# E = ground support (ground vehicles at airfields)
	"\\n" 			# F = static object (ground relay ?)
        ]
aprstypes=[
	"Unkown", 		# 0 = ?
	"Glider", 		# 1 = (moto-)glider (most frequent)
	"Plane", 		# 2 = tow plane (often)
	"Helicopter", 		# 3 = helicopter (often)
	"Parachute", 		# 4 = parachute (rare but seen - often mixed with drop plane)
	"DropPlane", 		# 5 = drop plane (seen)
	"HangGlider", 		# 6 = hang-glider (rare but seen)
	"ParaGlider", 		# 7 = para-glider (rare but seen)
	"PowerAircraft",	# 8 = powered aircraft (often)
	"Jet",	 		# 9 = jet aircraft (rare but seen)
	"UFO", 			# A = UFO (people set for fun)
	"Balloon", 		# B = balloon (seen once)
	"Airship", 		# C = airship (seen once)
	"Drone", 		# D = UAV (drones, can become very common)
	"GroundVehicle",	# E = ground support (ground vehicles at airfields)
	"GroundStation"		# F = static object (ground relay ?)
        ]
def get_aircraft_type(sym1, sym2):	# return the aircraft type based on the symbol table

    sym=sym1+sym2
    idx=0
    while idx < 16:
          if sym == aprssymtypes[idx]:
             return (aprstypes[idx])
          idx += 1
    return ("UNKOWN")

