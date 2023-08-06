import os
import secrets

USE_TZ = True
SECRET_KEY = secrets.token_hex()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "urltokenizer_test",
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": "localhost",
        "PORT": "5432",  # default postgresql port
    }
}

INSTALLED_APPS = ("tests",)

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = bool(os.getenv("EMAIL_USE_TLS"))

URL_TOKENIZER_SETTINGS = {
    # token
    "ENCODING_FIELD": "unique_id",
    "TIMEOUT": eval(os.getenv("URL_TOKENIZER_TIMEOUT")),
    "FAIL_SILENTLY": False,
    "VALIDATE_TOKEN_TYPE": True,
    # url
    "PROTOCOL": "https",
    "PORT": "443",
    "DOMAIN": os.getenv("DOMAIN"),
    # email
    "EMAIL_ENABLED": True,
    "EMAIL_FIELD": "email",
    # token config
    "TOKEN_CONFIG": {
        "default": {
            "path": "/",
        },
        "verify": {
            "path": "verify/",
            "attributes": ["verified", "verified_at"],
            "preconditions": {"active": True, "verified": False, "locked": False},
            "callbacks": [{"method": "verify"}],
            "email_subject": "Verify your account with the following link",
        },
        "activate": {
            "path": "activate/",
            "attributes": ["active"],
            "preconditions": {"active": False, "verified": True, "locked": False},
            "callbacks": [{"method": "activate"}],
            "email_subject": "Activate your account with the following link",
        },
        "deactivate": {
            "path": "deactivate/",
            "attributes": ["active"],
            "preconditions": {"active": True, "verified": True, "locked": False},
            "callbacks": [{"method": "deactivate"}],
            "email_subject": "Deactivate your account with the following link",
        },
        "eliminate": {
            "path": "eliminate/",
            "attributes": [],
            "preconditions": {"active": True, "verified": True, "locked": False},
            "callbacks": [{"method": "delete"}],
            "email_subject": "Eliminate your account with the following link",
        },
        "password-recovery": {
            "path": "password-recovery/",
            "attributes": ["password", "last_login"],
            "preconditions": {"active": True, "verified": True, "locked": False},
            "callbacks": [
                {
                    "method": "_set_password",
                    "defaults": {"raise_exception": True},
                }
            ],
            "email_subject": "Recover your password with the following link",
        },
    },
}
