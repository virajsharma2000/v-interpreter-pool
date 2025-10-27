import time, yaml, importlib, logging
from concurrent.futures import InterpreterPoolExecutor
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PyBatchX")

class Job:
    def __init__(self, name, callable_ref, schedule, retries):
        self.name = name
        self.callable_ref = callable_ref
        self.schedule = schedule
        self.retries = retries

class PyBatchXEngine:
    def __init__(self, config_path="config/jobs.yaml"):
        self.config = yaml.safe_load(Path(config_path).read_text())
        self.jobs = self._load_jobs()
        self.executor = InterpreterPoolExecutor(
            max_workers=self.config["scheduler"]["max_workers"]
        )

    def _load_jobs(self):
        jobs = []
        for job_cfg in self.config["jobs"]:
            if not job_cfg.get("enabled", True):
                continue
            if job_cfg.get("module"):
                mod = importlib.import_module(job_cfg["module"])
                fn = getattr(mod, job_cfg["function"])
            else:
                fn = self._load_script(job_cfg["script"])
            jobs.append(Job(job_cfg["name"], fn, job_cfg["schedule"], job_cfg.get("retries", 1)))
        return jobs

    def _load_script(self, path):
        code = Path(path).read_text()
        def run_script():
            exec(code, {})
        return run_script

    def run_cycle(self):
        for job in self.jobs:
            logger.info(f"Submitting job: {job.name}")
            future = self.executor.submit(job.callable_ref)
            future.add_done_callback(lambda f, j=job: logger.info(f"{j.name} completed: {f.result()}"))

    def start(self):
        interval = self.config["scheduler"]["interval"]
        logger.info("Starting PyBatchX scheduler...")
        while True:
            self.run_cycle()
            time.sleep(interval)
