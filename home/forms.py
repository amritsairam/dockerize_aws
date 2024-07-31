from django import forms

class DocumentQueryForm(forms.Form):
    query = forms.CharField(label='Query', max_length=200)
    pdf = forms.FileField(label='PDF')