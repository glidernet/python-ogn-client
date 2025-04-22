# CHANGELOG

## 1.3.1: - 2025-04-22
- parser: parse short path (#128)
- client: configurable socket timeout (#112)
- client: more helpful socket error message (#116)

## 1.3.0: - 2025-04-19
- parser: Handle messages that do not conform to the "ogn-aprs-protocol" specification/implementation (fixes #126)
- Moved dependency management to to poetry
- Added github action pipeline for automated testing and publishing

## 1.2.3: - 2025-04-01 (not released on PyPI)
- parser: Added support for OGNMTK (Microtrak) beacons

## 1.2.2: - 2025-03-31 (not released on PyPI)
- client: If no reference_timestamp provided use timestamp from APRS server (fixes #85)
- parser: Handle dst_calls 'OGFLR6' (protocol 6) and 'OGFLR7' (protocol 7) like 'OGFLR' (fixes #123)

## 1.2.1: - 2021-06-06
- client: Added peer IP to log messages
- parser: Added rainfall_1h and rainfall_24h to beacon_type 'position_weather'

## 1.2.0: - 2021-06-01
- parser: Added support for OGNSKY (safesky) beacons
- client: Replace bad characters with � instead of raising an exception (restore old behaviour with parameter ignore_decoding_error=False)

## 1.1.0: - 2021-04-05
- parser: Added no-tracking flag decoding
- parser: Fixed aircraft_type decoding
## 1.0.1: - 2020-11-02
- client: catch errors while connecting (fixes #74 and #91)
- client: no logging messages by default (fixes #92)

## 1.0.0: - 2020-10-15
- client: changed socket mode from blocking to 5s timeout (fixes #89)
- parser: Added optional distance/bearing/normalized_quality calculation if parameter "calculate_relatives" is True (fixes #86)
- parser: Added support for weather data (new in receiver software v0.2.8) from FANET ground stations (aprs_type: position_weather)
- parser: Added support for latency (new in receiver software v0.2.8) in receiver messages (OGNSDR) (fixes #87)
- parser: Added support for reference_timestamp with tzinfo (fixes #84)
- parser: Fixed textual altitude part (fixes #81)
- parser: Skip keys where value is "None"

## 0.9.8: - 2020-08-21
- parser: Changed InReach parser (fixes #73)
- parser: separated incompatible ID into parser dependant ID (lt24: address -> lt24_id, skylines: address -> skylines_id,
          spider: id_spider -> spider_registration, address -> spider_id, spot: address -> spot_id) (fixes #64)
- client: Added keyword arguments for the callback function in the 'run' method of the client

## 0.9.7: - 2020-05-21
- parser: Added support for OGPAW (PilotAware) beacons
- client: Dropped compatibility for Python 3.4

## 0.9.6: - 2020-01-17
- parser: Better support for OGFLR beacons from PilotAware
- client: Allow dynamic settings override with optional "settings" parameter

## 0.9.5: - 2019-09-07
- parser: fixed telnet parser

## 0.9.4: - 2019-06-10
- parser: Added support for OGINREACH (Garmin inReach) beacons
- parser: Added support for OGFLYM (Flymaster) beacons
- parser: Added support for comments in tracker beacons (OGNTRK)
- parser: Added support for OGCAPT (Capturs) beacons

## 0.9.3: - 2019-06-03
- parser: Added Generic parser for unknown formats

## 0.9.2: - 2019-05-07
- parser: Exception handling for bad OGNTRK beacons

## 0.9.1: - 2018-09-18
- parser: Fixed SPOT beacons and Tracker beacons
- parser: Fixed kph to ms conversion
- client: Catch ConnectionResetError

## 0.9.0: - 2018-05-14
- parser: Added support for OGNLT24 (LT24), OGSKYL (Skylines), OGSPID (Spider), OGSPOT (Spot) and OGNFNT (Fanet)
- parser: Added support for (server) comments
- parser: Added parser for local receiver output (port 50001)
- parser: Changed unit for rotation from "half turn per minute" to "degrees/s"

## 0.8.2: - 2018-01-20
- parser: Better validation of timestamp, lat/lon and altitude

## 0.8.1: - 2018-01-12
- client: Ignore messages other than UTF-8
- parser: Allow IDs only with hexadecimal values

## 0.8.0 - 2017-10-02
- parser: Merged function 'parse_aprs' and 'parse_ogn_beacon' to 'parse'
- parser: Added support for OGNSDR (receiver), OGNTRK (ogn tracker), OGNFLR (flarm) and OGNAV (Naviter) beacons
- parser: Added support for RELAYed messages
- parser: Added support for ddhhmm time format (eg. '312359z')
- parser: Added support for heared aircrafts
- client: Allow client to do sequential connect-disconnect

## 0.7.1 - 2017-06-05
- parser: Bugfix, error_count in aircraft beacon is a int

## 0.7.0 - 2017-06-04
- parser: Added support for OGN v0.2.6 aircraft and receiver beacons

## 0.6.0 - 2016-10-21
- parser: Added support for OGN v0.2.5 receiver beacons
- parser: Changed keys to adopt naming from [ogn\_client-ruby](https://github.com/svoop/ogn_client-ruby)

## 0.5.0 - 2016-09-29
- Added aprs destination callsign as `dstcall` to aprs beacon keys (#9)
- Changed aprs parser to allow other destination calls than `APRS`
- Fixed parsing of APRS precision and datum option (#7)
- Added optional `reference_time` argument to `parse_aprs` function and disabled
  magic date correction if this argument is missing

## 0.4.0 - 2016-03-29
- aprs client: Added the possibility of a timed callback
- Added ogn.ddb submodule which provides the generator `get_ddb_devices`

## 0.3.0 - 2016-03-18
The repository ogn-python splitted up into two separate repositories:
  - python-ogn-client (the repository this Changelog belongs to),
    including an APRS- & OGN-Parser and an APRS-Client.
  - python-ogn-gateway, including a database, CLI, logbook.

- Moved exceptions from `ogn.exceptions` to `ogn.parser.exceptions`
- Moved parsing from `ogn.model.*` to `ogn.parser`
- Renamed module `ogn.gateway` to `ogn.client`
- Renamed class `ognGateway` to `AprsClient`
- Simplified usage of the module: Imported parse functions at package level (`ogn.parser`)
- Refined timstamp reconstruction to accept delayed packets (fixed glidernet/ogn-python#31)

# Historic ogn-python releases
## 0.2.1 - 2016-02-17
First release via PyPi.
- Added CHANGELOG.

## 0.2
- Changed database schema.
- Changed aprs app name to 'ogn-gateway-python'.
- Moved repository to github-organisation glidernet.
- Added exception handling to the packet parser.
- Added some tests for ogn.gateway.client.
- Added setup.py to build this package.
- Added configuration via python modules.
- Added scheduled tasks with celery.
- Renamed command line option `db.updateddb` to `db.import_ddb`.
- Added command line options `db.drop`, `db.import_file`, `db.upgrade`,
  `logbook.compute` and `show.devices.stats`.

## 0.1
Initial version.
