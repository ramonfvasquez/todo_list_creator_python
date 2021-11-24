from datetime import datetime


def is_valid_date(date):
    today = datetime.today()
    last_date = datetime.strptime("31/12/2100 00:00:00", "%d/%m/%Y %H:%M:%S")

    if date < last_date:
        return date >= today
