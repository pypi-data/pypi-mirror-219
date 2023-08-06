"""State module for generating random strings usable as passwords"""
from typing import Any
from typing import Dict

import dict_tools.differ as differ


def present(
    hub,
    ctx,
    name: str,
    length: int,
    resource_id: str = None,
    keepers: Dict[str, Any] = None,
    upper: bool = True,
    min_upper: int = 0,
    lower: bool = True,
    min_lower: int = 0,
    numeric: bool = True,
    min_numeric: int = 0,
    special: bool = True,
    min_special: int = 0,
    override_special: str = None,
) -> Dict[str, Any]:
    r"""
    This is a logical state and doesn't interact with any cloud providers.
    This state can be used in conjunction with any other state to generate
    random password with the provided configurations. State's configuration
    data is stored in esm. If for a given state , the configuration changes
    , a new random password is generated. If there are no configuration changes
    , then the old password is retained.

    Args:
        name(str):
            An Idem name of the resource.

        length(int) :
            The length of the required random password.

        resource_id(str, Optional):
            Unique random password

        keepers(List, Optional):
            A list of arbitrary map of values that, when changed, will trigger recreation of resource.

        lower(bool, Optional):
            Include lowercase alphabet characters in the result. Default value is true.

        min_lower(int, Optional):
            Minimum number of lowercase alphabet characters in the result.Default value is 0.

        min_numeric(int, Optional):
            Minimum number of numeric characters in the result. Default value is 0.

        min_special(int, Optional):
            Minimum number of special characters in the result. efault value is 0.

        min_upper(int, Optional):
            Minimum number of uppercase alphabet characters in the result. Default value is 0.

        numeric(bool, Optional):
            Include numeric characters in the result. Default value is true.

        override_special(str, Optional):
            Supply your own list of special characters to use for string generation. This overrides the default
            character list in the special argument. The special argument must still be set to true for any overwritten
            characters to be used in generation.

        special(bool, Optional):
            Include special characters in the result. These are !@#$%&*()-_=+[]{}<>:?. Default value is true.

        upper(bool, Optional):
            Include uppercase alphabet characters in the result. Default value is true.

    Request Syntax:

    .. code-block:: sls

      [random_password_state]:
        random.password.present:
          - name: 'string'
          - length: 'int'
          - keepers:
              'string': 'string'
          - lower: 'boolean'
          - min_lower: 'int'
          - upper: 'boolean'
          - min_upper: 'int'
          - numeric: 'boolean'
          - min_numeric: 'int'
          - special: 'boolean'
          - override_special: 'string'

    Returns:
        Dict[str, Any]

    Examples:

    .. code-block:: sls

      random_passwd_state:
        random.password.present:
          - name: random_passwd
          - length: 13
          - keepers:
              key: value
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    params = dict(
        upper=upper,
        min_upper=min_upper,
        lower=lower,
        min_lower=min_lower,
        numeric=numeric,
        min_numeric=min_numeric,
        special=special,
        min_special=min_special,
        override_special=override_special,
    )

    if resource_id:
        result["old_state"] = result["new_state"] = {
            "keepers": keepers,
            "params": params,
            "name": name,
            "output": resource_id,
            "resource_id": resource_id,
        }
        return result

    before = ctx.get("old_state")

    if before:
        result["old_state"] = before
        keepers_old = before.get("keepers", {})
        keepers_new = keepers if keepers else {}

        result["changes"] = differ.deep_diff(keepers_old, keepers_new)

        old_params = before.get("params", {})
        new_params = params

        if result["changes"] or old_params != new_params:

            result["comment"].append(f"Confiig change detected for '{name}'.")

            result["new_state"] = {
                "keepers": keepers,
                "params": params,
                "name": name,
                "output": None,
            }
            if ctx.get("test"):
                result["comment"].append(f"Would generate new random.random.password.")

                return result

            ret = hub.exec.random.password.generate_random_string(
                length=length, **params
            )

            if ret and ret["result"]:
                result["new_state"]["output"] = ret["ret"]
                result["comment"].append(
                    f"Generated new random.random.password '{name}'."
                )
        else:
            result["comment"].append(
                f"No config change detected for '{name}'. Old password will be retained."
            )

            result["new_state"] = result["old_state"]

    else:
        result["new_state"] = {
            "keepers": keepers,
            "params": params,
            "name": name,
            "output": None,
        }
        if ctx.get("test"):
            result["comment"].append(f"Would generate random.random.password '{name}'.")
            return result

        ret = hub.exec.random.password.generate_random_string(length=length, **params)

        if not ret or not ret["result"]:
            result["result"] = ret["result"]
            result["comment"].append(
                f"Unable to generate random.random.password '{name}'."
            )
            return result
        result["new_state"]["output"] = ret["ret"]
        result["new_state"]["resource_id"] = result["new_state"]["output"]
        result["comment"].append(f"random.random.password '{name}' generated.")

    return result


def absent(
    hub,
    ctx,
    name: str,
) -> Dict[str, Any]:

    r"""

    This logical state is used to invalidate/delete the password.

    Args:
        name(str): An Idem name of the resource.

    Request Syntax:

    .. code-block:: sls

      [random_password_state]:
        random.password.absent:
          - name: 'string'

    Returns:
        Dict[str, Any]

    Examples:

    .. code-block:: sls

      random_state01011:
        random.password.absent:
          - name: rs01011

    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before = ctx.get("old_state")

    result["old_state"] = before

    if before:
        if ctx.get("test", False):
            result["comment"].append(
                f"Would remove the random.random.password '{name}'."
            )
            return result

        result["comment"].append(f"Removed the random.random.password '{name}'.")
    else:
        result["comment"].append(f"random.random.password '{name}' already absent.")

    return result
