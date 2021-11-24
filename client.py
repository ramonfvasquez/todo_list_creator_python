"""
###################################################################################
##################################   COMMANDS   ###################################
###################################################################################

###################################### TODOS ######################################

...................................................................................
count
...................................................................................
Get the number of todos stored in the database.


...................................................................................
s / search [text to search]
...................................................................................
Search todos by text. If no argument is entered, all todos will be displayed.


...................................................................................
sort [color / date / id / text] [desc]
...................................................................................
Get all the todos sorted by the argument entered.
Optional: enter 'desc' to sort downwards.


...................................................................................
todo [del / delete / edit / save]
...................................................................................
Open the todo editor.
Enter 'del' or 'delete' to remove a todo by its ID number.
Enter 'edit' to update a todo by its ID number.
Enter 'save' to create a new todo.



##################################### CONSOLE #####################################

...................................................................................
clear
...................................................................................
Clear the screen.


...................................................................................
clh
...................................................................................
Clear the command history.


...................................................................................
close / end / exit / x
...................................................................................
Exit client and shut down the server.


...................................................................................
commands
...................................................................................
Clear the screen and print the command list.


...................................................................................
h
...................................................................................
Command history.



*If no command is entered or the command is invalid, the client will continue to
ask for a command until the session is ended by the user.
"""

import socket
from os import name, system
from termcolor import colored
from todo import ToDo
from tools.colors import Color


class ClientSocket:
    BUFFER_SIZE = 1024
    HEADER_SIZE = 10
    HISTORY = []
    HOST = "127.0.0.1"
    PORT = 1111

    def __init__(self):
        self._app_header()
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.connect((ClientSocket.HOST, ClientSocket.PORT))

    def _app_header(self):
        """Client header.
        Displays all the commands available with some details about their use.
        """
        # HEADER
        print("• " * 38 + "•")
        print(f"•{' ':75}•")
        print(f"•{' ':33}{Color.BOLD}COMMANDS{Color.END}{' ':34}•")
        print(f"•{' ':75}•")
        print("• " * 38 + "•")
        print(f"•{' ':75}•")

        # TODO_LIST
        print(
            f"{'• '}{Color.BOLD}{colored('TODO LIST', 'white', 'on_red'):88}{Color.END}•"
        )
        print(f"{'•  |-'}{Color.BOLD}{Color.RED}{'count':71}{Color.END}{Color.END}•")
        print(f"{'•  | |-Get the number of todos stored in the database.':76}•")
        print(f"{'•  |':76}•")
        print(
            f"{'•  |-'}{Color.BOLD}{Color.RED}{'s / search [text to search]':71}{Color.END}{Color.END}•"
        )
        print(
            f"{'•  | |-Search todos by text. If no argument is entered, all todos will':76}•"
        )
        print(f"{'•  | | be displayed.':76}•")
        print(f"{'•  |':76}•")
        print(
            f"{'•  |-'}{Color.BOLD}{Color.RED}{'sort [color / date / id / text] [desc]':71}{Color.END}{Color.END}•"
        )
        print(f"{'•  | |-Get all the todos sorted by the argument entered.':76}•")
        print(f"{'•  | |-Optional: enter ':23}'desc'{' to sort downwards.':47}•")
        print(f"{'•  |':76}•")
        print(
            f"{'•  |-'}{Color.BOLD}{Color.RED}{'todo [del / delete / edit / save]':71}{Color.END}{Color.END}•"
        )
        print(f"{'•    |-Open the todo editor.':76}•")
        print(
            f"{'•    |-Enter ':13}'del'{' or ':4}'delete'{' to remove a todo by its ID number.':46}•"
        )
        print(f"{'•    |-Enter ':13}'edit'{' to update a todo by its ID number.':57}•")
        print(f"{'•    |-Enter ':13}'save'{' to create a new todo.':57}•")
        print(f"{'•':76}•")
        print(f"{'•':76}•")

        # CONSOLE
        print(
            f"{'• ':2}{Color.BOLD}{colored('CONSOLE','white','on_green'):88}{Color.END}•"
        )
        print(f"{'•  |-'}{Color.BOLD}{Color.GREEN}{'clear':71}{Color.END}{Color.END}•")
        print(f"{'•  | |-Clear the screen.':76}•")
        print(f"{'•  |':76}•")
        print(f"{'•  |-'}{Color.BOLD}{Color.GREEN}{'clh':71}{Color.END}{Color.END}•")
        print(f"{'•  | |-Clear command history.':76}•")
        print(f"{'•  |':76}•")
        print(
            f"{'•  |-'}{Color.BOLD}{Color.GREEN}{'close / end / exit / x':71}{Color.END}{Color.END}•"
        )
        print(f"{'•  | |-Exit client and shut down the server.':76}•")
        print(f"{'•  |':76}•")
        print(
            f"{'•  |-'}{Color.BOLD}{Color.GREEN}{'commands':71}{Color.END}{Color.END}•"
        )
        print(f"{'•  | |-Clear the screen and print the command list.':76}•")
        print(f"{'•  |':76}•")
        print(f"{'•  |-'}{Color.BOLD}{Color.GREEN}{'h':71}{Color.END}{Color.END}•")
        print(f"{'•    |-Command history.':76}•")
        print(f"{'•':76}•")
        print("• " * 38 + "•\n")

    def _todo_editor_header(self, title):
        """ToDo editor header"""
        print("\n" + "• " * 38 + "•")
        print(f"•{' ':75}•")
        print(
            f"•{' ':26}{Color.BOLD}TODO EDITOR - {Color.PURPLE}{title:35}{Color.END}{Color.END}•"
        )
        print(f"•{' ':75}•")
        print("• " * 38 + "•\n")

    def connection(self):
        """Send and receive messages to and from the server.
        Set conditions depending on which commands are entered into the command prompt.
        Some commands are sent to the server so as to receive certain responses, and
        others are used on the client's side.
        """
        command = ""
        if not command:
            while True:
                full_msg = ""
                new_msg = True
                if full_msg == "":
                    command = input(
                        f"{Color.BOLD}{Color.BLUE}command{Color.END}{Color.END}$ "
                    )

                    if not command:
                        command = " "
                        continue

                    # Save the command history chronologically with no repeated commands
                    else:
                        if command in ClientSocket.HISTORY:
                            for index, com in enumerate(ClientSocket.HISTORY):
                                if com == command:
                                    ClientSocket.HISTORY.pop(index)

                        if command != "h":
                            ClientSocket.HISTORY.append(command)

                    # Clear the screen
                    if command == "clear":
                        self.clear_screen()
                        command = ""
                        continue

                    # Clear the command history
                    elif command == "clh":
                        ClientSocket.HISTORY = []
                        command = ""
                        continue

                    # Close connection and server
                    elif command in ["close", "end", "exit", "x"]:
                        break

                    # Show the list of available commands
                    elif command == "commands":
                        self.clear_screen()
                        self._app_header()
                        continue

                    # Show the command history
                    elif command == "h":
                        print(
                            f"\n{Color.BOLD}{Color.CYAN}HISTORY:{Color.END}{Color.END}",
                            (", ").join(ClientSocket.HISTORY),
                            end="\n\n",
                        )
                        command = ""
                        continue

                    # Search todos by text
                    elif command.split(" ")[0] in ["s", "search"]:
                        args = (
                            " ".join(command.split(" ")[1:])
                            if len(command.split(" ")) > 1
                            else ""
                        )

                        print(
                            f"\n{Color.BOLD}{Color.GREEN}Results for {Color.END}{Color.END}'{args}'\n"
                            if args
                            else f"\n{Color.BOLD}{Color.YELLOW}Showing all todos{Color.END}{Color.END}\n"
                        )

                    # Open the todo editor
                    elif command.split(" ")[0] == "todo":
                        arg = (
                            command.split(" ")[1]
                            if len(command.split(" ")) == 2
                            else ""
                        )
                        header = "todo"

                        if arg:
                            try:
                                # If the first argument is save, enable the creation form
                                if arg == "save":
                                    self._todo_editor_header("CREATE")

                                    (
                                        todo_text,
                                        todo_date,
                                        todo_color,
                                    ) = Form().creation_form()
                                    command = f"{header};save;{todo_text};{todo_date};{todo_color.capitalize()}"

                                # If the first argument is del or delete, enable the deletion form
                                elif arg in ["del", "delete"]:
                                    self._todo_editor_header("DELETE")

                                    todo_id = Form().deletion_form()
                                    command = f"{'todo'};delete;{todo_id}"

                                # If the first argument is edit, enable the edition form
                                elif arg == "edit":
                                    self._todo_editor_header("EDIT")

                                    (
                                        todo_id,
                                        todo_text,
                                        todo_date,
                                        todo_color,
                                    ) = Form().edition_form()
                                    command = f"{header};edit;{todo_id};{todo_text};{todo_date};{todo_color.capitalize()}"
                            except:
                                continue
                        else:
                            command = header

                    # Send the command entered to the server
                    self.my_socket.sendall(bytes(command, "utf-8"))

                # Read and display the response from the server
                while True:
                    msg = self.my_socket.recv(ClientSocket.BUFFER_SIZE)

                    if new_msg:
                        msglen = int(msg[: ClientSocket.HEADER_SIZE])
                        new_msg = False

                    full_msg += msg.decode("utf-8")

                    if len(full_msg) - ClientSocket.HEADER_SIZE == msglen:
                        print(full_msg[ClientSocket.HEADER_SIZE :])
                        new_msg = True
                        break

                full_msg = ""
                continue

    def clear_screen(self):
        """Clear the screen"""

        # On Windows
        if name == "nt":
            _ = system("cls")
        else:
            # On Linux/Mac
            _ = system("clear")


class Form:
    def creation_form(self):
        """ToDo creatinon form."""
        todo_text = ToDo().set_text()
        todo_date = ToDo().set_date()
        todo_color = ToDo().set_color()

        return (todo_text, todo_date, todo_color)

    def deletion_form(self):
        """ToDo deletion form"""
        count = -1

        while True:
            try:
                count += 1

                todo_id = int(
                    input(
                        ("\n" if count > 0 else "")
                        + f"{Color.BOLD}{Color.PURPLE}ToDo ID N°:{Color.END}{Color.END} "
                    )
                )
            except ValueError:
                print("Please enter a valid ID number!")
                continue
            else:
                break

        return todo_id

    def edition_form(self):
        """ToDo edition form"""
        count = -1

        while True:
            try:
                count += 1

                todo_id = int(
                    input(
                        ("\n" if count > 0 else "")
                        + f"{Color.BOLD}{Color.PURPLE}ToDo ID N°:{Color.END}{Color.END} "
                    )
                )

            except ValueError:
                print("Please enter a valid ID number!")
                continue
            else:
                break

        todo_text, todo_date, todo_color = self.creation_form()

        return (todo_id, todo_text, todo_date, todo_color)


def run_client():
    ClientSocket().connection()


if __name__ == "__main__":
    run_client()
