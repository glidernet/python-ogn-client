# CHANGELOG
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
