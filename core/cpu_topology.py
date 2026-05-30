import psutil


def split_p_e_cores(exclude_core_0=True):
    """
    Auto split P-Core / E-Core
    """

    logical = psutil.cpu_count(logical=True)
    if logical is None:
        return [0], [] # Safety fallback

    # fallback old CPU
    if logical <= 8:
        start_index = 1 if exclude_core_0 else 0
        p_cores = list(range(start_index, logical))
        e_cores = []

        return p_cores, e_cores

    # estimate P-Core threads
    p_thread_count = round(logical * 0.6)

    # make even number
    if p_thread_count % 2 != 0:
        p_thread_count += 1

    start_index = 1 if exclude_core_0 else 0
    p_cores = list(range(start_index, p_thread_count))
    e_cores = list(range(p_thread_count, logical))

    return p_cores, e_cores
