from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler, BreedTypes

# Create pets
buddy = Pet(name="Buddy", pet_breed=BreedTypes.DOG, food=["kibble", "chicken"], needs=["daily walk"])
whiskers = Pet(name="Whiskers", pet_breed=BreedTypes.CAT, food=["tuna", "dry food"], clean=False)

# Create owner and add pets
owner = Owner(days=["Monday", "Wednesday", "Sunday"], pets=[buddy, whiskers])

# Create tasks with different due dates
task1 = Task(task_to_do="Morning walk", pet=buddy, priority=3, due_date=date(2026, 4, 9))
task2 = Task(task_to_do="Feed breakfast", pet=whiskers, priority=3, due_date=date(2026, 3, 30))
task3 = Task(task_to_do="Groom and bathe", pet=whiskers, priority=2, due_date=date(2026, 3, 31))
task4 = Task(task_to_do="Evening playtime", pet=buddy, priority=1, due_date=date(2026, 4, 3))

# Add tasks to the owner's task manager
for task in [task1, task2, task3, task4]:
    owner.task_manager.add_task(task)

# Build and print today's schedule
scheduler = Scheduler(owner=owner)
today = "Sunday"
plan = scheduler.build_daily_plan(today)

print("=" * 40)
print("       PawPal+ Today's Schedule")
print("=" * 40)
print(scheduler.explain_plan(plan))
print("=" * 40)
