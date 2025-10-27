import os
import time
from concurrent import interpreters
from concurrent.futures import InterpreterPoolExecutor

def cpu_bound_work(n: int):
    interp = interpreters.create()
    code = f"""
def compute():
    s = 0
    for i in range({n}):
        s += i * i       
    return s
compute()
"""
    interp.exec(code)
    
    return os.getpid()

def main():
    print("Main process PID:", os.getpid())

    with InterpreterPoolExecutor(max_workers=4) as executor:
        inputs = [10_000_000] * 4
        futures = [executor.submit(cpu_bound_work, x) for x in inputs]

        for idx, f in enumerate(futures):
            pid = f.result()
            print(f"Task {idx} ran in PID {pid}")

    print("Done.")

if __name__ == "__main__":
    start = time.time()
    main()
    print("Elapsed time:", time.time() - start)
