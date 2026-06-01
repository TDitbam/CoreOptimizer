import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
import sys
import os
import psutil
import pystray
from PIL import Image
from core.config_loader import load_config, save_config, get_targets, get_paths
from core.cpu_topology import split_p_e_cores
from core.cleaner import clean_junk

def run_optimization(stop_event: threading.Event):
    from main import optimize_processes
    config = load_config()
    try:
        interval = float(config["Settings"].get("interval", 5.0))
    except (ValueError, TypeError):
        interval = 5.0
    optimize_processes(stop_event, interval)

# ตั้งค่าธีมการแสดงผลตั้งต้น
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("P-Core Optimizer Pro")
        self.geometry("950x700")

        self.running = False
        self.thread = None
        self.stop_event = threading.Event()
        self.config = load_config()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SYSTEM TRAY SETUP
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.icon = None

        # SIDEBAR
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="OPTIMIZER", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.dashboard_btn = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard)
        self.dashboard_btn.grid(row=1, column=0, padx=20, pady=10)

        self.settings_btn = ctk.CTkButton(self.sidebar_frame, text="Settings", command=self.show_settings)
        self.settings_btn.grid(row=2, column=0, padx=20, pady=10)
        
        self.cleanup_btn = ctk.CTkButton(self.sidebar_frame, text="Cleanup Junk", command=self.show_cleanup)
        self.cleanup_btn.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                               command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("Dark")

        # CONTENT FRAMES
        self.dashboard_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cleanup_frame = ctk.CTkFrame(self, fg_color="transparent")

        # Initialize textboxes before logging
        self.textbox = ctk.CTkTextbox(self.dashboard_frame, font=ctk.CTkFont(family="Consolas", size=12))
        self.clean_log = ctk.CTkTextbox(self.cleanup_frame, height=300)

        self.setup_dashboard()
        self.setup_settings()
        self.setup_cleanup()

        self.show_dashboard()
        self.setup_tray()

    def setup_tray(self):
        # Create a simple icon (e.g., a colored square)
        image = Image.new('RGB', (64, 64), color=(0, 120, 215))
        
        menu = pystray.Menu(
            pystray.MenuItem("Restore", self.show_window),
            pystray.MenuItem("Exit", self.quit_app)
        )
        self.icon = pystray.Icon("P-Core Optimizer", image, "P-Core Optimizer Pro", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

    def on_closing(self):
        self.withdraw()
        self.log("Minimized to tray.")

    def show_window(self, icon, item):
        self.deiconify()
        self.lift()

    def quit_app(self, icon, item):
        self.icon.stop()
        self.destroy()
        sys.exit()

    def setup_dashboard(self):
        for widget in self.dashboard_frame.winfo_children():
            if widget != self.textbox: widget.destroy()

        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        self.dashboard_frame.grid_rowconfigure(3, weight=1)

        self.status_card = ctk.CTkFrame(self.dashboard_frame, height=100)
        self.status_card.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.status_card.grid_columnconfigure(0, weight=1)

        self.status_var = ctk.StringVar(value="Status: RUNNING" if self.running else "Status: IDLE")
        self.status_label = ctk.CTkLabel(self.status_card, textvariable=self.status_var, 
                                         font=ctk.CTkFont(size=24, weight="bold"),
                                         text_color="#28a745" if self.running else "#ABB2BF")
        self.status_label.grid(row=0, column=0, pady=20)

        self.core_info_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.core_info_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.core_info_frame.grid_columnconfigure((0, 1), weight=1)

        try:
            exclude_core_0 = self.config["Settings"].getboolean("exclude_core_0", fallback=True)
            disable_smt = self.config["Settings"].getboolean("disable_smt", fallback=False)
        except (ValueError, TypeError):
            exclude_core_0 = True
            disable_smt = False
            
        p_cores, e_cores = split_p_e_cores(exclude_core_0, disable_smt)

        self.pcore_box = ctk.CTkFrame(self.core_info_frame)
        self.pcore_box.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        ctk.CTkLabel(self.pcore_box, text="P-CORES", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 0))
        ctk.CTkLabel(self.pcore_box, text=f"{len(p_cores)} Cores", font=ctk.CTkFont(size=18)).pack(pady=(0, 10))

        self.ecore_box = ctk.CTkFrame(self.core_info_frame)
        self.ecore_box.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        ctk.CTkLabel(self.ecore_box, text="E-CORES", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 0))
        ctk.CTkLabel(self.ecore_box, text=f"{len(e_cores)} Cores", font=ctk.CTkFont(size=18)).pack(pady=(0, 10))

        self.dash_control_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.dash_control_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        self.dash_control_frame.grid_columnconfigure((0, 1), weight=1)

        self.start_btn = ctk.CTkButton(self.dash_control_frame, text="START OPTIMIZER", height=45, fg_color="#28a745", 
                                       state="disabled" if self.running else "normal", command=self.start_service)
        self.start_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.stop_btn = ctk.CTkButton(self.dash_control_frame, text="STOP SERVICE", height=45, fg_color="#dc3545", 
                                      state="normal" if self.running else "disabled", command=self.stop_service)
        self.stop_btn.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        self.textbox.grid(row=3, column=0, sticky="nsew", padx=20, pady=20)
        if self.textbox.get("1.0", "end-1c") == "":
            self.log("🚀 System initialized and ready.")

    def setup_settings(self):
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.settings_frame.grid_rowconfigure(1, weight=1)
        
        self.general_frame = ctk.CTkFrame(self.settings_frame)
        self.general_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(self.general_frame, text="Interval:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
        self.interval_entry = ctk.CTkEntry(self.general_frame, width=50)
        self.interval_entry.pack(side="left", padx=5)
        self.interval_entry.insert(0, self.config["Settings"].get("interval", "5"))
        self.interval_entry.bind("<Return>", lambda e: self.save_settings_realtime())
        
        try:
            exclude_val = self.config["Settings"].getboolean("exclude_core_0", fallback=True)
            disable_smt_val = self.config["Settings"].getboolean("disable_smt", fallback=False)
            auto_cleanup_val = self.config["Settings"].getboolean("auto_cleanup", fallback=False)
        except (ValueError, TypeError):
            exclude_val = True
            disable_smt_val = False
            auto_cleanup_val = False
            
        self.exclude_core0_var = ctk.BooleanVar(value=exclude_val)
        ctk.CTkSwitch(self.general_frame, text="Exclude Core 0", variable=self.exclude_core0_var, command=self.save_settings_realtime).pack(side="left", padx=10)

        self.disable_smt_var = ctk.BooleanVar(value=disable_smt_val)
        ctk.CTkSwitch(self.general_frame, text="Disable SMT (Phys Only)", variable=self.disable_smt_var, command=self.save_settings_realtime).pack(side="left", padx=10)

        self.auto_cleanup_var = ctk.BooleanVar(value=auto_cleanup_val)
        ctk.CTkSwitch(self.general_frame, text="Auto Junk Cleanup", variable=self.auto_cleanup_var, command=self.save_settings_realtime).pack(side="left", padx=10)
        
        self.lists_frame = ctk.CTkTabview(self.settings_frame, height=450)
        self.lists_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        self.tab_games = self.lists_frame.add("Managed Games")
        self.tab_paths = self.lists_frame.add("Managed Directories")
        
        self.setup_games_tab()
        self.setup_paths_tab()

    def setup_games_tab(self):
        self.tab_games.grid_columnconfigure(0, weight=1)
        self.tab_games.grid_rowconfigure(0, weight=1)
        self.game_scroll = ctk.CTkScrollableFrame(self.tab_games)
        self.game_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.add_game_ui = ctk.CTkFrame(self.tab_games, fg_color="transparent")
        self.add_game_ui.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.new_game_entry = ctk.CTkEntry(self.add_game_ui, placeholder_text="game.exe")
        self.new_game_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.game_prio = ctk.CTkOptionMenu(self.add_game_ui, values=["P-CORE", "E-CORE", "NORMAL"], width=100)
        self.game_prio.pack(side="left", padx=5)
        self.game_prio.set("P-CORE")
        ctk.CTkButton(self.add_game_ui, text="Add", width=60, command=self.add_game).pack(side="right", padx=5)
        ctk.CTkButton(self.add_game_ui, text="Scan PC", width=80, fg_color="#6c757d", command=self.scan_games).pack(side="right", padx=5)
        self.refresh_game_list_ui()

    def setup_paths_tab(self):
        self.tab_paths.grid_columnconfigure(0, weight=1)
        self.tab_paths.grid_rowconfigure(0, weight=1)
        self.path_scroll = ctk.CTkScrollableFrame(self.tab_paths)
        self.path_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.add_path_ui = ctk.CTkFrame(self.tab_paths, fg_color="transparent")
        self.add_path_ui.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.path_prio = ctk.CTkOptionMenu(self.add_path_ui, values=["P-CORE", "E-CORE"], width=100)
        self.path_prio.pack(side="left", padx=5)
        self.path_prio.set("P-CORE")
        ctk.CTkButton(self.add_path_ui, text="Add Directory", command=self.add_path).pack(side="left", padx=5)
        self.refresh_path_list_ui()

    def setup_cleanup(self):
        self.cleanup_frame.grid_columnconfigure(0, weight=1)
        self.cleanup_frame.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(self.cleanup_frame, text="System Junk Cleaner", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, pady=20)
        ctk.CTkLabel(self.cleanup_frame, text="This will remove temporary files and free up space.").grid(row=1, column=0, pady=10)
        
        self.clean_btn = ctk.CTkButton(self.cleanup_frame, text="SCAN & CLEAN JUNK", height=50, command=self.perform_cleanup)
        self.clean_btn.grid(row=2, column=0, pady=20)

        self.clean_log.grid(row=3, column=0, sticky="nsew", padx=20, pady=20)

    def perform_cleanup(self):
        self.clean_btn.configure(state="disabled", text="CLEANING...")
        self.clean_log.delete("1.0", "end")
        self.clean_log.insert("end", "Starting system cleanup...\n")
        
        def _task():
            def _cb(msg):
                self.clean_log.insert("end", f"{msg}\n")
                self.clean_log.see("end")
            
            try:
                f_count, b_saved = clean_junk(_cb)
                mb_saved = round(b_saved / (1024 * 1024), 2)
                self.clean_log.insert("end", f"\n✅ Cleanup Complete!\n")
                self.clean_log.insert("end", f"Files deleted: {f_count}\n")
                self.clean_log.insert("end", f"Space saved: {mb_saved} MB\n")
                messagebox.showinfo("Cleanup Complete", f"Successfully cleaned {f_count} files.\nSaved {mb_saved} MB of space.")
            except Exception as e:
                self.clean_log.insert("end", f"\n❌ Error during cleanup: {e}\n")
            finally:
                self.clean_btn.configure(state="normal", text="SCAN & CLEAN JUNK")

        threading.Thread(target=_task, daemon=True).start()

    def refresh_game_list_ui(self):
        for w in self.game_scroll.winfo_children(): w.destroy()
        targets = get_targets(self.config)
        for name, prio in targets:
            row = ctk.CTkFrame(self.game_scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=name, anchor="w").pack(side="left", padx=10, fill="x", expand=True)
            ctk.CTkLabel(row, text=f"[{prio}]", width=80).pack(side="left", padx=10)
            ctk.CTkButton(row, text="X", width=30, fg_color="#dc3545", command=lambda n=name: self.remove_game(n)).pack(side="right")

    def refresh_path_list_ui(self):
        for w in self.path_scroll.winfo_children(): w.destroy()
        paths = get_paths(self.config)
        for path, prio in paths:
            row = ctk.CTkFrame(self.path_scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=path, anchor="w", font=ctk.CTkFont(size=10)).pack(side="left", padx=10, fill="x", expand=True)
            ctk.CTkLabel(row, text=f"[{prio}]", width=80).pack(side="left", padx=10)
            ctk.CTkButton(row, text="X", width=30, fg_color="#dc3545", command=lambda p=path: self.remove_path(p)).pack(side="right")

    def add_game(self):
        name = self.new_game_entry.get().strip()
        if name:
            self.config["Targets"][name] = self.game_prio.get()
            self.new_game_entry.delete(0, 'end')
            self.refresh_game_list_ui()
            self.save_settings_realtime()

    def remove_game(self, name):
        if self.config.has_option("Targets", name):
            self.config.remove_option("Targets", name)
            self.refresh_game_list_ui()
            self.save_settings_realtime()

    def add_path(self):
        folder = filedialog.askdirectory()
        if folder:
            self.config["Paths"][folder] = self.path_prio.get()
            self.refresh_path_list_ui()
            self.save_settings_realtime()

    def remove_path(self, path):
        if self.config.has_option("Paths", path):
            self.config.remove_option("Paths", path)
            self.refresh_path_list_ui()
            self.save_settings_realtime()

    def save_settings_realtime(self):
        try:
            val = self.interval_entry.get().strip()
            if val.replace('.', '', 1).isdigit():
                self.config["Settings"]["interval"] = val
            self.config["Settings"]["exclude_core_0"] = str(self.exclude_core0_var.get()).lower()
            self.config["Settings"]["disable_smt"] = str(self.disable_smt_var.get()).lower()
            self.config["Settings"]["auto_cleanup"] = str(self.auto_cleanup_var.get()).lower()
            save_config(self.config)
            self.setup_dashboard()
            self.log("⚡ Config saved.")
        except Exception as e:
            self.log(f"⚠ Save error: {e}")

    def scan_games(self):
        self.log("🔍 Scanning for games...")
        def _task():
            found = []
            search_paths = ["D:/Games", "C:/Program Files", "C:/Program Files (x86)"]
            for p in search_paths:
                if os.path.exists(p):
                    try:
                        for root, dirs, files in os.walk(p):
                            for file in files:
                                if file.lower().endswith(".exe") and "uninst" not in file.lower() and "crash" not in file.lower():
                                    found.append(file)
                            if len(found) > 100: break
                    except Exception: continue
            self.log(f"✅ Found {len(found)} executables.")
        threading.Thread(target=_task, daemon=True).start()

    def show_dashboard(self):
        self.settings_frame.grid_forget()
        self.cleanup_frame.grid_forget()
        self.dashboard_frame.grid(row=0, column=1, sticky="nsew")

    def show_settings(self):
        self.dashboard_frame.grid_forget()
        self.cleanup_frame.grid_forget()
        self.settings_frame.grid(row=0, column=1, sticky="nsew")

    def show_cleanup(self):
        self.dashboard_frame.grid_forget()
        self.settings_frame.grid_forget()
        self.cleanup_frame.grid(row=0, column=1, sticky="nsew")

    def log(self, text):
        if hasattr(self, 'textbox'):
            self.textbox.insert("end", f"{text}\n")
            self.textbox.see("end")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def start_service(self):
        # ตรวจสอบสิทธิ์ Admin ก่อนเริ่มทำงาน
        is_admin = False
        try:
            if os.name == 'nt':
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                is_admin = os.getuid() == 0
        except AttributeError:
            is_admin = False

        if not is_admin:
            messagebox.showerror("Admin Required", "กรุณารันโปรแกรมด้วยสิทธิ์ Administrator เพื่อจัดการ CPU Affinity")
            self.log("❌ Error: Administrator privileges required.")
            return

        self.running = True
        self.stop_event.clear()
        self.setup_dashboard()
        threading.Thread(target=self.run_service, daemon=True).start()

    def stop_service(self):
        self.stop_event.set()
        self.running = False
        self.setup_dashboard()

    def run_service(self):
        try:
            run_optimization(self.stop_event)
        except Exception as e:
            self.log(f"❌ Error: {e}")
            self.running = False
            self.setup_dashboard()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
