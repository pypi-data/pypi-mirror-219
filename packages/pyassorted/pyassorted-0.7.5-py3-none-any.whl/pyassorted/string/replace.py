import re
from enum import Enum
from typing import Dict, Text


class Bracket(Enum):
    NoBracket = 0
    Parenthesis = 1
    CurlyBrackets = 2
    SquareBrackets = 3


def multiple_replace(
    d: Dict[Text, Text], text: Text, wraped_by: Bracket = Bracket.NoBracket
) -> Text:
    """Replace 'd' keys with 'd' values in 'text' string.

    Parameters
    ----------
    d : Dict[Text, Text]
        Dictionary with keys to be replaced by values.
    text : Text
        Text to be replaced.
    wraped_by : Bracket, optional
        If specified, the keys will be wrapped by the specified bracket type.
        If not specified, the keys will be replaced without any wrapping.
        The default is Bracket.NoBracket.

    Returns
    -------
    Text
        Text with replaced keys.

    Raises
    ------
    ValueError
        If 'wraped_by' is not a valid Bracket type.

    Examples
    --------
    >>> d = {"var1": "Hello", "var2": "World"}
    >>> text = "var1 var2"
    >>> multiple_replace(d, text)
    'Hello World'
    """

    if wraped_by is Bracket.NoBracket:
        regex = re.compile("%s" % "|".join(map(re.escape, d.keys())))
    elif wraped_by is Bracket.Parenthesis:
        regex = re.compile("\(\s*(%s)\s*\)" % "|".join(map(re.escape, d.keys())))
    elif wraped_by is Bracket.SquareBrackets:
        regex = re.compile("\[\s*(%s)\s*\]" % "|".join(map(re.escape, d.keys())))
    elif wraped_by is Bracket.CurlyBrackets:
        regex = re.compile("{\s*(%s)\s*}" % "|".join(map(re.escape, d.keys())))
    else:
        raise ValueError(f"Invalid Bracket type: {wraped_by}")

    if wraped_by is Bracket.Parenthesis:
        return regex.sub(lambda mo: d[mo.group().strip("() \t\n\r")], text)
    if wraped_by is Bracket.SquareBrackets:
        return regex.sub(lambda mo: d[mo.group().strip("[] \t\n\r")], text)
    else:
        return regex.sub(lambda mo: d[mo.group().strip("{} \t\n\r")], text)
