from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Step(ABC):

    predecessor : Step # previous step of this step
    successor: Step # next steps

    @abstractmethod
    def print_indented(self, indent: int=0):
        if self.successor != None:
            self.successor.print_indented(indent)

    @abstractmethod
    def count_interactions(self, only_userlevel: bool=False):
        return 0
    
    @abstractmethod
    def count_consecutive_interactions(self, last_entity):
        return 0
    
    @abstractmethod
    def get_last_step(self) -> Step:
        return None