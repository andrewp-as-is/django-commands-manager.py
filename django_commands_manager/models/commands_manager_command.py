from datetime import datetime, timedelta
import logging
import sys
from traceback import format_tb

from django.core.management import call_command
from django.db import models

from .commands_manager_exc import Exc
from .commands_manager_log import Log


class Command(models.Model):
    group = models.ForeignKey(
        'Group', related_name="command_set", on_delete=models.CASCADE)
    name = models.TextField()
    is_disabled = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    repeat_seconds = models.IntegerField(null=True)
    started_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'commands_manager_command'
        indexes = [
            models.Index(fields=["group"],),
            models.Index(fields=["is_disabled"],),
            models.Index(fields=["is_pending"],),
            models.Index(fields=["priority"],),
        ]
        unique_together = ['group', 'name']

    @property
    def expired_at(self):
        if not self.repeat_seconds or self.repeat_seconds <= 0:
            return
        if self.completed_at:
            return self.completed_at + timedelta(seconds=self.repeat_seconds)
        return datetime.now()

    def call_command(self):
        try:
            started_at = datetime.now()
            type(self).objects.filter(pk=self.pk).update(
                is_running=True,
                started_at=started_at
            )
            call_command(self.name)
            completed_at = datetime.now()
            type(self).objects.filter(pk=self.pk).update(
                is_pending=False,
                is_running=False,
                started_at=started_at,
                completed_at=completed_at
            )
            Log(
                command=self,
                started_at=started_at,
                completed_at=completed_at
            ).save()
        except Exception as e:
            logging.error(e, exc_info=True)
            exc, exc_value, tb = sys.exc_info()
            Exc(
                command=self,
                exc_type=exc.__name__,
                exc_value=exc_value if exc_value else '',
                exc_traceback='\n'.join(format_tb(tb))
            ).save()
