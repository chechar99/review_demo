from django.test import TestCase
from django.test import Client
from models import Review, Company
import json


class ReviewViewsTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def login_user(self, username, password):
        login_url = '/token/new.json'
        login_data = {'username': username, 'password': password}
        response = self.client.post(login_url, login_data)
        response_dict = json.loads(response.content)
        token = response_dict['token']
        user = response_dict['user']
        self.assertIsNotNone(token)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        return user, token

    def test_user_can_create_reviews(self):
        # Issue a GET request.
        user, token = self.login_user('pparker', 'spider123')
        data = {
            'user': user,
            'token': token,
            'title': 'My review',
            'rating': 3,
            'summary': 'Great review bla bla bla',
            'company_id': 1,
        }

        response = self.client.post('/api/set_review', data)
        response_dict = json.loads(response.content)
        self.assertEqual(response_dict['status'], 'success')
        self.assertIsNotNone(response_dict['review_id'])
        review = Review.objects.get(id=response_dict['review_id'])
        self.assertEqual(review.reviewer.username, 'pparker')
        self.assertEqual(review.company.name, Company.objects.get(id=1).name)
        self.assertEqual(review.title, 'My review')
        self.assertEqual(review.rating, 3)
        self.assertEqual(review.summary, 'Great review bla bla bla')

    def test_user_can_get_reviews_list(self):
        user, token = self.login_user('ckent', 'spider123')
        data = {
            'user': user,
            'token': token,
        }

        response = self.client.post('/api/get_review_list', data)
        response_dict = json.loads(response.content)
        self.assertEqual(response_dict['status'], 'success')
        reviews_count = len(response_dict['data'])
        # User ckent must have 2 reviews as in the data fixture
        self.assertEqual(reviews_count, 2)
