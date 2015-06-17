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


class TestProblemTag(TestCase):
    '''
    Test the behavior of the ProblemTag model. 
    '''

    def test_get_or_create_creation(self):
        '''
        Test that the get_or_create method correctly creates a new tag
        when one does not exist.
        '''
        test_name = 'testtag'
        tag = models.ProblemTag.get_or_create(test_name)
        self.assertIsInstance(tag, models.ProblemTag,
                              'Incorrect return, not a ProblemTag instance')
        self.assertEqual(tag.name, test_name,
                         'Incorrect name set on created tag')

    def test_get_or_create_getting(self):
        '''
        Test that the get_or_create method is able to discover and
        return tags that already exist.
        '''
        test_name = 'testtag'
        stored_tag = models.ProblemTag(name=test_name)
        stored_tag.save()

        tag = models.ProblemTag.get_or_create(test_name)
        self.assertEqual(tag.pk, stored_tag.pk,
                         'Method returned a tag with a different PK')
