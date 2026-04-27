from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class RegisterThrottle(AnonRateThrottle):
    """5 попыток регистрации в час с одного IP."""
    scope = 'register'


class OTPVerifyThrottle(AnonRateThrottle):
    """15 попыток верификации OTP в час с одного IP."""
    scope = 'otp_verify'


class OTPResendThrottle(AnonRateThrottle):
    """5 переотправок OTP в час с одного IP."""
    scope = 'otp_resend'


class LoginThrottle(AnonRateThrottle):
    """10 попыток входа в час с одного IP."""
    scope = 'login'
