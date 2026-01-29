import psutil
import shutil
import platform
from datetime import datetime

LOGFILE = "system_monitor.log"

def get_cpu_usage():
    # Percent over 1 second for stability
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    return psutil.virtual_memory().percent

def get_free_disk_gb(path):
    total, used, free = shutil.disk_usage(path)
    return round(free / (1024 ** 3), 2)

def count_external_filesystems():
    partitions = psutil.disk_partitions(all=False)
    os_name = platform.system()

    external_count = 0

    for p in partitions:
        if os_name == "Linux":
            # Exclude root filesystem
            if p.mountpoint != "/":
                external_count += 1

        elif os_name == "Windows":
            # Exclude system drive (usually C:\)
            if not p.mountpoint.upper().startswith("C:\\"):
                external_count += 1

    return external_count

def main():
    cpu = get_cpu_usage()
    ram = get_ram_usage()

    # System partition
    system_path = "C:\\" if platform.system() == "Windows" else "/"
    free_disk = get_free_disk_gb(system_path)

    external_fs = count_external_filesystems()

    log_line = f"CPU={cpu},RAM={ram},DISK_FREE={free_disk},EXT_FS={external_fs}"

    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

if __name__ == "__main__":
    main()
