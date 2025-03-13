from dataclasses import dataclass

from structure.step import Step
from structure.entity import Entity

@dataclass
class Interaction(Step):

    entity1 : Entity # entity that initiates the interaction
    entity2 : Entity # entity that receives the interaction

    returns : bool = False # whether the interaction returns a value (i.e., a -->> arrow, not a -->)
    description : str = "" # the label of the interaction

    def __init__(self, text: str, available_entities: list[Entity]):
        # parses an interaction from a line of the mermaid sequence diagram
        # e.g., "user ->> system : install the system using the deployment files"

        # split at the colon that delineates the relationship from its description
        parts: list[str] = text.strip().split(" : ")

        entities: list[str] = []
        if "-->>" in parts[0]:
            self.returns = True

            entities: list[str] = parts[0].split('-->>')
        else:
            entities: list[str] = parts[0].split('->>')

        # determine the matching entity from the list of available entities
        entity1_match = [ent for ent in available_entities if ent.entid == entities[0].strip()]
        self.entity1: Entity = entity1_match[0]

        entity2_match = [ent for ent in available_entities if ent.entid == entities[1].strip()]
        self.entity2: Entity = entity2_match[0]

        # record the description of the interaction
        self.description = parts[1].strip()

        self.predecessor = None
        self.successor = None

    def __repr__(self) -> str:
        return f'{self.entity1.entid} {"-->>" if self.returns else "->>"} {self.entity2.entid} : {self.description}'
    
    def print_indented(self, indent: int = 0):
        print("\t"*indent + str(self))

        Step.print_indented(self, indent)
        
    def count_interactions(self, only_userlevel: bool=False):
        count: int = 0
        if only_userlevel:
            if (self.entity1.actor and (not self.entity2.actor)) or ((not self.entity1.actor) and self.entity2.actor):
                count = 1
        else:
            count = 1

        if self.successor != None:
            return count + self.successor.count_interactions(only_userlevel)
        return count
    
    def count_consecutive_interactions(self, last_entity: Entity):
        count = 0
        if last_entity != None:
            if last_entity.entid == self.entity1.entid:
                count = 1
        if self.successor != None:
            return count + self.successor.count_consecutive_interactions(last_entity=self.entity2)
        return count
    
    def get_last_step(self) -> Step:
        if self.successor != None:
            return self.successor.get_last_step()
        return self