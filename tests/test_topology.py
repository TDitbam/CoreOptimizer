import psutil
from core.cpu_topology import split_p_e_cores

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
    
    assert len(p_cores) + len(e_cores) <= logical_total
