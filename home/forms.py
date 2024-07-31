from django import forms

class DocumentQueryForm(forms.Form):
    """
    A Django form for handling user input in the document query system.
    
    This form collects a query and a PDF file from the user. The query is a text field that
    allows users to enter their questions, and the PDF file is a file input that allows users
    to upload a document for processing.
    
    Attributes:
        query (forms.CharField): A text input field for the user's query. It accepts a maximum of
            200 characters.
        pdf (forms.FileField): A file input field for uploading the PDF document.
    """
    query = forms.CharField(label='Query', max_length=200)
    pdf = forms.FileField(label='PDF')