from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

# Create your tests here.


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password = 'somepassword')
        self.userb = User.objects.create_user(username='cfe2', password = 'somepassword2')

        # Tweet.objects.create(content='my first tweet', user = self.user)
        # Tweet.objects.create(content='my first tweet', user = self.user)
        # Tweet.objects.create(content='my first tweet', user = self.userb)
        # self.currentCount = Tweet.objects.all().count()

    def test_profile_created_via_signal(self):
        qs = Profile.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_following(self):
        first = self.user
        second = self.userb
        first.profile.followers.add(second) # added a follower
        second_user_following_whom = second.following.all()
        qs = second_user_following_whom.filter(user=first) # from a user, check other user is being followed
        first_user_following_none = first.following.all() # check new user is not following anyone
        self.assertTrue(qs.exists())
        self.assertFalse(first_user_following_none.exists())

