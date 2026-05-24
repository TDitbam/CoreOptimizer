import psutil

HIGH_PRIORITY = psutil.HIGH_PRIORITY_CLASS


def optimize_process(proc, p_cores):

    try:
        proc.cpu_affinity(p_cores)

        proc.nice(HIGH_PRIORITY)

        print(
            f"[OK] {proc.name()} "
            f"PID={proc.pid} "
            f"-> P-Core Only"
        )

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied
    ):
        pass

    except Exception as e:
        print(f"[ERROR] {e}")
