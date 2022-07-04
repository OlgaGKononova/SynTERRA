from imasyndata_web.data_handler.operations.constants import OPERATIONS_STEP_MAP, STEP2ID, ENVIRONMENT_DICT
from imasyndata_web.operations_utils import convert_temp, convert_time


def __get_operation_mapping():
    operations_map = {}
    for op, mapping in OPERATIONS_STEP_MAP.items():
        if mapping not in operations_map:
            operations_map[mapping] = []
        operations_map[mapping].append(op)
    operations_map["Start"] = []
    operations_map["End"] = []
    operations_map["Press"] = []
    return operations_map


def __get_attributes_list(data, operation_type):
    operations_map = __get_operation_mapping()
    attributes_data = []
    if all("_operations" in row for row in data):
        for row in data:
            # if operation_type == "FiringOperation":
            #     attributes_data.append(row["_operations"][firing_step]["attributes"])
            #     continue

            for op in row["_operations"]:
                if op["type"] in operations_map[operation_type]:
                    attributes_data.append(op["attributes"])

    if not attributes_data:
        return [], [], []

    temperatures, times, environment = [], [], []
    for condition in attributes_data:
        temperatures.extend(convert_temp(t) for t in condition["temperature"])
        times.extend(convert_time(t) for t in condition["time"])
        environment.extend(ENVIRONMENT_DICT.get(a.lower(), a) for a in condition["environment"] if a)

    return temperatures, times, environment


def get_operation_attributes(data, operation):
    if operation:
        operation_type = operation["label"]
    else:
        return {}

    temperatures, times, environment = __get_attributes_list(data, operation_type)

    return {"temperature": temperatures,
            "time": times,
            "environment": environment}


def get_operation_precursors(data, edge):
    start, end = STEP2ID[edge["source"].capitalize()], STEP2ID[edge["target"].capitalize()]
    all_precursors = {}
    i = 0
    for row in data:
        if row["graph"][start, end] > 0:
            for p in row["precursors"]:
                if p not in all_precursors:
                    all_precursors[p] = 0
                all_precursors[p] += 1
        i += 1
    all_precursors = [(k, v) for k, v in sorted(all_precursors.items(), key=lambda x: x[1])][-10:]
    return all_precursors