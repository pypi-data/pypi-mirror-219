"""State module for generating random integers"""
import copy
import random
from typing import Any
from typing import Dict

import dict_tools.differ as differ


def present(
    hub,
    ctx,
    name: str,
    min: int,
    max: int,
    resource_id: int = None,
    keepers: Dict[str, Any] = None,
    seed: str = None,
) -> Dict[str, Any]:
    r"""
    This is a logical state and doesn't interact with any cloud providers.
    This state can be used in conjunction with any other state to generate
    random integer with the provided configurations. State's configuration
    data is stored in esm. If for a given state , the configuration changes
    , a new random integer is generated. If there are no configuration changes
    , then the old integer is retained.

    Args:
        name(str):
            An Idem name of the resource.

        min(int):
            The minimum inclusive value of the range.

        max(int):
            The maximum inclusive value of the range.

        resource_id(int, Optional):
            Unique random Integer

        keepers(dict, Optional):
            Arbitrary map of values that, when changed, will trigger recreation of resource.

        seed(str, Optional):
            A custom seed to always produce the same value.

    Request Syntax:

    .. code-block:: sls

      [random_integer_state]:
        random.integer.present:
          - name: 'string'
          - keepers:
              'string': 'string'
          - min: 'int'
          - max: 'int'
          - seed: 'string'

    Returns:
        Dict[str, Any]

    Examples:

    .. code-block:: sls

      random_integer_state:
        random.integer.present:
          - name: random_integer
          - min: 0
          - max: 9
          - keepers:
              key: value
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    params = dict(
        min=min,
        max=max,
        seed=seed,
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

            result["comment"].append(f"Config change detected for '{name}'.")

            result["new_state"] = {
                "keepers": keepers,
                "params": params,
                "name": name,
                "output": None,
            }
            if ctx.get("test"):
                result["comment"].append(
                    f"Would generate new random.random.integer {name}."
                )

                return result

            if seed is not None:
                rand = random.Random(seed=seed)
            else:
                try:
                    # prefer to use system random number generator
                    rand = random.SystemRandom()
                except NotImplementedError:
                    # if that isn't available, fall back to pseudo-random number seeded by time
                    rand = random.Random()

            result["new_state"]["output"] = rand.randint(min, max)
            result["comment"].append(f"Generated new random.random.integer '{name}'.")

        else:
            result["comment"].append(
                f"No config change detected for '{name}'. Old random integer will be retained."
            )
            result["new_state"] = copy.deepcopy(result["old_state"])

    else:
        result["new_state"] = {
            "keepers": keepers,
            "params": params,
            "name": name,
            "output": None,
        }
        if ctx.get("test"):
            result["comment"].append(f"Would generate random.random.integer '{name}'.")
            return result

        if seed is not None:
            random.seed(seed)
        result["new_state"]["output"] = random.randint(min, max)
        result["new_state"]["resource_id"] = result["new_state"]["output"]
        result["comment"].append(f"random.random.integer '{name}' generated.")

    return result


def absent(
    hub,
    ctx,
    name: str,
) -> Dict[str, Any]:
    r"""

    This logical state is used to invalidate/delete the random integer resource.

    Args:
        name(str): An Idem name of the resource.

    Request Syntax:

    .. code-block:: sls

      [random_integer_state]:
        random.integer.absent:
          - name: 'string'

    Returns:
        Dict[str, Any]

    Example:

    .. code-block:: sls

      random_state01011:
        random.integer.absent:
          - name: rs01011

    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before = ctx.get("old_state")

    result["old_state"] = before

    if before:
        if ctx.get("test", False):
            result["comment"].append(
                f"Would remove the random.random.integer '{name}'."
            )
            return result

        result["comment"].append(f"Removed the random.random.integer '{name}'.")
    else:
        result["comment"].append(f"random.random.integer '{name}' already absent.")

    return result
