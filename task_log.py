import time


task_start: int


def start_task(task_name: str):
    global task_start
    print(task_name, end=" ", flush=True)
    task_start = time.perf_counter_ns()


def end_task():
    task_end = time.perf_counter_ns()
    print(f"✓ in {task_end - task_start:,d} nanoseconds")
