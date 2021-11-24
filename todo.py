import db.data_base as DB
from tools.colors import Color
from datetime import datetime
from tkinter.messagebox import askyesno, showwarning
from tools.colors import Color
from tools.validation import is_valid_date


class ToDo:
    def count_chars(self, count):
        """Count the caracters inserted"""
        count -= 1
        return count

    def create(self, date, text, color, widget):
        """Create a todo"""
        if is_valid_date(date):
            if text:
                DB.DataBase().insert(date, text, color)
            else:
                widget.focus_set()
                showwarning("Empty ToDo", "You can't create an empty todo!")
                return False
        else:
            widget.focus_set()
            showwarning("Invalid Date", "Please enter a valid date!")
            return False

        return True

    def delete(self, id):
        """Delete a todo"""
        answer = ""
        answer = askyesno("Delete ToDo", "Are you sure you want to delete this todo?")

        if answer:
            DB.DataBase().delete(id)

    def set_color(self):
        """Show an input for the color when working on the console"""
        count = 0
        colors = [
            "Coral",
            "Crimson",
            "Green",
            "Light Blue",
            "Orange",
            "Pink",
            "Royal Blue",
            "White Smoke",
        ]

        print(
            f"\n{Color.BOLD}COLORS:{Color.END} {Color.CORAL}coral{Color.END} "
            + f"(default), {Color.CRIMSON}crimson{Color.END}, {Color.GREEN}green"
            + f"{Color.END}, {Color.LIGHT_BLUE}light blue{Color.END}, {Color.ORANGE}"
            + f"orange{Color.END}, {Color.PINK}pink{Color.END}, {Color.ROYAL_BLUE}"
            + f"royal blue{Color.END}, white smoke."
        )

        while True:
            try:
                todo_color = input(
                    ("\n" if count > 0 else "")
                    + f"{Color.BOLD}{Color.PURPLE}Color:{Color.END}{Color.END} "
                )

                count += 1

                if (
                    todo_color.upper() in [col.upper() for col in colors]
                    or todo_color == ""
                ):
                    break
                else:
                    raise ValueError
            except ValueError:
                print(
                    "Please enter a valid color name or left blank for the default color."
                )
                continue

        return todo_color if todo_color != "" else "Coral"

    def set_date(self):
        """Show different inputs for the date (year, month, day, hour, and minutes)
        when working on the console.
        """
        print("\nSet the date and time for the todo:")
        count = -1

        # Year
        while True:
            try:
                count += 1

                year = int(
                    input(
                        ("\n" if count > 0 else "")
                        + f"{Color.BOLD}{Color.PURPLE}Year [YY]:{Color.END}{Color.END} "
                    )
                )

                if year < 21 or year > 50:
                    raise ValueError
                else:
                    break
            except ValueError:
                print(
                    f"Please enter a value between {datetime.now().year-2000} and 50."
                )
                continue

        # Month
        while True:
            try:
                month = int(
                    input(f"\n{Color.BOLD}{Color.PURPLE}Month:{Color.END}{Color.END} ")
                )
                if month < 1 or month > 12:
                    raise ValueError
            except ValueError:
                print("Please enter a value between 1 and 12.")
                continue
            else:
                break

        # Day
        while True:
            try:
                day = int(
                    input(f"\n{Color.BOLD}{Color.PURPLE}Day:{Color.END}{Color.END} ")
                )
                if day >= 1 and day <= 31:
                    if month in [1, 3, 5, 7, 8, 10, 12]:
                        break
                    elif month in [4, 6, 9, 11]:
                        if day > 30:
                            raise ValueError
                        else:
                            break
                    elif month == 2:
                        if day > 28:
                            raise ValueError
                        else:
                            break
                else:
                    raise ValueError
            except ValueError:
                _max = 31
                if month in [4, 6, 9, 11]:
                    _max = 30
                elif month == 2:
                    _max = 28

                print(f"Please enter a value between 1 and {_max}.")
                continue

        # Hour
        while True:
            try:
                hour = int(
                    input(f"\n{Color.BOLD}{Color.PURPLE}Hour:{Color.END}{Color.END} ")
                )
                if hour < 0 or hour > 23:
                    raise ValueError
            except ValueError:
                print("Please enter a value between 0 and 23.")
                continue
            else:
                break

        # Minutes
        while True:
            try:
                minutes = int(
                    input(
                        f"\n{Color.BOLD}{Color.PURPLE}Minutes:{Color.END}{Color.END} "
                    )
                )
                if minutes < 0 or minutes > 59:
                    raise ValueError
            except ValueError:
                print("Please enter a value between 0 and 59.")
                continue
            else:
                break

        # Parse the input values into a datetime object
        todo_date = datetime.strptime(
            f"{day:02}/{month:02}/{year} {hour:02}:{minutes:02}:00",
            "%d/%m/%y %H:%M:%S",
        )

        return todo_date

    def set_text(self):
        """Show an input for the text when working on the console"""
        count = -1

        while True:
            try:
                count += 1

                todo_text = input(
                    ("\n" if count > 0 else "")
                    + f"{Color.BOLD}{Color.PURPLE}Text [150 chars max]:{Color.END}{Color.END} "
                )

                if todo_text == "" or len(todo_text) > 150:
                    raise ValueError
                else:
                    break
            except ValueError:
                if todo_text == "":
                    print("The text can't be left empty!")
                elif len(todo_text) > 150:
                    print(
                        f"{Color.BOLD}{Color.RED}The text has more than 150 characters!{Color.END}{Color.END}"
                    )
                continue

        return todo_text

    def update(self, id, date, text, color, widget, outdated=False):
        """Update a todo"""
        if is_valid_date(date) or outdated:
            if text:
                DB.DataBase().update(id, date, text, color)
            else:
                widget.focus_set()
                showwarning("Empty ToDo", "You should insert some text to your todo!")
                return False
        else:
            widget.focus_set()
            showwarning("Invalid Date", "Please enter a valid date!")
            return False

        return True
