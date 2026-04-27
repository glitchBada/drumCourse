import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
        ('accounts', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        # Удаляем все старые поля
        migrations.RemoveField(model_name='application', name='first_name'),
        migrations.RemoveField(model_name='application', name='last_name'),
        migrations.RemoveField(model_name='application', name='phone_number'),
        migrations.RemoveField(model_name='application', name='email'),
        migrations.RemoveField(model_name='application', name='message'),

        # Добавляем новые поля
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='applications',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Пользователь',
                # null=True временно, чтобы миграция прошла на существующих строках
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='application',
            name='type',
            field=models.CharField(
                choices=[('product', 'Заказ товара'), ('trial', 'Пробный урок')],
                max_length=10,
                verbose_name='Тип заявки',
                default='product',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application',
            name='product',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='applications',
                to='store.product',
                verbose_name='Товар',
            ),
        ),
        migrations.AddField(
            model_name='application',
            name='product_name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Название товара'),
        ),
        migrations.AddField(
            model_name='application',
            name='message',
            field=models.TextField(blank=True, verbose_name='Сообщение пользователя'),
        ),
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'В ожидании'),
                    ('processing', 'В оформлении и доставке'),
                    ('cancelled', 'Отменён'),
                    ('delivered', 'Заказ доставлен'),
                ],
                default='pending',
                db_index=True,
                max_length=12,
                verbose_name='Статус',
            ),
        ),
        migrations.AddField(
            model_name='application',
            name='admin_comment',
            field=models.TextField(blank=True, verbose_name='Комментарий администратора'),
        ),
        migrations.AddField(
            model_name='application',
            name='telegram_message_id',
            field=models.CharField(blank=True, max_length=30, verbose_name='ID сообщения Telegram'),
        ),
        migrations.AddField(
            model_name='application',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),

        # Теперь убираем null=True с user (поле обязательно для новых записей)
        migrations.AlterField(
            model_name='application',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='applications',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Пользователь',
            ),
        ),

        # Обновляем Meta
        migrations.AlterModelOptions(
            name='application',
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
    ]
