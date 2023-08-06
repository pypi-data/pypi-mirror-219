
# Django Veryfi OCR API Integration

As the title says, its a *Django* integration for *Veryfi OCR API*.
For now, it can auto OCR receipts or invoices documents by using ***dj_veryfi.fields.OCRInvoiceOrReceiptField*** model field. It derives from ***django.db.models.JSONField*** model field and, takes a additional parameter ***upload_to*** which specifies the path where the file should be saved according to current defined Django STORAGE.

## Requirements

> Python 3
> Django >= 3.2.20 
> Veryfi 3.3.0

## How it works
Once you have defined a model field as ***dj_veryfi.fields.OCRInvoiceOrReceiptField***, you can assign a file-like instance to an instance model field of ***dj_veryfi.fields.OCRInvoiceOrReceiptField***, then, before saving the model, it gonna hit the Veryfi OCR API to extract information and persists it as JSON into datababse.
When the field instance is acceesed after extraction it returns a ***OCRData*** instance which has the file descriptor and the JSON data.

## How to install

    pip install dj-veryfi

## Setup
Add ***dj_veryfi*** into *INSTALLED_APPS* and set the *Veryfi API* authentication information into *settings.py* as described bellow:
		
    ...
    INSTALLED_APS = [
    ...
    "dj_veryfi"
    ]
    ...
    # Veryfi access settings
    VERYFI_CLIENT_ID = "Your client ID"
    VERYFI_CLIENT_SECRET = "Your client secret"
    VERYFI_USERNAME = "Your username"
    VERYFI_API_KEY = "Your api key"


## Usage
Once you have a django project, dj-veryfi installed and setedup, just declare your model field as ***dj_veryfi.fields.OCRInvoiceOrReceiptField***, as bellow.
   
    from django.db import models
    from dj_veryfi.fields import OCRInvoiceOrReceiptField
    
    class Document(models.Model):
        created_at = models.Datetime.FIeld(auto_now_add=True)
        name = models.CharFied(max_length=100)
        ocr_data = OCRInvoiceOrReceiptField(upload_to="receipts/") 

Note, the ***upload_to*** attribute is a relative path which will append to MEDIA_ROOT settings variable.

Now, you can just assign a file-like object to ***Document.ocr_data*** save the model and, the information from receipt or invoice file will be extracted and saved as json into database.

## Trade-Offs
I have chosen to extend the field from ***django.db.models.JSONField*** because the extracted data comes as JSON and I had to do nothing related to querying. 

If I had chosen another model field type like ***FileField*** to get a shortcut to manage files and save them as JSON, I would have had trouble with how to query it into the database, due to JSON querying definition is not that simple.

So, it seems easier to me to avoid dealing with querying definitions when it comes to JSON querying, due to ***JSONField*** comes with "query thing" already done and deal with managing the files from where the information was extracted is easier. 



 
