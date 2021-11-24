"""Module for the creation of the database and CRUD.
It was built to work with the ORM Peewee.
"""

from peewee import CharField, DateTimeField, Model, SqliteDatabase, TextField
from tools.db_logging import log

db = SqliteDatabase("./db/todos.db")


class BaseModel(Model):
    class Meta:
        database = db


class ToDo(BaseModel):
    """ToDo database"""

    date = DateTimeField()
    text = TextField()
    color = CharField(20)


class DataBase:
    def connect(self):
        db.connect()

    def create_table(self):
        try:
            db.create_tables([ToDo])
        except:
            print("The table already exists")

    @log
    def delete(self, id):
        """Delete record"""
        try:
            delete = ToDo.get(ToDo.id == id)
            delete.delete_instance()

            return f"ToDo DELETED: id={id}"
        except:
            print(
                "Deletion Error", "An error occurred while trying to delete the todo."
            )

    def get_record_by_id(self, id):
        """Get a record by it ID number"""
        try:
            record = ToDo.get(ToDo.id == id)
        except:
            print("The record does not exist.")

        return record

    def get_records_by_text(self, text):
        """Get a record by its text"""
        uppercased = text.upper()

        all_records = self.read_table()
        results = []

        for record in all_records:
            if (
                uppercased
                in record.text.replace("á", "a")
                .replace("é", "e")
                .replace("í", "i")
                .replace("ó", "o")
                .replace("ú", "u")
                .upper()
            ):
                results.append(record)

        return results

    @log
    def insert(self, date, text, color):
        """Insert a record"""
        ToDo.create(date=date, text=text, color=color)

        return f"ToDo CREATED: text={text}; date={date}; color={color}"

    def read_table(self):
        return ToDo.select()

    def sort_records(self, column=["date", "text"], desc=False):
        """Sort record by the column argument passed"""
        sorting = {
            "id": ToDo.id,
            "date": ToDo.date,
            "text": ToDo.text,
            "color": ToDo.color,
        }

        return self.read_table().order_by(
            *[(sorting[col].desc() if desc else sorting[col]) for col in column]
        )

    @log
    def update(self, id, date, text, color):
        """Update a record"""
        update = ToDo.update(date=date, text=text, color=color).where(ToDo.id == id)
        update.execute()

        return f"ToDo UPDATED: id={id}; text={text}; date={date}; color={color}"
