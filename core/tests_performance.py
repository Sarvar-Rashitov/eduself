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

from core.models import (
    Subject, Topic, Question, Answer, TopicResult,
    Certificate, CertificateTest, MockExam
)

User = get_user_model()


class LeaderboardPerformanceTest(TestCase):
    """Test leaderboard query performance"""
    
    def setUp(self):
        self.users = []
        for i in range(100):
            user = User.objects.create_user(
                username=f'testuser{i}',
                email=f'test{i}@example.com',
                password='testpass123',
                total_points=i * 10
            )
            self.users.append(user)
        
        self.subject = Subject.objects.create(
            name='Test Subject',
            description='Test description'
        )
        
        self.topic = Topic.objects.create(
            name='Test Topic',
            subject=self.subject,
            description='Test topic description',
            time_limit=30,
            passing_score=60
        )
        
        self.questions = []
        for i in range(20):
            question = Question.objects.create(
                text=f'Question {i}',
                topic=self.topic,
                points=i + 1
            )
            
            for j in range(4):
                Answer.objects.create(
                    text=f'Answer {j}',
                    question=question,
                    is_correct=(j == 0)
                )
            
            self.questions.append(question)
        
        for user in self.users[:50]:
            for attempt in range(3):
                TopicResult.objects.create(
                    user=user,
                    topic=self.topic,
                    score=70 + attempt * 10,
                    earned_points=sum(q.points for q in self.questions[:10 + attempt * 5]),
                    user_answers=json.dumps({str(q.id): 1 for q in self.questions})
                )
    
    def test_global_leaderboard_performance(self):
        client = Client()
        client.force_login(self.users[0])
        
        start_time = time.time()
        
        connection.queries_log.clear()
        
        response = client.get(reverse('core:global_leaderboard'))
        
        end_time = time.time()
        query_time = end_time - start_time
        query_count = len(connection.queries)
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(query_time, 1.0, f"Global leaderboard took {query_time:.3f}s, should be < 1s")
        self.assertLess(query_count, 5, f"Global leaderboard used {query_count} queries, should be < 5")
        
        top_users = response.context['top_users']
        self.assertTrue(len(top_users) > 0)
        
        for i in range(len(top_users) - 1):
            self.assertGreaterEqual(
                top_users[i].total_points,
                top_users[i + 1].total_points,
                "Users should be ordered by total_points descending"
            )
    
    def test_topic_leaderboard_performance(self):
        client = Client()
        client.force_login(self.users[0])
        
        start_time = time.time()
        
        connection.queries_log.clear()
        
        response = client.get(reverse('core:topic_leaderboard', kwargs={'pk': self.topic.pk}))
        
        end_time = time.time()
        query_time = end_time - start_time
        query_count = len(connection.queries)
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(query_time, 2.0, f"Topic leaderboard took {query_time:.3f}s, should be < 2s")
        self.assertLess(query_count, 10, f"Topic leaderboard used {query_count} queries, should be < 10")
        
        top_results = response.context['top_results']
        self.assertTrue(len(top_results) > 0)
        
        for i in range(len(top_results) - 1):
            self.assertGreaterEqual(
                top_results[i].earned_points,
                top_results[i + 1].earned_points,
                "Results should be ordered by earned_points descending"
            )


class RealTimeScorePerformanceTest(TestCase):
    """Test real-time score update latency"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.subject = Subject.objects.create(
            name='Test Subject',
            description='Test description'
        )
        
        self.topic = Topic.objects.create(
            name='Test Topic',
            subject=self.subject,
            description='Test topic description',
            time_limit=30,
            passing_score=60
        )
        
        self.question = Question.objects.create(
            text='Test Question',
            topic=self.topic,
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
        client = Client()
        client.force_login(self.user)
        
        start_time = time.time()
        
        response = client.get(
            reverse('core:check_answer', kwargs={
                'question_id': self.question.id,
                'answer_id': self.correct_answer.id
            }),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 0.5, f"Answer check took {response_time:.3f}s, should be < 0.5s")
        
        data = json.loads(response.content)
        self.assertTrue(data['is_correct'])
        self.assertEqual(data['points_earned'], 5)
        self.assertEqual(data['question_points'], 5)
    
    def test_multiple_answer_checks_performance(self):
        client = Client()
        client.force_login(self.user)
        
        questions_answers = []
        for i in range(10):
            question = Question.objects.create(
                text=f'Question {i}',
                topic=self.topic,
                points=i + 1
            )
            
            correct_answer = Answer.objects.create(
                text=f'Correct Answer {i}',
                question=question,
                is_correct=True
            )
            
            questions_answers.append((question, correct_answer))
        
        start_time = time.time()
        
        for question, answer in questions_answers:
            response = client.get(
                reverse('core:check_answer', kwargs={
                    'question_id': question.id,
                    'answer_id': answer.id
                }),
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            self.assertEqual(response.status_code, 200)
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / len(questions_answers)
        
        self.assertLess(total_time, 2.0, f"10 answer checks took {total_time:.3f}s, should be < 2s")
        self.assertLess(avg_time, 0.2, f"Average answer check took {avg_time:.3f}s, should be < 0.2s")


class DatabaseQueryOptimizationTest(TestCase):
    """Test database query optimization"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.subject = Subject.objects.create(name='Test Subject')
        self.topic = Topic.objects.create(
            name='Test Topic',
            subject=self.subject,
            time_limit=30,
            passing_score=60
        )
        
        for i in range(5):
            question = Question.objects.create(
                text=f'Question {i}',
                topic=self.topic,
                points=i + 1
            )
            
            for j in range(4):
                Answer.objects.create(
                    text=f'Answer {j}',
                    question=question,
                    is_correct=(j == 0)
                )
    
    def test_question_prefetch_optimization(self):
        client = Client()
        client.force_login(self.user)
        
        connection.queries_log.clear()
        
        response = client.get(reverse('core:take_topic_test', kwargs={'pk': self.topic.pk}))
        
        query_count = len(connection.queries)
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(query_count, 10, f"Take test view used {query_count} queries, should be < 10")
    
    def test_leaderboard_select_related_optimization(self):
        for i in range(10):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='pass',
                total_points=i * 10
            )
            
            TopicResult.objects.create(
                user=user,
                topic=self.topic,
                score=80,
                earned_points=15,
                user_answers=json.dumps({})
            )
        
        client = Client()
        client.force_login(self.user)
        
        connection.queries_log.clear()
        
        response = client.get(reverse('core:topic_leaderboard', kwargs={'pk': self.topic.pk}))
        
        query_count = len(connection.queries)
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(query_count, 15, f"Topic leaderboard used {query_count} queries, should be < 15")


def run_performance_tests():
    import unittest
    
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.makeSuite(LeaderboardPerformanceTest))
    suite.addTest(unittest.makeSuite(RealTimeScorePerformanceTest))
    suite.addTest(unittest.makeSuite(DatabaseQueryOptimizationTest))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    run_performance_tests()
