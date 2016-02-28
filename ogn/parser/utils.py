import math
from datetime import datetime, timedelta

from ogn.parser.exceptions import AmbigousTimeError


kmh2kts = 0.539957
feet2m = 0.3048
ms2fpm = 196.85

kts2kmh = 1 / kmh2kts
m2feet = 1 / feet2m
fpm2ms = 1 / ms2fpm


def dmsToDeg(dms):
    absDms = abs(dms)
    d = math.floor(absDms)
    m = (absDms - d) * 100 / 60
    return d + m


def createTimestamp(hhmmss, reference):
    packet_time = datetime.strptime(hhmmss, '%H%M%S').time()
    timestamp = datetime.combine(reference, packet_time)

    if reference.hour == 23 and timestamp.hour == 0:
        timestamp = timestamp + timedelta(days=1)
    elif reference.hour == 0 and timestamp.hour == 23:
        timestamp = timestamp - timedelta(days=1)

    if reference - timestamp > timedelta(hours=1):
        raise AmbigousTimeError(reference, packet_time)

    return timestamp
