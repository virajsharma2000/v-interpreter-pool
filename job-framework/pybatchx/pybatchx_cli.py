import argparse
from pybatchx.engine import PyBatchXEngine

def main():
    parser = argparse.ArgumentParser(description="PyBatchX Admin CLI")
    parser.add_argument("command", choices=["start", "list"])
    args = parser.parse_args()

    engine = PyBatchXEngine()

    if args.command == "list":
        for job in engine.jobs:
            print(f"{job.name} -> {job.schedule}")
    elif args.command == "start":
        engine.start()

if __name__ == "__main__":
    main()
