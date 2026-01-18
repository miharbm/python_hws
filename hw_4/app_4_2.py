import math
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from typing import Callable



def parallel_func(executor: ThreadPoolExecutor | ProcessPoolExecutor, n_jobs: int, n_iter: int, f: Callable, a, b):
    step = (b - a) / n_jobs
    it_per_job = n_iter // n_jobs
    with executor(max_workers=n_jobs) as exec:
        futures = []
        for i in range(n_jobs):
            sub_a = a + i * step
            sub_b = sub_a + step
            if i == n_jobs - 1:
                iterations_local = n_iter - (it_per_job * (n_jobs - 1))
            else:
                iterations_local = it_per_job
            futures.append(
                exec.submit(integrate, f=f, a=sub_a, b=sub_b, n_iter=iterations_local)
            )
        return sum(f.result() for f in futures)


def integrate(f, a, b, *, n_iter):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def write_to_file(time_threads: float, time_processes: float, jobs: int, n_iter: int):
    with open(f"./artifacts/app_4_2_jobs_{jobs}.txt", "w", encoding="UTF-8") as f:
        f.write(f"Время, затраченное на функцию в {jobs} потоках (для {n_iter} итераций): {time_threads} \n")
        f.write(f"Время, затраченное на функцию в {jobs} процессах (для {n_iter} итераций): {time_processes}")



if __name__ == "__main__":
    n_jobs = 5
    n_iter = 500000000
    time_start = time.perf_counter()
    parallel_func(ThreadPoolExecutor, n_jobs=n_jobs, n_iter=n_iter, f=math.cos, a=0, b=math.pi / 2)
    time_end_threads = time.perf_counter() - time_start

    time_start = time.perf_counter()
    time_processes = parallel_func(ProcessPoolExecutor, n_jobs=n_jobs, n_iter=n_iter, f=math.cos, a=0, b=math.pi / 2)
    time_end_processes = time.perf_counter() - time_start

    write_to_file(time_end_threads, time_end_processes, n_jobs, n_iter)