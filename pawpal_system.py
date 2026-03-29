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
        """Return a dictionary summary of the pet's attributes."""
        return {
            "name": self.name,
            "breed": self.pet_breed.value,
            "food": self.food,
            "clean": self.clean,
            "needs": self.needs,
        }

    def special_needs(self) -> list[str]:
        """Return the list of the pet's special needs."""
        return self.needs

    def clean_status(self) -> bool:
        """Return whether the pet is currently clean."""
        return self.clean


@dataclass
class Task:
    task_to_do: str
    pet: Pet
    status: TaskStatus = TaskStatus.PENDING
    due_date: date | None = None
    priority: int = 1  # 1=low, 2=medium, 3=high

    def update_status(self, new_status: TaskStatus):
        """Update the task's status to the given TaskStatus value."""
        self.status = new_status

    def review_task(self) -> dict:
        """Return a dictionary summary of the task's details."""
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
        """Append a task to the task list."""
        self.list_of_tasks.append(task)

    def delete_task(self, task: Task):
        """Remove a task from the task list."""
        self.list_of_tasks.remove(task)

    def update_task(self, task: Task, **kwargs):
        """Update one or more fields on an existing task."""
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)

    def get_tasks(self) -> list[Task]:
        """Return all tasks in the task list."""
        return self.list_of_tasks


@dataclass
class Owner:
    days: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)
    task_manager: TaskManager = field(default_factory=TaskManager)

    @property
    def number_of_pets(self) -> int:
        """Return the total number of pets owned."""
        return len(self.pets)

    def owner_info(self) -> dict:
        """Return a dictionary summary of the owner's availability and pets."""
        return {
            "days_available": self.days,
            "number_of_pets": self.number_of_pets,
            "pets": [pet.pet_info() for pet in self.pets],
        }

    def days_available(self) -> list[str]:
        """Return the list of days the owner is available."""
        return self.days

    def update_day_available(self, day: str):
        """Add a day to the owner's availability if not already present."""
        if day not in self.days:
            self.days.append(day)

    def get_pets(self) -> list[Pet]:
        """Return the list of the owner's pets."""
        return self.pets


@dataclass
class Scheduler:
    owner: Owner

    def build_daily_plan(self, day: str) -> dict:
        """Build and return a ranked task plan for the given day."""
        if day not in self.owner.days:
            return {}
        tasks = self.owner.task_manager.get_tasks()
        ranked = self.rank_tasks([t for t in tasks if t.status != TaskStatus.DONE])
        return {
            "day": day,
            "tasks": [t.review_task() for t in ranked],
        }

    def explain_plan(self, plan: dict) -> str:
        """Return a human-readable string describing the daily plan."""
        if not plan:
            return "No plan available for that day."
        lines = [f"Plan for {plan['day']}:"]
        for t in plan.get("tasks", []):
            lines.append(
                f"  - [{t['priority']}] {t['task']} for {t['pet']} (due: {t['due_date'] or 'anytime'})"
            )
        return "\n".join(lines)

    def rank_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by priority from highest to lowest."""
        return sorted(tasks, key=lambda t: t.priority, reverse=True)
