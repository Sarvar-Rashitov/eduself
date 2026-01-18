# Generated manually to fix TelegramLoginToken expires_at field
from django.db import migrations, models
from django.utils import timezone
from datetime import timedelta


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20260118_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramlogintoken',
            name='expires_at',
            field=models.DateTimeField(default=timezone.now() + timedelta(minutes=5)),
            preserve_default=False,
        ),
    ]