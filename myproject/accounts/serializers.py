from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import OTPCode, User
from .validators import validate_phone_number


class RegisterSerializer(serializers.ModelSerializer):
    """Регистрация нового пользователя."""

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )
    phone_number = serializers.CharField(validators=[validate_phone_number])

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password',
            'password_confirm',
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name':  {'required': True},
        }

    def validate_first_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Имя не может быть пустым.')
        return value

    def validate_last_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Фамилия не может быть пустой.')
        return value

    def validate_email(self, value: str) -> str:
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже зарегистрирован.'
            )
        return value

    def validate_phone_number(self, value: str) -> str:
        value = value.strip()
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким номером телефона уже зарегистрирован.'
            )
        return value

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Пароли не совпадают.'})
        return attrs

    def create(self, validated_data: dict) -> User:
        email = validated_data['email']  # уже нормализован в validate_email
        password = validated_data.pop('password')

        user = User(
            # username обязателен в AbstractUser; используем email
            username=email,
            email=email,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            # Аккаунт неактивен до подтверждения email и телефона
            is_active=False,
        )
        user.set_password(password)  # хэширует через PBKDF2 (Django default)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Вход по email + пароль."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs: dict) -> dict:
        email = attrs['email'].strip().lower()
        password = attrs['password']

        # authenticate использует backend по USERNAME_FIELD ('email')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError(
                {'non_field_errors': 'Неверный email или пароль.'}
            )

        if not user.email_verified or not user.phone_verified:
            raise serializers.ValidationError(
                {'non_field_errors': (
                    'Аккаунт не подтверждён. '
                    'Проверьте email и WhatsApp для ввода кодов подтверждения.'
                )}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {'non_field_errors': 'Аккаунт деактивирован. Обратитесь в поддержку.'}
            )

        attrs['user'] = user
        return attrs


class OTPVerifySerializer(serializers.Serializer):
    """Подтверждение OTP-кода (email или телефон)."""

    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)
    purpose = serializers.ChoiceField(choices=OTPCode.Purpose.choices)

    def validate_email(self, value: str) -> str:
        return value.strip().lower()

    def validate_code(self, value: str) -> str:
        if not value.isdigit():
            raise serializers.ValidationError('Код должен содержать только цифры.')
        return value


class ResendOTPSerializer(serializers.Serializer):
    """Запрос на повторную отправку OTP-кода."""

    email = serializers.EmailField()
    purpose = serializers.ChoiceField(choices=OTPCode.Purpose.choices)

    def validate_email(self, value: str) -> str:
        return value.strip().lower()


class UserSerializer(serializers.ModelSerializer):
    """Публичные данные пользователя (для /me и личного кабинета)."""

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'email_verified',
            'phone_verified',
        ]
        read_only_fields = ['id', 'email', 'email_verified', 'phone_verified']
