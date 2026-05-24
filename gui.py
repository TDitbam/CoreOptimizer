import customtkinter as ctk
from tkinter import messagebox
import threading
import sys
import os

from main import main
from cpu_topology import P_CORES, E_CORES
from config_loader import load_config, save_config

# Set appearance and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("P-Core Optimizer Pro")
        self.geometry("850x600")

        self.running = False
        self.thread = None
        self.stop_event = threading.Event()
        self.config = load_config()

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # =====================================================================
        # SIDEBAR
        # =====================================================================
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="OPTIMIZER", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.dashboard_btn = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard)
        self.dashboard_btn.grid(row=1, column=0, padx=20, pady=10)

        self.settings_btn = ctk.CTkButton(self.sidebar_frame, text="Settings", command=self.show_settings)
        self.settings_btn.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("Dark")

        # =====================================================================
        # CONTENT FRAMES
        # =====================================================================
        self.dashboard_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.settings_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.setup_dashboard()
        self.setup_settings()

        # Show initial frame
        self.show_dashboard()

    def setup_dashboard(self):
        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        self.dashboard_frame.grid_rowconfigure(2, weight=1)

        # Status Card
        self.status_card = ctk.CTkFrame(self.dashboard_frame, height=100)
        self.status_card.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.status_card.grid_columnconfigure(0, weight=1)

        self.status_var = ctk.StringVar(value="Status: IDLE")
        self.status_label = ctk.CTkLabel(self.status_card, textvariable=self.status_var, 
                                         font=ctk.CTkFont(size=24, weight="bold"),
                                         text_color="#ABB2BF")
        self.status_label.grid(row=0, column=0, pady=20)

        # Info Cores
        self.core_info_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.core_info_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.core_info_frame.grid_columnconfigure((0, 1), weight=1)

        self.pcore_box = ctk.CTkFrame(self.core_info_frame)
        self.pcore_box.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        ctk.CTkLabel(self.pcore_box, text="P-CORES", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 0))
        ctk.CTkLabel(self.pcore_box, text=f"{len(P_CORES)} Cores", font=ctk.CTkFont(size=18)).pack(pady=(0, 10))

        self.ecore_box = ctk.CTkFrame(self.core_info_frame)
        self.ecore_box.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        ctk.CTkLabel(self.ecore_box, text="E-CORES", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 0))
        ctk.CTkLabel(self.ecore_box, text=f"{len(E_CORES)} Cores", font=ctk.CTkFont(size=18)).pack(pady=(0, 10))

        # Controls
        self.dash_control_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.dash_control_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        self.dash_control_frame.grid_columnconfigure((0, 1), weight=1)

        self.start_btn = ctk.CTkButton(self.dash_control_frame, text="START OPTIMIZER", 
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       height=45, fg_color="#28a745", hover_color="#218838",
                                       command=self.start_service)
        self.start_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.stop_btn = ctk.CTkButton(self.dash_control_frame, text="STOP SERVICE", 
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      height=45, fg_color="#dc3545", hover_color="#c82333",
                                      state="disabled",
                                      command=self.stop_service)
        self.stop_btn.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        # Logs
        self.textbox = ctk.CTkTextbox(self.dashboard_frame, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.grid(row=3, column=0, sticky="nsew", padx=20, pady=20)
        self.log("🚀 System initialized and ready.")

    def setup_settings(self):
        self.settings_frame.grid_columnconfigure(0, weight=1)
        
        # Interval Setting
        self.interval_frame = ctk.CTkFrame(self.settings_frame)
        self.interval_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        ctk.CTkLabel(self.interval_frame, text="Monitoring Interval (sec):", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=20, pady=10)
        self.interval_entry = ctk.CTkEntry(self.interval_frame, width=60)
        self.interval_entry.pack(side="left", padx=10)
        self.interval_entry.insert(0, self.config["Settings"].get("interval", "15"))
        
        # Game List Management
        self.game_list_frame = ctk.CTkFrame(self.settings_frame)
        self.game_list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.game_list_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.game_list_frame, text="Managed Games (Executable names)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")
        
        self.game_scroll = ctk.CTkScrollableFrame(self.game_list_frame, height=200)
        self.game_scroll.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
        
        self.game_entries = []
        self.refresh_game_list_ui()
        
        # Add Game
        self.add_game_frame = ctk.CTkFrame(self.game_list_frame, fg_color="transparent")
        self.add_game_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.new_game_entry = ctk.CTkEntry(self.add_game_frame, placeholder_text="e.g. game.exe")
        self.new_game_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.add_btn = ctk.CTkButton(self.add_game_frame, text="Add Game", width=100, command=self.add_game)
        self.add_btn.pack(side="right")
        
        # Save Button
        self.save_btn = ctk.CTkButton(self.settings_frame, text="SAVE CONFIGURATION", 
                                      fg_color="#007bff", hover_color="#0069d9",
                                      command=self.save_settings)
        self.save_btn.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

    def refresh_game_list_ui(self):
        for widget in self.game_scroll.winfo_children():
            widget.destroy()
        
        self.game_entries = []
        for key, value in self.config["Games"].items():
            row = ctk.CTkFrame(self.game_scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            lbl = ctk.CTkLabel(row, text=value, anchor="w")
            lbl.pack(side="left", padx=10, fill="x", expand=True)
            
            # Using a lambda with the current key to ensure correct deletion
            del_btn = ctk.CTkButton(row, text="Remove", width=60, height=24, 
                                     fg_color="#dc3545", hover_color="#c82333",
                                     command=lambda k=key: self.remove_game(k))
            del_btn.pack(side="right", padx=10)

    def add_game(self):
        name = self.new_game_entry.get().strip()
        if not name: return
        
        # Generate new key
        new_id = 1
        while f"game{new_id}" in self.config["Games"]:
            new_id += 1
        
        self.config["Games"][f"game{new_id}"] = name
        self.new_game_entry.delete(0, 'end')
        self.refresh_game_list_ui()

    def remove_game(self, key):
        if key in self.config["Games"]:
            del self.config["Games"][key]
            self.refresh_game_list_ui()

    def save_settings(self):
        try:
            interval = self.interval_entry.get().strip()
            if not interval.isdigit():
                raise ValueError("Interval must be a number")
            
            self.config["Settings"]["interval"] = interval
            save_config(self.config)
            messagebox.showinfo("Success", "Configuration saved successfully!")
            self.log("💾 Configuration updated.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def show_dashboard(self):
        self.settings_frame.grid_forget()
        self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
        self.dashboard_btn.configure(fg_color=("gray75", "gray25"))
        self.settings_btn.configure(fg_color="transparent")

    def show_settings(self):
        self.dashboard_frame.grid_forget()
        self.settings_frame.grid(row=0, column=1, sticky="nsew")
        self.settings_btn.configure(fg_color=("gray75", "gray25"))
        self.dashboard_btn.configure(fg_color="transparent")

    def log(self, text):
        self.textbox.insert("end", f"{text}\n")
        self.textbox.see("end")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def run_service(self):
        try:
            self.log("🔧 Service process started in background...")
            main(stop_event=self.stop_event)
            self.log("🛑 Service loop terminated.")
        except Exception as e:
            self.log(f"❌ Critical Error: {e}")
            self.stop_service()

    def start_service(self):
        if self.running:
            return
        
        self.running = True
        self.stop_event.clear()
        self.status_var.set("Status: RUNNING")
        self.status_label.configure(text_color="#28a745")
        
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        self.thread = threading.Thread(target=self.run_service, daemon=True)
        self.thread.start()
        
        self.log("✅ Optimizer is now monitoring processes.")

    def stop_service(self):
        if not self.running:
            return
            
        self.log("⏳ Sending stop signal...")
        self.stop_event.set()
        self.running = False
        
        self.status_var.set("Status: STOPPING")
        self.status_label.configure(text_color="#dc3545")
        
        # Reset UI states
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_var.set("Status: IDLE")
        self.status_label.configure(text_color="#ABB2BF")
        
    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
