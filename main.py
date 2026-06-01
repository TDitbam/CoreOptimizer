import os
import sys
from core.optimizer_engine import optimize_processes

def run_cli():
    print("[*] Optimizing processes with CorePriority (CLI Mode)...")
    optimize_processes(None, 3.0)

def main():
    from gui.gui import App
    print("[*] Launching CorePriority GUI...")
    app = App()
    app.mainloop()

if __name__ == '__main__':
    # Administrator Elevation Logic
    if os.name == 'nt':
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("[*] Requesting Administrator privileges...")
            executable = sys.executable
            if getattr(sys, 'frozen', False):
                params = ' '.join(sys.argv[1:])
            else:
                params = f'"{os.path.abspath(sys.argv[0])}" ' + ' '.join(sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, params, None, 1)
            sys.exit(0)

    try:
        if "--cli" in sys.argv: run_cli()
        else: main()
    except KeyboardInterrupt: print("\n[!] Stopped by user.")
    except Exception as e: print(f"\n[!] Critical error: {e}")
