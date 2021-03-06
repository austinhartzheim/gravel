import django.test


class TestUrls(django.test.TestCase):
    '''
    These are some basic tests to make sure that the request routing
    setup isn't totally broken.
    '''

    def setUp(self):
        self.client = django.test.Client()

    def test_get_tokens(self):
        # Send a non-POST request, expect rejection
        response = self.client.get('/api/get_tokens')
        self.assertEqual(response.status_code, 405)

        # Send a non-authenticated request, expect rejection
        response = self.client.post('/api/get_tokens')
        self.assertEqual(response.status_code, 403)

    def test_problem_highest_id(self):
        # Send a non-POST request, expect rejection
        response = self.client.get('/api/problem/highest_id')
        self.assertEqual(response.status_code, 405)

        # Send a non-authenticated request, expect rejection
        response = self.client.post('/api/problem/highest_id')
        self.assertEqual(response.status_code, 403)

    def test_problem_reply(self):
        # Send a non-POST request, expect rejection
        response = self.client.get('/api/problem/replies/submit')
        self.assertEqual(response.status_code, 405)

        # Send a non-authenticated request, expect rejection
        response = self.client.post('/api/problem/replies/submit')
        self.assertEqual(response.status_code, 403)

    def test_problem_get_replies(self):
        # Send a non-POST request, expect rejection
        response = self.client.get('/api/problem/replies/get')
        self.assertEqual(response.status_code, 405)

        # Send a non-authenticated request, expect rejection
        response = self.client.post('/api/problem/replies/get')
        self.assertEqual(response.status_code, 403)

    def test_404(self):
        response = self.client.get('/api/this_should_404')
        self.assertEqual(response.status_code, 404)
