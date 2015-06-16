import django.test
from problems import views


class TestProblemReport(django.test.TestCase):
    
    def setUp(self):
        self.factory = django.test.RequestFactory()

    def test_request_without_user(self):
        path = '/problem/report'
        request = self.factory.get(path)
        response = views.problem_report(request)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code.')


class TestProblemView(django.test.TestCase):

    def setUp(self):
        self.factory = django.test.RequestFactory()

    def test_missing_problem(self):
        problemid = 10   # This problem ID should not exist
        path = '/problem/view/%i/' % problemid
        request = self.factory.get(path)
        response = views.problem_view(request, problemid)

        self.assertEqual(response.status_code, 404,
                         'View did not return 404 on mossing problem')
