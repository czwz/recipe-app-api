from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating a new user with a new email is successful"""
        email = "test@dummy.com"
        password = "dummy123"
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """test email for a new user is normalized"""
        email = "test@DUMMY.COM"
        user = get_user_model().objects.create_user(email, "dummy123")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test a new user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "dummy123")

    def test_create_new_superuser(self):
        """test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            email="test@dummy.com",
            password="dummy123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
