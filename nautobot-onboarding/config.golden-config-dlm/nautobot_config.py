"""Nautobot development configuration file."""

# pylint: disable=invalid-envvar-default
import os
import sys

from nautobot.core.settings import *  # noqa: F403  # pylint: disable=wildcard-import,unused-wildcard-import
from nautobot.core.settings_funcs import parse_redis_connection, is_truthy

#
# Debug
#

DEBUG = is_truthy(os.getenv("NAUTOBOT_DEBUG", False))
TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

# Do not sent metrics stats
INSTALLATION_METRICS_ENABLED = False

#
# Logging
#

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

#
# Redis
#

# Redis Cacheops
CACHEOPS_REDIS = parse_redis_connection(redis_database=1)

#
# Celery settings are not defined here because they can be overloaded with
# environment variables. By default they use `CACHES["default"]["LOCATION"]`.
#

# Enable installed plugins. Add the name of each plugin to the list.
# PLUGINS = ["nautobot_plugin_nornir", "nautobot_golden_config", "nautobot_device_lifecycle_mgmt", "nautobot_ssot"]
PLUGINS = ["nautobot_golden_config","nautobot_device_lifecycle_mgmt"]

# Plugins configuration settings. These settings are used by various plugins that the user may have installed.
# Each key in the dictionary is the name of an installed plugin and its value is a dictionary of settings.
PLUGINS_CONFIG = {
    "nautobot_plugin_nornir": {
        "nornir_settings": {
            "credentials": "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
            "runner": {
                "plugin": "threaded",
                "options": {
                    "num_workers": 20,
                },
            },
        },
    },
    "nautobot_golden_config": {
        "per_feature_bar_width": 0.15,
        "per_feature_width": 13,
        "per_feature_height": 4,
        "enable_backup": True,
        "enable_compliance": True,
        "enable_intended": True,
        "enable_sotagg": True,
        "enable_plan": True,
        "enable_deploy": True,
        "enable_postprocessing": False,
        "sot_agg_transposer": None,
        "postprocessing_callables": [],
        "postprocessing_subscribed": [],
        "jinja_env": {
            "undefined": "jinja2.StrictUndefined",
            "trim_blocks": True,
            "lstrip_blocks": False,
        },
        # "default_deploy_status": "Not Approved",
        # "get_custom_compliance": "my.custom_compliance.func"
    },
    "nautobot_device_lifecycle_mgmt": {
        "barchart_bar_width": float(os.environ.get("BARCHART_BAR_WIDTH", 0.1)),
        "barchart_width": int(os.environ.get("BARCHART_WIDTH", 12)),
        "barchart_height": int(os.environ.get("BARCHART_HEIGHT", 5)),
    },
}

# if OIDC is enabled in the environment, configure the OIDC settings
if str(os.environ.get("OIDC_ENABLED", "False")) == "True":
    # Authentication backend settings
    AUTHENTICATION_BACKENDS = [
        str(os.environ.get("AUTHENTICATION_BACKEND", "social_core.backends.open_id_connect.OpenIdConnectAuth")),
        "nautobot.core.authentication.ObjectPermissionBackend",
    ]

    SOCIAL_AUTH_OIDC_OIDC_ENDPOINT = str(os.environ.get("SOCIAL_AUTH_OIDC_OIDC_ENDPOINT", "https://localhost"))
    SOCIAL_AUTH_OIDC_KEY = str(os.environ.get("SOCIAL_AUTH_OIDC_KEY", "clientid"))
    SOCIAL_AUTH_OIDC_SECRET = str(os.environ.get("SOCIAL_AUTH_OIDC_SECRET", "clientsecret"))

    # The OIDC backend will check for a preferred_username key in the values 
    # returned by the server. If the username is under a different key, this can be overridden:
    # SOCIAL_AUTH_OIDC_USERNAME_KEY = 'nickname'

    # The default set of scopes requested are “openid”, “profile” and “email”. You can request additional claims, for example:
    # SOCIAL_AUTH_OIDC_SCOPE = ['groups']
    # and you can prevent the inclusion of the default scopes using:
    SOCIAL_AUTH_OIDC_IGNORE_DEFAULT_SCOPE = str(os.environ.get("SOCIAL_AUTH_OIDC_IGNORE_DEFAULT_SCOPE", "True")) == "True"
