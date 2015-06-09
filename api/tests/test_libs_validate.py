import django.test
from django.contrib.auth.models import User
from api.libs.validate import ValidateApiRequest
from api.tests import utils


class TestValidateApiRequest(django.test.TestCase):
    '''
    Test that the ValidateApiRequest decorator properly validates
    requirements such as the existence of a User ID and a valid
    HMAC for that user in the request.
    '''
    #: Headers to be individual obitted when testing header validation
    headers = ('HTTP_X_GRAVEL_USER_ID', 'HTTP_X_GRAVEL_HMAC_SHA256')

    #: An incorrect HMAC value to test HMAC validation
    bad_hmac = '0' * 64

    def setUp(self):

        # Create a protected view
        @ValidateApiRequest
        def dummy_view(*args, **kwargs):
            '''
            Raise an exception if this "view" is ever executed. The
            validation decorator should prevent this "view" from
            being executed.
            '''
            raise Exception('This function should not have been called')

        self.view = dummy_view

        # Create an API user
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('testpassword')
        self.user.save()

    def test_get_request(self):
        '''
        Check that the validator rejects HTTP GET and PUT requests.
        '''
        factory = django.test.RequestFactory()

        # Test GET request to ensure rejection
        request = factory.get('/')
        response = self.view(request)
        self.assertEqual(response.status_code, 405,
                         'Not returning 405 to notify of POST requirement')

        # Test PUT request to ensure rejection
        request = factory.put('/')
        response = self.view(request)
        self.assertEqual(response.status_code, 405,
                         'Not returning 405 to notify of POST requirement')

    def test_missing_individual_headers(self):
        '''
        Check that missing required headers result in a non-200 status.
        '''
        path = '/api/problem/highest_id'
        for header in self.headers:
            factory = utils.GravelApiRequestFactory(omit=(header,))

            request = factory.create_api_request(self.user, path, data={})
            response = self.view(request)

            self.assertNotEqual(response.status_code, 200,
                                'Request should have caused an HTTP error')

    def test_incorrect_content_type_header(self):
        '''
        Check that Content-Type headers other than application/json are
        rejected by the validator.
        '''
        path = '/api/problem/highest_id'
        override_headers = {'content_type': 'application/ecmascript'}

        for header in self.headers:
            factory = utils.GravelApiRequestFactory(override=override_headers)

            request = factory.create_api_request(self.user, path, data={})
            response = self.view(request)

            self.assertEqual(response.status_code, 400)

    def test_incorrect_hmac_header(self):
        '''
        Check that the HMAC validation code is properly executing and
        returning an HTTP 403 Forbidden response.
        '''
        path = '/api/problem/highest_id'
        override_headers = {'HTTP_X_GRAVEL_HMAC_SHA256': self.bad_hmac}

        for header in self.headers:
            factory = utils.GravelApiRequestFactory(override=override_headers)

            request = factory.create_api_request(self.user, path, data={})
            response = self.view(request)

            self.assertEqual(response.status_code, 403,
                             'Bad HMAC did not result in forbidden response')
