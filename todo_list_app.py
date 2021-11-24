"""This is a ToDo List application that allows the user to create, edit, and
delete todos with a text limit of 150 characters. It is built with the
Tkinter library.

At load it asks the user to decide whether the program should open the ToDo
List main window or if it should run in server mode, i.e. a server socket
is ran instead of the application so as to receive and respond different
requests from a client application (client.py). The server.py module can
run as a standalone program.

When not running in server mode, the window shows a create/edit form and a
canvas.

The form bears an Entry for the text, a DateEntry, two Spins (one for the
hours, one for the minutes, both max values of which are limited accordingly),
and a creation button (labeled with a "+"; it is replaced for an "Edit"
button when any of the todos' edition buttons are clicked).

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
"""


import db.data_base as DB
import server
from datetime import datetime
from tkcalendar import DateEntry
from tkinter import (
    Button,
    Canvas,
    Entry,
    Frame,
    Label,
    Scrollbar,
    Spinbox,
    StringVar,
    Tk,
    ttk,
)
from tkinter.constants import BOTH, E, FLAT, N, S, VERTICAL, W
from tkinter.messagebox import askyesno
from todo import ToDo


class ToDoListApp:
    """Application's main window.
    It has the form for creating/editing the todos, and a canvas to show the
    todos stored in the database.
    """

    # Coordinates for the insertion of the todos in the canvas
    x0 = 50
    y0 = 0
    x1 = 250
    y1 = 250

    def __init__(self, root):
        DB.DataBase().create_table()

        self.root = root
        self.root.geometry("1315x850")
        self.root.resizable(False, False)
        self.root.title("ToDo List")

        bg = "White Smoke"

        container = Frame(self.root)
        container.pack(fill=BOTH, expand=True)

        ######################################################################
        #                       Creation/edition form                        #
        ######################################################################
        self.frm_create = Frame(container, bg="Black", borderwidth=20)
        self.frm_create.pack(fill=BOTH)

        Label(self.frm_create, text="Write something...").grid(
            row=0, column=0, padx=10, sticky=W
        )

        self.val_todo = StringVar()
        self.ent_todo = Entry(
            self.frm_create, textvariable=self.val_todo, width=89, relief=FLAT, bg=bg
        )
        self.ent_todo.grid(row=1, column=0, padx=10, sticky=E + W)
        self.ent_todo.bind("<KeyPress>", lambda e: self._on_key_press(e))
        self.ent_todo.bind("<KeyRelease>", lambda e: self._on_key_press(e))

        self.lbl_char_count = Label(self.frm_create)
        self.lbl_char_count.grid(row=2, column=0, padx=10, sticky=E)

        Label(self.frm_create, text="Date").grid(row=0, column=1, padx=10, sticky=W)

        self.val_date = StringVar()
        self.ent_date = DateEntry(
            self.frm_create,
            textvariable=self.val_date,
            selectmode="day",
            date_pattern="dd/MM/yyyy",
            state="readonly",
            width=13,
            relief=FLAT,
            bg=bg,
        )
        self.ent_date.grid(row=1, column=1, padx=10, sticky=E + W)

        Label(self.frm_create, text="Time").grid(row=0, column=2, padx=10, sticky=W)

        self.val_hour = StringVar()
        self.spin_hour = Spinbox(
            self.frm_create,
            from_=0,
            to=23,
            wrap=False,
            textvariable=self.val_hour,
            format="%02.0f",
            width=6,
        )
        self.spin_hour.grid(row=1, column=2, padx=10, sticky=W)
        self.spin_hour.bind(
            "<KeyPress>",
            lambda e: [
                self._set_char_limit(self.val_hour, 2),
                self._set_max_value(e, self.val_hour, 23),
            ],
        )
        self.spin_hour.bind(
            "<KeyRelease>",
            lambda e: [
                self._set_char_limit(self.val_hour, 2),
                self._set_max_value(e, self.val_hour, 23),
            ],
        )

        Label(self.frm_create, text=":").grid(row=1, column=3, sticky=W)

        self.val_minutes = StringVar()
        self.spin_minutes = Spinbox(
            self.frm_create,
            from_=0,
            to=59,
            wrap=False,
            textvariable=self.val_minutes,
            format="%02.0f",
            width=6,
        )
        self.spin_minutes.grid(row=1, column=4, padx=10, sticky=W)
        self.spin_minutes.bind(
            "<KeyPress>",
            lambda e: [
                self._set_char_limit(self.val_minutes, 2),
                self._set_max_value(e, self.val_minutes, 59),
            ],
        )
        self.spin_minutes.bind(
            "<KeyRelease>",
            lambda e: [
                self._set_char_limit(self.val_minutes, 2),
                self._set_max_value(e, self.val_minutes, 59),
            ],
        )

        self.lbl_color = Label(self.frm_create, text="Color")
        self.lbl_color.grid(row=0, column=6, padx=10, sticky=W)

        self.colors = [
            "Coral",
            "Crimson",
            "Green",
            "Light Blue",
            "Orange",
            "Pink",
            "Royal Blue",
            "White Smoke",
        ]
        self.val_color = StringVar()
        self.val_color.set(self.colors[0])
        self.cmb_color = ttk.Combobox(
            self.frm_create,
            textvariable=self.val_color,
            values=self.colors,
            state="readonly",
            width=13,
        )
        self.cmb_color.grid(row=1, column=6, padx=10)
        self.cmb_color.bind("<<ComboboxSelected>>", lambda e: self.color_selection(e))
        ttk.Style().configure("TCombobox", relief=FLAT)

        self.btn_create = Button(
            self.frm_create,
            text="+",
            width=5,
            relief=FLAT,
            activebackground="Dark Orange",
            activeforeground="White Smoke",
            bg="White Smoke",
            fg="Orange",
            borderwidth=0,
            command=self.create_todo,
        )
        self.btn_create.grid(row=1, column=7, padx=10)

        self.btn_edit = Button(
            self.frm_create,
            text="Edit",
            width=5,
            relief=FLAT,
            activebackground="Dark Orange",
            activeforeground="White Smoke",
            fg="Orange",
            bg="White Smoke",
            borderwidth=0,
        )

        ######################################################################
        #                              Canvas                                #
        ######################################################################
        self.frm_canvas = Frame(container)
        self.frm_canvas.pack(fill=BOTH, expand=True)

        self.todo_canvas = Canvas(self.frm_canvas, width=1300, height=737, bg="Indigo")
        self.todo_canvas.grid(row=0, column=0, padx=0, pady=0)
        self.todo_canvas.bind(
            "<Enter>", lambda event: self._bound_to_mousewheel(event, self.todo_canvas)
        )
        self.todo_canvas.bind(
            "<Leave>",
            lambda event: self._unbound_to_mousewheel(event, self.todo_canvas),
        )

        self.scroll_canvas = Scrollbar(
            self.frm_canvas, orient=VERTICAL, command=self.todo_canvas.yview
        )
        self.scroll_canvas.grid(row=0, column=1, sticky=N + S)

        self.todo_canvas.configure(yscrollcommand=self.scroll_canvas.set)

        self.after_id = ""
        self.reset_form()
        self.show_in_canvas()

    def clear_canvas(self):
        """Clear the canvas and reset the coordinates before showing all the
        todos stored in the DB.
        """
        self.todo_canvas.delete("all")
        ToDoListApp.x0 = 50
        ToDoListApp.y0 = 50
        ToDoListApp.x1 = 250
        ToDoListApp.y1 = 250

    def color_selection(self, event):
        """Change the background colors of the creation/edition frame and of its
        children on color combobox selection change.
        """
        self.frm_create.configure(bg=self.val_color.get())  # Frame

        for child in self.frm_create.winfo_children():  # Labels
            if isinstance(child, Label):
                child["bg"] = self.val_color.get()

    def create_todo(self):
        """Call the create() method from the ToDo module, reset the form, and
        show the todos in the canvas.
        """
        _date = self._set_timestamp()
        text = self.val_todo.get()
        color = self.val_color.get()

        create = ToDo().create(
            _date,
            text,
            color,
            self.ent_todo,
        )

        if create:
            self.reset_form()

        self.todo_canvas.after_cancel(self.after_id)

        self.show_in_canvas()

    def delete_todo(self, id):
        """Call the delete() method from the ToDo module, reset the form, and
        show the todos in the canvas.
        """
        self.reset_form()
        ToDo().delete(id)

        self.todo_canvas.after_cancel(self.after_id)

        self.show_in_canvas()

    def edit_todo(self, todo):
        """Load the form with the data from the selected todo, show the Edit
        button in the form.
        """
        self.val_todo.set(todo.text)
        self.ent_todo.focus()
        self._on_key_press("")

        _date = self._datetime_to_str(todo.date).split(" ")
        self.val_date.set(_date[0])

        time = _date[1].split(":")

        hour = time[0]
        self.val_hour.set(hour)

        minutes = time[1]
        self.val_minutes.set(minutes)

        if todo.color == "Grey":
            self.val_color.set(self.colors[0])
        else:
            self.val_color.set(todo.color)
        self.color_selection("")

        self.btn_create.grid_forget()

        self.btn_edit.grid(row=1, column=7, padx=10)
        self.btn_edit.configure(command=lambda: self._on_edit_btn_click(todo.id))

    def grey_out_past_todos(self):
        """Delete from the DB all the todos dated before the present day"""
        todos = DB.ToDo().select()
        for todo in todos:
            today = datetime.now()

            if todo.date < today:
                ToDo().update(
                    todo.id, todo.date, todo.text, "Grey", self.ent_todo, True
                )

    def reset_form(self):
        """Clear the todo entry and set the focus on it, set the date to present
        date, set the color to the first one in the combobox, hide the Edit
        button, reset the character counter label.
        """
        self.frm_create.configure(bg=self.val_color.get())

        self.val_todo.set("")
        self._on_key_press("")
        self.ent_todo.focus_set()

        self.val_color.set(self.colors[0])
        self.color_selection("")

        today = datetime.strftime(datetime.today().date(), "%d/%m/%Y")
        self.val_date.set(today)

        self.val_hour.set("00")
        self.val_minutes.set("00")

        self.btn_edit.grid_forget()
        self.btn_create.grid(row=1, column=7, padx=10)

        self.lbl_char_count["text"] = "150 characters left"

    def show_in_canvas(self):
        """Clear the canvas and set all the todos stored in the DB. For each
        todo insert a square of 200x200, and within it a black rectangle and
        a white text element to show the todo date on the top; on the bottom,
        insert one black rectangle with the 'Edit' text in white, and a dark
        red rectangle with the text 'Delete' also in white, both half the
        width of the main square's width. Set the tags for the Edit and
        Delete buttons of each todo to permit their corresponding actions
        when they are clicked.

        Within the method there is a call to the canvas' method after() to
        call recursively the method show_in_canvas() every one second. This
        allows to keep the todo list up to date on the canvas. When a todo
        is old, it colors itself in grey. This happens in real time thanks
        to the recursion.

        Insert five todos per line. The scrollbar adapts to the increment or
        decrement of todos.
        """
        self.grey_out_past_todos()
        self.clear_canvas()

        eval_edit = lambda todo: (lambda p: self.edit_todo(todo))
        eval_delete = lambda id: (lambda p: self.delete_todo(id))

        # todos = DB.DataBase().read_table()
        todos = DB.DataBase().sort_records()
        for todo in todos:
            _date = datetime.strftime(todo.date, "%d/%m/%Y  -  %H:%M")

            # Main square - Contains the date header, the todo text, and the
            # Edit and Delete buttons.
            self.todo_canvas.create_rectangle(
                self.x0,
                self.y0,
                self.x1,
                self.y1,
                fill=todo.color,
            )

            # Date header
            self.todo_canvas.create_rectangle(
                self.x0,
                self.y0,
                self.x0 + 200,
                self.y0 + 20,
                fill="Black" if todo.color != "Grey" else "Grey",
            )

            self.todo_canvas.create_text(
                self.x0 + 100,
                self.y0 + 10,
                text=_date if todo.color != "Grey" else "Expired",
                fill="White Smoke" if todo.color != "Grey" else "Black",
                width=200,
            )

            # Todo text
            self.todo_canvas.create_text(
                self.x0 + 100, self.y0 + 100, text=todo.text, fill="Black", width=180
            )

            # Edit button
            self.todo_canvas.create_rectangle(
                self.x0,
                self.y0 + 180,
                self.x1 - 100,
                self.y1,
                fill="Dark Blue",
                tags=("edit_btn%s" % (todo.id)),
            )

            self.todo_canvas.create_text(
                self.x0 + 50,
                self.y0 + 190,
                text="Edit",
                fill="White Smoke",
                width=90,
                tags=("edit_btn%s" % (todo.id)),
            )

            # Delete button
            self.todo_canvas.create_rectangle(
                self.x0 + 100,
                self.y0 + 180,
                self.x1,
                self.y1,
                fill="Dark Red",
                tags=("delete_btn%s" % (todo.id)),
            )

            self.todo_canvas.create_text(
                self.x0 + 150,
                self.y0 + 190,
                text="Delete",
                fill="White Smoke",
                width=90,
                tags=("delete_btn%s" % (todo.id)),
            )

            self.todo_canvas.tag_bind(
                "edit_btn%s" % (todo.id), "<Button-1>", eval_edit(todo)
            )

            self.todo_canvas.tag_bind(
                "delete_btn%s" % (todo.id), "<Button-1>", eval_delete(todo.id)
            )

            ToDoListApp.x0 += 250
            ToDoListApp.x1 += 250
            self._set_coords()

        self.todo_canvas.configure(
            scrollregion=(
                0,
                1,
                0,
                ((ToDoListApp.y1 + 50) if (ToDoListApp.y1 >= 750) else 738),
            )
        )
        self.after_id = self.todo_canvas.after(1000, self.show_in_canvas)

    def _bound_to_mousewheel(self, event, canvas):
        """Bind widgets to the mousewheel"""
        # On Linux
        canvas.bind_all(
            "<Button-4>", lambda event: self._on_mousewheel_down(event, canvas)
        )
        canvas.bind_all(
            "<Button-5>", lambda event: self._on_mousewheel_up(event, canvas)
        )

        # On Windows
        canvas.bind_all(
            "<MouseWheel>", lambda event: self._on_mousewheel_up(event, canvas)
        )

    def _datetime_to_str(self, datetime_obj):
        """Convert datetime object to string"""
        return datetime.strftime(datetime_obj, "%d/%m/%Y %H:%M:%S")

    def _change_entry_color(self, count):
        """Change the text entry color depending on the text extension"""
        if count <= 10:
            self.ent_todo["fg"] = "Red"
        else:
            self.ent_todo["fg"] = "Black"

    def _count_chars(self, count):
        """Update the characters left in the text entry and show the message
        in the label below the entry.
        """
        self.lbl_char_count["text"] = "%s characters left" % (count)

    def _on_edit_btn_click(self, id):
        """Call the update() method from the ToDo module, reset the form, and
        show the todos in the canvas. Store the update() method return in a
        variable (a boolean value). If it is True, the form will be reset.
        Show in the canvas all the todos stored in the DB.
        """
        _date = self._set_timestamp()
        text = self.val_todo.get()
        color = self.val_color.get()

        update = ToDo().update(id, _date, text, color, self.ent_todo)

        if update:
            self.reset_form()

        self.todo_canvas.after_cancel(self.after_id)

        self.show_in_canvas()

    def _on_key_press(self, event):
        """The character limit for the todos is 150, so the color of the entry
        will change to red when the limit is about to be reached. Count the
        remaining space for the todo. When the limit is reached, prevent from
        inserting more than 150 characters.
        """
        count = 150 - len(self.val_todo.get())
        if count < 0:
            count = 0

        self._count_chars(count)
        self._change_entry_color(count)
        self._set_char_limit(self.val_todo, 150)

    def _on_mousewheel_down(self, event, canvas):
        """Mousewheel scrolling down"""
        canvas.yview_scroll(-1, "units")

    def _on_mousewheel_up(self, event, canvas):
        """Mousewheel scrolling up"""
        canvas.yview_scroll(1, "units")

    def _prevent_wrong_type(self, event, value):
        """Prevent entering a wrong type of character"""
        for char in value.get():
            if ord(char) < 48 or ord(char) > 57:
                value.set(value.get().replace(char, ""))

    def _set_char_limit(self, value, limit):
        """The user cannot write more than 150 characters in the text entry"""
        value.set(value.get()[:limit])

    def _set_coords(self):
        """Reset the canvas coordinates when reaching the top of todos per
        line.
        """
        if ToDoListApp.x0 == 1300 and ToDoListApp.x1 == 1500:
            ToDoListApp.x0 = 50
            ToDoListApp.x1 = 250
            ToDoListApp.y0 += 250
            ToDoListApp.y1 += 250

    def _set_max_value(self, event, value, max_value):
        """Set max values"""
        self._prevent_wrong_type(event, value)

        if value.get():
            if int(value.get()) > max_value:
                value.set(str(max_value))

    def _set_timestamp(self):
        """Set the full date"""
        date_str = "%s %s:%s:00" % (
            self.val_date.get(),
            self.val_hour.get(),
            self.val_minutes.get(),
        )

        _date = self._str_to_datetime(date_str)

        return _date

    def _str_to_datetime(self, string):
        """Convert string to datetime object"""
        return datetime.strptime(string, "%d/%m/%Y %H:%M:%S")

    def _unbound_to_mousewheel(self, event, canvas):
        """Unbind widgets from the mousewheel"""
        # On Linux
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

        # On Windows
        canvas.unbind_all("<MouseWheel>")


def quit(root, canvas, id):
    """Prevent an error with the canvas' after() method when closing
    the program, destroy the window.
    """
    canvas.after_cancel(id)
    root.destroy()


def main():
    win = Tk()
    win.withdraw()

    # When opening the program it asks the user if it should show the main
    # window or the server socket (server mode).
    answer = askyesno("Server Mode", "Run in server mode?")

    win.destroy()

    if answer:
        server.run_server()
    else:
        root = Tk()
        app = ToDoListApp(root)
        root.protocol(
            "WM_DELETE_WINDOW", lambda: quit(root, app.todo_canvas, app.after_id)
        )
        root.mainloop()


if __name__ == "__main__":
    main()
