from django import forms
from mail.models import Subscriber


class SubscriberCreateForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data['email']
        #if Subscriber.objects.filter(email__iexact=email).first():
        if Subscriber.get_by_email(email):
            raise forms.ValidationError('Подписчик с указанным email уже с уществует')
        return email


class LetterCreateForm(forms.Form):
    subject = forms.CharField(label='Тема письма')
    text = forms.CharField(label='Текст письма', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'rows': 3})

