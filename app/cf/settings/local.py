from .base import *

SECRET_KEY = "django-insecure-410rdl2nv&n!cgv%wgg)+zvlzeo%_u2mer3eq-!7*&dwoo#s(w"

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "emails"
