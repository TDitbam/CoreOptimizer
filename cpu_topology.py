import psutil


def split_p_e_cores():
    """
    Auto split P-Core / E-Core
    """

    logical = psutil.cpu_count(logical=True)

    # fallback old CPU
    if logical <= 8:
        p_cores = list(range(1, logical))
        e_cores = []

        return p_cores, e_cores

    # estimate P-Core threads
    p_thread_count = round(logical * 0.6)

    # make even number
    if p_thread_count % 2 != 0:
        p_thread_count += 1

    p_cores = list(range(1, p_thread_count))
    e_cores = list(range(p_thread_count, logical))

    return p_cores, e_cores


P_CORES, E_CORES = split_p_e_cores()
