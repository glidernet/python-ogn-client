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
