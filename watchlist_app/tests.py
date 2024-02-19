from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        """Creates A User for the test
        """
        self.user = User.objects.create_user(username='example', password='password@123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        """Post or create a stream platform object"""

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 streaming platform",
                                                           website="http://netflix.com")

    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 streaming platform",
            "website": "http://netflix.com"
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_update(self):
        data = {
            "name": "Netflix",
            "about": "No.1 streaming platform",
            "website": "http://netflix.com"
        }
        response = self.client.put(reverse('streamplatform-detail', args=(self.stream.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_delete(self):
        data = {
            "name": "Netflix",
            "about": "No.1 streaming platform",
            "website": "http://netflix.com"
        }
        response = self.client.delete(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):

        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StreamPlatformAdminTestCase(APITestCase):

    def setUp(self):
        """Created a supper user """
        self.user = User.objects.create_superuser(username='example', password='password@123')
        self.user.save()
        self.user.is_staff = True
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Prime",
                                                           about="#2 streaming platform",
                                                           website="http://prime.com")

    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 streaming platform",
            "website": "http://netflix.com"
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_streamplatform_update(self):
        data = {
            "name": "Netflix",
            "about": "No.1 streaming platform",
            "website": "http://netflix.com"
        }
        response = self.client.put(reverse('streamplatform-detail', args=(self.stream.id,)),  data)
        # serializer = PostSerializer(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_delete(self):
        data = {
            "name": "Netflix",
            "about": "No.1 streaming platform",
            "website": "http://netflix.com"
        }
        response = self.client.delete(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class WatchlistTestCase(APITestCase):
    """Testing Watchlist Api with a Normal user"""

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='password@123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 streaming platform",
                                                           website="http://netflix.com")
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="Exampletitle",
                                                         storyline="example storyline", active=True)



    def test_watclist_create(self):
        data = {
            "platform": self.stream.name,
            "title": "example",
            "storyline": "example storyline",
            "active": True
        }
        response = self.client.post(reverse('watchcreate'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_watchlist_get(self):
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(reverse('watchlist-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_delete(self):
        response = self.client.delete(reverse('watchlist-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(models.WatchList.objects.get().title, 'Exampletitle')

class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='password@123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                               about="#1 streaming platform",
                                                               website="http://netflix.com")
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="Exampletitle",
                                                             storyline="example storyline", active=True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream, title="Exampletitle2",
                                                             storyline="example storyline2", active=True)
        self.review = models.Review.objects.create(review_user=self.user, rating=5, description='Great Movie',
                                                   watchlist=self.watchlist2, active=True)

    def test_Review_create(self):
        data = {
            "rating": 4,
            "descrption": "example Description",
            "active": True
             }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(models.Review.objects.get().watchlist.title, self.watchlist.title)
        # self.assertEqual(models.Review.objects.get().review_user.username, self.user.username)

        """Trying to create review twice on a movie from a single user should fail."""
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_Review_create_unauth(self):
        data = {
            "rating": 4,
            "descrption": "example unauth Description",
            "active": True
            }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "rating": 5,
            "descrption": "Great Movie Test Description",
            "active": True
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_List(self):
        response = self.client.get(
            reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user(self):
        response = self.client.get('watch/review/?ruser' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)





