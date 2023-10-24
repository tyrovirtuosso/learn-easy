from typing import Optional

from django.contrib.auth import get_user_model
from django.test import TestCase

class UsersManagersTests(TestCase):
    """
    Test cases for custom user manager methods.
    """

    def test_create_user(self) -> None:
        """
        Test creating a standard user.
        """
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        
        # Check user properties
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        
        # Check if username is not available
        self.assertIsNone(user.username)

        # Check exceptions for invalid user creation
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self) -> None:
        """
        Test creating a superuser.
        """
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo")

        # Check admin user properties
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        # Check if username is not available
        self.assertIsNone(admin_user.username)

        # Check an exception for an invalid superuser creation
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)
