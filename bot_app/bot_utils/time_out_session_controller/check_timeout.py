import threading
import time
from data_base.session_operations import SessionOperations
from config.basic_config import settings
from datetime import timedelta
import schedule
from logger.logger import Level, log

time_out = timedelta(minutes=settings.game_settings.session_expires_in)
period_to_start_worker = settings.game_settings.start_expires_session_worker_period


def call_db():
    log.write(Level.INFO, 'Expired session worder was called')
    SessionOperations.delete_sessions_older_than(time_out)


schedule.every(period_to_start_worker).seconds.do(call_db)


def run_pending_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


def expires_session_worker():
    schedule_thread = threading.Thread(target=run_pending_schedule)
    schedule_thread.start()
