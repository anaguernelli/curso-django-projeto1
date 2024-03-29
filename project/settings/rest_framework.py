from datetime import timedelta
import os

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # este default abaixo serve para desativar o browser da nossa API,
    # porém é apenas uma opção desativá-la ou não
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

SIMPLE_JWT = {
    # duração de acesso ao token
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    # para quando expirar o acess token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'BLACKLIST_AFTER_ROTATION': False,

    'SIGNING_KEY': os.environ.get('SECRET_KEY_JWT', 'INSECURE'),

    'AUTH_HEADER_TYPES': ('Bearer',),
}
