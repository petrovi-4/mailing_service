from django import forms

from mailing.models import Client, Message, Newsletter


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('fio', 'email', 'comment',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ('start_time', 'end_time', 'periodicity', 'status', 'client', 'message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
