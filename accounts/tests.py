from django.test import TestCase
from accounts.models import User


class UserModelTests(TestCase):
    """Unit tests for User model methods"""
    
    def test_get_total_points_method(self):
        """Test that get_total_points() returns the correct value"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        # Test default value
        self.assertEqual(user.get_total_points(), 0)
        
        # Test with custom value
        user.total_points = 150
        user.save()
        self.assertEqual(user.get_total_points(), 150)
        
        # Test that method returns the same as direct field access
        self.assertEqual(user.get_total_points(), user.total_points)
