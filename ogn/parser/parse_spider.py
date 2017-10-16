def parse(aprs_comment):
    ac_match = re.search(PATTERN_AIRCRAFT_BEACON, aprs_comment)
    if ac_match:
        return {'address': ac_match.group('deviceID'),
                'climb_rate': int(ac_match.group('climb_rate')) * fpm2ms if ac_match.group('climb_rate') else None,
                'signal_quality': float(ac_match.group('signal_quality')) if ac_match.group('signal_quality') else None}
    else:
	return None
