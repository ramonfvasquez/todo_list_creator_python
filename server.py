import db.data_base as DB
import socket
from tools.colors import Color


class ServerSocket:
    HOST = "127.0.0.1"
    PORT = 1111
    HEADER_SIZE = 10
    INFO_HEAD = f"{Color.BOLD}{Color.GREEN}| INFO |{Color.END}{Color.END} "
    ERROR_HEAD = f"{Color.BOLD}{Color.RED}| ERROR |{Color.END}{Color.END} "
    COMMAND_ERROR_MSG = f"\n{ERROR_HEAD}Command error! Please try again!\n"
    VALID_COMMANDS = [
        "close",
        "count",
        "end",
        "exit",
        "s",
        "search",
        "sort",
        "todo",
        "x",
    ]

    def __init__(self):
        self._app_header()
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.bind((ServerSocket.HOST, ServerSocket.PORT))
        self.my_socket.listen(5)

        self.client_socket, self.address = self.my_socket.accept()

        print(
            f"{Color.BOLD}Connected by:\nHOST:{Color.END} {Color.YELLOW}"
            + f"{self.address[0]}{Color.END}\n{Color.BOLD}PORT:{Color.END} "
            + f"{Color.PURPLE}{self.address[1]}{Color.END}"
        )

    def _app_header(self):
        """Server header"""
        print("• " * 38 + "•")
        print(f"•{' ':75}•")
        print(f"•{' ':26}{Color.BOLD}TODO LIST - SERVER MODE{Color.END}{' ':26}•")
        print(f"•{' ':75}•")
        print("• " * 38 + "•")
        print()

    def add_header(self, msg):
        """Add a header to the passed message"""
        return f"{len(msg):<{ServerSocket.HEADER_SIZE}}" + str(msg)

    def connection(self):
        """Receive the messages and parse them so as to determine which commands where
        sent by the client.
        """
        while True:
            msg = self.client_socket.recv(1024)

            self.parse_command(msg)

            if not msg:
                break

    def parse_command(self, command):
        """Split the message sent by the client, get the commands and the arguments."""
        _command = command.decode("utf-8")
        com = None
        args = None

        # The command todo [args] will be sent by the client as a message with ';',
        # while every other command will have white spaces as separators.
        if _command[0:4] == "todo":
            com, *args = _command.split(";")
        else:
            com, *args = _command.split(" ")

        try:
            if len(com) > 0 and com in ServerSocket.VALID_COMMANDS:
                msg = ""

                # Close connection and server
                if com in ["close", "end", "exit", "x"]:
                    msg = self.command_close()

                # Return todo count
                elif com == "count":
                    msg = self.command_count()

                # Search todos by text
                elif com in ["s", "search"]:
                    msg = self.command_search(args if args else None)

                # Return sorted todos by arguments
                elif com == "sort":
                    msg = self.command_sort(args if args else None)

                # Create, delete, update todo
                elif com == "todo":
                    msg = self.command_todo(args if args else None)
                else:
                    msg = ServerSocket.COMMAND_ERROR_MSG
            else:
                msg = ServerSocket.COMMAND_ERROR_MSG
        except:
            msg = ServerSocket.COMMAND_ERROR_MSG

        self.client_socket.send(bytes(self.add_header(msg), "utf-8"))
        msg = ""

    def command_close(self):
        """End the server session"""
        self.my_socket.close()
        exit()

    def command_count(self):
        """Count the todos stored in the database"""
        todos = DB.DataBase().read_table()
        count = todos.count()

        if count > 0:
            if count > 1:
                msg = (
                    f"\n{Color.GREEN}{Color.BOLD}There are {str(count)} todos "
                    + f"in the database.{Color.END}{Color.END}\n"
                )
                return msg
            else:
                msg = (
                    f"{Color.GREEN}{Color.BOLD}There is 1 todo in the database."
                    + f"{Color.END}{Color.END}\n"
                )
                return msg
        else:
            return (
                f"\n{Color.BOLD}{Color.RED}The database is empty. No todos have "
                + f"been stored yet.{Color.END}{Color.END}\n"
            )

    def command_search(self, args=None):
        """Search todos by text"""
        msg = ""
        text = ""

        try:
            if args:
                # Join the arguments into a string
                text = " ".join([arg for arg in args if arg != ""])

            todos = DB.DataBase().get_records_by_text(text)

            for todo in todos:
                msg += f"[{todo.id}] {todo.text}\nDate: {todo.date}\n\n"

            return msg
        except:
            return ServerSocket.COMMAND_ERROR_MSG

    def command_sort(self, args=None):
        """Sort the todos by the argument passed. Optionally the user can
        include the 'desc' argument to sort the results downwards.
        """
        desc = False
        invalid_arg = False
        msg = ""
        valid_args = ["color", "date", "id", "text"]

        if args:
            # Remove the empty items of the args list
            args = [arg for arg in args if arg != ""]

            if len(args) < 3:
                # args cannot have more than two elements
                if not args[0] in valid_args:
                    invalid_arg = True

                # If args have two elements, check if the second one is 'desc'.
                if len(args) == 2:
                    if args[1] == "desc":
                        desc = True
                    else:
                        invalid_arg = True

                if not invalid_arg:
                    # Connect to the database if the arguments are valid
                    try:
                        todos = DB.DataBase().sort_records([args[0]], desc)
                        count = DB.DataBase().read_table().count()

                        order = "downwards" if desc else "upwards"

                        if count > 0:
                            msg = (
                                f"\n{Color.BOLD}{Color.GREEN}{str(count)} todos "
                                + f"sorted {order} by {args[0]}.{Color.END}"
                                + f"{Color.END}\n\n"
                            )
                        else:
                            msg = (
                                f"\n{Color.BOLD}{Color.RED}The database is empty. "
                                + f"No todos have been stored yet.{Color.END}"
                                + f"{Color.END}\n"
                            )

                        for todo in todos:
                            date = "Date: " + (
                                str(todo.date) if todo.color != "Grey" else "Expired"
                            )
                            color = (
                                ("Color: " + todo.color + "\n")
                                if todo.color != "Grey"
                                else ""
                            )

                            msg += f"[{todo.id}] {todo.text}\n{date}\n{color}\n"

                        return msg
                    except:
                        return f"\n{ServerSocket.ERROR_HEAD}An error occurred while trying to sort the todos.\n"
                else:
                    return f"\n{ServerSocket.ERROR_HEAD}The arguments are invalid.\n"
            else:
                return f"\n{ServerSocket.ERROR_HEAD}sort accepts one or two arguments, but {len(args)} were given.\n"
        else:
            return f"\n{ServerSocket.ERROR_HEAD}Arguments required: color, date, id or text. Optional: desc.\n"

    def command_todo(self, args=None):
        """Connect to the database depending on the argument included with the
        todo command.
        """
        if args:
            # Delete
            if args[0] == "delete":
                id = args[1]

                try:
                    todo = DB.DataBase().get_record_by_id(id)

                    if todo:
                        DB.DataBase().delete(id)

                        return f"\n{ServerSocket.INFO_HEAD}The todo has been deleted.\n"
                except:
                    return f"\n{ServerSocket.ERROR_HEAD}An error occurred while trying to delete the todo!\n"

            # Create
            elif args[0] == "save":
                todo_text, todo_date, todo_color = args[1:]

                try:
                    DB.DataBase().insert(todo_date, todo_text, todo_color)

                    return f"\n{ServerSocket.INFO_HEAD}The todo has been saved into de database!\n"
                except:
                    return f"\n{ServerSocket.ERROR_HEAD}An error occurred while trying to save the todo!\n"

            # Update
            elif args[0] == "edit":
                todo_id, todo_text, todo_date, todo_color = args[1:]

                try:
                    todo = DB.DataBase().get_record_by_id(todo_id)

                    if todo:
                        DB.DataBase().update(todo_id, todo_date, todo_text, todo_color)

                    return f"\n{ServerSocket.INFO_HEAD}The todo has been updated!\n"
                except:
                    return f"\n{ServerSocket.ERROR_HEAD}An error occurred while trying to edit the todo!\n"
        else:
            return f"\n{ServerSocket.ERROR_HEAD}Arguments required: del/delete, edit or save.\n"


def run_server():
    ServerSocket().connection()


if __name__ == "__main__":
    run_server()
