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

    load_short = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    load_med = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    load_long = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    memory_total_kb = models.IntegerField(null=True)

    memory_free_kb = models.IntegerField(null=True)

    memory_used_kb = models.IntegerField(null=True)

    memory_avail_kb = models.IntegerField(null=True)

    battery_charge = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    battery_standby = models.BooleanField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["system", "timestamp"]),
        ]

    def load_json(self, data: dict):
        body: dict = data["body"]
        self.__load_loadavgs(body["load"])
        self.__load_cpu(body["cpu"])
        self.__load_memory(body["memory"])
        self.__load_storage(body["storage"])
        self.__load_temps(body["temps"])
        self.__load_fans(body["fans"])
        self.__load_battery(body["battery"])
        self.save()

    def __load_loadavgs(self, data: list):
        self.load_short = data[0]
        self.load_med = data[1]
        self.load_long = data[2]

    def __load_cpu(self, data: dict):
        for i in range(data["count"]):
            c = CPUCore(snapshot=self)
            c.number = i
            c.freq_mhz = data["freq_mhz"][i]
            c.usage = data["usage"][i]
            c.save()

    def __load_memory(self, data: dict):
        self.memory_total_kb = data["total_kb"]
        self.memory_free_kb = data["free_kb"]
        self.memory_used_kb = data["used_kb"]
        self.memory_avail_kb = data["available_kb"]

    def __load_storage(self, data: dict):
        for mountpoint, params in data.items():
            s = Storage(snapshot=self)
            s.mountpoint = mountpoint
            s.total_kb = params["total_kb"]
            s.free_kb = params["free_kb"]
            s.used_kb = params["used_kb"]
            s.utilization = params["utilization"]
            s.save()

    def __load_temps(self, data: dict):
        for group, sensors in data.items():
            for sensor in sensors:
                t = Temperature(snapshot=self)
                t.group = group
                t.name = sensor["name"]
                t.temp_c = sensor["temp_c"]
                t.save()
    
    def __load_fans(self, data: dict):
        for group, fans in data.items():
            for fan in fans:
                f = Fan(snapshot=self)
                f.group = group
                f.name = fan["name"]
                f.rpm = fan["rpm"]
                f.save()

    def __load_battery(self, data: dict):
        self.battery_charge = data["charge"]
        self.battery_standby = data["standby"]

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
