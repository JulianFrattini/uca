from dataclasses import dataclass

from structure.step import Step
from structure.entity import Entity
from structure.interaction import Interaction

@dataclass
class Loop(Step):

    condition: str
    loop_sequence: Step

    def __init__(self, text: str, loop_sequence: Step):
        # extract the loop condition
        currentline: str = text.strip()
        self.condition = currentline.split("loop ")[1].strip()

        self.loop_sequence = loop_sequence

        self.predecessor = None
        self.successor = None

    def print_indented(self, indent: int = 0):
        print("\t"*indent + f'loop {self.condition}')
        self.loop_sequence.print_indented(indent=indent+1)
        print("\t"*indent + 'end')

        Step.print_indented(self, indent)

    def count_interactions(self, only_userlevel: bool=False):    
        if self.successor != None:
            return self.successor.count_interactions(only_userlevel) + self.loop_sequence.count_interactions(only_userlevel)
        return self.loop_sequence.count_interactions(only_userlevel)
    
    def count_consecutive_interactions(self, last_entity: Entity):
        # determine the number of consecutive interactions within the loop
        count = self.loop_sequence.count_consecutive_interactions(last_entity=last_entity)

        if self.successor != None:
            # obtain the last step in the loop sequence
            last: Step = self.loop_sequence.get_last_step()
            return count + self.successor.count_consecutive_interactions(last_entity=last.entity2)
        
        return count
    
    def get_last_step(self) -> Step:
        if self.successor != None:
            return self.successor.get_last_step()
        else:
            return self.loop_sequence.get_last_step()