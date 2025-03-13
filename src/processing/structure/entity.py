from dataclasses import dataclass

@dataclass
class Entity:

    entid: str # identifier of the entity
    name: str # name of the entity
    actor: bool # true if the entity is an "actor", false if it is a "participant"
    explicit: bool = False # true if the actor was explicit 

    def __init__(self, text: str):
        # parses an entity from a line of the mermaid sequence diagram
        # e.g., "actor user AS (User)"
        
        self.actor = text.strip().startswith("actor")

        # split the text into two parts at the mandatory AS section
        parts: list[str] = text.split(" AS ")

        # isolate the identifier of the entity
        if self.actor:
            self.entid = parts[0].split('actor ')[1]
        else:
            self.entid = parts[0].split('participant ')[1]

        # isolate the name of the entity
        namepart: str = parts[1].strip()
        self.explicit = not namepart.startswith("(") and not namepart.endswith(")")

        if self.explicit:
            self.name = namepart
        else:
            self.name = namepart[1:-1]

    def __repr__(self) -> str:
        return ('actor' if self.actor else 'participant') + f' {self.entid} as ' + (f'{self.name}' if self.explicit else f'({self.name})')