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

    @staticmethod
    def create_from_json(system: System, data: dict):
        
        s = Snapshot.objects.create(system=system)
        s.__load_cpu(data["cpu"])
        s.__load_memory(data["memory"])
        s.__load_storage(data["storage"])
        s.__load_temps(data["temps"])
        s.__load_fans(data["fans"])
        s.__load_battery(data["battery"])

        s.save()

    def __load_cpu(self, data: dict):
        for i in range(data["count"]):
            c = CPUCore(snapshot=self)
            c.freq_mhz = data["freq_mhz"][i]
            c.usage = data["usage"][i]

    def __load_memory(self, data: dict):
        self.memory_total_kb = data["total_kb"]
        self.memory_free_kb = data["free_kb"]
        self.memory_used_kb = data["used_kb"]
        self.memory_avail_kb = data["available_kb"]

    def __load_storage(self, data: dict):
        pass

    def __load_temps(self, data: dict):
        pass
    
    def __load_fans(self, data: dict):
        pass

    def __load_battery(self, data: dict):
        pass

    


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
        Snapshot, on_delete=models.CASCADE, related_name="zfs_pools",
    )

    name = models.CharField(max_length=128)

    size = models.CharField(max_length=32)

    allocated = models.CharField(max_length=32)

    free = models.CharField(max_length=32)

    usage = models.DecimalField(max_digits=4, decimal_places=3)

    health = models.CharField(max_length=32)
