from datetime import date, timedelta
import os


LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "notifications.log")


def send_borrow_notification(
    username: str,
    book_title: str
):

    os.makedirs(LOG_FOLDER, exist_ok=True)  # if no log folder this create the folder automatically otherwise if it exist_ok=True means "If the folder already exists, don't complain"

    due_date = date.today() + timedelta(days=14)

    with open(  # "with" is used so the py closes the file auto after finishing
        LOG_FILE,
        "a",  # a means append it keep old data and add new data at the end
        encoding="utf-8"  # allow writing unicode characters é 你
    ) as file:

        file.write("\n")
        file.write("LIBRARY NOTIFICATIONS\n")

        file.write(f"Member      : {username}\n")
        file.write(f"Book        : {book_title}\n")
        file.write(f"Borrow Date : {date.today()}\n")
        file.write(f"Due Date    : {due_date}\n")
        file.write("Status      : Borrowed Successfully\n")
        file.write("-" * 60 + "\n")