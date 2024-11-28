
import json
from datetime import datetime, timedelta

class Task:
    def _init_(self, title, description='', priority='Normal', due_date=None, completed=False):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

    def _str_(self):
        due_str = f", Due: {self.due_date}" if self.due_date else ""
        status_str = " [Completed]" if self.completed else " [Incomplete]"
        return f"Title: {self.title}, Description: {self.description}, Priority: {self.priority}{due_str}{status_str}"


class TaskTracker:
    def _init_(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
                return [Task(**task) for task in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump([task._dict_ for task in self.tasks], file)

    def add_task(self, title, description='', priority='Normal', due_date=None):
        task = Task(title, description, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()
        print(f'Task "{title}" added!')

    def view_tasks(self, show_completed=False):
        filtered_tasks = [task for task in self.tasks if task.completed == show_completed]
        if not filtered_tasks:
            print("No tasks available.")
            return
        for index, task in enumerate(filtered_tasks):
            print(f"{index + 1}. {task}")

    def delete_task(self, index):
        try:
            removed_task = self.tasks.pop(index - 1)
            self.save_tasks()
            print(f'Task "{removed_task.title}" deleted!')
        except IndexError:
            print("Invalid task number.")

    def edit_task(self, index):
        try:
            task = self.tasks[index - 1]
            print(f"Editing Task: {task}")
            title = input("Enter new task title (leave blank to keep current): ")
            description = input("Enter new task description (leave blank to keep current): ")
            priority = input("Enter new task priority (High, Normal, Low, leave blank to keep current): ")
            due_date = input("Enter new due date (YYYY-MM-DD, leave blank to keep current): ")

            if title:
                task.title = title
            if description:
                task.description = description
            if priority:
                task.priority = priority
            if due_date:
                try:
                    datetime.strptime(due_date, '%Y-%m-%d')
                    task.due_date = due_date
                except ValueError:
                    print("Invalid date format. Keeping current due date.")

            self.save_tasks()
            print("Task updated successfully.")
        except IndexError:
            print("Invalid task number.")

    def mark_task_completed(self, index):
        try:
            task = self.tasks[index - 1]
            task.completed = True
            self.save_tasks()
            print(f'Task "{task.title}" marked as completed!')
        except IndexError:
            print("Invalid task number.")

    def search_tasks(self, query):
        results = [task for task in self.tasks if query.lower() in task.title.lower() or query.lower() in task.description.lower()]
        if results:
            for index, task in enumerate(results):
                print(f"{index + 1}. {task}")
        else:
            print("No matching tasks found.")

    def notify_due_tasks(self):
        today = datetime.now().date()
        due_tasks = [task for task in self.tasks if task.due_date and datetime.strptime(task.due_date, '%Y-%m-%d').date() == today and not task.completed]
        if due_tasks:
            print("You have due tasks today:")
            for task in due_tasks:
                print(f"- {task.title} (Due Today)")
        else:
            print("No tasks are due today.")

    def run(self):
        while True:
            print("\nTask Tracker")
            print("1. Add Task")
            print("2. View All Tasks")
            print("3. View Completed Tasks")
            print("4. View Incomplete Tasks")
            print("5. Delete Task")
            print("6. Edit Task")
            print("7. Mark Task as Completed")
            print("8. Search Tasks")
            print("9. Notify Due Tasks")
            print("10. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                title = input("Enter task title: ")
                description = input("Enter task description (optional): ")
                priority = input("Enter task priority (High, Normal, Low): ")
                due_date = input("Enter due date (YYYY-MM-DD, optional): ")
                if due_date:
                    try:
                        datetime.strptime(due_date, '%Y-%m-%d')
                    except ValueError:
                        print("Invalid date format. Task will be added without a due date.")
                        due_date = None
                self.add_task(title, description, priority, due_date)
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.view_tasks(show_completed=True)
            elif choice == '4':
                self.view_tasks(show_completed=False)
            elif choice == '5':
                self.view_tasks()
                task_number = input("Enter task number to delete: ")
                if task_number.isdigit():
                    self.delete_task(int(task_number))
                else:
                    print("Please enter a valid number.")
            elif choice == '6':
                self.view_tasks()
                task_number = input("Enter task number to edit: ")
                if task_number.isdigit():
                    self.edit_task(int(task_number))
                else:
                    print("Please enter a valid number.")
            elif choice == '7':
                self.view_tasks(show_completed=False)
                task_number = input("Enter task number to mark as completed: ")
                if task_number.isdigit():
                    self.mark_task_completed(int(task_number))
                else:
                    print("Please enter a valid number.")
            elif choice == '8':
                query = input("Enter search query: ")
                self.search_tasks(query)
            elif choice == '9':
                self.notify_due_tasks()
            elif choice == '10':
                print("Exiting Task Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    tracker = TaskTracker()
    tracker.run()