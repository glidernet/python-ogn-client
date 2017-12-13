# CHANGELOG

## Unreleased
- client: Ignore messages other than UTF-8

## 0.8.0 - 2017-10-02
- parser: Merged function 'parse_aprs' and 'parse_ogn_beacon' to 'parse'
- parser: Added support for OGNSDR (receiver), OGNTRK (ogn tracker), OGNFLR (flarm) and OGNAV (Naviter) beacons
- parser: Added support for RELAYed messages
- parser: Added support for ddmmss time format (eg. '312359z')
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
