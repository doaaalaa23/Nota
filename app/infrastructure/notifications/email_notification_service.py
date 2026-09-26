import os
import smtplib
from email.message import EmailMessage
from typing import List

from app.domain.models.notification_model import UserNotification


class EmailNotificationService:
    def __init__(self):
        self.host = os.getenv("SMTP_HOST")
        self.port = int(os.getenv("SMTP_PORT", "587"))
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")
        self.sender = os.getenv("SMTP_FROM", self.username or "")
        self.use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

    @property
    def is_configured(self) -> bool:
        return bool(self.host and self.username and self.password and self.sender)

    def send_due_installment_email(
        self,
        recipient: str,
        user_name: str,
        notifications: List[UserNotification],
    ) -> None:
        if not self.is_configured:
            raise RuntimeError(
                "SMTP is not configured. Set SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, and SMTP_FROM."
            )

        message = EmailMessage()
        message["Subject"] = "Installments due today"
        message["From"] = self.sender
        message["To"] = recipient
        rows = "\n".join(
            f"- {item.client_name}: installment {item.installment_number}, "
            f"amount {item.installment_amount:.2f} (contract {item.contract_id})"
            for item in notifications
        )
        message.set_content(
            f"Hello {user_name},\n\n"
            f"You have {len(notifications)} unpaid installment(s) due today:\n\n"
            f"{rows}\n\n"
            "Please open Nota to record the payment."
        )

        with smtplib.SMTP(self.host, self.port, timeout=30) as smtp:
            if self.use_tls:
                smtp.starttls()
            smtp.login(self.username, self.password)
            smtp.send_message(message)