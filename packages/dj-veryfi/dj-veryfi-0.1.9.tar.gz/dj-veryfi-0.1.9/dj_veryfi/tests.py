import random
from unittest.mock import patch
from uuid import uuid4
from django.core.files import File
from django.core.files.base import ContentFile
from django.test import TestCase

from model_bakery import baker

from .fields import OCRData
from .models import Document


class OCRInvoiceOrReceiptFieldTestCase(TestCase):
    def __assertOcrDoc(self, doc, mocked_api_call):
        self.assertIsInstance(doc.ocr, OCRData)
        self.assertIsInstance(doc.ocr.file, File)
        self.assertIsInstance(doc.ocr.data, dict)
        self.assertIn("_filepath", doc.ocr.data)
        mocked_api_call.assert_called_once_with(doc.ocr.data["_filepath"])

    @patch(
        "dj_veryfi.veryfi.VeryfiService.extract_data",
        return_value={
            "document_type": "receipt",
            "some_key": random.choice(["the value", "the value 2", "the value 3"]),
        },
    )
    def test_saving_model_with_ocr_field(self, mocked_api_call):
        doc = baker.make(
            Document, ocr=ContentFile(b"Some receipt content", name="receipt.pdf")
        )

        self.__assertOcrDoc(doc, mocked_api_call)

    @patch(
        "dj_veryfi.veryfi.VeryfiService.extract_data",
        return_value={
            "document_type": "receipt",
            "some_key": random.choice(["the value", "the value 2", "the value 3"]),
        },
    )
    def test_retrieve_model_with_ocr_field(self, mocked_api_call):
        baker.make(
            Document,
            ocr=lambda: ContentFile(
                b"Some receipt content", name=f"receipt-{uuid4()}.pdf"
            ),
        )
        for doc in Document.objects.all():
            self.__assertOcrDoc(doc, mocked_api_call)

    @patch(
        "dj_veryfi.veryfi.VeryfiService.extract_data",
        return_value={
            "document_type": "receipt",
            "some_key": random.choice(["the value", "the value 2", "the value 3"]),
        },
    )
    def test_not_call_api_with_null_ocr_field(self, mocked_api_call):
        baker.make(Document)
        mocked_api_call.assert_not_called()
