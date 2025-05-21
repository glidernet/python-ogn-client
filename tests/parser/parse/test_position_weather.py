from ogn.parser import parse
from ogn.parser.utils import KNOTS_TO_MS, KPH_TO_MS, INCH_TO_MM, fahrenheit_to_celsius


def test_v028_fanet_position_weather():
    # with v0.2.8 fanet devices can report weather data
    raw_message = 'FNTFC9002>OGNFNT,qAS,LSXI2:/163051h4640.33N/00752.21E_187/004g007t075h78b63620 29.0dB -8.0kHz'
    message = parse(raw_message)

    assert message['aprs_type'] == 'position_weather'
    assert message['beacon_type'] == 'fanet'

    assert message['wind_direction'] == 187
    assert message['wind_speed'] == 4 * KNOTS_TO_MS / KPH_TO_MS
    assert message['wind_speed_peak'] == 7 * KNOTS_TO_MS / KPH_TO_MS
    assert message['temperature'] == fahrenheit_to_celsius(75)
    assert message['humidity'] == 78 * 0.01
    assert message['barometric_pressure'] == 63620

    assert message['signal_quality'] == 29.0
    assert message['frequency_offset'] == -8.0


def test_GXAirCom_fanet_position_weather_rainfall():
    raw_message = 'FNT08F298>OGNFNT,qAS,DREIFBERG:/082654h4804.90N/00845.74E_273/005g008t057r123p234h90b10264 0.0dB'
    message = parse(raw_message)

    assert message['aprs_type'] == 'position_weather'
    assert message['beacon_type'] == 'fanet'

    assert message['rainfall_1h'] == 123 / 100 * INCH_TO_MM
    assert message['rainfall_24h'] == 234 / 100 * INCH_TO_MM
