from rest_framework import serializers

from .models import Application


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заявки пользователем."""

    class Meta:
        model = Application
        fields = ['type', 'product', 'message']
        extra_kwargs = {
            'product': {'required': False},
            'message': {'required': False},
        }

    def validate(self, attrs):
        app_type = attrs.get('type')
        product = attrs.get('product')

        if app_type == Application.Type.PRODUCT and not product:
            raise serializers.ValidationError(
                {'product': 'Для заявки на заказ товара необходимо указать товар.'}
            )
        if app_type == Application.Type.TRIAL and product:
            raise serializers.ValidationError(
                {'product': 'Для заявки на пробный урок товар не нужен.'}
            )
        return attrs


class ApplicationSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения заявки пользователем (личный кабинет)."""

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    display_product_name = serializers.CharField(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'type', 'type_display',
            'display_product_name',
            'message',
            'status', 'status_display',
            'admin_comment',
            'created_at', 'updated_at',
        ]
        read_only_fields = fields


class AdminApplicationSerializer(serializers.ModelSerializer):
    """Сериализатор для администратора — включает личные данные пользователя."""

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    display_product_name = serializers.CharField(read_only=True)
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id',
            'type', 'type_display',
            'display_product_name',
            'message',
            'status', 'status_display',
            'admin_comment',
            'telegram_message_id',
            'created_at', 'updated_at',
            'user_info',
        ]

    def get_user_info(self, obj: Application) -> dict:
        u = obj.user
        return {
            'id':           u.id,
            'first_name':   u.first_name,
            'last_name':    u.last_name,
            'email':        u.email,
            'phone_number': u.phone_number,
        }


class AdminStatusUpdateSerializer(serializers.Serializer):
    """Тело запроса при смене статуса администратором."""

    comment = serializers.CharField(required=False, allow_blank=True, default='')
