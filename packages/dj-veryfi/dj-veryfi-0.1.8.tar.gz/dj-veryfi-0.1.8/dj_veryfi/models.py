from django.db import models
from .fields import OCRInvoiceOrReceiptField


class Document(models.Model):
    content_type = models.CharField(max_length=150)
    ocr = OCRInvoiceOrReceiptField(upload_to="docs/", null=True, blank=True)
