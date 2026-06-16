import logging
import copy
from django.utils.log import AdminEmailHandler

class DebugInfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.DEBUG, logging.INFO)

class WarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.WARNING

class ErrorCriticalFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.ERROR, logging.CRITICAL)

class ExcInfoFormatter(logging.Formatter):
    def format(self, record):
        # To avoid mutating the original record and messing up other handlers, we copy it
        record_copy = copy.copy(record)
        if record_copy.exc_info:
            record_copy.exc_info_str = self.formatException(record_copy.exc_info)
            # prevent standard formatter from appending it again at the end
            record_copy.exc_info = None
            record_copy.exc_text = None
        else:
            record_copy.exc_info_str = ""

        return super().format(record_copy)

class CustomAdminEmailHandler(AdminEmailHandler):
    def emit(self, record):
        try:
            request = record.request
            subject = '%s (%s IP): %s' % (
                record.levelname,
                ('internal' if request.META.get('REMOTE_ADDR') in getattr(self, 'settings', None) and self.settings.INTERNAL_IPS
                 else 'EXTERNAL'),
                record.getMessage()
            )
        except Exception:
            subject = '%s: %s' % (
                record.levelname,
                record.getMessage()
            )
            request = None
        subject = self.format_subject(subject)

        # Clone the record to avoid mutating shared state
        new_record = copy.copy(record)
        new_record.exc_info = None
        new_record.exc_text = None

        # Use our own formatter to get just the string we want
        message = self.format(new_record)

        self.send_mail(subject, message, fail_silently=True, html_message=None)
