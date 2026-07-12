from celery import Celery
from datetime import date
from pathlib import Path
import os


# CELERY CONFIGURATION

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

celery = Celery(
    "library",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
)

# BORROW NOTIFICATION TASK

@celery.task(name="tasks.send_borrow_notification")
def send_borrow_notification(username: str, book_title: str):

    try:

        # Make sure logs directory exists
        log_directory = Path("/app/logs")
        log_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        log_file = log_directory / "notifications.log"


        message = f"""
        
CELERY NOTIFICATION

Member      : {username}
Book        : {book_title}
Borrow Date : {date.today()}
Status      : Borrowed Successfully



"""


        # Append notification
        with open(log_file, "a") as file:
            file.write(message)


        print(
            f"Notification logged for {username}"
        )


        return {
            "status": "success",
            "message": "Notification logged successfully"
        }


    except Exception as e:

        print(
            f"Notification error: {str(e)}"
        )

        raise e