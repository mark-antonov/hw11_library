from django import forms


# HT 19. Bootstrap, JQuery, JSON, AJAX
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True)
    from_email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
