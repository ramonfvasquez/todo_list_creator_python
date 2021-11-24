# todo_list_creator_python

This is a ToDo List application that allows the user to create, edit, and
delete todos with a text limit of 150 characters. It is built with the
Tkinter library.

At load it asks the user whether the program should open the ToDo List
main window or if it should run in server mode, i.e. a server socket
(server.py) is ran instead of the application so as to receive and
respond different requests from a client application (client.py). The
server.py module can run as a standalone program.

The client can send any of the following commands:<br />

##################### TODO LIST - Handled by the server #####################<br />
count<br />
Get the number of todos stored in the database.

s / search [text to search]<br />
Search todos by text. If no argument is entered, all todos will be displayed.

sort [color / date / id / text] [desc]<br />
Get all the todos sorted by the argument entered.<br />
Optional: enter 'desc' to sort downwards.

todo [del / delete / edit / save]<br />
Open the todo editor.<br />
Enter 'del' or 'delete' to remove a todo by its ID number.<br />
Enter 'edit' to update a todo by its ID number.<br />
Enter 'save' to create a new todo.<br />
#############################################################################<br />

###################### CONSOLE - Handled by the client ######################<br />
clear<br />
Clear the screen.

clh<br />
Clear the command history.

close / end / exit / x<br />
Exit client and shut down the server.

commands<br />
Clear the screen and print the command list.

h<br />
Command history.<br />
#############################################################################<<br />

When not running in server mode, the window shows a create/edit form and a
canvas.

The form bears an Entry for the text, a DateEntry, two Spins (one for the
hours, one for the minutes, both max values of which are limited accordingly),
and a creation button (labeled with a "+"; it is replaced with an "Edit"
button when any of the todos' edition buttons is clicked).

All the todos saved into the database will be inserted into the canvas as
follows: one main square of 200x200 with a fill color chose by the user; a
little black rectangle on top that shows the date and time (or an "Expired"
message when the time is older than the present time); a dark blue, and a
dark red rectangles (the former acts as the "Edit" button; the latter as the
"Delete" button), both of wich have a width of half the square's width. Each
of these two buttons is bind with its corresponding method.

When editing a todo, the form will fill with all the todo data, including the
color, except when the todo is expired and its color is grey, in which case
the color selected in the color combobox is the first option.
