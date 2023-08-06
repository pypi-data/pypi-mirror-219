from django.conf import settings
from veryfi import Client


class VeryfiService:
    def __init__(self):
        self._client = Client(
            settings.VERYFI_CLIENT_ID,
            settings.VERYFI_CLIENT_SECRET,
            settings.VERYFI_USERNAME,
            settings.VERYFI_API_KEY,
        )

    def extract_data(self, filepath):
        return self._client.process_document(filepath)
