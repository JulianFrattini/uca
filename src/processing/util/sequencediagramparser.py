from structure.entity import Entity

from structure.step import Step
from structure.interaction import Interaction
from structure.loop import Loop
from structure.fork import Fork

def find_end_of_loop(lines: list[str]) -> int:
    """Find the index of the line of a list of sequence diagram steps that ends the current sequence (e.g., a loop or condition).

    attributes:
        lines : list of verbatim lines

    returns: index where the sequence ends
    """
    indent: int = 0
    index: int = 0
    currentline: str = lines[index]

    while True:
        if currentline.strip().startswith('end'):
            if indent == 0:
                break
            else:
                indent -= 1
        elif currentline.strip().startswith('alt') or currentline.strip().startswith('loop'):
            # observing any line starting with "alt" or "loop" indicates another nested control structure, meaning that the next "end" statement refers to that loop rather than the current one
            indent += 1

        index += 1
        currentline = lines[index]

    return index

def find_alternatives(lines: list[str]) -> int:
    indent: int = 0
    index: int = 0
    currentline: str = lines[index].strip()
    indices_of_alternatives: list[int] = []

    while True:
        if currentline.startswith('end'):
            if indent == 0:
                break
            else:
                indent -= 1
        elif currentline.startswith('alt') or currentline.startswith('loop'):
            # observing any line starting with "alt" or "loop" indicates another nested control structure, meaning that the next "end" statement refers to that loop rather than the current one
            indent += 1
        elif currentline.startswith('else') and indent == 0:
            # if the current line starts with "else", then it marks an alternative
            indices_of_alternatives.append(index)

        index += 1
        currentline = lines[index].strip()

    # finally, add the end index of the fork
    indices_of_alternatives.append(index)

    return indices_of_alternatives


def parse_sequence_diagram(lines: list[str], entities: list[Entity], predecessor: Step = None) -> Step:
    step: Step = None
    currentline: str = lines[0].strip()

    # determine the index of the line to continue at
    next_index: int = 1

    if currentline.startswith('alt'):
        # beginning of a fork
        alternative_indices = find_alternatives(lines[1:])
        alternative_indices = [0] + [idx+1 for idx in alternative_indices]

        alternative_conditions: list[str] = []
        alternative_sequences: list[Step] = []

        previous_index: int = 0
        for alternative_index in alternative_indices[1:]:
            alternative_conditions.append(lines[previous_index])
            alternative_sequence = parse_sequence_diagram(lines[previous_index+1:alternative_index], entities)
            alternative_sequences.append(alternative_sequence)
            previous_index = alternative_index

        step = Fork(alternative_conditions, alternative_sequences)
        
        next_index = alternative_indices[-1]+1
    elif currentline.startswith('loop'):
        # beginning of a loop
        end_index: int = find_end_of_loop(lines[1:])+1
        loop_sequence: Step = parse_sequence_diagram(lines[1:end_index], entities)
        step = Loop(text=currentline, loop_sequence=loop_sequence)
        next_index = end_index+1
    else:
        # regular step
        step = Interaction(currentline, available_entities=entities)

    step.predecessor = predecessor

    # determine the successor
    if len(lines) > next_index:
        step.successor = parse_sequence_diagram(lines[next_index:], entities, predecessor=step)

    return step