# To-Do List Manager

A simple command-line tool to manage a SQLite database. The tool allows the addition, deletion, and management of tasks.

## Usage

1. Download the script to the desired location.
2. Navigate to directory containing the script in a terminal window.
3. Run "--help" to read the script manual.

## Script Tags

--view: View the entire table.
--add ADD ADD: Add an entry to the table. The first value should be the name of the task, the second should be the description. Encase both with quotations.
--delete DELETE: Remove an entry from the table. The value should be the name of the entry you would like to remove.
--mark MARK: Mark an entry as "complete". This is done in the form of a boolean. The value should be the name of the entry you would like to mark as complete.
--reset: Removes all data from the table.
--filter FILTER: Filters the table to sohw results that include the value.

## Modules

Python 3+
SQLite3
Argparse
Re
