import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, timedelta
from pawpal_system import Pet, Task, TaskManager, TaskStatus, BreedTypes, Owner, Scheduler


def test_mark_complete_changes_status():
    pet = Pet(name="Buddy", pet_breed=BreedTypes.DOG)
    task = Task(task_to_do="Feed Buddy", pet=pet)

    assert task.status == TaskStatus.PENDING

    task.update_status(TaskStatus.DONE)

    assert task.status == TaskStatus.DONE


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Whiskers", pet_breed=BreedTypes.CAT)
    manager = TaskManager()

    assert len(manager.get_tasks()) == 0

    manager.add_task(Task(task_to_do="Brush Whiskers", pet=pet))

    assert len(manager.get_tasks()) == 1


def test_sort_by_date_returns_chronological_order():
    pet = Pet(name="Buddy", pet_breed=BreedTypes.DOG)
    manager = TaskManager()

    today = date.today()
    task_later = Task(task_to_do="Vet visit", pet=pet, due_date=today + timedelta(days=5))
    task_sooner = Task(task_to_do="Feed Buddy", pet=pet, due_date=today + timedelta(days=1))
    task_no_date = Task(task_to_do="Play fetch", pet=pet, due_date=None)

    manager.add_task(task_later)
    manager.add_task(task_sooner)
    manager.add_task(task_no_date)

    sorted_tasks = manager.sort_by_date()

    assert sorted_tasks[0] == task_sooner
    assert sorted_tasks[1] == task_later
    assert sorted_tasks[2] == task_no_date  # None dates go last


def test_complete_daily_task_creates_next_day_task():
    pet = Pet(name="Buddy", pet_breed=BreedTypes.DOG)
    manager = TaskManager()

    today = date.today()
    task = Task(task_to_do="Feed Buddy", pet=pet, due_date=today, recurrence="daily")
    manager.add_task(task)

    next_task = manager.complete_task(task)

    assert task.status == TaskStatus.DONE
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.recurrence == "daily"
    assert next_task.status == TaskStatus.PENDING
    assert len(manager.get_tasks()) == 2


def test_check_conflicts_warns_on_same_due_date():
    pet = Pet(name="Buddy", pet_breed=BreedTypes.DOG)
    owner = Owner(days=["Monday"])
    owner.pets.append(pet)

    conflict_date = date.today() + timedelta(days=1)
    task1 = Task(task_to_do="Feed Buddy", pet=pet, due_date=conflict_date)
    task2 = Task(task_to_do="Vet visit", pet=pet, due_date=conflict_date)
    owner.task_manager.add_task(task1)
    owner.task_manager.add_task(task2)

    scheduler = Scheduler(owner=owner)
    warnings = scheduler.check_conflicts([task1, task2])

    assert len(warnings) == 1
    assert conflict_date.isoformat() in warnings[0]
