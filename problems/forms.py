from django import forms
from problems import models


class ProblemSubmitForm(forms.ModelForm):
    class Meta:
        model = models.Problem
        fields = ['title', 'description', 'username']


class ReplySubmit(forms.ModelForm):
    class Meta:
        model = models.Reply
        fields = ['text']
