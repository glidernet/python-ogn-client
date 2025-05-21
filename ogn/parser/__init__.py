from ogn.parser import parse as parse_module    # noqa: F40 --- only for test functions. Without this a mock of parse would mock the function instead of the module
from ogn.parser.parse import parse   # noqa: F401
from ogn.parser.exceptions import AprsParseError     # noqa: F401
