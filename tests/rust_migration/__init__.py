import os


def get_valid_beacons():
    # iterate over all txt files in the valid_messages directory
    valid_beacons = []
    for filename in os.listdir(os.path.dirname(__file__) + '/../../ogn-aprs-protocol/valid_messages/'):
        if filename in ('OGADSB_ADSB.txt', 'OGCAPT_Capturs.txt'):
            continue

        if filename.endswith('.txt'):
            with open(os.path.dirname(__file__) + '/../../ogn-aprs-protocol/valid_messages/' + filename) as f:
                for line in f:
                    if line.strip() == '':
                        continue

                    valid_beacons.append(line.strip())

    return valid_beacons
