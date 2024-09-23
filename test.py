import uuid
import hashlib
import platform
import os
import sys

# Get machine-specific information (you can add more identifiers)
id = os.popen('wmic diskdrive get serialnumber').read()
print(id)

def get_machine_fingerprint():
    mac_address = hex(uuid.getnode())
    cpu_id = platform.processor()
    disk_serial = get_disk_serial()

    # Combine identifiers and create a hash
    fingerprint = f"{mac_address}-{cpu_id}-{disk_serial}"
    hashed_fingerprint = hashlib.sha256(fingerprint.encode()).hexdigest()

    return hashed_fingerprint

def get_disk_serial():
    if platform.system() == "Windows":
        # Windows specific way to get disk serial number
        return os.popen("wmic diskdrive get serialnumber").read().strip().split("\n")[1]
    else:
        # Example for Linux/MacOS (adjust as needed)
        return os.popen("diskutil info / | grep 'Disk Identifier'").read().split(":")[1].strip()

if __name__ == "__main__":
    machine_fingerprint = get_machine_fingerprint()
    print(f"Machine Fingerprint: {machine_fingerprint}")
