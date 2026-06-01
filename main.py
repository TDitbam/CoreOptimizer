import time
import psutil
import os
import sys
from core.config_loader import load_config, get_targets, get_paths
from core.cpu_topology import split_p_e_cores, calculate_affinity_mask

# Platform detection for priority/affinity logic
IS_WINDOWS = os.name == 'nt'

def get_optimal_cores(exclude_core_0=True):
    """
    Returns detected P-cores and E-cores from cpu_topology based on setting.
    """
    return split_p_e_cores(exclude_core_0)

def set_process_priority(proc, priority_name, verbose=True):
    """
    Handles platform-specific priority settings.
    """
    priority_name = priority_name.upper()
    try:
        if IS_WINDOWS:
            # Windows Priority Classes
            if priority_name in ['HIGH', 'P-CORE']:
                p_class = psutil.HIGH_PRIORITY_CLASS
            elif priority_name in ['BELOW_NORMAL', 'E-CORE']:
                p_class = psutil.BELOW_NORMAL_PRIORITY_CLASS
            else:
                p_class = psutil.NORMAL_PRIORITY_CLASS
            proc.nice(p_class)
        else:
            # Linux/macOS Nice Value (-20 high priority, 19 low priority)
            if priority_name in ['HIGH', 'P-CORE']:
                nice_val = -10 # Higher priority
            elif priority_name in ['BELOW_NORMAL', 'E-CORE']:
                nice_val = 5   # Lower priority
            else:
                nice_val = 0
            proc.nice(nice_val)
        
        if verbose:
            print(f"[OK] Priority set for {proc.name()} to {priority_name}")
    except (psutil.AccessDenied, psutil.ZombieProcess, psutil.NoSuchProcess):
        pass

def set_process_cores(proc, cores_list):
    """Sets CPU affinity for the process."""
    try:
        proc.cpu_affinity(cores_list)
    except (psutil.AccessDenied, psutil.ZombieProcess, psutil.NoSuchProcess, NotImplementedError):
        pass

def optimize_processes(stop_event, default_interval):
    # Print targets info once if in CLI
    is_cli = stop_event is None
    if is_cli:
        config_preview = load_config()
        t_count = len(get_targets(config_preview))
        p_count = len(get_paths(config_preview))
        print(f"[*] Loaded: {t_count} Targets | {p_count} Managed Directories")
        print(f"[*] Interval: {config_preview['Settings'].get('interval', default_interval)}s")
        print("[*] Press Ctrl+C to stop.")

    while True:
        config = load_config()
        try:
            exclude_core_0 = config["Settings"].getboolean("exclude_core_0", fallback=True)
            interval = float(config["Settings"].get("interval", default_interval))
        except (ValueError, TypeError, KeyError):
            exclude_core_0 = True
            interval = default_interval
            
        p_cores, e_cores = get_optimal_cores(exclude_core_0)
        
        if not p_cores:
            if is_cli:
                print("[!] Unable to detect P-cores/E-cores. Sleeping.")
            if stop_event and stop_event.is_set():
                break
            time.sleep(interval)
            continue

        targets_map = {name.lower(): priority.upper() for name, priority in get_targets(config)}
        paths_list = [(path.lower().replace('\\', '/'), priority.upper()) for path, priority in get_paths(config)]
        
        # Iterate through processes
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                raw_name = proc.info['name']
                if not raw_name:
                    continue
                name = raw_name.lower()
                
                exe_path = proc.info['exe']
                if exe_path:
                    exe_path = exe_path.lower().replace('\\', '/')
                
                priority = None
                
                # Match 1: Filename
                if name in targets_map:
                    priority = targets_map[name]
                
                # Match 2: Path-based
                if not priority and exe_path:
                    for folder, p_val in paths_list:
                        if exe_path.startswith(folder):
                            priority = p_val
                            break
                
                if priority:
                    pid = proc.pid
                    
                    # Determine Cores
                    if priority in ['HIGH', 'P-CORE']:
                        cores_to_use = p_cores
                    elif priority == 'E-CORE':
                        cores_to_use = e_cores
                    else:
                        cores_to_use = list(range(psutil.cpu_count()))

                    # Determine Target Priority Class
                    if IS_WINDOWS:
                        if priority in ['HIGH', 'P-CORE']:
                            target_prio = psutil.HIGH_PRIORITY_CLASS
                        elif priority in ['BELOW_NORMAL', 'E-CORE']:
                            target_prio = psutil.BELOW_NORMAL_PRIORITY_CLASS
                        else:
                            target_prio = psutil.NORMAL_PRIORITY_CLASS
                    else:
                        if priority in ['HIGH', 'P-CORE']:
                            target_prio = -10
                        elif priority in ['BELOW_NORMAL', 'E-CORE']:
                            target_prio = 5
                        else:
                            target_prio = 0

                    try:
                        current_affinity = proc.cpu_affinity()
                        current_prio = proc.nice()
                        
                        changed = False
                        if sorted(current_affinity) != sorted(cores_to_use):
                            set_process_cores(proc, cores_to_use)
                            changed = True
                        
                        if current_prio != target_prio:
                            set_process_priority(proc, priority, verbose=False) # Silent in loop, we print below
                            changed = True
                            
                        if changed:
                            mask = calculate_affinity_mask(cores_to_use)
                            print(f"[OPT] PID: {pid} | Process: {raw_name} | Mode: {priority} | Mask: {hex(mask)} | Cores: {cores_to_use}")
                    except (psutil.AccessDenied, psutil.ZombieProcess, psutil.NoSuchProcess):
                        continue
                        
            except (psutil.AccessDenied, psutil.ZombieProcess, psutil.NoSuchProcess):
                continue

        # Sleep loop logic
        if stop_event and stop_event.is_set():
            print("\n[INFO] Optimization stopped.")
            break
            
        if not stop_event:
            time.sleep(interval)
        else:
            stop_event.wait(interval)

def run_cli():
    print("[*] Optimizing processes with CorePriority (CLI Mode)...")
    optimize_processes(None, 3.0)

def main():
    from gui.gui import App
    print("[*] Launching CorePriority GUI...")
    app = App()
    app.run()

if __name__ == '__main__':
    # Automatic Administrator Elevation for Windows
    if os.name == 'nt':
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("[*] Requesting Administrator privileges...")
            # Relaunch the program with admin rights
            script = os.path.abspath(sys.argv[0])
            params = ' '.join(sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
            sys.exit(0)

    try:
        # Check for --cli flag to run in terminal mode
        if "--cli" in sys.argv:
            run_cli()
        else:
            main()
    except KeyboardInterrupt:
        print("\n[!] Script interrupted by user.")
    except Exception as e:
        print(f"\n[!] Critical error: {e}")
