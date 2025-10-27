from concurrent.futures import InterpreterPoolExecutor
import datetime, time

def run_job(job_name, payload):
    print(f"[{datetime.datetime.now()}] Running {job_name} with {payload}")
    return sum(range(payload))

def scheduler_loop(jobs, interval_sec=5):
    with InterpreterPoolExecutor(max_workers=4) as executor:
        while True:
            for job in jobs:
                future = executor.submit(run_job, job["name"], job["data"])
                future.add_done_callback(lambda f: print(f"Result: {f.result()}"))
            time.sleep(interval_sec)

if __name__ == "__main__":
    jobs = [
        {"name": "Job-A", "data": 10_000_000},
        {"name": "Job-B", "data": 5_000_000},
    ]
    scheduler_loop(jobs)