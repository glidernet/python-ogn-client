from datetime import datetime, timedelta, timezone
import math

FEETS_TO_METER = 0.3048             # ratio feets to meter
FPM_TO_MS = FEETS_TO_METER / 60     # ratio fpm to m/s
KNOTS_TO_MS = 0.5144                # ratio knots to m/s
KPH_TO_MS = 0.27778                 # ratio kph to m/s
HPM_TO_DEGS = 180 / 60              # ratio between half turn per minute and degrees/s


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32.0) * 5.0 / 9.0


def parseAngle(dddmmhht):
    return float(dddmmhht[:3]) + float(dddmmhht[3:]) / 60


def createTimestamp(time_string, reference_timestamp):
    if time_string[-1] == "z":
        dd = int(time_string[0:2])
        hh = int(time_string[2:4])
        mm = int(time_string[4:6])

        result = datetime(reference_timestamp.year,
                          reference_timestamp.month,
                          dd,
                          hh, mm, 0,
                          tzinfo=timezone.utc if reference_timestamp.tzinfo is not None else None)

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
                          hh, mm, ss,
                          tzinfo=timezone.utc if reference_timestamp.tzinfo is not None else None)

        if result > reference_timestamp + timedelta(hours=12):
            # shift timestamp to previous day
            result -= timedelta(days=1)
        elif result < reference_timestamp - timedelta(hours=12):
            # shift timestamp to next day
            result += timedelta(days=1)

    return result


MATH_PI = 3.14159265359


class CheapRuler():
    """Extreme fast distance calculating for distances below 500km."""

    def __init__(self, lat):
        c = math.cos(lat * MATH_PI / 180)
        c2 = 2 * c * c - 1
        c3 = 2 * c * c2 - c
        c4 = 2 * c * c3 - c2
        c5 = 2 * c * c4 - c3

        self.kx = 1000 * (111.41513 * c - 0.09455 * c3 + 0.00012 * c5)  # longitude correction
        self.ky = 1000 * (111.13209 - 0.56605 * c2 + 0.0012 * c4)       # latitude correction

    def distance(self, a, b):
        """Distance between point a and b. A point is a tuple(lon,lat)."""

        dx = (a[0] - b[0]) * self.kx
        dy = (a[1] - b[1]) * self.ky
        return math.sqrt(dx * dx + dy * dy)

    def bearing(self, a, b):
        """Returns the bearing from point a to point b."""

        dx = (b[0] - a[0]) * self.kx
        dy = (b[1] - a[1]) * self.ky
        if dx == 0 and dy == 0:
            return 0
        result = math.atan2(-dy, dx) * 180 / MATH_PI + 90
        return result if result >= 0 else result + 360


def normalized_quality(distance, signal_quality):
    """Signal quality normalized to 10km."""

    return signal_quality + 20.0 * math.log10(distance / 10000.0) if distance > 0 else None
