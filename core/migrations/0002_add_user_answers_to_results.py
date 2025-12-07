# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificateresult',
            name='user_answers',
            field=models.JSONField(blank=True, default=dict, verbose_name='Foydalanuvchi javoblari'),
        ),
        migrations.AddField(
            model_name='mockexamresult',
            name='user_answers',
            field=models.JSONField(blank=True, default=dict, verbose_name='Foydalanuvchi javoblari'),
        ),
    ]

