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
PLUGINS = ["nautobot_ssot", "nautobot_plugin_nornir", "nautobot_device_onboarding"]

# Plugins configuration settings. These settings are used by various plugins that the user may have installed.
# Each key in the dictionary is the name of an installed plugin and its value is a dictionary of settings.
PLUGINS_CONFIG = {
    "nautobot_ssot": {
        "hide_example_jobs": True,
        "enable_bootstrap": is_truthy(os.getenv("NAUTOBOT_SSOT_ENABLE_BOOTSTRAP", "true")),
        "bootstrap_nautobot_environment_branch": os.getenv("NAUTOBOT_BOOTSTRAP_SSOT_ENVIRONMENT_BRANCH", "develop"),
        "bootstrap_models_to_sync": {
            "secret": True,
            "secrets_group": True,
            "git_repository": True,
            "dynamic_group": True,
            "computed_field": True,
            "custom_field": True,
            "tag": True,
            "graph_ql_query": True,
            "software": False,
            "software_image": False,
            "tenant_group": True,
            "tenant": True,
            "role": True,
            "manufacturer": True,
            "platform": True,
            "location_type": True,
            "location": True,
            "team": True,
            "contact": True,
            "provider": True,
            "provider_network": True,
            "circuit_type": True,
            "circuit": True,
            "circuit_termination": True,
            "namespace": True,
            "rir": True,
            "vlan_group": True,
            "vlan": True,
            "vrf": True,
            "prefix": True,
            "scheduled_job": True,
        },
    },
    "nautobot_plugin_nornir": {
        "nornir_settings": {
            "credentials": "nautobot_plugin_nornir.plugins.credentials.nautobot_secrets.CredentialsNautobotSecrets",
            "runner": {
                "plugin": "threaded",
                "options": {
                    "num_workers": 20,
                },
            },
        },
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
