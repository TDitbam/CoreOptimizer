import customtkinter as ctk
import sys
import os
import threading

# Add subfolders to path
sys.path.append(os.path.abspath("chat-tts"))
sys.path.append(os.path.abspath("CoreOptimizer"))

# Import GUI classes (will need slight modification to be embeddable)
# For now, let's just make a simple launcher that can start both.

class TDitbamSuite(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TDitbam Streamer Suite")
        self.geometry("800x600")
        
        self.label = ctk.CTkLabel(self, text="TDitbam Streamer Suite", font=("Helvetica", 24, "bold"))
        self.label.pack(pady=20)
        
        self.btn_chat_tts = ctk.CTkButton(self, text="Launch Chat TTS", command=self.launch_chat_tts, height=60, width=300)
        self.btn_chat_tts.pack(pady=20)
        
        self.btn_core_optimizer = ctk.CTkButton(self, text="Launch Core Optimizer", command=self.launch_core_optimizer, height=60, width=300)
        self.btn_core_optimizer.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(self, text="Select a tool to launch")
        self.status_label.pack(pady=20)

    def launch_chat_tts(self):
        self.status_label.configure(text="Launching Chat TTS...")
        threading.Thread(target=self._run_chat_tts, daemon=True).start()

    def _run_chat_tts(self):
        # We need to change directory to chat-tts so it can find its config/core
        old_cwd = os.getcwd()
        os.chdir("chat-tts")
        try:
            # Re-add current dir to path to ensure imports work
            sys.path.insert(0, os.getcwd())
            from start_gui import ChatTTSGui
            app = ChatTTSGui()
            app.mainloop()
        except Exception as e:
            print(f"Error launching Chat TTS: {e}")
        finally:
            os.chdir(old_cwd)

    def launch_core_optimizer(self):
        self.status_label.configure(text="Launching Core Optimizer...")
        threading.Thread(target=self._run_core_optimizer, daemon=True).start()

    def _run_core_optimizer(self):
        old_cwd = os.getcwd()
        os.chdir("CoreOptimizer")
        try:
            sys.path.insert(0, os.getcwd())
            from gui.gui import App
            app = App()
            app.mainloop()
        except Exception as e:
            print(f"Error launching Core Optimizer: {e}")
        finally:
            os.chdir(old_cwd)

if __name__ == "__main__":
    app = TDitbamSuite()
    app.mainloop()
