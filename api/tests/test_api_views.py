import json

import django.test
from django.contrib.auth.models import User

from api import views
from api.tests import utils
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

        self.assertNotEqual(response.status_code, 200,
                            'OK status given when the problem is missing')

    def test_expected_case(self):
        self.skipTest('Not implemented')

    def test_invalid_request_body(self):
        self.skipTest('Not implemented')

