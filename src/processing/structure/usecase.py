from dataclasses import dataclass

from structure.entity import Entity
from structure.step import Step

@dataclass
class UseCase:

    req: str # ID of the requirement, e.g., "REQ-0001"
    ucid: str # ID of the use case, e.g., "uc1"

    entities: list[Entity]
    initial_step: Step

    def print(self):
        print(f'{self.req} {self.ucid}')
        print()

        for entity in self.entities:
            print(entity)
        print()

        self.initial_step.print_indented()

    def get_number_of_entities(self, only_actors: bool=False, only_explicit: bool=False):
        """Determine the number of entities associated with this use case

        parameters:
            only_actors : True to filter for actors (and exclude participants)
            only_explicit : True to filter for explicit entities
        
        returns: number of entities associated with the use case complying to the conditions
        """
        result: list[Entity] = self.entities

        if only_actors:
            if only_explicit:
                result = [e for e in self.entities if (e.actor and e.explicit)]
            else:
                result = [e for e in self.entities if (e.actor)]
        else:
            if only_explicit:
                result = [e for e in self.entities if (e.explicit)]

        return len(result)
    
    def get_number_of_interactions(self, only_userlevel: bool=False):
        """Count the number of interactions associated with this use case

        parameters:
            only_userlevel : True to filter for interactions between one actor and one participant
            only_consecutive : True to filter for interactions where the first entity is the last entity of the preceding interaction

        returns: number of interactions complying to the conditions
        """
        return self.initial_step.count_interactions(only_userlevel)
    
    def get_number_of_consecutive_interactions(self):
        return self.initial_step.count_consecutive_interactions(None)