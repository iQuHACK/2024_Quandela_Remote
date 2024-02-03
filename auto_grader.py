import math
import cmath as cm
from enum import Enum
import perceval as pcvl


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


def get_heralded_and_ancillaries(processor: pcvl.Processor):
    return pcvl.BasicState(list(processor.heralds.values()))


def get_proba_amplitude_error(processor, mapping, data_states):
    sim = pcvl.SimulatorFactory().build(processor)
    herald_states = get_heralded_and_ancillaries(processor)
    modulus_value = None
    phase_value = None
    states = [state * herald_states for state in mapping]
    data_states = [state * herald_states for state in data_states]
    error = 0
    for i_state in states:
        for o_state in states:
            pa = sim.prob_amplitude(i_state, o_state)
            modulus = abs(pa)
            phase = cm.phase(pa)
            if i_state == o_state:
                if modulus_value is None:
                    modulus_value = modulus
                error += abs(modulus - modulus_value)/modulus_value
                assert modulus != 0

                if i_state not in data_states:
                    if phase_value is None:
                        phase_value = phase
                    error += abs(phase - phase_value)/(2*cm.pi)
                else:
                    error += abs(phase - phase_value - cm.pi)/(2*cm.pi)

            else:
                error += modulus / modulus_value
    return error


def rate_processor(
        processor: pcvl.Processor,
        mapping: dict,
        target: dict,
        criteria: dict,
        gate_type: GateType = GateType.CNOT,
        data_states: list[pcvl.BasicState] = None) -> float:

    if gate_type == GateType.CCNOT or gate_type == GateType.CCZ:
        h_mode = 4
    elif gate_type == GateType.CNOT or gate_type == GateType.CZ:
        h_mode = 2

    if gate_type == GateType.CNOT or gate_type == GateType.CCNOT:
        cnot = processor
        cz = pcvl.Processor("SLOS", processor.m)
        cz.add(h_mode, pcvl.BS.H())
        cz.add(0, processor)
        cz.add(h_mode, pcvl.BS.H())
    elif gate_type == GateType.CZ or gate_type == GateType.CCZ:
        cz = processor
        cnot = pcvl.Processor("SLOS", processor.m)
        cnot.add(h_mode, pcvl.BS.H())
        cnot.add(0, processor)
        cnot.add(h_mode, pcvl.BS.H())

    analyzer = pcvl.algorithm.Analyzer(cnot, mapping)
    analyzer.compute(expected=target)
    score = 0

    for criteria_name in criteria:
        current_criteria = CriteriaType[criteria_name]

        if current_criteria == CriteriaType.n_photons:
            score += get_score(current_criteria.name,
                               criteria, get_photon_number(cnot))

        elif current_criteria == CriteriaType.n_modes:
            score += get_score(current_criteria.name,
                               criteria, cnot.circuit_size)

        elif current_criteria == CriteriaType.performance:
            score += get_score(current_criteria.name,
                               criteria, analyzer.performance)

        elif current_criteria == CriteriaType.prob_error:
            score += get_score(current_criteria.name,
                               criteria, 1-analyzer.fidelity)

        elif current_criteria == CriteriaType.prob_amplitude_error:
            get_proba_amplitude_error(cz, mapping.keys(), data_states)
            score += get_score(current_criteria.name,
                               criteria, 1-analyzer.fidelity)

    return score


if __name__ == "__main__":
    from main import get_CCZ
    criteria = {
        'n_photons': {
            'method': 'log',
            'direction': 'minus',
            'weight': 1e-3
        },
        'n_modes': {
            'method': 'log',
            'direction': 'minus',
            'weight': 1e-4
        },
        'performance': {
            'method': 'log',
            'direction': 'plus',
            'weight': 10
        },
        'prob_amplitude_error': {
            'method': 'log',
            'direction': 'minus',
            'weight': 1e7
        }
    }

    mapping = {pcvl.BasicState('|1,0,1,0,1,0>'): '000',
               pcvl.BasicState('|1,0,1,0,0,1>'): '001',
               pcvl.BasicState('|1,0,0,1,1,0>'): '010',
               pcvl.BasicState('|1,0,0,1,0,1>'): '011',
               pcvl.BasicState('|0,1,1,0,1,0>'): '100',
               pcvl.BasicState('|0,1,1,0,0,1>'): '101',
               pcvl.BasicState('|0,1,0,1,1,0>'): '110',
               pcvl.BasicState('|0,1,0,1,0,1>'): '111'}

    target = {"000": "000", "001": "001", "010": "010", "011": "011",
              "100": "100", "101": "101", "110": "111", "111": "110"}

    print(rate_processor(get_CCZ(), mapping, target, criteria,
          GateType.CCZ, [pcvl.BasicState("|0,1,0,1,0,1>")]))
