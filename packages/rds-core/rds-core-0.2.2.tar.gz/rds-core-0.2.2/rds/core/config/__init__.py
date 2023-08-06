"""
Documentar.
"""
from dynaconf import Dynaconf
from rds.core.helpers import env

environment = env("ENVIRONMENT", "local")

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.yaml", "settings.toml"],
)
