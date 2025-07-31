from django import forms

class MessageForm(forms.Form):
    content = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Écris ton message ici...'}),
        max_length=100
    )
