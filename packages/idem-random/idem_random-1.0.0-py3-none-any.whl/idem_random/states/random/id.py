"""State module for generating ids"""
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
    prefix: str = None,
) -> Dict[str, Any]:
    r"""
    This is a logical state and doesn't interact with any cloud providers.
    This state can be used in conjunction with any other state to generate
    random id with the provided configurations. State's configuration
    data is stored in esm. If for a given state, the configuration changes,
    a new random id is generated. If there are no configuration changes,
    then the old id is retained.

    The generated id is alphanumeric, starting with a letter.

    Args:
        name(str): An Idem name of the resource.
        length(int): The number of random characters to produce.
        resource_id(str, Optional): Unique random Id
        keepers(dict, Optional): A list of arbitrary map of values that,
          when changed, will trigger recreation of resource.
        prefix(str, Optional): Arbitrary string to prefix the output value with. This string is supplied as-is, meaning
          it is not guaranteed to be URL-safe or base64 encoded.

    Request Syntax:

    .. code-block:: sls

      [random_id_state]:
        random.id.present:
          - name: 'string'
          - length: 'int'
          - keepers:
              'string': 'string'
          - prefix: 'string'

    Returns:
        Dict[str, Any]

    Example:

    .. code-block:: sls

      random_passwd_state:
        random.id.present:
          - name: random_id
          - length: 2
          - keepers:
              name: random_id
          - prefix: random_prefix
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    config_map = dict(
        keepers=keepers,
        length=length,
        prefix=prefix,
    )

    if resource_id:
        result["old_state"] = result["new_state"] = {
            "config_map": config_map,
            "name": name,
            "output": resource_id,
            "resource_id": resource_id,
        }
        return result

    if prefix is None:
        prefix = ""

    before = ctx.get("old_state")
    if before:
        result["old_state"] = before
        config_map_old = before.get("config_map", {})
        config_map_new = config_map

        result["changes"] = differ.deep_diff(config_map_old, config_map_new)

        if result["changes"]:

            result["comment"].append(f"Confiig change detected for '{name}'.")

            result["new_state"] = {
                "config_map": config_map,
                "name": name,
                "output": None,
            }
            if ctx.get("test"):
                result["comment"].append(f"Would generate new random.random.id.")

                return result

            ret = prefix + hub.tool.random.id.generate_random_id(length=length)

            result["new_state"]["output"] = ret
            result["comment"].append(f"Generated new random.random.id '{name}'.")
        else:
            result["comment"].append(
                f"No config change detected for '{name}'. Old ID will be retained."
            )
            result["old_state"]["output"] = resource_id
            result["old_state"]["resource_id"] = resource_id
            result["new_state"] = result["old_state"]

    else:
        result["new_state"] = {
            "config_map": config_map,
            "name": name,
            "output": None,
        }
        if ctx.get("test"):
            result["comment"].append(f"Would generate random.random.id '{name}'.")
            return result

        ret = prefix + hub.tool.random.id.generate_random_id(length=length)

        result["new_state"]["output"] = ret
        result["new_state"]["resource_id"] = ret
        result["comment"].append(f"random.random.id '{name}' generated.")
    return result


def absent(
    hub,
    ctx,
    name: str,
) -> Dict[str, Any]:

    r"""
    This logical state is used to invalidate/delete the id.

    Args:
        name(str): An Idem name of the resource.

    Request Syntax:

    .. code-block:: sls

      [random_id_state]:
        random.id.absent:
          - name: 'string'

    Returns:
        Dict[str, Any]

    Example:

    .. code-block:: sls

      random_state01011:
        random.id.absent:
          - name: rs01011
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before = ctx.get("old_state")

    result["old_state"] = before

    if before:
        if ctx.get("test", False):
            result["comment"].append(f"Would remove the random.random.id '{name}'.")
            return result

        result["comment"].append(f"Removed the random.random.id '{name}'.")
    else:
        result["comment"].append(f"random.random.id '{name}' already absent.")

    return result
