import psutil
from core.cpu_topology import split_p_e_cores, calculate_affinity_mask, get_cpu_topology
import unittest.mock as mock

def test_split_p_e_cores_basic():
    p_cores, e_cores = split_p_e_cores(exclude_core_0=False)
    assert isinstance(p_cores, list)
    assert isinstance(e_cores, list)

def test_calculate_affinity_mask():
    assert calculate_affinity_mask([0]) == 1
    assert calculate_affinity_mask([0, 2]) == 5
    assert calculate_affinity_mask([0, 1, 2, 3]) == 15
    assert calculate_affinity_mask([]) == 0

def test_hybrid_topology_mock():
    # Simulate 8P + 8E (24 logical, 16 physical)
    # smt_pairs = 24 - 16 = 8. 
    # Physical 0-7: [0,1], [2,3], ..., [14,15] (P-cores)
    # Physical 8-15: [16], [17], ..., [23] (E-cores)
    
    def mock_cpu_count(logical=True):
        return 24 if logical else 16

    with mock.patch('psutil.cpu_count', side_effect=mock_cpu_count):
        p, e = split_p_e_cores(exclude_core_0=False)
        assert p == list(range(16))
        assert e == list(range(16, 24))
        
        p, e = split_p_e_cores(exclude_core_0=True)
        # Excludes logical 0 and 1
        assert p == list(range(2, 16))
        assert e == list(range(16, 24))

def test_full_smt_topology_mock():
    # Simulate 8 physical cores, all with SMT (16 logical, 8 physical)
    def mock_cpu_count(logical=True):
        return 16 if logical else 8

    with mock.patch('psutil.cpu_count', side_effect=mock_cpu_count):
        p, e = split_p_e_cores(exclude_core_0=False)
        assert p == list(range(16))
        assert e == []
        
        p, e = split_p_e_cores(exclude_core_0=True)
        # Excludes logical 0 and 1
        assert p == list(range(2, 16))
        assert e == []

def test_no_smt_topology_mock():
    # Simulate 4 physical cores, no SMT (4 logical, 4 physical)
    def mock_cpu_count(logical=True):
        return 4 if logical else 4

    with mock.patch('psutil.cpu_count', side_effect=mock_cpu_count):
        p, e = split_p_e_cores(exclude_core_0=False)
        assert p == list(range(4))
        assert e == []
        
        p, e = split_p_e_cores(exclude_core_0=True)
        # Excludes logical 0 only as it's its own physical core
        assert p == list(range(1, 4))
        assert e == []
