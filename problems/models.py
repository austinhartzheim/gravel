import datetime
from django.db import models
from django.contrib.auth.models import User

import bleach
import markdown


class Problem(models.Model):
    title = models.CharField(max_length=80)
    reference = models.TextField()
    description = models.TextField()

    #: Was the user logged in when submitting the problem
    userauthed = models.BooleanField(default=False)
    #: The textual username of the user if they were not logged in
    username = models.CharField(default=None, max_length=40, null=True)
    #: A reference to the user object if they were logged in
    userref = models.ForeignKey(User, default=None, null=True, related_name='+')

    date_created = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(default=None, null=True)
    resolved = models.BooleanField(default=False)
    last_updated = models.DateTimeField(default=None, null=True)
    last_update_user = models.ForeignKey(User, default=None, null=True, related_name='+')

    assigned_to = models.ManyToManyField(User, default=None, related_name='+')
    percent_complete = models.PositiveSmallIntegerField(default=0)

    tags = models.ManyToManyField('ProblemTag')

    responses = models.ManyToManyField('Reply')

    def replies(self):
        return self.responses.all().order_by('date')

    def add_response(self, response):
        '''
        Add the response, update last_updated, and save.
        '''
        self.last_updated = datetime.datetime.now()
        self.responses.add(response)
        self.last_update_user = response.user
        self.save()

    def markdown_description(self):
        cleaned_description = bleach.clean(self.description)
        html = markdown.markdown(cleaned_description)
        return html

    def markdown_reference(self):
        cleaned_reference = bleach.clean(self.reference)
        html = markdown.markdown(cleaned_reference)
        return html


class ProblemTag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    @classmethod
    def get_or_create(cls, name):
        try:
            cls.objects.get(name=name)
        except cls.DoesNotExist:
            newtag = cls(name=name)
            newtag.save()
            return newtag


class Reply(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    user = models.ForeignKey(User)

    def format(self):
        cleaned = bleach.clean(self.text)
        return markdown.markdown(cleaned)

    def serialize(self):
        return {
            'id': self.pk,
            'date': self.date.isoformat(),
            'text': self.text,
            'userid': self.user.pk
        }
