import time
from contextlib import contextmanager


@contextmanager
def task(task_name: str):
    print(task_name, end=" ", flush=True)
    task_start = time.perf_counter_ns()
    try:
        yield
    finally:
        task_end = time.perf_counter_ns()
        print(f"✓ in {task_end - task_start:,d} nanoseconds")
