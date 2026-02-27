"""
Lives System Test Script
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User, LivesSettings
from django.utils import timezone

print("=" * 60)
print("LIVES SYSTEM TEST")
print("=" * 60)

# 1. Test Lives Settings
print("\n1. Testing Lives Settings...")
settings = LivesSettings.get_settings()
print(f"   ✓ Daily lives: {settings.daily_lives}")
print(f"   ✓ Max lives: {settings.max_lives}")
print(f"   ✓ Refill time: {settings.refill_time_minutes} minutes")
print(f"   ✓ Lives cost on fail: {settings.lives_cost_on_fail}")
print(f"   ✓ Passing score: {settings.passing_score}%")
print(f"   ✓ System active: {settings.is_active}")

# 2. Test User Lives
print("\n2. Testing User Lives...")
user = User.objects.first()
if user:
    print(f"   User: {user.username}")
    print(f"   ✓ Current lives: {user.current_lives}")
    print(f"   ✓ Has lives: {user.has_lives()}")
    
    # Test get_lives_info
    lives_info = user.get_lives_info()
    print(f"   ✓ Lives info:")
    print(f"      - Current: {lives_info['current_lives']}/{lives_info['max_lives']}")
    print(f"      - Is full: {lives_info['is_full']}")
    print(f"      - System active: {lives_info['system_active']}")
    print(f"      - Next life in: {lives_info['next_life_in']}")
else:
    print("   ✗ No users found")

# 3. Test Lose Life
print("\n3. Testing Lose Life...")
if user and user.current_lives > 0:
    initial_lives = user.current_lives
    user.lose_life()
    print(f"   ✓ Lives before: {initial_lives}")
    print(f"   ✓ Lives after: {user.current_lives}")
    print(f"   ✓ Last life lost at: {user.last_life_lost_at}")
    
    # Restore life for next tests
    user.current_lives = initial_lives
    user.save()
    print(f"   ✓ Lives restored to: {user.current_lives}")

# 4. Test Daily Reset
print("\n4. Testing Daily Reset...")
if user:
    user.last_daily_reset = timezone.now().date() - timezone.timedelta(days=1)
    user.current_lives = 2
    user.save()
    print(f"   ✓ Set lives to 2 and last reset to yesterday")
    
    user.check_daily_lives_reset()
    print(f"   ✓ After daily reset: {user.current_lives} lives")
    print(f"   ✓ Last reset date: {user.last_daily_reset}")

# 5. Test Lives Methods
print("\n5. Testing Lives Methods...")
if user:
    # Test get_current_level
    current_level = user.get_current_level()
    print(f"   ✓ Current level: {current_level.name if current_level else 'None'}")
    
    # Test has_lives
    has_lives = user.has_lives()
    print(f"   ✓ Has lives: {has_lives}")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED!")
print("=" * 60)
print("\nNext steps:")
print("1. Open http://127.0.0.1:8000/ in browser")
print("2. Check header for lives display")
print("3. Go to profile page to see lives card")
print("4. Try taking a test and failing to see lives decrease")
print("5. Check admin panel at http://127.0.0.1:8000/admin/")
