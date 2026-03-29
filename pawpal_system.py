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
        return {
            "name": self.name,
            "breed": self.pet_breed.value,
            "food": self.food,
            "clean": self.clean,
            "needs": self.needs,
        }

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
        self.status = new_status

    def review_task(self) -> dict:
        return {
            "task": self.task_to_do,
            "pet": self.pet.name,
            "status": self.status.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
        }


@dataclass
class TaskManager:
    list_of_tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.list_of_tasks.append(task)

    def delete_task(self, task: Task):
        self.list_of_tasks.remove(task)

    def update_task(self, task: Task, **kwargs):
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)

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
        return {
            "days_available": self.days,
            "number_of_pets": self.number_of_pets,
            "pets": [pet.pet_info() for pet in self.pets],
        }

    def days_available(self) -> list[str]:
        return self.days

    def update_day_available(self, day: str):
        if day not in self.days:
            self.days.append(day)

    def get_pets(self) -> list[Pet]:
        return self.pets


@dataclass
class Scheduler:
    owner: Owner

    def build_daily_plan(self, day: str) -> dict:
        if day not in self.owner.days:
            return {}
        tasks = self.owner.task_manager.get_tasks()
        ranked = self.rank_tasks([t for t in tasks if t.status != TaskStatus.DONE])
        return {
            "day": day,
            "tasks": [t.review_task() for t in ranked],
        }

    def explain_plan(self, plan: dict) -> str:
        if not plan:
            return "No plan available for that day."
        lines = [f"Plan for {plan['day']}:"]
        for t in plan.get("tasks", []):
            lines.append(
                f"  - [{t['priority']}] {t['task']} for {t['pet']} (due: {t['due_date'] or 'anytime'})"
            )
        return "\n".join(lines)

    def rank_tasks(self, tasks: list[Task]) -> list[Task]:
        return sorted(tasks, key=lambda t: t.priority, reverse=True)
