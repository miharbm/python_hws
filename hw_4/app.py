from time import perf_counter
import threading
import multiprocessing


def fib(n: int) -> int:
    first = 0
    second = 1
    for _ in range(1, n):
        first, second = second, first + second
    
    return second



def single_flow():
    time_start = perf_counter()
    for _ in range(10):
        fib(500000)

    time_end = perf_counter() - time_start
    return time_end


def threading_flow():
    threads = []
    time_start = perf_counter()

    for _ in range(10):
        t = threading.Thread(target=fib, args=(500000,))
        threads.append(t)
    
    for thread in threads:
        thread.start()

    for thread in threads:   
        thread.join()

    time_end = perf_counter() - time_start
    return time_end


def multiprocessing_flow():
    time_start = perf_counter()
    processes = []
    for _ in range(10):
        p = multiprocessing.Process(target=fib, args=(500000,))
        processes.append(p)

    for process in processes:
        process.start()

    for process in processes:   
        process.join()

    time_end = perf_counter() - time_start
    return time_end


if __name__ == "__main__":
    time_single = single_flow()
    time_threads = threading_flow()
    time_processes = multiprocessing_flow()

    with open("./artifacts/app.txt", "w", encoding="UTF-8") as f:
        f.write(f"Время, затраченное на выполнение в синхронных вызовах: {time_single}\n")
        f.write(f"Время, затраченное на выполнение в 10 потоках: {time_threads}\n")
        f.write(f"Время, затраченное на выполнение в 10 процессах: {time_processes}\n")
