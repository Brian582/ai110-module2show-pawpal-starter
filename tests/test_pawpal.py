import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import Pet, Task, TaskManager, TaskStatus, BreedTypes


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
