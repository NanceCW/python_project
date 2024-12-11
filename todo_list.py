import sqlite3, argparse, re

# Create a connection to a database called database.db
conn = sqlite3.connect('database.db')
# Create a cursor to perform database operations
cursor = conn.cursor()

 # Create a table for todo list (taken from 'test_e1_sqlite.py from Python SQL assignment)
def setup_database():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todo (
            name TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            status BOOLEAN NOT NULL
        )
    ''')

def main():
    setup_database()
    parser = argparse.ArgumentParser(description='To-Do List Manager')

    # Allows user to view their tasks
    parser.add_argument('--view', action='store_true', help='List all tasks in the table.')
    # Allows user to add a task with a description
    parser.add_argument('--add', nargs=2, help='Adds a task. First value is tasks name, second is description of task. Encase values in quotes.')
    # Allows user to remove a task
    parser.add_argument('--delete', help='Deletes the provided task (Must enter valid task name).')
    # Allows user to mark task as completed
    parser.add_argument('--mark', help="Marks the provided task as complete.")
    # Allows users to restart their to-do list (removes all entries)
    parser.add_argument('--reset', action='store_true', help="Resets the entire table. Use carefully.")
    # Allows users to filter rows that include provided string
    parser.add_argument('--filter', help="Filter search results.")

    # Parse the arguments
    args, unkown_args = parser.parse_known_args()

    # Store argument values
    is_view = args.view
    is_add = args.add
    is_delete = args.delete
    is_mark = args.mark
    is_reset = args.reset
    is_filter = args.filter
    
    # Selects all rows from table
    if is_view:
        cursor.execute("SELECT * FROM todo")
        rows = cursor.fetchall()
        if rows:
            print(f"Table results:")
            for row in rows:
                print(row)
        else: 
            print("The table is empty.")
            
    # Adds row to table with provided values, status is set to FALSE by default (indicating an incomplete task)
    elif is_add:
        try:
            cursor.execute("INSERT INTO todo (name, description, status) VALUES (?, ?, ?)", (is_add[0], is_add[1], False))
            conn.commit()
            print(f"Values added to table: Name={is_add[0]}, Description={is_add[1]}, Complete?=FALSE")
        except Exception as e:
            print(f'There was an error while adding the task: "{e}". Please try again.')
            
    # Deletes the row from the table with the provided name
    elif is_delete:
        try:
            cursor.execute(f"SELECT name FROM todo")
            rows = cursor.fetchall()
            values = [row[0] for row in rows]
            for column_value in values:
                if column_value==is_delete:
                    cursor.execute("DELETE FROM todo WHERE name = ?", (is_delete,))
                    conn.commit()
                    print(f"Row '{is_delete}' deleted from table.")
                    return
            print(f'Name value "{is_delete}" not found. Please try again.')
        except Exception as e:
            print(f'There was an error while deleting the task: "{e}". Please try again.')
            
    # Marks the task provided as complete
    elif is_mark:
        try:
            cursor.execute(f"SELECT name FROM todo")
            rows = cursor.fetchall()
            values = [row[0] for row in rows]
            for column_value in values:
                if column_value==is_mark:
                    cursor.execute('UPDATE todo SET status = ? WHERE name = ?', (True, is_mark))
                    conn.commit()
                    print(f'Task "{is_mark}" marked as complete.')
                    return
            print(f'Name value "{is_mark}" not found. Please try again.')
        except Exception as e:
            print(f'There was an error while marking the task: "{e}". Please try again.')
            
    # Removes the entire table (table is recreated at the start of next command)
    elif is_reset:
        try:
            print(f"Table reset.")
            cursor.execute("DROP TABLE todo")
            conn.commit()
        except Exception as e:
            print(f'There was an error while resetting the table: "{e}". Please try again.')
            
    # Filters the table to only show results with the string provided. Filtered string can either be in the name or description columns.
    elif is_filter:
        try:
            filter = re.compile(is_filter)     
            cursor.execute("SELECT * FROM todo")
            rows = cursor.fetchall()
            filtered_results = [row for row in rows if re.search(filter, row[0]) or re.search(filter, row[1])]
            if filtered_results:
                for row in filtered_results:
                    print(row)
            else:
                print(f'No filtered results for "{is_filter}" found!')
        except re.error:
            print(f'There was an error while filtering the table: "{e}". Please try again.')
            
    # If no arguments provided, print message to direct user to use "--help"
    else:
        if unkown_args:
            print(f'An unkown argument is present: {unkown_args[0]}. See below and try again:')
            parser.print_help()
        else:
            print('No arguments were provided. See below and try again:')
            parser.print_help()
        
if __name__ == "__main__":
    main()