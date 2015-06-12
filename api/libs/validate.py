from hashlib import sha256
import hmac

import django.http
from django.contrib.auth.models import User
from api import models


class ValidateApiRequest():
    def __init__(self, view):
        self.view = view

    def __call__(self, request, *args, **kwargs):
        '''
        Check that `request` is a POST request that contains the
        headers to indicate that it is a Gravel request with a user ID
        and a valid HMAC.
        
        If the request is valid, forward it to the view along with the
        User object for the requesting user. Otherwise, return an
        appropriate error code.
        '''
        # Check that the request is using the POST method
        if request.method != 'POST':
            return django.http.HttpResponseNotAllowed(['POST'])

        # Check that the Gravel User ID header is present
        if 'HTTP_X_GRAVEL_USER_ID' not in request.META:
            return django.http.HttpResponseForbidden('No User ID specified')
        if 'HTTP_X_GRAVEL_HMAC_SHA256' not in request.META:
            return django.http.HttpResponseForbidden('No HMAC given')
        if 'CONTENT_TYPE' not in request.META:
            return django.http.HttpResponseBadRequest('Missing Content-Type')
        if request.META['CONTENT_TYPE'] != 'application/json':
            return django.http.HttpResponseBadRequest('Non-JSON Content-Type')

        # Check that the user exists and has API access permission
        try:
            userid = int(request.META['HTTP_X_GRAVEL_USER_ID'])
            user = User.objects.get(pk=userid)
        except ValueError:
            return django.http.HttpResponseBadRequest('Non-integer User ID')
        except User.DoesNotExist:
            return django.http.HttpResponseForbidden('User ID does not exist')

        # TODO: check that the user has API access permission

        # Check that the HMAC is valid
        if not self.validate_request_hmac(request, user):
            return django.http.HttpResponseForbidden('Invalid HMAC')

        # Parse the JSON data
        try:
            data = json.loads(request.body.decode('utf8'))
        except ValueError:
            return django.http.HttpResponseBadRequest('Invalid JSON data')

        # The checks pass; forward the request and the user to the View
        return self.view(request, user, data, *args, **kwargs)

    def validate_request_hmac(self, request, user):
        '''
        Grab the shared secret for the given user and use it to
        validate the HMAC given in the message headers.
        
        :param django.http.HttpRequest request: A Django request object
          that contains the headers, POST data, etc.
        :param django.contrib.auth.models.User user: A user object that
          the request is claiming to be the originating user.
        :returns: a boolean value; `true` indicates a valid request;
          `false` indicates an invalid request
        '''
        if 'HTTP_X_GRAVEL_HMAC_SHA256' not in request.META:
            return False

        try:
            shared_secret = models.SharedSecret.get_or_create(user)
        except models.SharedSecret.DoesNotExist:
            return False

        digest = hmac.new(shared_secret, request.body, sha256).hexdigest()
        return self.__safe_compare(digest, request.META['HTTP_X_GRAVEL_HMAC_SHA256'])

    @staticmethod
    def __safe_compare(a, b):
        '''
        Attempt to use hmac.compare_digest(), which is available in
        Python 3.3+. If that fails, iterate over the entire digest to
        detect a difference; only return after iterating over the
        entire digest to avoid a timing attack.
        '''
        # TODO: implement the manual comparison in a low-level language
        #   Python might optimize the comparison loop
        try:
            return hmac.safe_compare(a, b)
        except AttributeError:
            if len(a) != len(b):
                return False

            result = True
            count = 0  # Hack to prevent optimization
            for i in range(0, len(a)):
                if a[i] != b[i]:
                    result = False
                count += 1
            return result


class ValidateToken():
    def __init__(self, view):
        self.view = view

    def __call__(self, request, user, data, *args, **kwargs):
        '''
        Check that `request` contains the expected token data for a
        request from the User ID specified in the headers.
        
        If the request is valid, delete the token object and forward
        the request to the view. Otherwise, return an error code.
        
        This should follow the ValidateApiRequest decorator because it
        requires a user object, which that decorator fetches.
        '''
        try:
            tokenstr = data['token']
        except IndexError:
            return django.http.HttpResponseBadRequest('Missing token in JSON')

        try:
            token = models.RequestToken.objects.get(user=user, token=tokenstr)
            token.delete()
        except models.RequestToken.DoesNotExist:
            return django.http.HttpResponseForbidden('Invalid token used')

        return self.view(request, user, data, *args, **kwargs)
