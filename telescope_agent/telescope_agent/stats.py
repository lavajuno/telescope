import psutil
import subprocess
import json

class Stats:
    @staticmethod
    def __is_valid_storage(device: str, mountpoint: str | None = None):
        device_valid = False
        for search in [
            "/dev/sd",
            "/dev/nvme",
            "/dev/hd",
            "/dev/scd"
            "/dev/mmcblk"
        ]:
            if device.startswith(search):
                device_valid = True
                break
        mountpoint_valid = True
        if mountpoint:
            for search in [
                "/var/snap",
            ]:
                if mountpoint.startswith(search):
                    mountpoint_valid = False
                    break
        return device_valid and mountpoint_valid
    
    @staticmethod
    def __storage_usage(path):
        disk = psutil.disk_usage(path)
        return {
            "total_kb": disk.total // 1024,
            "used_kb": disk.used // 1024,
            "free_kb": disk.free // 1024,
            "utilization": disk.percent / 100,
        }
    
    @staticmethod
    def __storage_smart(device: str):
        result = subprocess.run(
            [
                "sudo",
                "smartctl",
                "--attributes",
                "--health",
                "--info",
                "--json",
                device
            ],
            stdout=subprocess.PIPE
        )
        result.check_returncode()
        return json.loads(result.stdout)
    
    @staticmethod
    def load() -> dict[str]:
        return list(psutil.getloadavg())
    
    @staticmethod
    def cpu() -> dict[str]:
        cpu_count = psutil.cpu_count()
        cpu_physical = psutil.cpu_count(logical=False)
        cpu_usage = list(e / 100.0 for e in psutil.cpu_percent(interval=0.25, percpu=True))
        cpu_freq = list(e[0] for e in psutil.cpu_freq(percpu=True))
        return {
            "count": cpu_count,
            "physical": cpu_physical,
            "usage": cpu_usage,
            "freq_mhz": cpu_freq,
        }

    @staticmethod
    def memory() -> dict[str]:
        mem = psutil.virtual_memory()
        return {
            "total_kb": mem.total // 1024,
            "free_kb": mem.free // 1024,
            "used_kb": mem.used // 1024,
            "available_kb": mem.available // 1024,
        }
    
    @staticmethod
    def storage() -> dict[str]:
        partitions_raw = psutil.disk_partitions(all=False)
        storage = {}
        for p in partitions_raw:
            if Stats.__is_valid_storage(p.device, p.mountpoint):
                storage[p.mountpoint] = {
                    "device": p.device,
                    "filesystem": p.fstype,
                    "usage": Stats.__storage_usage(p.mountpoint),
                }
        return storage
    
    @staticmethod
    def smart(devices: list[str]) -> dict[str]:
        smart = {}
        for dev_name in devices:
            if Stats.__is_valid_storage(dev_name):
                device = smart.get(dev_name)
                if not device:
                    smart[dev_name] = Stats.__storage_smart(dev_name)
        return smart

    @staticmethod
    def temps() -> dict[str]:
        temps = psutil.sensors_temperatures()
        groups = {}
        for k, v in temps.items():
            group = []
            for sensor in v:
                group.append(
                    {
                        "name": sensor.label,
                        "temp_c": sensor.current,
                    }
                )
            groups[k] = group
        return groups

    @staticmethod
    def fans() -> dict[str]:
        fans = psutil.sensors_fans()
        groups = {}
        for k, v in fans.items():
            group = []
            for fan in v:
                group.append(
                    {
                        "name": fan.label,
                        "rpm": fan.current,
                    }
                )
            groups[k] = group
        return groups
    
    @staticmethod
    def battery() -> dict[str]:
        batt = psutil.sensors_battery()
        if batt is None:
            return {}
        return {
            "charge": batt.percent / 100,
            "standby": batt.power_plugged,
        }
    
    @staticmethod
    def all(smart_devices: list[str] = []):
        result = {
            "load": Stats.load(),
            "cpu": Stats.cpu(),
            "memory": Stats.memory(),
            "storage": Stats.storage(),
            "temps": Stats.temps(),
            "fans": Stats.fans(),
            "battery": Stats.battery(),
        }
        if smart_devices:
            result["smart"] = Stats.smart(smart_devices)
        return result

if __name__ == "__main__":
    print(json.dumps(Stats.all(), indent=4))
