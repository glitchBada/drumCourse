from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_chat_id',
            field=models.CharField(
                blank=True,
                help_text='Заполняется автоматически при подключении через бот (/start).',
                max_length=30,
                null=True,
                unique=True,
                verbose_name='Telegram Chat ID',
            ),
        ),
    ]
