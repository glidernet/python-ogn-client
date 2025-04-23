from ogn.parser.aprs_comment.generic_parser import GenericParser


def test_position_comment():
    message = GenericParser().parse_position("id0123456789 weather is good, climbing with 123fpm")
    assert 'comment' in message

    message = GenericParser().parse_status("id0123456789 weather is good, climbing with 123fpm")
    assert 'comment' in message
