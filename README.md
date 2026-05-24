# P-Core Game Optimizer

Optimize game performance by forcing processes to run on P-Cores (Performance Cores) and setting high process priority.

## Features
- **Auto CPU Topology Detection**: Automatically splits P-Cores and E-Cores.
- **Process Optimization**: Sets CPU affinity and priority for specified games.
- **Configurable**: Easily add games and adjust monitoring intervals via `config.ini`.
- **GUI & CLI Support**: Run as a background service or with a simple interface.

## Project Structure
```text
project/
│
├── main.py                # Core logic and monitoring loop
├── gui.py                 # Tkinter-based user interface
├── cpu_topology.py        # Logic to detect P/E core layout
├── process_optimizer.py   # logic to apply affinity and priority
├── config_loader.py       # Configuration parser
└── config.ini             # Settings and game list
```

## Getting Started

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
- **GUI Mode**:
  ```bash
  python gui.py
  ```
- **CLI Mode**:
  ```bash
  python main.py
  ```

### Testing
Run automated unit tests using pytest:
```bash
pytest
```

## Configuration
Edit `config.ini` to add your games:
```ini
[Games]
game1 = BlackDesert64.exe
game2 = cs2.exe
```
