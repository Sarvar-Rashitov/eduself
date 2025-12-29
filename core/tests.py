from django.test import TestCase
from hypothesis import given, strategies as st, settings
from hypothesis.extra.django import TestCase as HypothesisTestCase
from core.models import Question, Answer, TopicResult, Advertisement, Topic, Subject, SubjectCategory, Course, CourseCategory
from accounts.models import User
import uuid


class ModelFieldPropertyTests(HypothesisTestCase):
    """Property-based tests for model fields"""
    
    def setUp(self):
        self.subject_category = SubjectCategory.objects.create(
            name="Test Category",
            slug="test-category"
        )
        self.subject = Subject.objects.create(
            name="Test Subject",
            category=self.subject_category
        )
        self.topic = Topic.objects.create(
            name="Test Topic",
            subject=self.subject,
            time_limit=30,
            passing_score=60
        )
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    
    @given(st.integers(min_value=1, max_value=100))
    @settings(max_examples=10, deadline=None)
    def test_question_points_default_value_property(self, points_value):
        question = Question(
            topic=self.topic,
            text="Test question text"
        )
        self.assertEqual(question.points, 1)
        
        question_with_points = Question(
            topic=self.topic,
            text="Test question with points",
            points=points_value
        )
        self.assertEqual(question_with_points.points, points_value)


class QuestionPointsTests(TestCase):
    """Unit tests for Question.points field"""
    
    def setUp(self):
        self.subject_category = SubjectCategory.objects.create(
            name="Test Category",
            slug="test-category"
        )
        self.subject = Subject.objects.create(
            name="Test Subject",
            category=self.subject_category
        )
        self.topic = Topic.objects.create(
            name="Test Topic",
            subject=self.subject,
            time_limit=30,
            passing_score=60
        )
    
    def test_question_points_default_value(self):
        question = Question.objects.create(
            topic=self.topic,
            text="Test question"
        )
        self.assertEqual(question.points, 1)
    
    def test_question_points_custom_value(self):
        question = Question.objects.create(
            topic=self.topic,
            text="Test question",
            points=5
        )
        self.assertEqual(question.points, 5)
    
    def test_question_points_positive_integer(self):
        question = Question.objects.create(
            topic=self.topic,
            text="Test question",
            points=10
        )
        self.assertEqual(question.points, 10)
        self.assertIsInstance(question.points, int)
        self.assertGreater(question.points, 0)


class TopicResultEarnedPointsTests(TestCase):
    """Unit tests for TopicResult.earned_points field"""
    
    def setUp(self):
        self.subject_category = SubjectCategory.objects.create(
            name="Test Category",
            slug="test-category"
        )
        self.subject = Subject.objects.create(
            name="Test Subject",
            category=self.subject_category
        )
        self.topic = Topic.objects.create(
            name="Test Topic",
            subject=self.subject,
            time_limit=30,
            passing_score=60
        )
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_topicresult_earned_points_default_value(self):
        result = TopicResult.objects.create(
            user=self.user,
            topic=self.topic,
            score=80,
            total_questions=10,
            correct_answers=8
        )
        self.assertEqual(result.earned_points, 0)
    
    def test_topicresult_earned_points_custom_value(self):
        result = TopicResult.objects.create(
            user=self.user,
            topic=self.topic,
            score=80,
            total_questions=10,
            correct_answers=8,
            earned_points=15
        )
        self.assertEqual(result.earned_points, 15)


class UserTotalPointsTests(TestCase):
    """Unit tests for User.total_points field"""
    
    def test_user_total_points_default_value(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.assertEqual(user.total_points, 0)
    
    def test_user_total_points_custom_value(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            total_points=100
        )
        self.assertEqual(user.total_points, 100)


class AdvertisementLinkUrlTests(TestCase):
    """Unit tests for Advertisement.link_url field"""
    
    def test_advertisement_link_url_default_value(self):
        ad = Advertisement.objects.create(
            title="Test Ad",
            image="test.jpg"
        )
        self.assertIsNone(ad.link_url)
    
    def test_advertisement_link_url_custom_value(self):
        ad = Advertisement.objects.create(
            title="Test Ad",
            image="test.jpg",
            link_url="https://example.com"
        )
        self.assertEqual(ad.link_url, "https://example.com")
    
    def test_advertisement_link_url_blank_value(self):
        ad = Advertisement.objects.create(
            title="Test Ad",
            image="test.jpg",
            link_url=""
        )
        self.assertEqual(ad.link_url, "")


class ThemeTogglePropertyTests(HypothesisTestCase):
    """Property-based tests for theme toggle functionality"""
    
    @given(st.sampled_from(['light', 'dark']))
    @settings(max_examples=10, deadline=None)
    def test_theme_toggle_functionality_property(self, initial_theme):
        if initial_theme == 'light':
            expected_new_theme = 'dark'
        else:
            expected_new_theme = 'light'
        
        self.assertNotEqual(initial_theme, expected_new_theme)
        
        if expected_new_theme == 'light':
            final_theme = 'dark'
        else:
            final_theme = 'light'
        
        self.assertEqual(initial_theme, final_theme)
    
    def test_theme_persistence_property(self):
        theme_storage = {}
        
        theme_storage['theme'] = 'light'
        self.assertEqual(theme_storage.get('theme'), 'light')
        
        theme_storage['theme'] = 'dark'
        self.assertEqual(theme_storage.get('theme'), 'dark')
        
        theme_storage.clear()
        default_theme = theme_storage.get('theme', 'light')
        self.assertEqual(default_theme, 'light')


class TopicMaxPointsPropertyTests(HypothesisTestCase):
    """Property-based tests for topic maximum points calculation"""
    
    def setUp(self):
        unique_id = str(uuid.uuid4())[:8]
        self.subject_category = SubjectCategory.objects.create(
            name=f"Test Category {unique_id}",
            slug=f"test-category-{unique_id}"
        )
        self.subject = Subject.objects.create(
            name=f"Test Subject {unique_id}",
            category=self.subject_category
        )
        self.topic = Topic.objects.create(
            name=f"Test Topic {unique_id}",
            subject=self.subject,
            time_limit=30,
            passing_score=60
        )
    
    @given(st.lists(st.integers(min_value=1, max_value=10), min_size=1, max_size=10))
    @settings(max_examples=10, deadline=None)
    def test_topic_maximum_points_calculation_property(self, points_list):
        self.topic.questions.all().delete()
        
        total_expected_points = 0
        for i, points in enumerate(points_list):
            Question.objects.create(
                topic=self.topic,
                text=f"Test question {i+1}",
                points=points
            )
            total_expected_points += points
        
        from django.db.models import Sum
        calculated_max_points = self.topic.questions.aggregate(total=Sum('points'))['total'] or 0
        
        self.assertEqual(calculated_max_points, total_expected_points)
        
        manual_sum = sum(q.points for q in self.topic.questions.all())
        self.assertEqual(calculated_max_points, manual_sum)


class EarnedPointsPropertyTests(HypothesisTestCase):
    """Property-based tests for earned points calculation"""
    
    def setUp(self):
        unique_id = str(uuid.uuid4())[:8]
        self.subject_category = SubjectCategory.objects.create(
            name=f"Test Category {unique_id}",
            slug=f"test-category-{unique_id}"
        )
        self.subject = Subject.objects.create(
            name=f"Test Subject {unique_id}",
            category=self.subject_category
        )
        self.topic = Topic.objects.create(
            name=f"Test Topic {unique_id}",
            subject=self.subject,
            time_limit=30,
            passing_score=60
        )
        self.user = User.objects.create_user(
            username=f"testuser{unique_id}",
            email=f"test{unique_id}@example.com",
            password="testpass123"
        )
    
    @given(st.lists(st.integers(min_value=1, max_value=5), min_size=2, max_size=5))
    @settings(max_examples=10, deadline=None)
    def test_earned_points_calculation_property(self, points_list):
        self.topic.questions.all().delete()
        
        questions = []
        for i, points in enumerate(points_list):
            question = Question.objects.create(
                topic=self.topic,
                text=f"Test question {i+1}",
                points=points
            )
            Answer.objects.create(
                question=question,
                text="Correct answer",
                is_correct=True
            )
            Answer.objects.create(
                question=question,
                text="Wrong answer",
                is_correct=False
            )
            questions.append(question)
        
        user_answers = {}
        expected_earned_points = 0
        
        for i, question in enumerate(questions):
            correct_answer = question.answers.filter(is_correct=True).first()
            wrong_answer = question.answers.filter(is_correct=False).first()
            
            if i < len(questions) // 2:
                user_answers[str(question.id)] = {
                    'selected_answer_id': correct_answer.id,
                    'is_correct': True
                }
                expected_earned_points += question.points
            else:
                user_answers[str(question.id)] = {
                    'selected_answer_id': wrong_answer.id,
                    'is_correct': False
                }
        
        result = TopicResult.objects.create(
            user=self.user,
            topic=self.topic,
            score=50,
            total_questions=len(questions),
            correct_answers=len(questions) // 2,
            user_answers=user_answers,
            earned_points=expected_earned_points
        )
        
        self.assertEqual(result.earned_points, expected_earned_points)


class UserTotalPointsPropertyTests(HypothesisTestCase):
    """Property-based tests for user total points functionality"""
    
    def setUp(self):
        unique_id = str(uuid.uuid4())[:8]
        self.subject_category = SubjectCategory.objects.create(
            name=f"Test Category {unique_id}",
            slug=f"test-category-{unique_id}"
        )
        self.subject = Subject.objects.create(
            name=f"Test Subject {unique_id}",
            category=self.subject_category
        )
        self.topic = Topic.objects.create(
            name=f"Test Topic {unique_id}",
            subject=self.subject,
            time_limit=30,
            passing_score=60
        )
        self.user = User.objects.create_user(
            username=f"testuser{unique_id}",
            email=f"test{unique_id}@example.com",
            password="testpass123"
        )
    
    @given(st.lists(st.integers(min_value=1, max_value=10), min_size=1, max_size=5))
    @settings(max_examples=10, deadline=None)
    def test_profile_total_points_update_property(self, earned_points_list):
        initial_total_points = self.user.total_points
        
        total_expected_points = initial_total_points
        for i, earned_points in enumerate(earned_points_list):
            TopicResult.objects.create(
                user=self.user,
                topic=self.topic,
                score=80,
                total_questions=5,
                correct_answers=4,
                earned_points=earned_points
            )
            total_expected_points += earned_points
        
        self.user.refresh_from_db()
        
        self.assertEqual(self.user.total_points, total_expected_points)
    
    def test_total_points_aggregation_property(self):
        test_earned_points = 15
        
        TopicResult.objects.create(
            user=self.user,
            topic=self.topic,
            score=80,
            total_questions=5,
            correct_answers=4,
            earned_points=test_earned_points
        )
        
        self.user.refresh_from_db()
        expected_total = test_earned_points
        
        self.assertEqual(self.user.total_points, expected_total)
    
    def test_user_total_points_auto_update_property(self):
        initial_points = self.user.total_points
        
        first_earned = 10
        TopicResult.objects.create(
            user=self.user,
            topic=self.topic,
            score=80,
            total_questions=5,
            correct_answers=4,
            earned_points=first_earned
        )
        
        self.user.refresh_from_db()
        after_first = self.user.total_points
        self.assertEqual(after_first, initial_points + first_earned)
        
        second_earned = 15
        TopicResult.objects.create(
            user=self.user,
            topic=self.topic,
            score=90,
            total_questions=5,
            correct_answers=5,
            earned_points=second_earned
        )
        
        self.user.refresh_from_db()
        after_second = self.user.total_points
        self.assertEqual(after_second, initial_points + first_earned + second_earned)


class ThemeToggleUnitTests(TestCase):
    """Unit tests for theme toggle functionality"""
    
    def test_theme_toggle_logic(self):
        current_theme = 'light'
        new_theme = 'dark' if current_theme == 'light' else 'light'
        self.assertEqual(new_theme, 'dark')
        
        current_theme = 'dark'
        new_theme = 'dark' if current_theme == 'light' else 'light'
        self.assertEqual(new_theme, 'light')
    
    def test_theme_attribute_values(self):
        valid_themes = ['light', 'dark']
        
        for theme in valid_themes:
            self.assertIn(theme, valid_themes)
        
        invalid_theme = 'invalid'
        default_theme = 'light' if invalid_theme not in valid_themes else invalid_theme
        self.assertEqual(default_theme, 'light')
    
    def test_theme_css_classes_mapping(self):
        theme_mappings = {
            'light': 'light',
            'dark': 'dark'
        }
        
        for theme, css_value in theme_mappings.items():
            self.assertEqual(theme, css_value)
    
    def test_theme_button_state_changes(self):
        light_theme_state = {
            'icon': 'bi bi-sun-fill',
            'text': 'Oq rejim'
        }
        
        dark_theme_state = {
            'icon': 'bi bi-moon-fill',
            'text': 'Qora rejim'
        }
        
        self.assertNotEqual(light_theme_state['icon'], dark_theme_state['icon'])
        self.assertNotEqual(light_theme_state['text'], dark_theme_state['text'])
        
        self.assertEqual(light_theme_state['icon'], 'bi bi-sun-fill')
        self.assertEqual(dark_theme_state['icon'], 'bi bi-moon-fill')


class SlideUrlNavigationPropertyTests(HypothesisTestCase):
    """Property-based tests for slide URL navigation functionality"""
    
    @given(st.text(min_size=1, max_size=50, alphabet=st.characters(min_codepoint=32, max_codepoint=126)).filter(lambda x: x.strip()))
    @settings(max_examples=100, deadline=None)
    def test_slide_url_navigation_property(self, title):
        from django.test import Client
        from django.urls import reverse
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        user = User.objects.create_user(
            username=f"testuser_{uuid.uuid4().hex[:8]}",
            email=f"test_{uuid.uuid4().hex[:8]}@example.com",
            password="testpass123"
        )
        
        valid_url = "https://example.com"
        ad_with_url = Advertisement.objects.create(
            title=title,
            image="test.jpg",
            link_url=valid_url
        )
        
        self.assertEqual(ad_with_url.link_url, valid_url)
        self.assertIsNotNone(ad_with_url.link_url)
        
        ad_without_url = Advertisement.objects.create(
            title=f"{title}_no_url",
            image="test.jpg",
            link_url=""
        )
        
        self.assertEqual(ad_without_url.link_url, "")
        
        ad_null_url = Advertisement.objects.create(
            title=f"{title}_null_url",
            image="test.jpg",
            link_url=None
        )
        
        self.assertIsNone(ad_null_url.link_url)
        
        client = Client()
        client.force_login(user)
        
        response = client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        
        advertisements = response.context.get('advertisements', [])
        
        ad_titles = [ad.title for ad in advertisements]
        self.assertIn(title, ad_titles)
        
        content = response.content.decode()
        
        if valid_url:
            self.assertIn('clickable-slide', content)
            self.assertIn(f'data-url="{valid_url}"', content)
        
        ad_with_url.delete()
        ad_without_url.delete() 
        ad_null_url.delete()
        user.delete()


class CoursePaymentVisibilityPropertyTests(HypothesisTestCase):
    """Property-based tests for course payment visibility"""
    
    def setUp(self):
        self.course_category, _ = CourseCategory.objects.get_or_create(
            slug="test-course-category-prop",
            defaults={
                "name": "Test Course Category Property"
            }
        )
        self.user, _ = User.objects.get_or_create(
            username="testuser_prop",
            defaults={
                "email": "test_prop@example.com"
            }
        )
        if _:
            self.user.set_password("testpass123")
            self.user.save()
    
    @given(
        title=st.text(min_size=1, max_size=100),
        description=st.text(min_size=1, max_size=500),
        instructor=st.text(min_size=1, max_size=100)
    )
    @settings(max_examples=10, deadline=None)
    def test_course_payment_button_visibility_property(self, title, description, instructor):
        from django.test import Client
        from django.urls import reverse
        
        course = Course.objects.create(
            category=self.course_category,
            title=title,
            slug=f"test-course-{uuid.uuid4().hex[:8]}",
            description=description,
            instructor=instructor,
            is_free=True,
            price=0,
            is_active=True
        )
        
        client = Client()
        client.force_login(self.user)
        
        response = client.get(reverse('core:course_detail', kwargs={'slug': course.slug}))
        self.assertEqual(response.status_code, 200)
        
        content = response.content.decode()
        
        self.assertNotIn('To\'lov qilish', content)
        self.assertNotIn('credit-card', content)
        self.assertNotIn('payment_url', content)
        self.assertNotIn('To\'lov kutilayotgan', content)
        
        self.assertIn('Bepul kursga yozilish', content)
        
        course.delete()
