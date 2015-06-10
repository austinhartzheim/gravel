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
        path = '/api/problem/reply'
        data = {'id': problemid, 'text': 'helloworld'}
        request = self.factory.create_api_request(self.user, path, data)
        response = views.problem_reply(request)

        self.assertEqual(response.status_code, 404,
                         'View did not return a 404 for a missing problem')

    def test_expected_case(self):
        problem = problems.models.Problem(title='Teset', reference='test',
                                          description='test')
        problem.save()

        path = '/api/problem/reply'
        data = {'id': problem.pk, 'text': 'test reply'}
        request = self.factory.create_api_request(self.user, path, data)
        response = views.problem_reply(request)

        self.assertEqual(len(problem.replies()), 1,
                         'Problem has the incorrect number of replies')
        reply = problem.replies()[0]
        self.assertEqual(reply.user, self.user)
        self.assertEqual(reply.text, data['text'])

    def test_invalid_text(self):
        self.skipTest('Not implemented')


class TestProblemGetReplies(TestWithUser):
    '''
    Test that the problem_get_replies view returns the correct reply
    informaon.
    '''
    def setUp(self):
        super().setUp()
        self.factory = utils.GravelApiRequestFactory()

    def test_problem_does_not_exist(self):
        '''
        Test that a HTTP 404 error is returned when the requested
        problem does not exist.
        '''
        problemid = 10  # No Problem should have this PK
        path = '/api/problem/%i/get_replies' % problemid
        data = {}
        request = self.factory.create_api_request(self.user, path, data)
        response = views.problem_get_replies(request, problemid)

        self.assertEqual(response.status_code, 404,
                         'View did not return a 404 for a missing problem')

    def test_problem_without_replies(self):
        '''
        Test that a problem without replies returns an empty list of
        replies.
        '''
        problem = problems.models.Problem(title='Test', reference='test',
                                          description='test')
        problem.save()
        path = '/api/problem/%i/get_replies' % problem.pk
        data = {}
        request = self.factory.create_api_request(self.user, path, data)
        response = views.problem_get_replies(request, problem.pk)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')

        rdata = json.loads(response.content.decode('utf8'))
        self.assertEqual(rdata['problemid'], problem.pk,
                         'Response included an unexpected `problemid` value')
        self.assertEqual(len(rdata['replies']), 0,
                         'The returned data contained unexpected replies')

    def test_problem_with_reply(self):
        '''
        Test that a problem with a reply returns a list containing the
        reply with the expected data.
        '''
        # Create a Problem object
        problem = problems.models.Problem(title='Test', reference='test',
                                          description='test')
        problem.save()

        # Create a Reply object
        reply_text = 'hello there, world'
        reply = problems.models.Reply(text=reply_text, user=self.user)
        reply.save()

        # Add reply to problem
        problem.add_response(reply)

        # Create a request to the API
        path = '/api/problem/%i/get_replies' % problem.pk
        data = {}
        request = self.factory.create_api_request(self.user, path, data)
        response = views.problem_get_replies(request, problem.pk)

        # Check the API response
        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')

        rdata = json.loads(response.content.decode('utf8'))
        self.assertEqual(rdata['problemid'], problem.pk,
                         'Response included an unexpected `problemid` value')
        self.assertEqual(len(rdata['replies']), 1,
                         'The returned data contained unexpected replies')
        rreply = rdata['replies'][0]
        self.assertEqual(rreply['text'], reply_text,
                         'Returned reply response text does not match')
        self.assertEqual(rreply['userid'], self.user.pk,
                         'User ID in reply is incorrect')


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
