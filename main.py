import os
import sys
from core.config_loader import load_config
from core.optimizer_engine import optimize_processes

# Platform detection for priority/affinity logic
IS_WINDOWS = os.name == 'nt'

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
