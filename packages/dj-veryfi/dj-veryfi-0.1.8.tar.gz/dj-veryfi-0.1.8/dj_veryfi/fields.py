import json
from pathlib import Path
from django.db import models
from django.core.files import File
from django.core.files.storage import default_storage
from .veryfi import VeryfiService
from dataclasses import dataclass


@dataclass
class OCRData:
    data: dict
    file: File

    @classmethod
    def parse(cls, value):
        abspath = value.get("_filepath")
        return OCRData(file=File(open(abspath)), data=value)


class OCRInvoiceOrReceiptField(models.JSONField):
    def __init__(self, upload_to="", *args, **kwargs):
        self.upload_to = upload_to
        self._veryfi = VeryfiService()
        super(OCRInvoiceOrReceiptField, self).__init__(*args, **kwargs)

    def _mk_path(self, fileobj):
        temp_filepath = Path(fileobj.name)
        return Path(self.upload_to) / temp_filepath.name

    def _save_file(self, fileobj):
        filepath = self._mk_path(fileobj)
        saved_path = default_storage.save(filepath, fileobj)
        return default_storage.path(saved_path)

    def _extract_data(self, abspath):
        return self._veryfi.extract_data(abspath)

    def from_db_value(self, value, expression, connection):
        return value if not value else OCRData.parse(json.loads(value))

    def to_python(self, value):
        return (
            value if isinstance(value, OCRData) or not value else OCRData.parse(value)
        )

    def pre_save(self, instance, add):
        data = None
        fileobj = getattr(instance, self.attname, None)
        if fileobj:
            abspath = self._save_file(fileobj)
            data = self._extract_data(abspath)
            data["_filepath"] = abspath
            ocr_data = OCRData.parse(data)
            setattr(instance, self.attname, ocr_data)
        return data
