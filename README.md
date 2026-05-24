# CoreOptimizer

A lightweight Windows utility to optimize game performance by managing CPU affinity (P-Core/E-Core separation) and process priority.

## Features

- **Auto P-Core Detection**: Automatically identifies Performance and Efficiency cores on modern hybrid CPUs.
- **E-Core Separation**: Ensures game processes run exclusively on P-Cores to reduce latency and micro-stutter.
- **Game Process Monitor**: Automatically detects and optimizes configured games as they start.
- **High Priority Automation**: Automatically sets game processes to High Priority class.
- **Modern GUI**: Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for a sleek, Windows 11-style interface.
- **Lightweight Background Service**: Efficiently monitors system processes with minimal overhead.

## Screenshots

*(Add screenshots here)*

## Project Structure

```text
CoreOptimizer/
│
├── core/
│   ├── cpu_topology.py       # CPU Core detection logic
│   ├── process_optimizer.py   # Affinity and priority logic
│   └── config_loader.py      # Configuration management
│
├── gui/
│   └── gui.py                # Main GUI application
│
├── config/
│   └── config.ini            # User configuration
│
├── logs/                     # System logs
├── screenshots/              # UI Screenshots
│
├── requirements.txt
├── README.md
├── LICENSE
└── main.py                   # CLI Entry point & Core logic
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TDitbam/CoreOptimizer.git
   cd CoreOptimizer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running from source
Execute the GUI application (requires administrative privileges):
```bash
python gui/gui.py
```

### Administrative Requirements
This application **must run as administrator** to modify process affinity and priority of other applications.

## How it Works

### P-Core Affinity
The optimizer uses `psutil` to set the CPU affinity of game processes. By limiting a game to only P-Cores, we avoid the Windows scheduler's occasional mistake of placing time-critical game threads on slower E-Cores.

### Core 0 Management
By default, the optimizer includes Core 0 if it is a P-Core. However, it can be configured to avoid Core 0 if the user prefers to leave it for OS background tasks.

## Known Issues
- Some Anti-Cheat systems might block affinity changes.
- Requires Windows 10/11 for best results with hybrid architecture.

## License
MIT License - see [LICENSE](LICENSE) for details.
