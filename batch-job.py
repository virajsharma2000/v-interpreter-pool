from concurrent.futures import InterpreterPoolExecutor
import  time

def run_job(job_name, payload, interval_sec):
    #print(f"[{datetime.datetime.now()}] Running {job_name} with {payload}")
    time.sleep(interval_sec)

    if job_name == '+':
      return sum(range(payload))
    
    elif job_name == 'max':
     return sum(range(payload)) / len(range(payload))

def scheduler_loop(jobs, interval_sec = 5):
    with InterpreterPoolExecutor(max_workers=4) as executor:
        while True:
            futures = []

            for job in jobs:
                future = executor.submit(run_job, job["name"], job["data"], interval_sec)
                futures.append(future)

            for f in futures:
             print(f.result())
                

if __name__ == "__main__":
    jobs = [
        {"name": "+", "data": 10_000_000},
        {"name": "mean", "data": 5_000_000},
    ]
    scheduler_loop(jobs)