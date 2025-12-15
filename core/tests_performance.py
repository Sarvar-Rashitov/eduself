"""
Performance tests for EduSelf platform
Testing leaderboard query performance and real-time score update latency
"""

import time
import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import connection
from django.test.utils import override_settings
from django.core.cache import cache

from core.models import (
    Subject, Topic, Test, Question, Answer, TestResult,
    Certificate, CertificateTest, MockExam
)

User = get_user_model()


class LeaderboardPerformanceTest(TestCase):
    """Test leaderboard query performance"""
    
    def setUp(self):
        """Create test data for performance testing"""
        # Create users
        self.users = []
        for i in range(100):  # Create 100 users for realistic testing
            user = User.objects.create_user(
                username=f'testuser{i}',
                email=f'test{i}@example.com',
                password='testpass123',
                total_points=i * 10  # Varying points
            )
            self.users.append(user)
        
        # Create subject and topic
        self.subject = Subject.objects.create(
            name='Test Subject',
            description='Test description'
        )
        
        self.topic = Topic.objects.create(
            name='Test Topic',
            subject=self.subject,
            description='Test topic description'
        )
        
        # Create test
        self.test = Test.objects.create(
            title='Performance Test',
            topic=self.topic,
            time_limit=30,
            is_active=True
        )
        
        # Create questions
        self.questions = []
        for i in range(20):  # 20 questions per test
            question = Question.objects.create(
                text=f'Question {i}',
                test=self.test,
                points=i + 1  # Varying points
            )
            
            # Create answers
            for j in range(4):
                Answer.objects.create(
                    text=f'Answer {j}',
                    question=question,
                    is_correct=(j == 0)  # First answer is correct
                )
            
            self.questions.append(question)
        
        # Create test results for performance testing
        for user in self.users[:50]:  # 50 users have taken the test
            for attempt in range(3):  # Each user has 3 attempts
                TestResult.objects.create(
                    user=user,
                    test=self.test,
                    score=70 + attempt * 10,  # Varying scores
                    earned_points=sum(q.points for q in self.questions[:10 + attempt * 5]),
                    user_answers=json.dumps({str(q.id): 1 for q in self.questions})
                )
    
    def test_global_leaderboard_performance(self):
        """Test global leaderboard query performance"""
        client = Client()
        client.force_login(self.users[0])
        
        # Measure query performance
        start_time = time.time()
        
        # Reset query count
        connection.queries_log.clear()
        
        response = client.get(reverse('global_leaderboard'))
        
        end_time = time.time()
        query_time = end_time - start_time
        query_count = len(connection.queries)
        
        # Performance assertions
        self.assertEqual(response.status_code, 200)
        self.assertLess(query_time, 1.0, f"Global leaderboard took {query_time:.3f}s, should be < 1s")
        self.assertLess(query_count, 5, f"Global leaderboard used {query_count} queries, should be < 5")
        
        # Check that top users are correctly ordered
        top_users = response.context['top_users']
        self.assertTrue(len(top_users) > 0)
        
        # Verify ordering
        for i in range(len(top_users) - 1):
            self.assertGreaterEqual(
                top_users[i].total_points,
                top_users[i + 1].total_points,
                "Users should be ordered by total_points descending"
            )
    
    def test_test_leaderboard_performance(self):
        """Test test-specific leaderboard query performance"""
        client = Client()
        client.force_login(self.users[0])
        
        # Measure query performance
        start_time = time.time()
        
        # Reset query count
        connection.queries_log.clear()
        
        response = client.get(reverse('test_leaderboard', kwargs={'pk': self.test.pk}))
        
        end_time = time.time()
        query_time = end_time - start_time
        query_count = len(connection.queries)
        
        # Performance assertions
        self.assertEqual(response.status_code, 200)
        self.assertLess(query_time, 2.0, f"Test leaderboard took {query_time:.3f}s, should be < 2s")
        self.assertLess(query_count, 10, f"Test leaderboard used {query_count} queries, should be < 10")
        
        # Check that results are correctly ordered
        top_results = response.context['top_results']
        self.assertTrue(len(top_results) > 0)
        
        # Verify ordering by earned_points
        for i in range(len(top_results) - 1):
            self.assertGreaterEqual(
                top_results[i].earned_points,
                top_results[i + 1].earned_points,
                "Results should be ordered by earned_points descending"
            )
    
    def test_leaderboard_with_large_dataset(self):
        """Test leaderboard performance with larger dataset"""
        # Create more users and results
        additional_users = []
        for i in range(100, 500):  # Add 400 more users
            user = User.objects.create_user(
                username=f'testuser{i}',
                email=f'test{i}@example.com',
                password='testpass123',
                total_points=i * 5
            )
            additional_users.append(user)
        
        # Add more test results
        for user in additional_users[:200]:  # 200 more users take the test
            TestResult.objects.create(
                user=user,
                test=self.test,
                score=60 + (user.id % 40),
                earned_points=sum(q.points for q in self.questions[:15]),
                user_answers=json.dumps({str(q.id): 1 for q in self.questions})
            )
        
        client = Client()
        client.force_login(self.users[0])
        
        # Test global leaderboard with larger dataset
        start_time = time.time()
        response = client.get(reverse('global_leaderboard'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 2.0, "Large dataset leaderboard should load in < 2s")
        
        # Should still return only top 100
        top_users = response.context['top_users']
        self.assertLessEqual(len(top_users), 100)


class RealTimeScorePerformanceTest(TestCase):
    """Test real-time score update latency"""
    
    def setUp(self):
        """Create test data for real-time score testing"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create subject and topic
        self.subject = Subject.objects.create(
            name='Test Subject',
            description='Test description'
        )
        
        self.topic = Topic.objects.create(
            name='Test Topic',
            subject=self.subject,
            description='Test topic description'
        )
        
        # Create test
        self.test = Test.objects.create(
            title='Real-time Test',
            topic=self.topic,
            time_limit=30,
            is_active=True
        )
        
        # Create question with answers
        self.question = Question.objects.create(
            text='Test Question',
            test=self.test,
            points=5
        )
        
        self.correct_answer = Answer.objects.create(
            text='Correct Answer',
            question=self.question,
            is_correct=True
        )
        
        self.wrong_answer = Answer.objects.create(
            text='Wrong Answer',
            question=self.question,
            is_correct=False
        )
    
    def test_check_answer_response_time(self):
        """Test AJAX answer checking response time"""
        client = Client()
        client.force_login(self.user)
        
        # Test correct answer response time
        start_time = time.time()
        
        response = client.get(
            reverse('check_answer', kwargs={
                'question_id': self.question.id,
                'answer_id': self.correct_answer.id
            }),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Performance assertions
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 0.5, f"Answer check took {response_time:.3f}s, should be < 0.5s")
        
        # Verify response content
        data = json.loads(response.content)
        self.assertTrue(data['is_correct'])
        self.assertEqual(data['points_earned'], 5)
        self.assertEqual(data['question_points'], 5)
    
    def test_multiple_answer_checks_performance(self):
        """Test performance of multiple rapid answer checks"""
        client = Client()
        client.force_login(self.user)
        
        # Create multiple questions
        questions_answers = []
        for i in range(10):
            question = Question.objects.create(
                text=f'Question {i}',
                test=self.test,
                points=i + 1
            )
            
            correct_answer = Answer.objects.create(
                text=f'Correct Answer {i}',
                question=question,
                is_correct=True
            )
            
            questions_answers.append((question, correct_answer))
        
        # Measure time for multiple checks
        start_time = time.time()
        
        for question, answer in questions_answers:
            response = client.get(
                reverse('check_answer', kwargs={
                    'question_id': question.id,
                    'answer_id': answer.id
                }),
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            self.assertEqual(response.status_code, 200)
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / len(questions_answers)
        
        # Performance assertions
        self.assertLess(total_time, 2.0, f"10 answer checks took {total_time:.3f}s, should be < 2s")
        self.assertLess(avg_time, 0.2, f"Average answer check took {avg_time:.3f}s, should be < 0.2s")
    
    def test_concurrent_answer_checks(self):
        """Test performance under concurrent requests"""
        import threading
        import queue
        
        client = Client()
        client.force_login(self.user)
        
        results_queue = queue.Queue()
        
        def check_answer_worker():
            """Worker function for concurrent testing"""
            start_time = time.time()
            response = client.get(
                reverse('check_answer', kwargs={
                    'question_id': self.question.id,
                    'answer_id': self.correct_answer.id
                }),
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            end_time = time.time()
            results_queue.put((response.status_code, end_time - start_time))
        
        # Create and start threads
        threads = []
        for _ in range(5):  # 5 concurrent requests
            thread = threading.Thread(target=check_answer_worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Collect results
        response_times = []
        while not results_queue.empty():
            status_code, response_time = results_queue.get()
            self.assertEqual(status_code, 200)
            response_times.append(response_time)
        
        # Performance assertions
        max_response_time = max(response_times)
        avg_response_time = sum(response_times) / len(response_times)
        
        self.assertLess(max_response_time, 1.0, f"Max concurrent response time {max_response_time:.3f}s, should be < 1s")
        self.assertLess(avg_response_time, 0.5, f"Avg concurrent response time {avg_response_time:.3f}s, should be < 0.5s")


class DatabaseQueryOptimizationTest(TestCase):
    """Test database query optimization"""
    
    def setUp(self):
        """Create test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test data
        self.subject = Subject.objects.create(name='Test Subject')
        self.topic = Topic.objects.create(name='Test Topic', subject=self.subject)
        self.test = Test.objects.create(title='Test', topic=self.topic, is_active=True)
        
        # Create questions with answers
        for i in range(5):
            question = Question.objects.create(
                text=f'Question {i}',
                test=self.test,
                points=i + 1
            )
            
            for j in range(4):
                Answer.objects.create(
                    text=f'Answer {j}',
                    question=question,
                    is_correct=(j == 0)
                )
    
    def test_question_prefetch_optimization(self):
        """Test that questions are properly prefetched with answers"""
        client = Client()
        client.force_login(self.user)
        
        # Reset query count
        connection.queries_log.clear()
        
        response = client.get(reverse('take_test', kwargs={'pk': self.test.pk}))
        
        query_count = len(connection.queries)
        
        self.assertEqual(response.status_code, 200)
        # Should use minimal queries due to prefetch_related
        self.assertLess(query_count, 10, f"Take test view used {query_count} queries, should be < 10")
    
    def test_leaderboard_select_related_optimization(self):
        """Test that leaderboard queries use select_related properly"""
        # Create test results
        for i in range(10):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='pass',
                total_points=i * 10
            )
            
            TestResult.objects.create(
                user=user,
                test=self.test,
                score=80,
                earned_points=15,
                user_answers=json.dumps({})
            )
        
        client = Client()
        client.force_login(self.user)
        
        # Reset query count
        connection.queries_log.clear()
        
        response = client.get(reverse('test_leaderboard', kwargs={'pk': self.test.pk}))
        
        query_count = len(connection.queries)
        
        self.assertEqual(response.status_code, 200)
        # Should use reasonable number of queries with proper optimization
        self.assertLess(query_count, 15, f"Test leaderboard used {query_count} queries, should be < 15")


def run_performance_tests():
    """Helper function to run all performance tests and report results"""
    import unittest
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTest(unittest.makeSuite(LeaderboardPerformanceTest))
    suite.addTest(unittest.makeSuite(RealTimeScorePerformanceTest))
    suite.addTest(unittest.makeSuite(DatabaseQueryOptimizationTest))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    run_performance_tests()