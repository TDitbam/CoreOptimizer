from policy.models import PolicyType, CorePool
from typing import List

class PolicyResolver:
    def __init__(self, core_pool: CorePool):
        self.core_pool = core_pool

    def resolve(self, policy: str) -> List[int]:
        if policy == PolicyType.P_CORE:
            return self.core_pool.performance_cores
        elif policy == PolicyType.E_CORE:
            return self.core_pool.efficiency_cores
        else:
            return [] # Logic to handle normal
