from django.utils.log import AdminEmailHandler
from django.views.debug import ExceptionReporter


class CustomAdminEmailHandler(AdminEmailHandler):
    def emit(self, record):
        try:
            request = record.request
            subject = self.format_subject(record.getMessage())
            try:
                request_repr = repr(request)
            except Exception:
                request_repr = "Request repr() unavailable"

            if record.exc_info:
                exc_info = record.exc_info
                reporter = ExceptionReporter(request, is_email=True, *exc_info)
                html_message = reporter.get_traceback_html()
            else:
                html_message = "%s\n\n%s" % (self.format(record), request_repr)

            self.send_mail(subject, html_message, fail_silently=True, html_message=html_message)
        except Exception:
            self.handleError(record)
