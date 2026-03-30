# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Features

- **Chronological sorting** — `TaskManager.sort_by_date` orders tasks by due date ascending using a tuple sort key `(due_date is None, due_date)`, so undated tasks always fall to the bottom of the list.
- **Conflict warnings** — `Scheduler.check_conflicts` groups active tasks by due date into a dictionary and emits a warning message for every date that contains more than one task, catching both same-pet and cross-pet pile-ups before the day begins.
- **Priority-ranked scheduling** — `Scheduler.rank_tasks` sorts active tasks by the integer `priority` field (1 = low → 3 = high) in descending order so the daily plan always leads with the most urgent care items.
- **Daily/weekly recurrence** — `TaskManager.complete_task` marks a task `DONE` and immediately appends a new `PENDING` copy with the due date bumped forward by one day (`timedelta(days=1)`) for daily tasks or seven days (`timedelta(weeks=1)`) for weekly tasks, copying all other task attributes unchanged.
- **Status and pet filtering** — `TaskManager.filter_tasks` narrows the task list by `TaskStatus` and/or pet name; both filters are optional and composable, returning all tasks when neither is supplied.
- **Daily plan generation** — `Scheduler.build_daily_plan` checks owner availability, removes `DONE` tasks, runs the priority ranker, and bundles the ranked task list with any conflict warnings into a single plan dictionary.
- **Human-readable plan output** — `Scheduler.explain_plan` converts a plan dictionary into a formatted string that lists each task with its priority, description, pet name, and due date, plus any conflict warnings appended at the end.

## Smarter Scheduling

- **Conflict detection** — `Scheduler.check_conflicts` scans for tasks that share the same due date and surfaces a warning in the plan output, letting the owner spot overloaded days before they happen.
- **Recurring task automation** — `TaskManager.complete_task` automatically creates the next occurrence of a daily or weekly task when the current one is marked done, so no recurring care item ever falls off the schedule.
- **Sorting and filtering** — `TaskManager.sort_by_date` returns tasks in chronological order (undated tasks last), and `TaskManager.filter_tasks` lets the UI narrow the list by status or pet name.

## Testing PawPal  
python -m pytest

My tests demonstrate the following:
1. When tasks are added out of order, they are returned in returned in chronological order. 
2. When a daily task is completed, the test checks that a new task is created for the following day and that recurrence="daily" and status=PENDING.
3. The last test schedules two tasks on the same date and makes sure that one warning is returned containing that date.

Confidence level: 4

