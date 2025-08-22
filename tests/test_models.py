from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUserModel(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        """Test that we can create a user"""
        user = self.User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test that we can create a superuser"""
        user = self.User.objects.create_superuser(
            username="testadmin", email="admin@example.com", password="testpass123"
        )
        self.assertEqual(user.username, "testadmin")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
