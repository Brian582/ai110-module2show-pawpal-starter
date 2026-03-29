from dataclasses import dataclass, field
from enum import Enum
from datetime import date


class BreedTypes(Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    RABBIT = "rabbit"
    OTHER = "other"


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@dataclass
class Pet:
    name: str
    pet_breed: BreedTypes
    food: list[str] = field(default_factory=list)
    clean: bool = True
    needs: list[str] = field(default_factory=list)

    def pet_info(self) -> dict:
        pass

    def special_needs(self) -> list[str]:
        return self.needs

    def clean_status(self) -> bool:
        return self.clean


@dataclass
class Task:
    task_to_do: str
    pet: Pet
    status: TaskStatus = TaskStatus.PENDING
    due_date: date | None = None
    priority: int = 1  # 1=low, 2=medium, 3=high

    def update_status(self, new_status: TaskStatus):
        pass

    def review_task(self) -> dict:
        pass


@dataclass
class TaskManager:
    list_of_tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def delete_task(self, task: Task):
        pass

    def update_task(self, task: Task, **kwargs):
        pass

    def get_tasks(self) -> list[Task]:
        return self.list_of_tasks


@dataclass
class Owner:
    days: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)
    task_manager: TaskManager = field(default_factory=TaskManager)

    @property
    def number_of_pets(self) -> int:
        return len(self.pets)

    def owner_info(self) -> dict:
        pass

    def days_available(self) -> list[str]:
        return self.days

    def update_day_available(self, day: str):
        pass

    def get_pets(self) -> list[Pet]:
        return self.pets


@dataclass
class Scheduler:
    owner: Owner

    def build_daily_plan(self, day: str) -> dict:
        pass

    def explain_plan(self, plan: dict) -> str:
        pass

    def rank_tasks(self, tasks: list[Task]) -> list[Task]:
        pass
