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
