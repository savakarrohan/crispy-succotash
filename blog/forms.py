from django import forms
class EmailPostForm(forms.Form):
    """
    Email posting form 
    """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    