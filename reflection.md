# PawPal+ Project Reflection

## 1. System Design

Core actions:
Actions user should be able to perform:
1. Track pet care tasks 
2. Consider constraints 
3. Produce a daily plan and explain why it chose that plan

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
Answer:
The classes that I want to create are a Task class, Pet class, and an Owner class.

1. Task class responsibilities:
Attributes: Complete, InProgress, Done, taskToDo, Hashmap listOfTasks
Methods: 
a. addTask: add a task
b. deleteTask: delete a task
c. updateTask: update a specific task
d. reviewTask: review a specific task
e. getTasks: return list of tasks (return values of listOfTasks)

2. Pet class responsibilities:
Attributes: BreedTypes petBreed, List food, Boolean clean
Methods: 
a. petInfo: info about the pet
b. specialNeeds: any special needs that this pet needs
c. cleanStatus: check if pet is clean or not

3. Owner class responsibilities:
Attributes: List days, List pets, Int NumberOfPets
Methods: 
a. OwnerInfo: info about the owner
b. DaysAvailable: days that are good for the owner to take care of their pet(s)
c. updateDayAvailable: updates the days of owner's availability
d. getPets: return list of owner's pets

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---
Claude Code made some changes to the skeleton on pawpal_system.py. One of the changes was that it 
made my Boolean atributes, Complete, in_progress, and done into a single enum type. Now a task can 
only be in one state at a time.


## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
