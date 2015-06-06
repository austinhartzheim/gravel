import hmac
import hashlib
import json
import django.test
from api import models


class GravelApiRequestFactory():
    '''
    Emulate Gravel API requests.
    '''
    def __init__(self, omit=[], override={}):
        '''
        :param iterable omit: An iterable object of headers to omit.
          Note that only headers explicitly added for Gravel emulation
          can be removed from the request.
        :param dict override: A dictionary of (header, value) pairs
          that will be used to override the default header values. This
          is useful when injecting invalid data for tests.
        '''
        self.omit = omit
        self.override = override
        self.factory = django.test.RequestFactory()

    def create_api_request(self, user, path, data):
        '''
        Createa a Gravel API request for testing purposes. The returned
        request object will have headers and a SHA256 HMAC as if it was
        a real API request.
        
        :param django.contrib.auth.models.User user: The user for which
          this request should be generated.
        :param str path: The path which the emulated request would have
          if it actually reached the view.
        :param dict data: This dict will be converted to a JSON string,
          used to compute the HMAC, and used as the request body.
        :param str topic: The topic for the Shopify-Topic header. This
          has a form such as "customers/create".
        :returns: a Django request object containing the given data;
          this can be passed to a view to simulate an actual request.
        '''
        shared_secret = models.SharedSecret.get_or_create(user).shared_secret
        datastr = json.dumps(data)
        hmac256 = self.compute_hmac(datastr, shared_secret)

        # Define headers to add to the request
        headers = {
            'HTTP_X_GRAVEL_USER_ID': user.pk,
            'HTTP_X_GRAVEL_HMAC_SHA256': hmac256,
            'content_type': 'application/json'
        }

        # Omit headers
        for header in self.omit:
            if header in headers:
                headers.pop(header)

        # Override headers
        for header, value in self.override.items():
            headers[header] = value

        # Create the POST request
        return self.factory.post(path, datastr, **headers)

    def compute_hmac(self, data, shared_secret):
        '''
        Calculate the HMAC for `data` and `shared_secret`. Theese
        parameters can be supplied as `str` or `bytes` objects. If a
        string is passed, it will be encoded using utf8.
        
        :param bytes data: The data of the request.
        :param bytes secret_key: The secret key
        '''
        # Convert `data` and `secret_key` to bytes if necessary.
        if isinstance(data, str):
            data = data.encode('utf8')
        if isinstance(shared_secret, str):
            shared_secret = shared_secret.encode('utf8')

        # Compute the digest
        return hmac.new(shared_secret, data, hashlib.sha256).hexdigest()
