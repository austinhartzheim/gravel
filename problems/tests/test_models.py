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

    def test_description_html_sanitization(self):
        '''
        Test that HTML is correctly removed when the provided
        description is being rendered.
        '''
        problem = models.Problem(title='test', reference='test')
        problem.description = 'hello<script>'
        problem.save()

        self.assertFalse('<script>' in problem.markdown_description())
        self.assertTrue('hello' in problem.markdown_description())

    def test_reference_html_sanitization(self):
        '''
        Test that HTML is correctly removed when the provided
        reference is being rendered.
        '''
        problem = models.Problem(title='test', description='test')
        problem.reference = 'hello<script>'
        problem.save()

        self.assertFalse('<script>' in problem.markdown_reference())
        self.assertTrue('hello' in problem.markdown_reference())
