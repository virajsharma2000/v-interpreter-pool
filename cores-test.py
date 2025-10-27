import os
import time
import threading
from concurrent.futures import InterpreterPoolExecutor

def get_current_core():
    # Linux: read /proc/self/stat or /proc/self/task/<tid>/stat 
    tid = threading.get_native_id()  # thread id
    try:
        with open(f"/proc/self/task/{tid}/stat", "r") as f:
            fields = f.read().split()
            # core number is field #39 (zero‐based 38) in some kernels 
            core = int(fields[38])
            return core
    except Exception:
        return None

def cpu_bound_work(n: int):
    core = get_current_core()
    s = 0
    for i in range(n):
        s += i * i
    return (os.getpid(), threading.get_native_id(), core, s)

def main():
    print("Main PID:", os.getpid())
    with InterpreterPoolExecutor(max_workers=4) as executor:
        inputs = [10_000_000] * 4
        futures = [executor.submit(cpu_bound_work, x) for x in inputs]
        for idx, f in enumerate(futures):
            pid, tid, core, result = f.result()
            print(f"Task {idx}: PID={pid}, TID={tid}, reported core={core}, result≈{result}")

if __name__ == "__main__":
    start = time.time()
    main()
    print("Elapsed:", time.time() - start)
