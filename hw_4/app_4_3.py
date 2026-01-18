import codecs
import time
from multiprocessing import Queue, Process
from datetime import datetime
import os


def log(fp, msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pid = os.getpid()
    line = f"[{ts}][PID={pid}] {msg}"
    fp.write(line + "\n")
    fp.flush()
    print(line, flush=True)


def rot13(s: str) -> str:
    return codecs.encode(s, "rot_13")


def process_a(input_q: Queue, output_q: Queue, log_path: str):
    with open(log_path, "a", encoding="utf-8") as fp:
        log(fp, "Процесс A запущен")
        while True:
            msg = input_q.get()

            msg = msg.lower()
            time.sleep(5)
            log(fp, f"Процесс A отправил в B: {msg}")
            output_q.put(msg)


def process_b(input_q: Queue, output_q: Queue, log_path: str):
    with open(log_path, "a", encoding="utf-8") as fp:
        log(fp, "Процесс B запущен")
        while True:
            msg = input_q.get()

            encoded = rot13(msg)
            log(fp, f"Процесс B stdout: {encoded}")
            output_q.put(encoded)



def main():
    log_path = "./artifacts/app_4_3.txt"

    q_main_to_a = Queue()
    q_a_to_b = Queue()
    q_b_to_main = Queue()

    with open(log_path, "w", encoding="utf-8") as fp:
        log(fp, "Главный Процесс запущен")

    proc_a = Process(
        target=process_a,
        args=(q_main_to_a, q_a_to_b, log_path)
    )
    proc_b = Process(
        target=process_b,
        args=(q_a_to_b, q_b_to_main, log_path)
    )

    proc_a.start()
    proc_b.start()

    with open(log_path, "a", encoding="utf-8") as fp:
        while True:
            text = input()
            if text == "exit":
                log(fp, "Main получил сигнал для остановки")
                q_main_to_a.put(None)
                break

            log(fp, f"User input: {text}")
            q_main_to_a.put(text)

    proc_a.join()
    proc_b.join()


if __name__ == "__main__":
    main()