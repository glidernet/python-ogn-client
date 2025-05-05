from ogn.parser.parse import parse
from datetime import datetime

from tests.rust_migration import get_valid_beacons

valid_beacons = get_valid_beacons()


def legacy_parser():
    reference_timestamp = datetime(2015, 4, 10, 17, 0)
    for line in valid_beacons:
        parse(line, reference_timestamp=reference_timestamp)


def rust_parser():
    reference_timestamp = datetime(2015, 4, 10, 17, 0)
    for line in valid_beacons:
        parse(line, reference_timestamp=reference_timestamp, use_rust_parser=True)


def test_legacy_parser(benchmark):
    benchmark(legacy_parser)


def test_rust_parser(benchmark):
    benchmark(rust_parser)
