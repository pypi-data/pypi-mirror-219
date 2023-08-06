import json


def process_extra_context(context: dict):
    if not context:
        return ""
    if type(context) is str:
        raise TypeError(
            f"Context must be a object dict, not {type(context).__name__}!!!"
        )
    return " - " + json.dumps(context)
