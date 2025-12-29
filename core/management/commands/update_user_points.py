from django.core.management.base import BaseCommand
from django.db.models import Sum
from accounts.models import User
from core.models import TopicResult, CertificateResult, MockExamResult


class Command(BaseCommand):
    help = 'Barcha foydalanuvchilarning total_points maydonini yangilash'

    def handle(self, *args, **options):
        users = User.objects.all()
        updated_count = 0
        
        for user in users:
            # Mavzu testlaridan balllar
            topic_points = TopicResult.objects.filter(user=user).aggregate(
                total=Sum('earned_points')
            )['total'] or 0
            
            # Sertifikat testlaridan balllar
            cert_points = CertificateResult.objects.filter(user=user).aggregate(
                total=Sum('earned_points')
            )['total'] or 0
            
            # Mock exam testlaridan balllar
            mock_points = MockExamResult.objects.filter(user=user).aggregate(
                total=Sum('earned_points')
            )['total'] or 0
            
            # Umumiy ball
            total_points = topic_points + cert_points + mock_points
            
            # Faqat o'zgargan bo'lsa yangilash
            if user.total_points != total_points:
                user.total_points = total_points
                user.save(update_fields=['total_points'])
                updated_count += 1
                
                self.stdout.write(
                    f"Yangilandi: {user.username} - {total_points} ball "
                    f"(Topic: {topic_points}, Cert: {cert_points}, Mock: {mock_points})"
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Muvaffaqiyatli yakunlandi! {updated_count} foydalanuvchi yangilandi.'
            )
        )