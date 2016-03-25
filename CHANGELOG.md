# CHANGELOG

## Unreleased
- aprs client: Added the possibility of a timed callback

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
