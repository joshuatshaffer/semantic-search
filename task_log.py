import time


task_start: int | None = None


def start_task(task_name: str):
    global task_start
    if task_start is not None:
        print("Oi! You forgot to end the previous task!")
        return
    print(task_name, end=" ", flush=True)
    task_start = time.perf_counter_ns()


def end_task():
    global task_start
    task_end = time.perf_counter_ns()
    if task_start is None:
        print("Oi! You forgot to start the task!")
        return
    print(f"✓ in {task_end - task_start:,d} nanoseconds")
    task_start = None
