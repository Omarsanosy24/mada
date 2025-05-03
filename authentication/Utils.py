import time
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email_text(email, body):
    email_sender = EmailMessage(
        subject="join to our team",
        body=body,
        to=[
            email
        ]
    )
    email_sender.send()


def send_html_email(email, context):
    # قراءة محتوى HTML من ملف
    html_content = render_to_string('Untitled-1.html', context=context)
    # إنشاء رسالة بريد إلكتروني
    email = EmailMessage(
        subject="permit to work",
        body=html_content,
        to=[
            email
        ]
    )

    email.content_subtype = "html"
    # email.attach_alternative(html_content, "text/html")

    # إرسال البريد الإلكتروني
    email.send()


def send_email_without_file(*, html=False, **data):
    email = EmailMessage(**data)
    if html:
        email.content_subtype = "html"
    email.send()


from PIL import Image
import os
import boto3
from io import BytesIO
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from botocore.client import Config
import logging
# إعداد Boto3
session = boto3.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

s3_client = session.client(
    's3',
    endpoint_url=settings.AWS_S3_ENDPOINT_URL
)


def save_image_with_multiple_qualities(instance, image_field):
    image = getattr(instance, image_field)

    if not image:
        return

    # فتح الصورة الأصلية باستخدام Pillow
    img = Image.open(image)

    # رفع الصورة الأصلية إلى S3
    image.seek(0)
    s3_client.upload_fileobj(image, settings.AWS_STORAGE_BUCKET_NAME, image.name)

    # إنشاء الصورة المصغرة بجودة 360 بكسل
    img.thumbnail((360, img.height * (360 / img.width)))

    # حفظ الصورة المصغرة في الذاكرة المؤقتة
    thumb_io = BytesIO()
    img.save(thumb_io, format='JPEG')
    print(thumb_io)

    # رفع الصورة المصغرة إلى S3
    thumb_io.seek(0)
    thumbnail_name = f"{os.path.splitext(image.name)[0]}_360.jpg"

    s3_client.put_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=thumbnail_name,  # اسم الكائن في S3
        Body=thumb_io,  # محتوى الصورة المخزن في الذاكرة
        ContentType='image/jpeg'  # تحديد نوع المحتوى
    )
