#This is an example of the file you must have in your main git branch
import perceval as pcvl

def get_CCZ() -> pcvl.Processor:
    return pcvl.catalog["postprocessed ccz"].build_processor()

def get_CZ() -> pcvl.Processor:
    return pcvl.Processor("SLOS",6).add(0, pcvl.Unitary(pcvl.Matrix.eye(6)))