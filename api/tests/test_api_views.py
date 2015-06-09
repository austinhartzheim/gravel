import json

import django.test
from django.contrib.auth.models import User

from api import views
from api.tests import utils
import api.models
import problems.models


class TestWithUser(django.test.TestCase):
    '''
    Create a User object with API access and save it in self.user.
    
    This is useful for other tests to subclass because access to a user
    object is required to make valid API requests.
    '''

    def setUp(self):
        self.user = User(username='test', email='test@example.com')
        self.user.set_password('testpassword')
        self.user.save()


class TestProblemGetHighestId(TestWithUser):
    '''
    Test that the problem_highest_id view returns correct responses.
    '''
    def setUp(self):
        super().setUp()
        self.factory = utils.GravelApiRequestFactory()

    def test_no_problems(self):
        path = '/api/problem/highest_id'
        data = {}
        request = self.factory.create_api_request(self.user, path, data)
        response = views.problem_highest_id(request)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')

        rdata = json.loads(response.content.decode('utf8'))
        self.assertIn('id', rdata)
        self.assertEqual(rdata['id'], 0, 'API should report no current IDs')

    def test_with_problems(self):
        prob1 = problems.models.Problem(title='Test', reference='test',
                                        description='test')
        prob1.save()

        path = '/api/problem/highest_id'
        data = {}
        request = self.factory.create_api_request(self.user, path, data)
        response = views.problem_highest_id(request)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')

        rdata = json.loads(response.content.decode('utf8'))
        self.assertIn('id', rdata)
        self.assertEqual(rdata['id'], prob1.pk,
                         'API should report one problem')

        prob2 = problems.models.Problem(title='Test', reference='test',
                                        description='test')
        prob2.save()

        request = self.factory.create_api_request(self.user, path, data)
        response = views.problem_highest_id(request)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')

        rdata = json.loads(response.content.decode('utf8'))
        self.assertIn('id', rdata)
        self.assertEqual(rdata['id'], prob2.pk,
                         'API should report two problems')


class TestProblemReply(TestWithUser):
    '''
    Test that the problem_reply view returns correct responses and
    properly creates Reply objects in the database.
    '''
    def setUp(self):
        super().setUp()
        self.factory = utils.GravelApiRequestFactory()

    def test_no_problems(self):
        '''
        Test that an error is returned when the specified Problem
        object cannot be located.
        '''
        problemid = 10  # No object in the database should have this PK
        path = '/api/problem/%i/reply' % problemid
        data = 'helloworld'
        request = self.factory.create_api_text_request(self.user, path, data)
        response = views.problem_reply(request, problemid)

        self.assertIsInstance(response, django.http.Http404,
                              'View did not return 404 for a missing problem')

    def test_expected_case(self):
        self.skipTest('Not implemented')

    def test_invalid_request_body(self):
        self.skipTest('Not implemented')


class TestApiGetTokens(TestWithUser):
    '''
    Test that the api_get_tokens view returns correct responses and
    properly creates RequestToken objects in the database.
    '''
    def setUp(self):
        super().setUp()
        self.factory = utils.GravelApiRequestFactory()

    def test_expected_case(self):
        token_count = 10
        path = '/api/get_tokens'
        data = {'count': token_count}
        request = self.factory.create_api_request(self.user, path, data)
        response = views.api_get_tokens(request)

        self.assertEqual(response.status_code, 200,
                         'Server returned an error on a valid request')
        rdata = json.loads(response.content.decode('utf8'))
        self.assertEqual(len(rdata['tokens']), token_count,
                         'Incorrect number of tokens returned')

        tokens = api.models.RequestToken.objects.filter(user=self.user)
        self.assertEqual(len(tokens), token_count,
                         'Incorrect number of RequestToken objects saved')

    def test_non_numeric_count(self):
        '''
        Test that a request for a non-numeric number of tokens is
        rejected and returns a HTTP BAD REQUEST status code.
        '''
        path = '/api/get_tokens'
        data = {'count': 'non-numeric string'}
        request = self.factory.create_api_request(self.user, path, data)
        response = views.api_get_tokens(request)

        self.assertEqual(response.status_code, 400,
                         'View did not return a BAD REQUEST status code')

    def test_count_bounds(self):
        '''
        Test that the view properly denies requests that are out of
        resonable boundaries for a count.
        '''
        '''
        Test that a request for a non-numeric number of tokens is
        rejected and returns a HTTP BAD REQUEST status code.
        '''
        path = '/api/get_tokens'
        data = {'count':-1}
        request = self.factory.create_api_request(self.user, path, data)
        response = views.api_get_tokens(request)

        self.assertEqual(response.status_code, 400,
                         'View accepted a negative count')

        data = {'count': 1000000}
        request = self.factory.create_api_request(self.user, path, data)
        response = views.api_get_tokens(request)

        self.assertEqual(response.status_code, 400,
                         'View accepted an overly-large count')
