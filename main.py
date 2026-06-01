import time
import psutil
import os
import sys
from core.config_loader import load_config, get_targets, get_paths, save_config
from core.cpu_topology import split_p_e_cores, calculate_affinity_mask
from core.cleaner import clean_junk
from engine.cache import ProcessStateCache
from engine.enforcer import Enforcer
from engine.registry import ProcessRegistry
from policy.models import CorePool
from policy.engine import PolicyEngine

# Platform detection for priority/affinity logic
IS_WINDOWS = os.name == 'nt'

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

    # Initialize v3 Engine
    cache = ProcessStateCache()
    registry = ProcessRegistry()
    
    # Initial topology detection
    exclude_core_0 = True 
    disable_smt = False
    p_cores, e_cores = split_p_e_cores(exclude_core_0, disable_smt)
    core_pool = CorePool(performance_cores=p_cores, efficiency_cores=e_cores, is_hybrid=len(e_cores) > 0)
    
    enforcer = Enforcer(cache, core_pool)
    
    # Track topology settings for changes
    last_exclude_core_0 = exclude_core_0
    last_disable_smt = disable_smt

    while True:
        config = load_config()
        try:
            exclude_core_0 = config["Settings"].getboolean("exclude_core_0", fallback=True)
            disable_smt = config["Settings"].getboolean("disable_smt", fallback=False)
            auto_cleanup = config["Settings"].getboolean("auto_cleanup", fallback=False)
            last_cleanup = float(config["Settings"].get("last_cleanup", 0))
            interval = float(config["Settings"].get("interval", default_interval))
        except (ValueError, TypeError, KeyError):
            exclude_core_0 = True
            disable_smt = False
            auto_cleanup = False
            last_cleanup = 0
            interval = default_interval
            
        # Update CorePool if settings changed
        if exclude_core_0 != last_exclude_core_0 or disable_smt != last_disable_smt:
             p_cores, e_cores = split_p_e_cores(exclude_core_0, disable_smt)
             core_pool = CorePool(performance_cores=p_cores, efficiency_cores=e_cores, is_hybrid=len(e_cores) > 0)
             enforcer.core_pool = core_pool
             last_exclude_core_0 = exclude_core_0
             last_disable_smt = disable_smt

        # Policy Engine
        policy_engine = PolicyEngine(dict(get_targets(config)), get_paths(config))
            
        # Auto Cleanup Logic
        current_time = time.time()
        if auto_cleanup and (current_time - last_cleanup > 30):
            files, bytes_saved = clean_junk()
            config["Settings"]["last_cleanup"] = str(current_time)
            save_config(config)

        # Process Tracking
        active_pids = {}
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'create_time']):
            try:
                if not proc.info['pid'] or not proc.info['name']: continue
                
                # Get Decision
                exe_path = proc.info['exe'] or ""
                decision = policy_engine.decide(proc.info['name'], exe_path, disable_smt)
                
                # State Machine
                state = registry.update_or_create(proc.pid, proc.info['create_time'], exe_path)
                
                # Get cores from enforcer helper mapping (or recalculate)
                cores, _ = enforcer._map_decision_to_hardware(decision)
                
                # Enforce
                if enforcer.enforce(proc, state, decision):
                     mask = calculate_affinity_mask(cores)
                     print(f"[OPT] PID: {proc.pid} | Process: {proc.info['name']} | Mode: {decision.policy_type.value} | Mask: {hex(mask)} | Cores: {cores}")

                active_pids[registry.get_entry_key(proc.pid, proc.info['create_time'], exe_path)] = True
            except (psutil.AccessDenied, psutil.ZombieProcess, psutil.NoSuchProcess):
                continue
                
        registry.remove_stale(active_pids)

        # Sleep logic
        if stop_event and stop_event.is_set(): break
        if stop_event: stop_event.wait(interval)
        else: time.sleep(interval)

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
            # Detect if running as frozen EXE or script
            if getattr(sys, 'frozen', False):
                # Frozen EXE: sys.executable is the EXE path
                executable = sys.executable
                params = ' '.join(sys.argv[1:])
            else:
                # Script: sys.executable is python.exe, sys.argv[0] is the script
                executable = sys.executable
                params = f'"{os.path.abspath(sys.argv[0])}" ' + ' '.join(sys.argv[1:])
            
            ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, params, None, 1)
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
