from django.test import TestCase
from django.contrib.auth.models import User
from problems import models


class TestProblem(TestCase):
    '''
    Test the behavior of the Problem model.
    '''

    def test_add_response(self):
        problem = models.Problem()
        problem.title = 'test'
        problem.reference = 'test'
        problem.description = 'test'
        problem.save()

        user = User()
        user.username = 'testuser'
        user.email = 'test@example.com'
        user.set_password('test')
        user.save()

        reply = models.Reply()
        reply.text = 'test'
        reply.user = user
        reply.save()

        problem.add_response(reply)

        self.assertEqual(len(problem.replies()), 1,
                         'Response not added correctly')

