from rest_framework.test import APITestCase
from .views import get_random, get_access_token, get_refresh_token
from .models import CustomUser, UserProfile
from message_control.tests import create_image, SimpleUploadedFile


class TestGenericFunctions(APITestCase):

    def test_get_random(self):
        rand1 = get_random(10)
        rand2 = get_random(10)
        rand3 = get_random(15)

        # check getting result
        self.assertTrue(rand1)

        # check rand1 is not equal to rand2
        self.assertNotEqual(rand1, rand2)

        self.assertEqual(len(rand1), 10)
        self.assertEqual(len(rand3), 15)

    def test_get_access_token(self):
        payload = {
            "id": 1
        }
        token = get_access_token(payload)

        self.assertTrue(token)

    def test_get_refresh_token(self):

        token = get_refresh_token()

        self.assertTrue(token)


class TestAuth(APITestCase):
    login_url = "/user/login"
    register_url = "/user/register"
    refresh_url = "/user/refresh"

    def test_register(self):
        payload = {
            "username": "asdfghjkl",
            "password": "asd123",
        }

        response = self.client.post(self.register_url, data=payload)

        # check status
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        payload = {
            "username": "asdfghjkl",
            "password": "asd123",
        }

        # register
        self.client.post(self.register_url, data=payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        result = response.json()

        # check status
        self.assertEqual(response.status_code, 201)

        # check both the refresh and access token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])

    def test_refresh(self):
        payload = {
            "username": "asdfghjkl",
            "password": "asd123",
        }

        # register
        self.client.post(self.register_url, data=payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        refresh = response.json()["refresh"]

        # get refresh
        response = self.client.post(
            self.refresh_url, data={"refresh": refresh})
        result = response.json()

        # check status
        self.assertEqual(response.status_code, 201)

        # check both the refresh and access token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])


class TestUserInfo(APITestCase):
    profile_url = "/user/profile"
    file_upload_url = "/message/file-upload"

    def setUp(self):
        self.user = CustomUser.objects._create_user(
            username="asdfghjkl", password="asd123")

        self.client.force_authenticate(user=self.user)

    def test_post_user_profile(self):

        payload = {
            "user_id": self.user.id,
            "first_name": "Adefemi",
            "last_name": "Greate",
            "caption": "Being alive is different from living",
            "about": "I am a passionation lover of ART, graphics and creation"
        }

        response = self.client.post(
            self.profile_url + f"/{result['id']}", data=payload)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "Adefemi")
        self.assertEqual(result["last_name"], "Greate")
        self.assertEqual(result["user"]["username"], "asdfghjkl")

    def test_post_user_profile_with_profile_picture(self):

        # upload image
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        data = {
            "file_upload": avatar_file
        }

        # processing
        response = self.client.post(self.file_upload_url, data=data)
        result = response.json()

        payload = {
            "user_id": self.user.id,
            "first_name": "Adefemi",
            "last_name": "Greate",
            "caption": "Being alive is different from living",
            "about": "I am a passionation lover of ART, graphics and creation",
            "profile_picture_id": result["id"]
        }

        response = self.client.post(self.profile_url, data=payload)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "Adefemi")
        self.assertEqual(result["last_name"], "Greate")
        self.assertEqual(result["user"]["username"], "asdfghjkl")
        self.assertEqual(result["profile_picture"]["id"], 1)

    def test_user_search(self):

        UserProfile.objects.create(user=self.user, first_name="Asdfg", last_name="oseni",
                                   caption="live is all about living", about="I'm a youtuber")

        user2 = CustomUser.objects._create_user(
            username="tester", password="test123")
        UserProfile.objects.create(user=user2, first_name="vergil", last_name="makabaka",
                                   caption="POWER", about="I'm a youtuber")

        user3 = CustomUser.objects._create_user(
            username="maskcf", password="vestdf123")

        UserProfile.objects.create(user=user3, first_name="asdfgh", last_name="lkuj",
                                   caption="POWER", about="I'm a youtuber")

        url = self.profile_url + "?keyword = asdfgh"

        response = self.client.get(url)
        result = response.json()["result"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["user"]["username"], "asdhdyusajk")

        url = self.profile_url + "?keyword = asd"

        response = self.client.get(url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["user"]["username"], "asdhdyusajk")
