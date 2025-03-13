from dataclasses import dataclass

from structure.step import Step
from structure.entity import Entity

@dataclass
class Fork(Step):
    
    branches: dict

    def __init__(self, alternative_conditions: list[str], alternative_sequences: list[Step]):
        self.branches = {}

        for condition_line, sequence in zip(alternative_conditions, alternative_sequences):
            condition: str = ""
            if condition_line.strip().startswith("alt"):
                condition = condition_line.strip().split("alt ")[1]
            else:
                condition = condition_line.strip().split("else ")[1]
            
            self.branches[condition] = sequence

        self.predecessor = None
        self.successor = None

    def print_indented(self, indent: int = 0):

        first_condition = True
        for condition in self.branches:
            # print the conditions
            print("\t"*indent + ("alt " if first_condition else "else ") + condition)
            first_condition = False
            # print the sequence below the condition
            self.branches[condition].print_indented(indent+1)
        print("\t"*indent + "end")

        Step.print_indented(self, indent)

    def count_interactions(self, only_userlevel: bool=False):
        count: int = 0
        for branch in self.branches:
            count = count + self.branches[branch].count_interactions(only_userlevel)

        if self.successor != None:
            count = count + self.successor.count_interactions(only_userlevel)
        return count
    
    def count_consecutive_interactions(self, last_entity: Entity):
        count: int = 0
        for branch in self.branches:
            count = count + self.branches[branch].count_consecutive_interactions(last_entity)

        if self.successor != None:
            # obtain the last step in the loop sequence
            last: Step = self.branches[list(self.branches.keys())[0]].get_last_step()
            return count + self.successor.count_consecutive_interactions(last_entity=last.entity2)
        return count
    
    def get_last_step(self) -> Step:
        if self.successor != None:
            return self.successor.get_last_step()
        else:
            return self.branches[list(self.branches.keys())[0]].get_last_step()