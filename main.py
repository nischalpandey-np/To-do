import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

# Configure your MySQL connection
db_config = {
    'user': 'root',
    'password': '#####',
    'host': '127.0.0.1',
    'database': 'todo_db'
}

# Create a connection to the MySQL database
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor() 

    # Create the tasks table if it doesn't exist
    cursor.execute(
        '''
    CREATE TABLE IF NOT EXISTS tasks 
    (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task VARCHAR(255) NOT NULL
    )
    '''
    )
    connection.commit()

    def display_options():
        """Display the main options for the TO-DO list manager."""
        while True:
            print("\nPlease select one of the following options:")
            print("-" * 50)
            print("1. Add new task")
            print("2. View your tasks")
            print("3. Delete a task")
            print("4. Exit")
            print("-" * 50)
            choice = input("Enter your choice (1-4): ")
            if choice == "1":
                add_new_task()
            elif choice == "2":
                view_tasks()
            elif choice == "3":
                delete_task()
            elif choice == "4":
                print("Exiting the TO-DO list manager. Goodbye!")
                break
            else:
                print("Please enter a valid choice (1-4).")

    def add_new_task():
        """Add a new task to the TO-DO list and insert it into the database."""
       
        task = input("Please enter a task: ").strip()
        if task:
            try:
                cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
                connection.commit()
                print(f"Task '{task}' has been added to your TO-DO list.")
            except Error as e:
                print(f"Error adding task: {e}")
        else:
            print("Task cannot be empty. Please enter a valid task.")
        input("Press Enter to continue...")

    def view_tasks():
        """View all tasks in the TO-DO list from the database."""
        try:
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
            
            if tasks:
               print(tabulate(tasks, headers=['ID', 'Task'], tablefmt='pretty'))
            else:
                print("There are no tasks currently.")
        except Error as e:
            print(f"Error retrieving tasks: {e}")
        input("Press Enter to continue...")

    def delete_task():
        """Delete a task from the TO-DO list and remove it from the database."""
        view_tasks()
        try:
            task_to_delete = int(input("Enter the task number to delete: "))
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_to_delete,))
            connection.commit()
            if cursor.rowcount > 0:
                print(f"Task #{task_to_delete} was deleted successfully.")
            else:
                print(f"Task #{task_to_delete} was not found.")
        except ValueError:
            print("Invalid input. Please enter a valid task number.")
        except Error as e:
            print(f"Error deleting task: {e}")
        input("Press Enter to continue...")

    if __name__ == "__main__":
        print("\tWelcome to the TO-DO List Manager\t")
        display_options()

except Error as e:
    print(f"Error connecting to MySQL: {e}")
finally:
    # Close the connection when the program exits
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
