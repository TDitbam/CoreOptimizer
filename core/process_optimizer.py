import psutil
import os
from core.cpu_topology import calculate_affinity_mask

HIGH_PRIORITY = psutil.HIGH_PRIORITY_CLASS

def optimize_process(proc, cores):
    """
    Optimizes a single process by setting its CPU affinity and priority.
    Includes robust error handling for system-level access issues.
    """
    try:
        # 1. Set CPU Affinity
        # psutil accepts a list of logical core IDs
        proc.cpu_affinity(cores)
        
        # Calculate bitmask for logging/verification as requested
        affinity_mask = calculate_affinity_mask(cores)
        
        # 2. Set Priority Class
        # On Windows, we use Priority Classes (HIGH_PRIORITY_CLASS = 0x00000080)
        if os.name == 'nt':
            proc.nice(psutil.HIGH_PRIORITY_CLASS)
        else:
            proc.nice(-10) # High priority on Unix

        print(
            f"[OK] Process: {proc.name()} (PID: {proc.pid}) | "
            f"Affinity Mask: {hex(affinity_mask)} | "
            f"Status: P-Core Optimized"
        )

    except psutil.NoSuchProcess:
        print(f"[DEBUG] Process PID {proc.pid} no longer exists.")
    except psutil.AccessDenied:
        print(f"[ERROR] Access Denied for PID {proc.pid}. Please run as Administrator.")
    except psutil.ZombieProcess:
        print(f"[DEBUG] PID {proc.pid} is a zombie process.")
    except Exception as e:
        print(f"[CRITICAL ERROR] Failed to optimize PID {proc.pid}: {e}")
