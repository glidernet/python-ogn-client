import unittest.mock as mock
import pytest
import os

from datetime import datetime
from time import sleep

from ogn.parser.parse import parse
from ogn.parser.exceptions import AprsParseError, OgnParseError


def _parse_valid_beacon_data_file(filename, beacon_type):
    with open(os.path.dirname(__file__) + '/../../ogn-aprs-protocol/valid_messages/' + filename) as f:
        for line in f:
            if line.strip() == '':
                continue

            try:
                message = parse(line, datetime(2015, 4, 10, 17, 0))
                assert message is not None
                if message['aprs_type'] == 'position' or message['aprs_type'] == 'status':
                    assert message['beacon_type'] == beacon_type
            except NotImplementedError as e:
                print(e)


def test_aprs_aircraft_beacons():
    _parse_valid_beacon_data_file(filename='APRS_aircraft.txt', beacon_type='aprs_aircraft')


def test_aprs_receiver_beacons():
    _parse_valid_beacon_data_file(filename='APRS_receiver.txt', beacon_type='aprs_receiver')


def test_flyxc_beacons():
    _parse_valid_beacon_data_file(filename='FXCAPP_flyxc.txt', beacon_type='unknown')


def test_adsb_beacons():
    _parse_valid_beacon_data_file(filename='OGADSB_ADSB.txt', beacon_type='unknown')


def test_adsl_beacons():
    _parse_valid_beacon_data_file(filename='OGADSL_Tracker_with_ADSL.txt', beacon_type='unknown')


def test_airmate_beacons():
    _parse_valid_beacon_data_file(filename='OGAIRM_Airmate.txt', beacon_type='unknown')


def test_apik_beacons():
    _parse_valid_beacon_data_file(filename='OGAPIK_APIKdevice.txt', beacon_type='unknown')


@pytest.mark.skip(reason="todo")
def test_capturs_beacons():
    _parse_valid_beacon_data_file(filename='OGCAPT_Capturs.txt', beacon_type='capturs')


def test_evario_beacons():
    _parse_valid_beacon_data_file(filename='OGEVARIO_evario.txt', beacon_type='unknown')


def test_flarm_beacons():
    _parse_valid_beacon_data_file(filename='OGFLR_Flarm.txt', beacon_type='flarm')


def test_flymaster_beacons():
    _parse_valid_beacon_data_file(filename='OGFLYM_Flymaster.txt', beacon_type='flymaster')


@pytest.mark.skip(reason="todo")
def test_inreach_beacons():
    _parse_valid_beacon_data_file(filename='OGNINRE_InReach.txt', beacon_type='inreach')


def test_lt24_beacons():
    _parse_valid_beacon_data_file(filename='OGLT24_LiveTrack24.txt', beacon_type='lt24')


def test_naviter_beacons():
    _parse_valid_beacon_data_file(filename='OGNAVI_Naviter.txt', beacon_type='naviter')


@pytest.mark.skip(reason="todo")
def test_delay_beacons():
    _parse_valid_beacon_data_file(filename='OGNDELAY_Delay.txt', beacon_type='tracker')


def test_wx_beacons():
    _parse_valid_beacon_data_file(filename='OGNDVS_wx.txt', beacon_type='unknown')


def test_nemo_beacons():
    _parse_valid_beacon_data_file(filename='OGNEMO_Nemo.txt', beacon_type='unknown')


def test_flying_neurons_beacons():
    _parse_valid_beacon_data_file(filename='OGNFNO_FlyingNeurons.txt', beacon_type='unknown')


def test_fanet_weather_beacons():
    _parse_valid_beacon_data_file(filename='OGNFNT_Fanet_weather.txt', beacon_type='fanet')


def test_fanet_beacons():
    _parse_valid_beacon_data_file(filename='OGNFNT_Fanet.txt', beacon_type='fanet')


def test_microtrack_beacons():
    _parse_valid_beacon_data_file(filename='OGNMTK_Microtrack.txt', beacon_type='microtrak')


def test_myc_tracker_beacons():
    _parse_valid_beacon_data_file(filename='OGNMYC_OGNtracker.txt', beacon_type='unknown')


def test_receiver_beacons():
    _parse_valid_beacon_data_file(filename='OGNSDR_TCPIPmsgs.txt', beacon_type='receiver')


def test_safesky_beacons():
    _parse_valid_beacon_data_file(filename='OGNSKY_SafeSky.txt', beacon_type='safesky')


def test_ognbase_beacons():
    _parse_valid_beacon_data_file(filename='OGNSXR_OGNbase.txt', beacon_type='unknown')


def test_tracker_beacons():
    _parse_valid_beacon_data_file(filename='OGNTRK_OGNtracker.txt', beacon_type='tracker')


def test_thethingsnetwork_beacons():
    _parse_valid_beacon_data_file(filename='OGNTTN_TheThingsNetwork.txt', beacon_type='unknown')


def test_wingman_beacons():
    _parse_valid_beacon_data_file(filename='OGNWMN_Wingman.txt', beacon_type='unknown')


def test_pilot_aware_beacons():
    _parse_valid_beacon_data_file(filename='OGPAW_PilotAware.txt', beacon_type='pilot_aware')


def test_skylines_beacons():
    _parse_valid_beacon_data_file(filename='OGSKYL_Skylines.txt', beacon_type='skylines')


def test_spider_beacons():
    _parse_valid_beacon_data_file(filename='OGSPID_Spider.txt', beacon_type='spider')


def test_spot_beacons():
    _parse_valid_beacon_data_file(filename='OGSPOT_Spot.txt', beacon_type='spot')


def test_generic_beacons():
    message = parse("EPZR>WTFDSTCALL,TCPIP*,qAC,GLIDERN1:>093456h this is a comment")
    assert message['beacon_type'] == 'unknown'
    assert message['comment'] == "this is a comment"


def test_fail_parse_aprs_none():
    with pytest.raises(TypeError):
        parse(None)


def test_fail_empty():
    with pytest.raises(AprsParseError):
        parse("")


def test_fail_bad_string():
    with pytest.raises(AprsParseError):
        parse("Lachens>APRS,TCPIwontbeavalidstring")


def test_v026_chile():
    # receiver beacons from chile have a APRS position message with a pure user comment
    message = parse("VITACURA1>APRS,TCPIP*,qAC,GLIDERN4:/201146h3322.79SI07034.80W&/A=002329 Vitacura Municipal Aerodrome, Club de Planeadores Vitacura")
    assert message['user_comment'] == "Vitacura Municipal Aerodrome, Club de Planeadores Vitacura"

    message_with_id = parse("ALFALFAL>APRS,TCPIP*,qAC,GLIDERN4:/221830h3330.40SI07007.88W&/A=008659 Alfalfal Hidroelectric Plant, Club de Planeadores Vitacurs")
    assert message_with_id['user_comment'] == "Alfalfal Hidroelectric Plant, Club de Planeadores Vitacurs"


@mock.patch('ogn.parser.parse_module.createTimestamp')
def test_default_reference_date(createTimestamp_mock):
    valid_aprs_string = "Lachens>APRS,TCPIP*,qAC,GLIDERN2:/165334h4344.70NI00639.19E&/A=005435 v0.2.1 CPU:0.3 RAM:1764.4/2121.4MB NTP:2.8ms/+4.9ppm +47.0C RF:+0.70dB"

    parse(valid_aprs_string)
    call_args_before = createTimestamp_mock.call_args

    sleep(1)

    parse(valid_aprs_string)
    call_args_seconds_later = createTimestamp_mock.call_args

    assert call_args_before != call_args_seconds_later


def test_copy_constructor():
    valid_aprs_string = "FLRDDA5BA>APRS,qAS,LFMX:/160829h4415.41N/00600.03E'342/049/A=005524 id0ADDA5BA -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5"
    message = parse(valid_aprs_string)

    assert message['name'] == 'FLRDDA5BA'
    assert message['address'] == 'DDA5BA'


def test_bad_naviter_format():
    with pytest.raises(OgnParseError):
        parse("FLRA51D93>OGNAVI,qAS,NAVITER2:/204507h4444.98N/09323.34W'000/000/A=000925 !W67! id06A51D93 +000fpm +0.0rot")


def test_no_receiver():
    result = parse("EDFW>OGNSDR:/102713h4949.02NI00953.88E&/A=000984")

    assert result['aprs_type'] == 'position'
    assert result['beacon_type'] == 'receiver'
    assert result['name'] == 'EDFW'
    assert result['dstcall'] == 'OGNSDR'
    assert result['receiver_name'] is None
