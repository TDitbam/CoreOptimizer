import time
import hashlib
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

# Lifecycle States
STATE_NEW = "NEW"
STATE_STABLE = "STABLE"
STATE_TERMINATING = "TERMINATING"

@dataclass
class ProcessState:
    pid: int
    create_time: float
    exe_path: str
    last_decision_id: Optional[Tuple] = None
    last_apply_ts: float = 0.0
    state: str = STATE_NEW

class ProcessRegistry:
    def __init__(self, cooldown_ms: int = 500):
        self._entries: Dict[Tuple, ProcessState] = {}
        self.cooldown_s = cooldown_ms / 1000.0

    def _get_exe_hash(self, exe_path: str) -> str:
        return hashlib.sha256(exe_path.lower().encode()).hexdigest()

    def get_entry_key(self, pid: int, create_time: float, exe_hash: str) -> Tuple:
        return (pid, create_time, exe_hash)

    def update_or_create(self, pid: int, create_time: float, exe_path: str) -> ProcessState:
        exe_hash = self._get_exe_hash(exe_path)
        key = self.get_entry_key(pid, create_time, exe_hash)
        if key not in self._entries:
            self._entries[key] = ProcessState(pid, create_time, exe_path)
        return self._entries[key]

    def remove_stale(self, active_pids_info: Dict[Tuple, bool]):
        """
        active_pids_info: Dict of (pid, create_time, hash(exe_path)) -> is_active
        """
        for key in list(self._entries.keys()):
            if key not in active_pids_info:
                del self._entries[key]
