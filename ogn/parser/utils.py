from datetime import datetime, timedelta

from ogn.parser.exceptions import AmbigousTimeError


kmh2kts = 0.539957
feet2m = 0.3048
ms2fpm = 196.85

kts2kmh = 1 / kmh2kts
m2feet = 1 / feet2m
fpm2ms = 1 / ms2fpm


def parseAngle(dddmmhht):
    return float(dddmmhht[:3]) + float(dddmmhht[3:]) / 60


def createTimestamp(timestamp, reference_date, reference_time=None):
    if timestamp[-1] == "z":
        day = int(timestamp[0:2])
        hhmm = timestamp[2:6]
        if reference_date.day < day:
            if reference_date.month == 1:
                reference_date = reference_date.replace(year=reference_date.year - 1, month=12, day=day)
            else:
                reference_date = reference_date.replace(month=reference_date.month - 1, day=day)
        else:
            reference_date = reference_date.replace(day=day)
        packet_time = datetime.strptime(hhmm, '%H%M').time()
        return datetime.combine(reference_date, packet_time)
    elif timestamp[-1] == "h":
        hhmmss = timestamp[:-1]
        packet_time = datetime.strptime(hhmmss, '%H%M%S').time()
    else:
        raise ValueError()

    if reference_time is None:
        return datetime.combine(reference_date, packet_time)
    else:
        reference_datetime = datetime.combine(reference_date, reference_time)
        timestamp = datetime.combine(reference_date, packet_time)
        delta = timestamp - reference_datetime

        # This function reconstructs the packet date from the timestamp and a reference_datetime time.
        # delta vs. packet date:
        # -24h                      -12h                   0                       +12h                   +24h
        #  |-------------------------|---------------------|------------------------|----------------------|
        #  [-] <-- tomorrow          [---------today---------]                      [-------yesterday------]

        if timedelta(hours=-12) <= delta <= timedelta(minutes=30):
            # Packet less than 12h from the past or 30min from the future
            return timestamp
        elif delta < timedelta(hours=-23, minutes=-30):
            # Packet from next day, less than 30min from the future
            return datetime.combine(reference_datetime + timedelta(hours=+12), packet_time)
        elif timedelta(hours=12) < delta:
            # Packet from previous day, less than 12h from the past
            return datetime.combine(reference_datetime + timedelta(hours=-12), packet_time)
        else:
            raise AmbigousTimeError(reference_datetime, packet_time)
