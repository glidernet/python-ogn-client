from ogn.parser.parse import parse
from datetime import datetime
import pytest

from tests.rust_migration import get_valid_beacons

valid_beacons = get_valid_beacons()


def test_parser_differences_keywise():
    differences = []
    error_combinations = {}
    for line in valid_beacons:
        py_parse_result = parse(line, reference_timestamp=datetime(2015, 4, 10, 17, 0), use_server_timestamp=False)
        rust_parse_result = parse(line, reference_timestamp=datetime(2015, 4, 10, 17, 0), use_server_timestamp=False, use_rust_parser=True)
        py_parse_result, rust_parse_result = sort_dicts(py_parse_result, rust_parse_result)

        # Skip deprecated APRS messages
        if py_parse_result['aprs_type'] in ('status', 'position') and py_parse_result['dstcall'] == 'APRS':
            continue

        missing_keys = [k for k in py_parse_result.keys() - rust_parse_result.keys() if py_parse_result[k] not in ('', None) and k not in ('comment')]
        extra_keys = rust_parse_result.keys() - py_parse_result.keys()
        if (missing_keys or extra_keys) and str((py_parse_result['dstcall'], missing_keys, extra_keys)) not in error_combinations:
            error_combinations[str((py_parse_result['dstcall'], missing_keys, extra_keys))] = True
            missing_entries = ('\n' + '\n'.join([f"  - {k}: {py_parse_result[k]}" for k in missing_keys])) if missing_keys else ' []'
            extra_entries = ('\n' + '\n'.join([f"  - {k}: {rust_parse_result[k]}" for k in extra_keys])) if extra_keys else ' []'
            delta = f"```\n{line}\ndropped:{missing_entries}\nadded:{extra_entries}\n```"
            differences.append(delta)

    if differences:
        pytest.fail('\n\n'.join(differences))


def test_parser_differences_valuewise():
    differences = []
    for line in valid_beacons:
        py_parse_result = parse(line, reference_timestamp=datetime(2015, 4, 10, 17, 0), use_server_timestamp=False)
        rust_parse_result = parse(line, reference_timestamp=datetime(2015, 4, 10, 17, 0), use_server_timestamp=False, use_rust_parser=True)
        py_parse_result, rust_parse_result = sort_dicts(py_parse_result, rust_parse_result)

        # Skip deprecated APRS messages
        if py_parse_result['aprs_type'] in ('status', 'position') and py_parse_result['dstcall'] == 'APRS':
            continue

        for key in py_parse_result.keys() & rust_parse_result.keys():
            # Skip keys that differ too much (comment: intended; gps_quality and timestamp: FIXME)
            if key in ('comment', 'gps_quality'):
                continue

            py_value, rust_value = py_parse_result[key], rust_parse_result[key]

            # Skip keys that are not equal but are close enough (float values)
            if isinstance(py_value, float) and isinstance(rust_value, float) and abs(py_value - rust_value) < 1e-4:
                continue

            if py_value != rust_value:
                entry = f"{line}\nPython: {key}={py_value}\nRust:   {key}={rust_value}"
                differences.append(entry)

    if differences:
        pytest.fail('\n\n'.join(differences))


def test_failing():
    failing_lines = [
        r"""MYC78FF44>OGNMYC:>140735h Pilot=RichardHunt""",
    ]

    for line in failing_lines:
        py_parse_result = parse(line, reference_timestamp=datetime(2015, 4, 10, 17, 0), use_server_timestamp=False)
        rust_parse_result = parse(line, reference_timestamp=datetime(2015, 4, 10, 17, 0), use_server_timestamp=False, use_rust_parser=True)
        py_parse_result, rust_parse_result = sort_dicts(py_parse_result, rust_parse_result)

        assert py_parse_result == rust_parse_result, f"Results do not match for line: {line}\nPy: {py_parse_result}\nRu: {rust_parse_result}"


def sort_dicts(dict1, dict2):
    # sort dictionaries for comparison
    dict1 = {k: dict1[k] for k in sorted(dict1.keys())}
    dict2 = {k: dict2[k] for k in sorted(dict2.keys())}
    return dict1, dict2
