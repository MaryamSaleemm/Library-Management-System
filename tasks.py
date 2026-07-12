from celery_worker import celery

from datetime import date, timedelta
import os

LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "notifications.log")


@celery.task
def send_borrow_notification(
    username,
    book_title
):

    os.makedirs(LOG_FOLDER, exist_ok=True)

    due_date = date.today() + timedelta(days=14)

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        file.write("\n")
        file.write("=" * 60 + "\n")
        file.write("CELERY NOTIFICATION\n")
        file.write("=" * 60 + "\n")
        file.write(f"Member      : {username}\n")
        file.write(f"Book        : {book_title}\n")
        file.write(f"Borrow Date : {date.today()}\n")
        file.write(f"Due Date    : {due_date}\n")
        file.write("Status      : Borrowed Successfully\n")
        file.write("=" * 60 + "\n")