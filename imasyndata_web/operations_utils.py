"""
Very naive and rough implementation of the function to guess which heating step is a firing step
and to assign solution mixing to a mixing step
"""
from imasyndata_web.constants import SOLUTION_VERBS, DISPERSION_VERBS, MIXING_ENV, MILLING_TERMS


def convert_temp(temp):
    if temp["units"] == "K":
        return temp["max"]-273.15
    return temp["max"]


def convert_time(time):
    if time["units"] in ['min', 'minutes']:
        return round(time["max"]/60.0, 2)
    if time["units"] in ['d', 'day']:
        return time["max"]*24
    return time["max"]


def get_last_heating_step(operations):
    firing_step = None

    if not operations:
        return firing_step

    shapings = 0
    quenchings = 0
    heatings = 0
    mixings = 0
    max_T = 0
    for op in operations:
        if op["type"] == "HeatingOperation":
            heatings += 1
        if op["type"] == "ShapingOperation":
            shapings += 1
        if op["type"] == "MixingOperation":
            mixings += 1
        if op["type"] == "QuenchingOperation":
            quenchings += 1

    if not heatings:
        return firing_step

    """
    if only one heating operation, assume it is a firing operation as well
    """
    if heatings == 1:
        firing_step = [i for i, op in enumerate(operations) if op["type"] == "HeatingOperation"][0]
        return firing_step

    include_shape = shapings != 0
    # include_quench = quenchings != 0
    # current_sent = operations[0]["i"][0]
    for op_id, op in enumerate(operations):

        """
        if no more heating operations finishing the search
        """
        if not heatings:
            break

        if op["type"] == "ShapingOperation":
            shapings -= 1
        if op["type"] == "QuenchingOperation":
            quenchings -= 1

        if op["type"] == "HeatingOperation":
            heatings -= 1
            if any(convert_temp(t) > max_T for t in op["attributes"]["temperature"] if t["max"]):
                max_T = max([convert_temp(t) for t in op["attributes"]["temperature"] if t["max"]])
                # max_T_id = op_id

            """
            avoiding re-heat without temperature and pre-heat otherwise consider as possible firing step
            """
            if not ("re" == op["string"][0:2] and not op["attributes"]["temperature"]) \
                    and "pre" != op["string"][0:3]:
                firing_step = op_id
                if include_shape and shapings == 0 and op["attributes"]["temperature"]:
                    break

        # current_sent = op["i"][0]

    """
    checking temperature condition - implementation is stupid, need to re-write it
    """
    if firing_step:
        op_id = firing_step
        firing_op = operations[firing_step]
        while op_id >= 0 and not firing_op["attributes"]["temperature"]:
            op = operations[op_id]
            if op["type"] == "HeatingOperation" and "pre" not in op["string"][0:3]:
                firing_step = op_id
                firing_op = operations[firing_step]
            op_id -= 1

        if all(convert_temp(t) < max_T for t in firing_op["attributes"]["temperature"] if t["max"]) \
                and "anneal" in firing_op["string"]:
            op_id = firing_step
            while op_id >= 0 and not firing_op["attributes"]["temperature"]:
                op = operations[op_id]
                if op["type"] == "HeatingOperation" and "pre" not in op["string"][0:3]:
                    firing_step = op_id
                    firing_op = operations[firing_step]
                op_id -= 1

    return firing_step


def is_solution_mixing(operation, tokens):
    if any(w in operation["op_token"] for w in SOLUTION_VERBS):
        return True
    if "dropwise" in tokens[operation["subsent"][0]:operation["subsent"][1]]:
        return True

    return False


def is_dispersing_mixing(operation, tokens):
    if any(w in operation["op_token"] for w in DISPERSION_VERBS):
        return True

    if any(env in MIXING_ENV for env in operation["env_toks"]) and not is_solution_mixing(operation, tokens):
        return True

    return False


def is_hot_pressing(operation, tokens):
    if operation["op_type"] == "ShapingOperation" \
            and "hot" in [t for i, t in enumerate(tokens) if operation["op_id"] - 2 <= i < operation["op_id"]]:
        return True

    return False


def is_ball_milling(operation, tokens):
    if any(w in operation["op_token"] for w in MILLING_TERMS):
        return True

    if "by ball" in tokens[operation["subsent"][0]:operation["subsent"][1]]:
        return True

    return False


def reassign_operations(extraction_data):
    operations = []
    prev_op_type = ""
    for sent_id, sent in enumerate(extraction_data):
        for op_id, op in enumerate(sent["graph"]):

            ## ignoring StartingSynthesis referred to final step
            if op["op_type"] == "StartingSynthesis" and "final" in op["subject"]:
                continue

            if op["op_token"] in ["uniaxially", "uniaxial"]:
                continue

            if not (op["ref_op"] and prev_op_type == op["op_type"]) and op["op_type"] != "StartingSynthesis":
                op_type = op["op_type"]
                if op_type == "MixingOperation" and is_solution_mixing(op, sent["tokens"]):
                    op_type = "SolutionMixing"
                if op_type == "MixingOperation" and is_dispersing_mixing(op, sent["tokens"]):
                    op_type = "DispersionMixing"

                operations.append({"string": op["op_token"],
                                   #"i": (sent_id, op["op_id"]),
                                   "type": op_type,
                                   "attributes": {"temperature": op["temp_values"],
                                                  "time": op["time_values"],
                                                  "environment": op["env_toks"]}})

                prev_op_type = op["op_type"]

    return operations
