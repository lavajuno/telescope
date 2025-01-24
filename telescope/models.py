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

    memory_total_kb = models.IntegerField()

    memory_free_kb = models.IntegerField()

    memory_used_kb = models.IntegerField()

    memory_avail_kb = models.IntegerField()

    battery_charge = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    battery_standby = models.BooleanField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["system", "timestamp"]),
        ]

class CPUCore(models.Model):
    snapshot = models.ForeignKey(
        Snapshot, on_delete=models.CASCADE, related_name="cpu_cores",
    )

    number = models.IntegerField()

    usage = models.DecimalField(max_digits=4, decimal_places=3)

    freq_mhz = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["snapshot", "number"]),
        ]

class Storage(models.Model):
    snapshot = models.ForeignKey(
        Snapshot, on_delete=models.CASCADE, related_name="storages",
    )

    device = models.CharField(max_length=128)

    mountpoint = models.CharField(max_length=256)

    filesystem = models.CharField(max_length=32)

    total_kb = models.IntegerField()

    free_kb = models.IntegerField()

    used_kb = models.IntegerField()

    utilization = models.DecimalField(max_digits=4, decimal_places=3)

    class Meta:
        indexes = [
            models.Index(fields=["snapshot", "device"]),
        ]

class Temperature(models.Model):
    snapshot = models.ForeignKey(
        Snapshot, on_delete=models.CASCADE, related_name="temps",
    )

    group = models.CharField(max_length=128)

    name = models.CharField(max_length=128)

    temp_c = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        indexes = [
            models.Index(fields=["snapshot", "group", "name"]),
        ]

class Fan(models.Model):
    snapshot = models.ForeignKey(
        Snapshot, on_delete=models.CASCADE, related_name="fans",
    )

    group = models.CharField(max_length=128)

    name = models.CharField(max_length=128)

    rpm = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["snapshot", "group", "name"]),
        ]

class ZFSPool(models.Model):
    snapshot = models.ForeignKey(
        Snapshot, on_delete=models.CASCADE, related_name="fans",
    )

    name = models.CharField(max_length=128)

    size = models.CharField(max_length=32)

    allocated = models.CharField(max_length=32)

    free = models.CharField(max_length=32)

    usage = models.DecimalField(max_digits=4, decimal_places=3)

    health = models.CharField(max_length=32)
