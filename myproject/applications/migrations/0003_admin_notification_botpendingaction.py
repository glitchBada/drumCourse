import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_redesign_application'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=30, verbose_name='Telegram Chat ID администратора')),
                ('message_id', models.CharField(max_length=30, verbose_name='ID сообщения в Telegram')),
                ('is_active', models.BooleanField(default=True, verbose_name='Кнопки активны')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='admin_notifications',
                    to='applications.application',
                    verbose_name='Заявка',
                )),
            ],
            options={
                'verbose_name': 'Уведомление администратора',
                'verbose_name_plural': 'Уведомления администраторов',
            },
        ),
        migrations.AddConstraint(
            model_name='adminnotification',
            constraint=models.UniqueConstraint(
                fields=['application', 'chat_id'],
                name='unique_application_chat',
            ),
        ),
        migrations.CreateModel(
            name='BotPendingAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=30, verbose_name='Telegram Chat ID администратора')),
                ('action', models.CharField(
                    choices=[('approve', 'Одобрить'), ('cancel', 'Отменить')],
                    max_length=10,
                    verbose_name='Действие',
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='pending_action',
                    to='applications.application',
                    verbose_name='Заявка',
                )),
            ],
            options={
                'verbose_name': 'Ожидающее действие бота',
                'verbose_name_plural': 'Ожидающие действия бота',
            },
        ),
    ]
