from django.db import models
from django.contrib.auth.models import User


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

    assigned_to = models.ManyToManyField(User, default=None, related_name='+')
    percent_complete = models.PositiveSmallIntegerField(default=0)

    tags = models.ManyToManyField('ProblemTag')

    responses = models.ManyToManyField('Reply')

    def replies(self):
        return responses.all().order_by('date')


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
    date = models.DateTimeField()
    text = models.TextField()
    user = models.ForeignKey(User)
