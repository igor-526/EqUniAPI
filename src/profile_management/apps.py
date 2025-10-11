import time

from django.apps import AppConfig
from django.core.signals import request_started


class ProfileManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "profile_management"

    def ready(self):
        request_started.connect(self.run_startup_tasks, weak=False)

    def run_startup_tasks(self, sender, **kwargs):
        request_started.disconnect(self.run_startup_tasks)
        from .utils.set_user_groups import set_user_groups

        set_user_groups()
