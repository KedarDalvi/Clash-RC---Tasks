from django.test import TestCase, Client
from .models import Profile
from datetime import date


class ViewsTest(TestCase):
    """
    TestCase to test all exposed views for anonymous users.
    """

    fixtures = [
        'user.yaml',
    ]

    def setUp(self):
        pass

    def testHome(self):
        response = self.client.get('/user/')
        self.assertEquals(response.status_code, 200)

    def testLoginAnonymous(self):
        response = self.client.get('/user/login/')
        self.assertEquals(response.status_code, 200)

    def testLoginAuthenticated(self):
        response = self.client.post(
            '/user/login/',
            {
                'username': 'andreas',
                'password': '',
            }
        )
        self.assertEquals(response.status_code, 200)

    def testLogoutGetAnonymous(self):
        response = self.client.get('/user/logout/')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/user/')

    def testLogoutPostAnonymous(self):
        response = self.client.post('/user/logout/')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/user/')

    def testLogoutGetAuthenticated(self):
        response = self.client.get('/user/logout/')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/user/')

    def testLogoutPostAuthenticated(self):
        response = self.client.post('/user/logout/')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/user/')


class ManagerTest(TestCase):
    """
    Test managers
    """
    fixtures = [
        'user.yaml',
        'profile.yaml',
    ]

    def setUp(self):
        pass

    def testCount(self):
        p = Profile.objects.count()
        self.assertEquals(p, 5)

    def testFemaleCount(self):
        p = Profile.objects.female_count()
        self.assertEquals(p, 2)

    def testMaleCount(self):
        p = Profile.objects.male_count()
        self.assertEquals(p, 3)


class ModelTest(TestCase):
    """
    Test models
    """
    fixtures = [
        'profile.yaml',
        'user.yaml',
    ]

    def setUp(self):
        pass

    def testAbsoluteUrl(self):
        p = Profile.objects.get(pk=1)
        url = p.get_absolute_url()
        self.assertEqual(url, "/user/profile/1/")

    def testAge(self):
        p = Profile.objects.get(pk=1)
        age = int((date.today() - p.dob).days / 365)
        self.assertEquals(p.age, age)

    def testRepr(self):
        p = Profile.objects.get(pk=1)
        self.assertEqual(str(p), "Johann (M, 2)")
