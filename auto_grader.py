auto_grader.py
import math
import cmath as cm
from enum import Enum
import perceval as pcvl
import numpy as np

class CriteriaType(Enum):
    n_photons = 0
    n_modes = 1
    performance = 2
    prob_error = 3
    prob_amplitude_error = 4
class CriteriaArgs(Enum):
    method = 0
    weight = 1
    direction = 2
class MethodType(Enum):
    linear = 0
    log = 1
    exp = 2
class DirectionType(Enum):
    plus = 0
    minus = 1
class GateType(Enum):
    CZ = 0
    CNOT = 1
    CCZ = 2
    CCNOT = 3
def get_photon_number(processor: pcvl.Processor) -> int:
    return processor._input_state.n
def calculate_score(weight: list[float, int], value: float, penalty_type: MethodType):
    weight = float(weight)
    score = value * weight
    if penalty_type == MethodType.log:
        score = (math.log(1+value)) * weight
    elif penalty_type == MethodType.exp:
        score = value ** weight
    return score
def get_score(criteria_key: str, criteria: dict, value: list[float, int]) -> float:
    crit = criteria[criteria_key]
    for ca in CriteriaArgs:
        if ca.name not in crit:
            raise KeyError(
                f"Missing criteria {ca.name} in criteria {criteria_key}")
    value = float(value)
    method_type = MethodType[crit[CriteriaArgs.method.name]]
    direction_type = DirectionType[crit[CriteriaArgs.direction.name]]
    score = calculate_score(crit[CriteriaArgs.weight.name], value, method_type)
    if direction_type == DirectionType.minus:
        score = -score
    print(
        f"For criteria {criteria_key}, penalty type is {method_type.name}, direction criteria type is {direction_type.name}, weight is {crit[CriteriaArgs.weight.name]}, penalty value is {value}, score is {score}")
    return score 


# Define the initial state
initial_state = np.zeros((max_a + 1, max_b + 1, max_c + 1))
initial_state[n_a, n_b, n_c] = 1  # Set the coefficient of the initial state to 1

# Apply CZ(a, b)
cz_ab_matrix = (-1) ** np.outer(np.arange(max_a + 1), np.arange(max_b + 1))
state_after_cz_ab = np.einsum('abc,ab->abc', initial_state, cz_ab_matrix)

# Apply CZ(b, c)
cz_bc_matrix = (-1) ** np.outer(np.arange(max_b + 1), np.arange(max_c + 1))
state_after_cz_bc = np.einsum('abc,bc->abc', state_after_cz_ab, cz_bc_matrix)

# Print the states
print("Initial State:")
print(initial_state)

print("\nState after CZ(a, b):")
print(state_after_cz_ab)

print("\nState after CZ(b, c):")
print(state_after_cz_bc)
