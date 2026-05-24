import psutil
import time
import threading

from cpu_topology import P_CORES, E_CORES
from config_loader import load_config
from process_optimizer import optimize_process


def main(stop_event=None):

    config = load_config()

    interval = int(
        config["Settings"].get("interval", 15)
    )

    games = [
        value.strip().lower()
        for key, value in config["Games"].items()
    ]

    already_done = set()

    print(f"[INFO] P-Cores : {P_CORES}")
    print(f"[INFO] E-Cores : {E_CORES}")

    print("[INFO] Monitoring started...")
    print(f"[INFO] Games: {games}")

    while True:
        if stop_event and stop_event.is_set():
            print("[INFO] Stop event received. Exiting loop...")
            break

        try:

            for proc in psutil.process_iter(
                ["pid", "name"]
            ):

                try:
                    name = proc.info["name"]

                    if not name:
                        continue

                    name_lower = name.lower()

                    if name_lower in games:

                        pid = proc.info["pid"]

                        if pid not in already_done:

                            optimize_process(
                                proc,
                                P_CORES
                            )

                            already_done.add(pid)

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied
                ):
                    continue

            # cleanup closed process
            alive = set(psutil.pids())

            already_done.intersection_update(alive)

            time.sleep(interval)

        except KeyboardInterrupt:

            print("\n[INFO] Exit")

            break

        except Exception as e:

            print(f"[MAIN ERROR] {e}")

            time.sleep(5)


if __name__ == "__main__":
    main()
