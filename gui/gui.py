import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
import sys
import os
from PIL import Image
import pystray
from pystray import MenuItem as item
from core.config_loader import load_config, save_config, get_targets, get_paths
from core.cpu_topology import split_p_e_cores
from core.cleaner import clean_junk

# GUI Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CorePriority Pro v3.1.0")
        self.geometry("1000x750")

        self.running = False
        self.config = load_config()
        self.stop_event = threading.Event()

        # System Tray Setup
        self.protocol('WM_DELETE_WINDOW', self.withdraw_to_tray)
        self.create_tray_icon()

        # Layout Setup
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_sidebar()
        
        # Main Containers (Static Layout)
        self.dashboard_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.dashboard_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cleanup_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.setup_dashboard_ui()
        self.setup_settings_ui()
        self.setup_cleanup_ui()
        
        self.show_dashboard()

    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1E1E1E")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar_frame, text="COREPRIORITY", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=40)
        
        btn_style = {"height": 40, "corner_radius": 8, "fg_color": "transparent", "hover_color": "#333333"}
        ctk.CTkButton(self.sidebar_frame, text="Dashboard", **btn_style, command=self.show_dashboard).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.sidebar_frame, text="Settings", **btn_style, command=self.show_settings).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.sidebar_frame, text="Cleanup Junk", **btn_style, command=self.show_cleanup).pack(pady=10, padx=20, fill="x")

    def setup_dashboard_ui(self):
        # KPI Card
        self.status_card = ctk.CTkFrame(self.dashboard_frame, corner_radius=15, fg_color="#2D2D2D")
        self.status_card.pack(pady=10, padx=20, fill="x")
        self.status_label = ctk.CTkLabel(self.status_card, text="Status: IDLE", font=ctk.CTkFont(size=24, weight="bold"))
        self.status_label.pack(pady=20)
        
        # Stats Cards
        stats_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        stats_frame.pack(pady=10, fill="x")
        
        card_p = ctk.CTkFrame(stats_frame, corner_radius=15, fg_color="#2D2D2D")
        card_p.pack(side="left", expand=True, fill="x", padx=10)
        ctk.CTkLabel(card_p, text="P-CORES", font=ctk.CTkFont(size=12)).pack(pady=(15, 0))
        self.pcore_lbl = ctk.CTkLabel(card_p, text="0", font=ctk.CTkFont(size=30, weight="bold"))
        self.pcore_lbl.pack(pady=(0, 15))
        
        card_e = ctk.CTkFrame(stats_frame, corner_radius=15, fg_color="#2D2D2D")
        card_e.pack(side="right", expand=True, fill="x", padx=10)
        ctk.CTkLabel(card_e, text="E-CORES", font=ctk.CTkFont(size=12)).pack(pady=(15, 0))
        self.ecore_lbl = ctk.CTkLabel(card_e, text="0", font=ctk.CTkFont(size=30, weight="bold"))
        self.ecore_lbl.pack(pady=(0, 15))
        
        # Controls
        ctrl_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        ctrl_frame.pack(pady=20, fill="x", padx=20)
        self.start_btn = ctk.CTkButton(ctrl_frame, text="START OPTIMIZER", height=45, fg_color="#28a745", command=self.start_service)
        self.start_btn.pack(side="left", expand=True, fill="x", padx=5)
        self.stop_btn = ctk.CTkButton(ctrl_frame, text="STOP SERVICE", height=45, fg_color="#dc3545", state="disabled", command=self.stop_service)
        self.stop_btn.pack(side="right", expand=True, fill="x", padx=5)
        
        # Log
        self.textbox = ctk.CTkTextbox(self.dashboard_frame, corner_radius=10, fg_color="#1E1E1E")
        self.textbox.pack(fill="both", expand=True, padx=20, pady=20)
        self.update_stats()

    def update_stats(self):
        ex = self.config["Settings"].getboolean("exclude_core_0", fallback=True)
        smt = self.config["Settings"].getboolean("disable_smt", fallback=False)
        p, e = split_p_e_cores(ex, smt)
        self.pcore_lbl.configure(text=str(len(p)))
        self.ecore_lbl.configure(text=str(len(e)))

    def setup_settings_ui(self):
        self.settings_frame.grid_columnconfigure(0, weight=1)
        
        # Perf Group
        p_frame = ctk.CTkFrame(self.settings_frame, fg_color="#2D2D2D", corner_radius=15)
        p_frame.pack(pady=20, padx=20, fill="x")
        ctk.CTkLabel(p_frame, text="Performance Settings", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        self.exclude_core0_var = ctk.BooleanVar(value=self.config["Settings"].getboolean("exclude_core_0", fallback=True))
        ctk.CTkSwitch(p_frame, text="Exclude Core 0", variable=self.exclude_core0_var, command=self.save_settings).pack(pady=5, padx=20, anchor="w")
        self.disable_smt_var = ctk.BooleanVar(value=self.config["Settings"].getboolean("disable_smt", fallback=False))
        ctk.CTkSwitch(p_frame, text="Disable SMT (Phys Only)", variable=self.disable_smt_var, command=self.save_settings).pack(pady=5, padx=20, anchor="w")
        
        # Maintenance
        m_frame = ctk.CTkFrame(self.settings_frame, fg_color="#2D2D2D", corner_radius=15)
        m_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(m_frame, text="Maintenance", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        self.auto_cleanup_var = ctk.BooleanVar(value=self.config["Settings"].getboolean("auto_cleanup", fallback=False))
        ctk.CTkSwitch(m_frame, text="Auto Junk Cleanup", variable=self.auto_cleanup_var, command=self.save_settings).pack(pady=5, padx=20, anchor="w")
        
        timer_frame = ctk.CTkFrame(m_frame, fg_color="transparent")
        timer_frame.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(timer_frame, text="Interval (min):").pack(side="left")
        self.cleanup_int_var = ctk.StringVar(value=self.config["Settings"].get("cleanup_interval", "1440"))
        self.cleanup_int_entry = ctk.CTkEntry(timer_frame, textvariable=self.cleanup_int_var, width=60)
        self.cleanup_int_entry.pack(side="left", padx=10)
        ctk.CTkButton(timer_frame, text="Apply", width=60, command=self.save_settings).pack(side="left")
        
        # Lists
        self.tabs = ctk.CTkTabview(self.settings_frame, corner_radius=15)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        self.setup_games_tab(self.tabs.add("Games"))
        self.setup_paths_tab(self.tabs.add("Directories"))
        self.refresh_lists()

    def setup_games_tab(self, tab):
        self.g_scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        self.g_scroll.pack(fill="both", expand=True)
        ui = ctk.CTkFrame(tab, fg_color="transparent"); ui.pack(fill="x", pady=5)
        self.g_entry = ctk.CTkEntry(ui, placeholder_text="game.exe")
        self.g_entry.pack(side="left", expand=True, fill="x")
        self.g_prio = ctk.CTkOptionMenu(ui, values=["P-CORE", "E-CORE", "NORMAL"], width=100)
        self.g_prio.pack(side="left", padx=5)
        ctk.CTkButton(ui, text="Add", width=60, command=self.add_game).pack(side="right")

    def setup_paths_tab(self, tab):
        self.p_scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        self.p_scroll.pack(fill="both", expand=True)
        ctk.CTkButton(tab, text="Add Managed Directory", command=self.add_path).pack(fill="x", pady=5)

    def setup_cleanup_ui(self):
        ctk.CTkButton(self.cleanup_frame, text="SCAN & CLEAN JUNK", height=60, fg_color="#28a745", command=self.run_clean).pack(pady=40, padx=40, fill="x")
        self.clean_log = ctk.CTkTextbox(self.cleanup_frame, fg_color="#1E1E1E")
        self.clean_log.pack(fill="both", expand=True, padx=20, pady=20)

    # --- Utility Methods ---
    def save_settings(self):
        self.config["Settings"].update({"exclude_core_0": str(self.exclude_core0_var.get()).lower(),
                                        "disable_smt": str(self.disable_smt_var.get()).lower(),
                                        "auto_cleanup": str(self.auto_cleanup_var.get()).lower(),
                                        "cleanup_interval": str(self.cleanup_int_var.get())})
        save_config(self.config); self.update_stats()

    def show_dashboard(self): self.settings_frame.grid_forget(); self.cleanup_frame.grid_forget(); self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
    def show_settings(self): self.dashboard_frame.grid_forget(); self.cleanup_frame.grid_forget(); self.settings_frame.grid(row=0, column=1, sticky="nsew")
    def show_cleanup(self): self.dashboard_frame.grid_forget(); self.settings_frame.grid_forget(); self.cleanup_frame.grid(row=0, column=1, sticky="nsew")
    def log(self, text):
        self.after(0, lambda: self._log_ui(text))

    def _log_ui(self, text):
        self.textbox.insert("end", f"{text}\n")
        self.textbox.see("end")

    def log_clean(self, text):
        self.after(0, lambda: self._log_clean_ui(text))

    def _log_clean_ui(self, text):
        self.clean_log.insert("end", f"{text}\n")
        self.clean_log.see("end")

    def start_service(self):
        self.running = True; self.start_btn.configure(state="disabled"); self.stop_btn.configure(state="normal")
        self.status_label.configure(text="Status: RUNNING", text_color="#28a745"); self.stop_event.clear()
        threading.Thread(target=self.run_service, daemon=True).start()
    def stop_service(self):
        self.running = False; self.start_btn.configure(state="normal"); self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="Status: IDLE", text_color="#ABB2BF"); self.stop_event.set()
    def run_service(self):
        from core.optimizer_engine import optimize_processes
        try: optimize_processes(self.stop_event, 5.0, log_callback=self.log)
        except Exception as e: self.log(f"Error: {e}")
    def run_clean(self):
        def _target():
            self.log_clean("Starting junk cleanup...")
            files, bytes_saved = clean_junk(self.log_clean)
            mb = bytes_saved / (1024 * 1024)
            self.log_clean(f"--- Cleanup Finished ---")
            self.log_clean(f"Files deleted: {files}")
            self.log_clean(f"Space recovered: {mb:.2f} MB")
        threading.Thread(target=_target, daemon=True).start()
    def refresh_lists(self):
        for w in self.g_scroll.winfo_children(): w.destroy()
        for name, prio in get_targets(self.config):
            r = ctk.CTkFrame(self.g_scroll); r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=name).pack(side="left", padx=10)
            ctk.CTkButton(r, text="X", width=30, fg_color="#dc3545", command=lambda n=name: self.rem_game(n)).pack(side="right")
        for w in self.p_scroll.winfo_children(): w.destroy()
        for path, prio in get_paths(self.config):
            r = ctk.CTkFrame(self.p_scroll); r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=path, font=ctk.CTkFont(size=10)).pack(side="left", padx=10)
            ctk.CTkButton(r, text="X", width=30, fg_color="#dc3545", command=lambda p=path: self.rem_path(p)).pack(side="right")
    def add_game(self):
        n = self.g_entry.get().strip()
        if n: self.config["Targets"][n] = self.g_prio.get(); self.g_entry.delete(0, 'end'); self.refresh_lists(); self.save_settings()
    def rem_game(self, n): self.config.remove_option("Targets", n); self.refresh_lists(); self.save_settings()
    def add_path(self):
        f = filedialog.askdirectory()
        if f: self.config["Paths"][f] = "P-CORE"; self.refresh_lists(); self.save_settings()
    def rem_path(self, p): self.config.remove_option("Paths", p); self.refresh_lists(); self.save_settings()

    # --- System Tray Methods ---
    def create_tray_icon(self):
        icon_path = 'gui/icon.ico'
        if os.path.exists(icon_path):
            image = Image.open(icon_path)
        else:
            image = Image.new('RGB', (64, 64), color=(40, 167, 69))
            
        menu = (item('Open CorePriority', self.show_from_tray, default=True),
                item('Exit', self.exit_app))
        self.tray_icon = pystray.Icon("CorePriorityPro", image, "CorePriority Pro", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def withdraw_to_tray(self):
        self.withdraw()

    def show_from_tray(self, icon=None, item=None):
        self.after(0, self.deiconify)
        self.after(0, self.focus_force)

    def exit_app(self, icon=None, item=None):
        self.stop_service()
        self.tray_icon.stop()
        self.quit()
        sys.exit(0)
