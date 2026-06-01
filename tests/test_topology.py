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

@mock.patch('core.cpu_topology.get_cpu_topology_windows', return_value=None)
def test_hybrid_topology_mock(mock_win_topo):
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

@mock.patch('core.cpu_topology.get_cpu_topology_windows', return_value=None)
def test_full_smt_topology_mock(mock_win_topo):
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

@mock.patch('core.cpu_topology.get_cpu_topology_windows', return_value=None)
def test_no_smt_topology_mock(mock_win_topo):
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

def test_robust_windows_topology_mock():
    # Simulate 2P (with SMT) and 2E (without SMT) via Windows API mock
    # P: EfficiencyClass 1, E: EfficiencyClass 0
    # Logical 0,1 -> P1; Logical 2,3 -> P2; Logical 4 -> E1; Logical 5 -> E2
    mock_topo = [
        ([0, 1], 1),
        ([2, 3], 1),
        ([4], 0),
        ([5], 0)
    ]
    
    with mock.patch('core.cpu_topology.get_cpu_topology_windows', return_value=mock_topo):
        p, e = split_p_e_cores(exclude_core_0=False)
        assert p == [0, 1, 2, 3]
        assert e == [4, 5]
        
        p, e = split_p_e_cores(exclude_core_0=True)
        # Excludes physical core 0 (logical 0 and 1)
        assert p == [2, 3]
        assert e == [4, 5]

def test_disable_smt_mock():
    # Simulate 2P (with SMT) and 2E (without SMT)
    # Logical 0,1 -> P1; Logical 2,3 -> P2; Logical 4 -> E1; Logical 5 -> E2
    mock_topo = [
        ([0, 1], 1),
        ([2, 3], 1),
        ([4], 0),
        ([5], 0)
    ]
    
    with mock.patch('core.cpu_topology.get_cpu_topology_windows', return_value=mock_topo):
        # With disable_smt=True, should only get [0, 2] for P and [4, 5] for E
        p, e = split_p_e_cores(exclude_core_0=False, disable_smt=True)
        assert p == [0, 2]
        assert e == [4, 5]
        
        # With exclude_core_0=True and disable_smt=True, should only get [2] for P and [4, 5] for E
        p, e = split_p_e_cores(exclude_core_0=True, disable_smt=True)
        assert p == [2]
        assert e == [4, 5]
