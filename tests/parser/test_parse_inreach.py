from ogn.parser.aprs_comment.inreach_parser import InreachParser


def test_position_comment():
    message = InreachParser().parse_position("id300434060496190 inReac True")
    assert message['address'] == "300434060496190"
    assert message['model'] == 'inReac'
    assert message['status'] is True
    assert message['pilot_name'] is None

    message = InreachParser().parse_position("id300434060496190 inReac True Jim Bob")
    assert message['address'] == "300434060496190"
    assert message['model'] == 'inReac'
    assert message['status'] is True
    assert message['pilot_name'] == "Jim Bob"
