from tkinter import Tk
from todo_list_app import ToDoListApp


class App:
    def __init__(self, root):
        self.root = root
        ToDoListApp(root)


def main():
    root = Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
