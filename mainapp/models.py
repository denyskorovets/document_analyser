from __future__ import unicode_literals
from django.db import models
import PyPDF2
import datetime

now = datetime.datetime.now()
# This list contains document type choices for Document model in format of(Document_Type, Validation_Parameter)
DOCUMENT_TYPE = (
    ('Undefined', 'Undefined'),
    ('W2', 'Wage and Tax Statement'),
    ('BankStatement', 'Account Statement'),
    ('BankTransfer', 'Bank Transfer')
)
# This list contains validation error type choices for Error model in format of(error_name, error_text)
ERROR_TYPES = (
    ('corrupted', 'File Cannot Be Opened'),
    ('encrypted', 'File Password Protected'),
    ('clean', 'No Errors detected')
)


class DocumentManager(models.Manager):
    """
    Handles all Document related functions.
    """
    @staticmethod
    def create_doc(user, doc_path, document_name, user_selected_document_type):
        """
        Creates a document instance per with given parameters. Returns the document object.
        """
        doc = Document.DocumentManager.create(user=user, document_path=doc_path, document_name=document_name,
                                              user_selected_document_type=user_selected_document_type, created_at=now)
        if doc is not None:
            return doc
        else:
            return "Error while attempting to create a Document"

    def analyse_doc_type(self, new_doc):
        """
        Analyses a given document object for document type. Returns the calculated document type.
        """
        document_str_arr = self.open_document(new_doc)
        if isinstance(document_str_arr, str):
            return document_str_arr
        predicted_category = self.search_match(new_doc, document_str_arr)
        return predicted_category

    def open_document(self, new_doc):
        """
        Analyses a given document object for document type. Returns the calculated document type.
        """
        document_text_list = []
        doc = self.filter(pk=new_doc.pk).first()
        input_document = PyPDF2.PdfFileReader(open(doc.document_path, 'rb'))

        # If PDF file is encrypted
        if input_document.isEncrypted:
            error = Error.objects.create(document=doc, type_of_error='encrypted')
            if error is not None:
                return error

        # If PDF file is corrupted
        elif input_document.getNumPages() < 1:
            error = Error.objects.create(document=doc, type_of_error='corrupted')
            if error is not None:
                return error

        # If no validation errors, proceeds to extracting the text
        else:
            for i in range(input_document.numPages):
                document_text_list.append(input_document.getPage(i).extractText())

            # Convert text to string and save into document
            doc_text = ''.join(document_text_list)

            # Document_Text field currently holds only up to 25,000 characters. This needs validation
            if len(doc_text) > 24999:
                return "The maximum length of the document is more than allowed. Please reduce the number of pages"
            doc.document_text = doc_text
            doc.save()
            return document_text_list

    def update_document_type(self, new_doc, doc_type):
        """
        Updates a document with an updated document type.
        """
        document = self.filter(pk=new_doc.pk).first()
        document.type_of_document = doc_type
        document.save()
        return document

    def search_match(self, new_doc, document_str_arr):
        """
        Searches the document text for document type patterns, returns a match or string with Warning message.
        """
        matches = []
        doc = self.filter(pk=new_doc.pk).first()
        for (doc_name, doc_type) in DOCUMENT_TYPE:
            for single_page in document_str_arr:
                if doc_type in single_page:
                    matches.append(doc_type)
                    break

        matches = list(set(matches))
        if len(matches) == 0:
            return "WARNING: Scanned document did not match any document type patterns"
        elif len(matches) > 1:
            return "WARNING: Scanned document matched multiple document type patterns"
        elif matches[0] != doc.user_selected_document_type:
            return "WARNING: User defined document type did not match the one chosen by algorithm"
        else:
            return matches


class User(models.Model):
    username = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Document(models.Model):
    user = models.ForeignKey(User)
    document_name = models.CharField(max_length=50, blank=True)
    document_path = models.CharField(max_length=300, blank=True)
    user_selected_document_type = models.CharField(max_length=20, default='Undefined')
    document_text = models.TextField(max_length=25000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type_of_document = models.CharField(max_length=20, choices=DOCUMENT_TYPE, default='Undefined')
    DocumentManager = DocumentManager()


class Error(models.Model):
    document = models.ManyToManyField(Document, related_name="errors")
    type_of_error = models.CharField(max_length=30, choices=ERROR_TYPES, default="clean")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type_of_error



