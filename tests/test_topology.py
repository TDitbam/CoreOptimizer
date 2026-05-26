import psutil
from core.cpu_topology import split_p_e_cores
import unittest.mock as mock

def test_split_p_e_cores_basic():
    p_cores, e_cores = split_p_e_cores(exclude_core_0=False)
    assert isinstance(p_cores, list)
    assert isinstance(e_cores, list)

def test_split_p_e_cores_exclusion():
    # Test with Core 0 exclusion
    p_with, e_with = split_p_e_cores(exclude_core_0=True)
    p_without, e_without = split_p_e_cores(exclude_core_0=False)
    
    # If there are P-cores, Core 0 should be missing in the 'True' case
    if p_with and p_without:
        assert 0 not in p_with
        assert 0 in p_without
        assert len(p_without) == len(p_with) + 1

def test_mocked_topology():
    # Mock psutil.cpu_count to simulate a 16-thread hybrid CPU
    with mock.patch('psutil.cpu_count', return_value=16):
        # 16 * 0.6 = 9.6 -> round to 10. 10 is even.
        # exclude_core_0=False -> P: 0-9 (10 cores), E: 10-15 (6 cores)
        p, e = split_p_e_cores(exclude_core_0=False)
        assert p == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert e == [10, 11, 12, 13, 14, 15]
        
        # exclude_core_0=True -> P: 1-9 (9 cores), E: 10-15 (6 cores)
        p, e = split_p_e_cores(exclude_core_0=True)
        assert p == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert e == [10, 11, 12, 13, 14, 15]

def test_low_core_count():
    with mock.patch('psutil.cpu_count', return_value=4):
        # logical <= 8 logic: p = range(start, logical), e = []
        p, e = split_p_e_cores(exclude_core_0=False)
        assert p == [0, 1, 2, 3]
        assert e == []
        
        p, e = split_p_e_cores(exclude_core_0=True)
        assert p == [1, 2, 3]
        assert e == []
