# P-Core Optimizer Pro 🚀

A powerful Windows utility designed to maximize game performance on modern Intel Hybrid CPUs (12th Gen+) by intelligently managing CPU affinity and process priority.

## 🌟 Key Features

- **Intel Hybrid Architecture Support**: Automatically detects P-Cores (Performance) and E-Cores (Efficiency).
- **Advanced Core Affinity**: 
    - **P-CORE Mode**: Force critical apps/games onto high-performance cores.
    - **E-CORE Mode**: Assign background tasks to efficiency cores to keep P-Cores free.
    - **NORMAL Mode**: Let Windows manage threads naturally.
- **Smart Optimization Zones**: 
    - **Managed Games**: Target specific executables by name.
    - **Managed Directories**: Automatically optimize *any* game launched from a specific folder (e.g., your Steam or Games library).
- **System Junk Cleaner**: Integrated cleaner to remove temporary files and free up disk space.
- **Real-time Configuration**: Changes in the GUI are saved and applied instantly without needing a restart.
- **Core 0 Management**: Explicit toggle to exclude Core 0 from optimization to reserve it for OS tasks.
- **Unified Entry Point**: Run as a modern GUI by default or use `--cli` for terminal-based operation.
- **PC Scanner**: Quickly scan common directories to find and add game executables.

## 🛠 Project Structure

```text
CoreOptimizer/
├── core/
│   ├── config_loader.py   # Centralized configuration management
│   ├── cpu_topology.py    # Advanced CPU core detection
│   ├── cleaner.py         # System junk cleaning logic
│   └── process_optimizer.py # Legacy optimization helpers
├── gui/
│   └── gui.py             # Modern CustomTkinter interface
├── config/
│   └── config.ini         # Standardized user configuration
├── main.py                # Main entry point (GUI/CLI)
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/TDitbam/CoreOptimizer.git
   cd CoreOptimizer
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

### Launching the Application
The application **requires Administrative Privileges** to manage other processes.

- **GUI Mode (Default)**:
  ```bash
  python main.py
  ```
- **CLI Mode**:
  ```bash
  python main.py --cli
  ```

### How to Optimize
1. **Settings Tab**: Add your game executables or entire game directories.
2. **Select Mode**: Choose between P-CORE or E-CORE for each entry.
3. **Dashboard**: Click **START OPTIMIZER** to begin monitoring.
4. **Cleanup**: Use the **Cleanup Junk** tab to free up system space.

## 🔍 How it Works

### P-Core vs E-Core Separation
Windows doesn't always place game threads on P-Cores, leading to micro-stutter. P-Core Optimizer Pro forces the OS to use only the fastest cores for your games, reducing latency and improving 1% lows.

### Path-Based Matching
Instead of adding every game manually, you can add your entire `D:\Games` library. The optimizer will monitor every process launched and, if its path starts with your library folder, it will apply your chosen performance profile.

## 📜 License
MIT License - see [LICENSE](LICENSE) for details.
