from dataclasses import dataclass, field
from enum import Enum


class BreedTypes(Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    RABBIT = "rabbit"
    OTHER = "other"


@dataclass
class Pet:
    pet_breed: BreedTypes
    food: list[str] = field(default_factory=list)
    clean: bool = True

    def pet_info(self):
        pass

    def special_needs(self):
        pass

    def clean_status(self) -> bool:
        return self.clean


@dataclass
class Task:
    task_to_do: str
    complete: bool = False
    in_progress: bool = False
    done: bool = False
    list_of_tasks: dict = field(default_factory=dict)

    def add_task(self):
        pass

    def delete_task(self):
        pass

    def update_task(self):
        pass

    def review_task(self):
        pass

    def get_tasks(self) -> dict:
        return self.list_of_tasks


@dataclass
class Owner:
    days: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    @property
    def number_of_pets(self) -> int:
        return len(self.pets)

    def owner_info(self):
        pass

    def days_available(self) -> list[str]:
        return self.days

    def update_day_available(self):
        pass

    def get_pets(self) -> list[Pet]:
        return self.pets
