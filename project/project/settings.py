import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "your-secret-key"
DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",  # Your app name here
#    "windows_auth",  # Keep it here if you want to enable it later
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Comment out the middleware for now
    # 'windows_auth.middleware.WindowsAuthenticationMiddleware',
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": "IEC",
        "USER": "IECApp",
        "PASSWORD": "Byre!UWXYa2e",
        "HOST": "NUTRA-DB01\\sqlexpress",
        "PORT": "",
        "OPTIONS": {
            "driver": "ODBC Driver 17 for SQL Server",
            "extra_params": "Trusted_Connection=no;",
        },
    }
}




AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# WINDOWS_AUTH = {
#     "CALLBACK": lambda request,
#     user,
#     domain,
#     username: None,  # Optional: callback for customizing user creation
#     "AUTO_CREATE_USER": True,  # Automatically create users in Django's database
#     "REMOVE_WINDOWS_GROUPS": [],  # Optional: groups to remove
#     "CREATE_WINDOWS_GROUPS": False,  # Optional: automatically create groups
# }
#
# WAUTH_DOMAINS = {
#     "NUTRASOURCE": {  # this is your domain's NetBIOS Name, same as in "EXAMPLE\\username" login scheme
#         "SERVER": "localhost",  # the FQDN of the DC server, usually is the FQDN of the domain itself
#         "SEARCH_BASE": "DC=example,DC=local",  # the default Search Base to use when searching
#         "USERNAME": "EXAMPLE\\bind_account",  # username of the account used to authenticate your Django project to Active Directory
#         "PASSWORD": "<super secret>",  # password for the binding account
#     },
#     'LDAP': {
#         'SERVER_URI': 'ldap://localhost',  # Fake URI
#         'SEARCH_BASE': 'DC=example,DC=com',  # Fake search base
#         'BIND_DN': 'CN=fakeuser,OU=Users,DC=example,DC=com',  # Fake bind DN
#         'BIND_PASSWORD': 'fakepassword',  # Fake bind password
#     },
# }
