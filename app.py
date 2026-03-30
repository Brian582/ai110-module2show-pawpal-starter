import streamlit as st
from pawpal_system import BreedTypes, Owner, Pet, Scheduler, Task, TaskStatus

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session state vault ---
# Only create these objects on the FIRST run. Every subsequent rerun reuses them.
if "owner" not in st.session_state:
    st.session_state.owner = Owner()

st.title("🐾 PawPal+")

# ──────────────────────────────────────────────
# SECTION 1: Add a Pet
# ──────────────────────────────────────────────
st.subheader("Add a Pet")

# Map the human-readable selectbox labels to BreedTypes enum members
BREED_OPTIONS = {
    "Dog": BreedTypes.DOG,
    "Cat": BreedTypes.CAT,
    "Bird": BreedTypes.BIRD,
    "Rabbit": BreedTypes.RABBIT,
    "Other": BreedTypes.OTHER,
}

with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    breed_label = st.selectbox("Species", list(BREED_OPTIONS.keys()))
    submitted_pet = st.form_submit_button("Add Pet")

if submitted_pet:
    if pet_name.strip():
        # Pet.__init__ requires name + pet_breed — every other field has a default
        new_pet = Pet(name=pet_name.strip(), pet_breed=BREED_OPTIONS[breed_label])
        # Owner.pets is a plain list; no add_pet helper needed
        st.session_state.owner.pets.append(new_pet)
        st.success(f"Added {new_pet.name} ({breed_label}) to your pets.")
    else:
        st.error("Pet name cannot be empty.")

# Always show current pets so the user sees the vault is working
owner: Owner = st.session_state.owner
if owner.pets:
    st.write(f"Your pets ({owner.number_of_pets}):")
    st.table([p.pet_info() for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ──────────────────────────────────────────────
# SECTION 2: Schedule a Task
# ──────────────────────────────────────────────
st.subheader("Schedule a Task")

PRIORITY_MAP = {"Low": 1, "Medium": 2, "High": 3}

if not owner.pets:
    st.warning("Add a pet first before scheduling tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        task_description = st.text_input("Task description", value="Morning walk")
        # Let the user pick which pet this task is for
        pet_names = [p.name for p in owner.pets]
        selected_pet_name = st.selectbox("For which pet?", pet_names)
        priority_label = st.selectbox("Priority", list(PRIORITY_MAP.keys()), index=2)
        due_date = st.date_input("Due date (optional)", value=None)
        submitted_task = st.form_submit_button("Add Task")

    if submitted_task:
        if task_description.strip():
            # Resolve the selected pet object from the owner's list
            selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)
            new_task = Task(
                task_to_do=task_description.strip(),
                pet=selected_pet,
                priority=PRIORITY_MAP[priority_label],
                due_date=due_date,  # date | None — matches Task.due_date type
            )
            # TaskManager.add_task appends to its internal list
            owner.task_manager.add_task(new_task)
            st.success(f"Task '{new_task.task_to_do}' added for {selected_pet.name}.")
        else:
            st.error("Task description cannot be empty.")

    # Show all pending/in-progress tasks, sorted by due date via TaskManager
    sorted_tasks = owner.task_manager.sort_by_date()
    visible_tasks = [t for t in sorted_tasks if t.status != TaskStatus.DONE]
    if visible_tasks:
        # Surface conflicts ABOVE the table so a pet owner sees them immediately
        scheduler = Scheduler(owner=owner)
        conflicts = scheduler.check_conflicts(visible_tasks)
        if conflicts:
            for conflict in conflicts:
                # Strip the baked-in "WARNING: " prefix — st.warning provides the visual cue
                st.warning(conflict.replace("WARNING: ", "", 1))
            st.caption("Tip: reschedule one of the conflicting tasks to a different date to avoid overloading your day.")
        st.caption("Tasks sorted by due date — soonest first, no-date tasks at the bottom.")
        st.table([t.review_task() for t in visible_tasks])
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# ──────────────────────────────────────────────
# SECTION 3: Generate Daily Schedule
# ──────────────────────────────────────────────
st.subheader("Generate Daily Schedule")

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

selected_day = st.selectbox("Which day?", DAYS)

if st.button("Mark me available this day"):
    # Owner.update_day_available guards against duplicates
    owner.update_day_available(selected_day)
    st.success(f"You are now available on {selected_day}.")

st.caption(f"Days you're available: {owner.days_available() or ['none yet']}")

if st.button("Generate schedule"):
    if not owner.pets:
        st.error("Add at least one pet first.")
    elif selected_day not in owner.days:
        st.warning(f"You haven't marked yourself available on {selected_day}. Click 'Mark me available' first.")
    else:
        scheduler = Scheduler(owner=owner)
        plan = scheduler.build_daily_plan(selected_day)
        if not plan or not plan.get("tasks"):
            st.info("No active tasks to schedule for that day.")
        else:
            # Show conflicts first — a pet owner needs to act on these before the day begins
            conflicts = plan.get("warnings", [])
            if conflicts:
                for conflict in conflicts:
                    st.error(conflict.replace("WARNING: ", "", 1))
                st.caption("Resolve these conflicts before the day starts by rescheduling one of the affected tasks.")

            st.success(f"Plan for {plan['day']} — {len(plan['tasks'])} task(s), ranked by priority.")
            st.table(plan["tasks"])
