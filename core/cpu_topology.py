import psutil

def get_cpu_topology():
    """
    Groups logical cores into physical core pairs/groups.
    Heuristic: On Windows, SMT/Hyper-Threading pairs are usually (0,1), (2,3), etc.
    On Intel Hybrid CPUs, P-cores have SMT (2 threads) and E-cores do not (1 thread).
    """
    logical = psutil.cpu_count(logical=True)
    physical = psutil.cpu_count(logical=False)
    
    if logical is None or physical is None:
        return []

    # Number of physical cores that have SMT (2 threads)
    # Assumes each physical core has either 1 or 2 threads.
    smt_pairs_count = logical - physical
    
    topology = []
    
    # 1. Map SMT pairs (Physical cores with 2 logical threads)
    # These are usually P-cores on modern Intel or all cores on AMD with SMT
    for i in range(smt_pairs_count):
        topology.append([2*i, 2*i + 1])
    
    # 2. Map single threads (Physical cores with 1 logical thread)
    # These are usually E-cores on modern Intel
    start_logical_index = smt_pairs_count * 2
    for i in range(start_logical_index, logical):
        topology.append([i])
        
    return topology

def calculate_affinity_mask(cores_list):
    """
    Calculates CPU Affinity Bitmask from a list of logical core IDs.
    Example: [0, 2] -> (1 << 0) | (1 << 2) = 5
    """
    mask = 0
    for core in cores_list:
        if isinstance(core, int):
            mask |= (1 << core)
    return mask

def split_p_e_cores(exclude_core_0=True):
    """
    Splits cores into P-cores and E-cores based on topology.
    Correctly handles SMT by excluding all threads of a physical core if requested.
    """
    topology = get_cpu_topology()
    if not topology:
        return [0], []

    logical = psutil.cpu_count(logical=True)
    physical = psutil.cpu_count(logical=False)
    smt_pairs_count = logical - physical

    p_phys_cores = []
    e_phys_cores = []

    if smt_pairs_count > 0:
        if smt_pairs_count < physical:
            # Hybrid CPU: SMT cores are P-cores, non-SMT are E-cores
            p_phys_cores = topology[:smt_pairs_count]
            e_phys_cores = topology[smt_pairs_count:]
        else:
            # All cores have SMT
            p_phys_cores = topology
            e_phys_cores = []
    else:
        # No cores have SMT
        p_phys_cores = topology
        e_phys_cores = []

    # Handle exclusion of Physical Core 0
    if exclude_core_0 and p_phys_cores:
        # Exclude the first physical core's logical threads
        p_phys_cores = p_phys_cores[1:]

    # Flatten lists of logical cores
    p_cores = [core for phys in p_phys_cores for core in phys]
    e_cores = [core for phys in e_phys_cores for core in phys]

    return p_cores, e_cores
