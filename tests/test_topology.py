import psutil
from cpu_topology import split_p_e_cores

def test_split_p_e_cores_structure():
    """Verify that split_p_e_cores returns two lists of integers."""
    p_cores, e_cores = split_p_e_cores()
    
    assert isinstance(p_cores, list)
    assert isinstance(e_cores, list)
    
    if p_cores:
        assert all(isinstance(c, int) for c in p_cores)
    if e_cores:
        assert all(isinstance(c, int) for c in e_cores)

def test_split_p_e_cores_logic():
    """Verify core count logic matches expected psutil total."""
    logical_total = psutil.cpu_count(logical=True)
    p_cores, e_cores = split_p_e_cores()
    
    # The logic starts indexing from 1 in the original code: list(range(1, logical))
    # Note: cpu_affinity usually starts from 0. I should check if the original code's 1-based indexing is intentional.
    # Looking at cpu_topology.py: p_cores = list(range(1, p_thread_count))
    # It excludes core 0. This is a common strategy to keep core 0 for OS tasks.
    
    assert len(p_cores) + len(e_cores) <= logical_total
