import datetime
import threading
import time
from data_base.db_utils.session import Session
from config.basic_config import settings
from datetime import timedelta
import schedule


time_out = timedelta(minutes=settings.game_settings.session_expires_in)
period_to_start_worker = settings.game_settings.start_expires_session_worker_period


def call_db():
    print(datetime.datetime.now(), 'expires session worker was called')
    Session.delete_sessions_older_than(time_out)


schedule.every(period_to_start_worker).seconds.do(call_db)


def run_pending_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


def expires_session_worker():
    schedule_thread = threading.Thread(target=run_pending_schedule)
    schedule_thread.start()
