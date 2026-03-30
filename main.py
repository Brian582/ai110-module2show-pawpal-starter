from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler, BreedTypes, TaskStatus

# Create pets
buddy = Pet(name="Buddy", pet_breed=BreedTypes.DOG, food=["kibble", "chicken"], needs=["daily walk"])
whiskers = Pet(name="Whiskers", pet_breed=BreedTypes.CAT, food=["tuna", "dry food"], clean=False)

# Create owner and add pets
owner = Owner(days=["Monday", "Wednesday", "Sunday"], pets=[buddy, whiskers])

# Add tasks out of order (latest dates first)
task1 = Task(task_to_do="Morning walk", pet=buddy, priority=3, due_date=date(2026, 4, 9))
task2 = Task(task_to_do="Evening playtime", pet=buddy, priority=1, due_date=date(2026, 4, 3))
task3 = Task(task_to_do="Groom and bathe", pet=whiskers, priority=2, due_date=date(2026, 3, 31))
task4 = Task(task_to_do="Vet checkup", pet=buddy, priority=2, due_date=None)
task5 = Task(task_to_do="Feed breakfast", pet=whiskers, priority=3, due_date=date(2026, 3, 30))
task6 = Task(task_to_do="Trim nails", pet=buddy, priority=2, due_date=date(2026, 3, 31))  # conflicts with task3

for task in [task1, task2, task3, task4, task5, task6]:
    owner.task_manager.add_task(task)

# Mark one task done for filtering demo
task2.update_status(TaskStatus.DONE)

tm = owner.task_manager

# --- Sort by date ---
print("=" * 40)
print("  Sorted by Due Date (earliest first)")
print("=" * 40)
for t in tm.sort_by_date():
    due = t.due_date.isoformat() if t.due_date else "no date"
    print(f"  [{due}] {t.task_to_do} ({t.pet.name})")

# --- Filter: pending tasks only ---
print()
print("=" * 40)
print("  Filter: PENDING tasks only")
print("=" * 40)
for t in tm.filter_tasks(status=TaskStatus.PENDING):
    print(f"  {t.task_to_do} ({t.pet.name}) — {t.status.value}")

# --- Filter: tasks for Buddy only ---
print()
print("=" * 40)
print("  Filter: Buddy's tasks only")
print("=" * 40)
for t in tm.filter_tasks(pet_name="Buddy"):
    print(f"  {t.task_to_do} — {t.status.value}")

# --- Filter: Buddy's pending tasks (combined) ---
print()
print("=" * 40)
print("  Filter: Buddy's PENDING tasks")
print("=" * 40)
for t in tm.filter_tasks(status=TaskStatus.PENDING, pet_name="Buddy"):
    print(f"  {t.task_to_do} — due: {t.due_date or 'anytime'}")

# --- Today's schedule ---
print()
scheduler = Scheduler(owner=owner)
today = "Sunday"
plan = scheduler.build_daily_plan(today)
print("=" * 40)
print("       PawPal+ Today's Schedule")
print("=" * 40)
print(scheduler.explain_plan(plan))
print("=" * 40)
