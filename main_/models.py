import binascii
import os
import re

from django.db import models
from django.utils.html import escape


def custom_upload_to(instance, filename):
    # Generate a new filename using a custom logic
    new_filename = f"{binascii.hexlify(os.urandom(5)).decode()}_{filename}"

    # Return the new filename
    return os.path.join('uploads', new_filename)


class Model(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if hasattr(self, "message"):
            self.message = escape(self.message)
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     # إنشاء سجل تاريخي جديد وحفظه في جدول السجلات التاريخية
    #     history_record = self.history.model(self.id,history_change_reason='Saved new record',)
    #     history_record.save()
    #     super().__class__.save(*args, **kwargs)


def remove_html_tags(text):
    clean = re.sub(r'<[^>]*>', '', text)
    return clean
