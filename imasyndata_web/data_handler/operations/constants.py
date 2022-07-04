ID2STEP = ["Start", "Solution", "Mixing", "Heating", "Press", "Sinter", "End"]
STEP2ID = {op: i for i, op in enumerate(ID2STEP)}

LABELS_POSITION = {"Start": {"x": 0, "y": 0},
                   "Solution": {"x": 60, "y": 50},
                   "Mixing": {"x": -60, "y": 100},
                   "Heating": {"x": 60, "y": 150},
                   "Press": {"x": -60, "y": 200},
                   "Sinter": {"x": 60, "y": 250},
                   "End": {"x": 0, "y": 300}}

OPERATION_TYPES = {"DryingOperation",
                   "FiringOperation",
                   "HeatingOperation",
                   "DispersionMixing",
                   "MixingOperation",
                   "QuenchingOperation",
                   "ShapingOperation",
                   "SolutionMixing"}

OPERATIONS_STEP_MAP = {"SolutionMixing": "Solution",
                       "MixingOperation": "Mixing",
                       "DispersionMixing": "Mixing",
                       "DryingOperation": "Heating",
                       "HeatingOperation": "Heating",
                       "ShapingOperation": "Press",
                       "FiringOperation": "Sinter"}

DEFAULT_ATTRIBUTES_LBL = "Operation attributes"
DEFAULT_PRECURSORS_LBL = "Commonly used precursors"


ATTRIBUTES_PLOT_TITLE = {"temperature": "Max. Temperature, C",
                         "time": "Max. Time, hr",
                         "environment": "Environment"}


ENVIRONMENT_DICT = {"argon": "Ar",
                    "hydrogen": "H2",
                    "oxygen": "O2",
                    "nitrogen": "N2"
                    }