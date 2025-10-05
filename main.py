from app.app import app
import os

# from app.utils.celery_worker import celery_init_app
# from app.utils import task
# from celery.schedules import crontab, timedelta

# celery_app = celery_init_app(app)

# @celery_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Run monthly activity report every minute
#     # sender.add_periodic_task(crontab(minute='*', hour='*'), task.monthly_activity_report.s())
#     # Run daily reminders every 5 seconds
#     sender.add_periodic_task(timedelta(seconds=5), task.daily_reminders.s())
    # Run store manager report every minute
    # sender.add_periodic_task(crontab(minute='*', hour='*'), task.store_manager_report.s())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
