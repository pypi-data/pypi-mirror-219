import environ

env = environ.Env(
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True),
)

SECRET_KEY = "dummy"

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("SENDGRID_API_KEY")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")

URLTOKENIZER_SETTINGS = {
    "ENCODING_FIELD": "unique_id",
    "PROTOCOL": "https",
    "PORT": "443",
    "DOMAIN": env("DOMAIN"),
    "EMAIL_ENABLED": True,
    "EMAIL_FIELD": "email",
    "VALIDATE_TOKEN_TYPE": True,
    "TOKEN_CONFIG": {
        "verify": {
            "attributes": ["verified", "verified_at"],
            "preconditions": {"active": True, "verified": False, "locked": False},
            "callbacks": [{"method": "verify"}],
            "email_subject": "Verify your account with the following link",
        },
        "activate": {
            "attributes": ["active"],
            "preconditions": {"active": False, "verified": True, "locked": False},
            "callbacks": [{"method": "activate"}],
            "email_subject": "Activate your account with the following link",
        },
        "deactivate": {
            "attributes": ["active"],
            "preconditions": {"active": True, "verified": True, "locked": False},
            "callbacks": [{"method": "deactivate"}],
            "email_subject": "Deactivate your account with the following link",
        },
        "eliminate": {
            "attributes": [],
            "preconditions": {"active": True, "verified": True, "locked": False},
            "callbacks": [{"method": "delete"}],
            "email_subject": "Eliminate your account with the following link",
        },
        "password-recovery": {
            "attributes": ["password"],
            "preconditions": {"active": True, "verified": True, "locked": False},
            "callbacks": [
                {
                    "method": "_set_password",
                    "kwargs": ["password", "password2"],
                    "defaults": {"raise_exception": True},
                }
            ],
            "email_subject": "Recover your password with the following link",
        },
    },
}
