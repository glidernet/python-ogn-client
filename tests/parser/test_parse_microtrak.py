from ogn.parser.aprs_comment.microtrak_parser import MicrotrakParser


def test_position_comment():
    message = MicrotrakParser().parse_position("id21A8CBA8")

    assert message['address_type'] == 1
    assert message['aircraft_type'] == 8
    assert message['stealth'] is False
    assert message['no-tracking'] is False
    assert message['address'] == "A8CBA8"


def test_position_comment_relevant_keys_only():
    # return only keys where we got informations
    message = MicrotrakParser().parse_position("id21A8CBA8")

    assert message is not None
    assert sorted(message.keys()) == sorted(['address_type', 'aircraft_type', 'stealth', 'address', 'no-tracking'])
