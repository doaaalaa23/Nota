import logging
from datetime import date

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.infrastructure.repositories.notifi_user_impl import NotificationRepositoryImpl
from app.infrastructure.notifications.email_notification_service import (
    EmailNotificationService,
)
from app.infrastructure.database.session import get_session
from app.infrastructure.models.user_model import UserTable

logger = logging.getLogger(__name__)

# Fixed wall-clock time the job runs at every day (24h format, server timezone).
NOTIFICATION_HOUR = 8
NOTIFICATION_MINUTE = 0


def send_due_installment_emails() -> None:
    email_service = EmailNotificationService()
    if not email_service.is_configured:
        logger.warning("Daily installment emails skipped: SMTP is not configured")
        return

    db = get_session()
    try:
        users = db.query(UserTable).filter(UserTable.is_active.is_(True)).all()
        for user in users:
            repository = NotificationRepositoryImpl(db, user.user_id)
            notifications = repository.read_due_today(date.today())
            if not notifications:
                continue
            try:
                email_service.send_due_installment_email(
                    recipient=user.email,
                    user_name=user.user_name,
                    notifications=notifications,
                )
                logger.info("Sent installment email to %s", user.email)
            except Exception:
                logger.exception("Could not send installment email to %s", user.email)
    finally:
        db.close()


def start_notification_scheduler() -> AsyncIOScheduler:
    """
    Runs send_due_installment_emails once a day at a fixed time, instead of a
    sleep-based loop that drifts on every restart. `coalesce=True` collapses
    any missed runs (e.g. the process was down) into a single catch-up run
    rather than firing repeatedly; `misfire_grace_time` allows a late start
    within that window to still count as on-time.
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_due_installment_emails,
        trigger=CronTrigger(hour=NOTIFICATION_HOUR, minute=NOTIFICATION_MINUTE),
        id="daily_installment_emails",
        coalesce=True,
        misfire_grace_time=3600,
        max_instances=1,
    )
    scheduler.start()
    logger.info(
        "Installment notification scheduler started (daily at %02d:%02d)",
        NOTIFICATION_HOUR,
        NOTIFICATION_MINUTE,
    )
    return scheduler


def stop_notification_scheduler(scheduler: AsyncIOScheduler) -> None:
    scheduler.shutdown(wait=False)
    logger.info("Installment notification scheduler stopped")