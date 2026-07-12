from datetime import date
from pathlib import Path

from celery_worker import celery


LOG_DIRECTORY = Path("/app/logs")
LOG_FILE = LOG_DIRECTORY / "notifications.log"


@celery.task(name="tasks.send_borrow_notification")
def send_borrow_notification(username: str, book_title: str):
    """
    Background task that logs a borrow notification.
    """

    try:
        # Create logs directory if it doesn't exist
        LOG_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True
        )

        message = (
            f"\n"
            f"CELERY NOTIFICATION\n"
            f"Member      : {username}\n"
            f"Book        : {book_title}\n"
            f"Borrow Date : {date.today()}\n"
            f"Status      : Borrowed Successfully\n"
            f"{'-' * 60}\n"
        )

        # Append notification to log file
        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as file:
            file.write(message)

        print(
            f"Notification logged for {username}",
            flush=True
        )

        return {
            "status": "success",
            "message": "Notification logged successfully"
        }

    except Exception as e:
        print(
            f"Notification error: {e}",
            flush=True
        )
        raise