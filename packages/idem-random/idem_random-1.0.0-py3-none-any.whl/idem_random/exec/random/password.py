"""Exec module for generating random strings usable as passwords"""
import random
import string
from typing import Any
from typing import Dict


def generate_random_string(
    hub,
    length: int,
    *,
    upper: bool = True,
    lower: bool = True,
    numeric: bool = True,
    special: bool = True,
    min_numeric: int = 0,
    min_lower: int = 0,
    min_upper: int = 0,
    min_special: int = 0,
    override_special: str = None,
) -> Dict[str, Any]:
    """
    Generate a random string.

    Args:
        length(int) :
            The length of the required random password. Defaults to True.

        upper(bool, Optional):
            Include upper-case in generated password. Defaults to True.

        lower(bool, Optional):
            Include lower-case in generated password. Defaults to True.

        numeric(bool, Optional):
            Include numbers in generated password. Defaults to True.

        special(bool, Optional):
            Include special characters (!@#$%&*()-_=+[]{}<>:?) in generated password. Defaults to True.

        min_lower(int, Optional):
            Minimum number of lowercase alphabet characters in the result. Default value is 0.

        min_numeric(int, Optional):
            Minimum number of numeric characters in the result. Default value is 0.

        min_special(int, Optional):
            Minimum number of special characters in the result. Default value is 0.

        min_upper(int, Optional):
            Minimum number of uppercase alphabet characters in the result. Default value is 0.

        override_special(str, Optional):
            Supply your own sequence of special characters to use for string generation. This overrides
            the default special character list. The special argument must still be set to true for any
            overwritten characters to be used in generation.

    Returns:
        Dict[str, Any]

    Command line example:

    .. code-block:: bash

        idem exec random.password.generate_random_string length=10

    State example:

    .. code-block:: yaml

        service_password:
          exec.run:
            - path: random.password.generate_random_string
            - kwargs:
                length: 10
    """

    ret = dict(comment=(), ret="", result=True)

    num_chars = string.digits
    lower_chars = string.ascii_lowercase
    upper_chars = string.ascii_uppercase
    special_chars = "!@#$%&*()-_=+[]{}<>:?"
    if override_special:
        special_chars = override_special

    chars = ""
    if upper:
        chars = chars + upper_chars

    if lower:
        chars = chars + lower_chars

    if numeric:
        chars = chars + num_chars

    if special:
        chars = chars + special_chars

    try:
        # prefer to use system random number generator
        rand = random.SystemRandom()
    except NotImplementedError:
        # if that isn't available, fall back to pseudo-random number seeded by time
        rand = random.Random()

    result = []
    result.extend(rand.choices(num_chars, k=min_numeric))
    result.extend(rand.choices(lower_chars, k=min_lower))
    result.extend(rand.choices(upper_chars, k=min_upper))
    result.extend(rand.choices(special_chars, k=min_special))
    result.extend(rand.choices(chars, k=length - len(result)))

    rand.shuffle(result)
    resultant_string = "".join(result)
    ret["comment"] += ("Successfully generated password",)
    ret["ret"] = resultant_string
    return ret
