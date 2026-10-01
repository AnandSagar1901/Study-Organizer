import os
import shelve
import time

from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6JyfEl6ODDSnsvWOTz3IB4V3hln40dU-uPN44_A3sXvSA"
)


def call_ai(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    print(response.text)


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


with shelve.open("database") as db:
    tasks = db.get("tasks", [])

print("Study Organizer")
choice = 0

while choice != 6:
    print("Options")
    print("1. Add New Task")
    print("2. View All Tasks")
    print("3. Recommend Next Task")
    print("4. Remove Task")
    print("5. Set Timer")
    print("6. Save and Exit")

    choice = int(input("Please select an option: "))

    if choice == 1:
        print("Please be specific")
        new_task = input("Enter the new task: ")
        tasks.append(new_task)
        print(f"'{new_task}' added to your current session.")
    elif choice == 2:
        print("\nYour Current Tasks:")
        print(tasks)
    elif choice == 3:
        print("Recommending next task...")
        call_ai(
            f"Here are the tasks: {tasks}. Please recemmond the next task I should do and give 1-2 sentences of reasioning."
        )
    elif choice == 4:
        for i in tasks[:]:
            remove_choice = input(f"Do you want to remove {i}: ")
            if remove_choice == "Yes" or remove_choice == "yes":
                tasks.remove(i)
                print("Task Succesfully Removed")
    elif choice == 5:
        try:
            task_name = input("Which task are you working on? ")
            minutes = int(input("How long should it take (in minutes)? "))

            adjusted_minutes = minutes * 0.8
            seconds = int(adjusted_minutes * 60)

            while seconds > 0:
                clear_terminal()  # Clears the screen to keep it updating in place
                print(f"Working on: '{task_name}'")
                print(
                    f"Time reduced by 20% for efficiency! Target duration: {adjusted_minutes:.1f} minutes."
                )
                mins, secs = divmod(seconds, 60)
                print(f"Time remaining: {mins:02d}:{secs:02d}")
                time.sleep(1)
                seconds -= 1

            print(f"\nTime's up! Finished working on '{task_name}'.\n")
        except ValueError:
            print("Please enter a valid number of minutes.")

with shelve.open("database") as db:
    db["tasks"] = tasks

print("Goodbye! Your list has been permanently saved.")
