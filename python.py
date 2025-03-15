class Task:
    def __init__(self, title, description, deadline, priority):
        """
        Initialize a task with a title, description, deadline, and priority.
        """
        self.title = title
        self.description = description
        self.deadline = deadline  # Format: YYYY-MM-DD
        self.priority = priority  # Low, Medium, High
        self.completed = False  # Default status is "Pending"

    def __str__(self):
        """
        Return a string representation of the task.
        """
        status = "Completed" if self.completed else "Pending"
        return f"{self.title} ({status}) - Deadline: {self.deadline}, Priority: {self.priority}"
import json
from task import Task

def save_tasks(tasks):
    """
    Save a list of tasks to a JSON file.
    """
    with open("tasks.json", "w") as file:
        # Convert tasks to a list of dictionaries and save to JSON
        json.dump([task.__dict__ for task in tasks], file)

def load_tasks():
    """
    Load tasks from a JSON file. If the file doesn't exist, return an empty list.
    """
    try:
        with open("tasks.json", "r") as file:
            # Load tasks from JSON and convert them back to Task objects
            tasks_data = json.load(file)
            return [Task(**data) for data in tasks_data]
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []
from datetime import datetime
from task import Task

def calculate_priority_score(task):
    """
    Calculate a priority score for a task based on its deadline and priority.
    """
    # Priority weights
    priority_weights = {"Low": 1, "Medium": 2, "High": 3}
    
    # Calculate urgency based on the deadline
    deadline = datetime.strptime(task.deadline, "%Y-%m-%d")
    days_until_deadline = (deadline - datetime.now()).days
    urgency = max(0, 10 - days_until_deadline)  # Higher urgency if closer to deadline
    
    # Calculate total score
    score = priority_weights[task.priority] * urgency
    return score

def prioritize_tasks(tasks):
    """
    Sort tasks based on their priority score (higher score comes first).
    """
    return sorted(tasks, key=calculate_priority_score, reverse=True)
from task import Task
from storage import save_tasks, load_tasks
from prioritizer import prioritize_tasks

class TaskManager:
    def __init__(self):
        """
        Initialize the TaskManager and load tasks from the JSON file.
        """
        self.tasks = load_tasks()

    def add_task(self, title, description, deadline, priority):
        """
        Add a new task to the task list and save it to the JSON file.
        """
        task = Task(title, description, deadline, priority)
        self.tasks.append(task)
        save_tasks(self.tasks)

    def delete_task(self, task_title):
        """
        Delete a task by its title and save the updated list to the JSON file.
        """
        self.tasks = [task for task in self.tasks if task.title != task_title]
        save_tasks(self.tasks)

    def mark_completed(self, task_title):
        """
        Mark a task as completed by its title and save the updated list to the JSON file.
        """
        for task in self.tasks:
            if task.title == task_title:
                task.completed = True
        save_tasks(self.tasks)

    def list_tasks(self):
        """
        List all tasks, sorted by priority.
        """
        prioritized_tasks = prioritize_tasks(self.tasks)
        for task in prioritized_tasks:
            print(task)
from task_manager import TaskManager

def main():
    """
    Main function to run the Task Management System CLI.
    """
    manager = TaskManager()
    while True:
        # Display menu options
        print("\nTask Manager")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            # Add a new task
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            deadline = input("Enter deadline (YYYY-MM-DD): ")
            priority = input("Enter priority (Low, Medium, High): ")
            manager.add_task(title, description, deadline, priority)
            print("Task added successfully!")
        elif choice == "2":
            # List all tasks
            print("\nTasks:")
            manager.list_tasks()
        elif choice == "3":
            # Mark a task as completed
            title = input("Enter task title to mark as completed: ")
            manager.mark_completed(title)
            print(f"Task '{title}' marked as completed!")
        elif choice == "4":
            # Delete a task
            title = input("Enter task title to delete: ")
            manager.delete_task(title)
            print(f"Task '{title}' deleted!")
        elif choice == "5":
            # Exit the program
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
