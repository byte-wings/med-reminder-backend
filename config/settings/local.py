from decouple import config

from . import BASE_DIR, INSTALLED_APPS, MIDDLEWARE

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*']

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INTERNAL_IPS = ["127.0.0.1"]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    # Display only for staff members
    # 'SHOW_TOOLBAR_CALLBACK': lambda request: request.users.is_staff,
    'RESULTS_CACHE_SIZE': 5,  # Store more query results for analysis
    'SQL_WARNING_THRESHOLD': 50,  # Lower threshold for quicker SQL query warnings
    'TAG': 'div',  # Change the toolbar tag to div
    'SHOW_COLLAPSED': True,  # Display the toolbar collapsed by default
    "ROOT_TAG_EXTRA_ATTRS": "data-turbo-permanent",
}
