from django.db import models
from django.utils import timezone

class System(models.Model):
    """
    """

    name = models.CharField(max_length=64, unique=True)
    agent_id = models.CharField(max_length=32, unique=True)
    agent_secret = models.CharField(max_length=64)

    class Meta:
        indexes = [
            models.Index(fields=["agent_id"]),
            models.Index(fields=["name"]),
        ]

class SystemRegistration(models.Model):
    """
    """

    agent_id = models.CharField(max_length=32)
    agent_secret = models.CharField(max_length=64)

    class Meta:
        indexes = [
            models.Index(fields=["agent_id"]),
        ]

class Snapshot(models.Model):
    """
    """

    system = models.ForeignKey(
        System, on_delete=models.CASCADE, related_name="snapshots"
    )

    timestamp = models.DateTimeField(default=timezone.now)

    body = models.JSONField(default=dict)

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["system", "timestamp"]),
        ]

