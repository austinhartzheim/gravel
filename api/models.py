import os
import time
import base64
import hashlib
import datetime

from django.db import models
from django.contrib.auth.models import User


class RequestToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=64)

    expires = models.DateTimeField()

    @classmethod
    def build_tokens(cls, user, count=1):
        '''
        Generate one or more tokens for the given user.
        
        :param `django.contrib.auth.models.User` user: The user that
          the generated tokens should be valid for.
        :param int count: The number of tokens to generate.
        '''
        i = 0
        tokens = []

        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

        while i < count:
            hash = hashlib.sha256(str(time.time()).encode('utf8')).hexdigest()
            token = RequestToken(user=user, token=hash, expires=expiration)
            tokens.append(token)
            i += 1

        cls.objects.bulk_create(tokens)

        return tokens


class SharedSecret(models.Model):
    user = models.OneToOneField(User)
    shared_secret = models.BinaryField(max_length=64)

    @classmethod
    def get_or_create(cls, user):
        try:
            return cls.objects.get(user=user).shared_secret
        except cls.DoesNotExist:
            secret = base64.b64encode(os.urandom(46))
            obj = cls(user=user, shared_secret=secret)
            obj.save()
            return obj.shared_secret
