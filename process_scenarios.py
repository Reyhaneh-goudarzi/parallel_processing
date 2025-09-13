# process_scenarios.py

# noinspection PyUnresolvedReferences
from multiprocessing import Process, current_process, Queue as mpQueue, Lock, Event, Barrier, Pool , Manager
import os
import time
from datetime import datetime
import random
import logging
import multiprocessing
from functools import partial

# -------------------------------------------------------
#  QueueHandler برای ارسال log به WebSocket queue
# -------------------------------------------------------
class QueueHandler(logging.Handler):
    def __init__(self, queue: mpQueue):
        super().__init__()
        self.queue = queue

    def emit(self, record):
        msg = self.format(record)
        if self.queue is not None:
            self.queue.put(msg)  # ارسال پیام به log_queue
        else:
            print(msg)  # فال‌بک به stdout

# -------------------------------------------------------
#  تابع کانفیگ logger برای Processها
# -------------------------------------------------------
def configure_logger(queue: mpQueue = None) -> logging.Logger :
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)

    # جلوگیری از اضافه شدن هندلر تکراری
    if not logger.handlers:
        if queue is not None:
            handler = QueueHandler(queue)
            formatter = logging.Formatter('[%(processName)s | PID %(process)d] %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        else:
            handler = logging.StreamHandler()  # فال‌بک به stdout
            formatter = logging.Formatter('[%(processName)s | PID %(process)d] %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.info("Logger configured for process")  # برای دیباگ

    return logger


# -------------------------------------------------------
# SECTION 1 - HELPERS
# -------------------------------------------------------

def task_s1_1(log_queue):
    logger = configure_logger(log_queue)
    logger.info(f"Child process started: PID {os.getpid()}")


def task_s1_2(n,log_queue):
    logger = configure_logger(log_queue)
    logger.info(f" calling myFunc from process n°: {n}")
    for i in range(n):
        logger.info(f" output from myFunc is : {i}")
    time.sleep(0.5)


def task_s1_3(number,log_queue):
    logger = configure_logger(log_queue)
    result = number * number
    logger.info(f"Square of {number} is {result}")


# -------------------------------------------------------
# SECTION 2 - HELPERS
# -------------------------------------------------------
def task_s2_1(log_queue):
    logger = configure_logger(log_queue)
    logger.info(f"Starting process name = {current_process().name}")


def task_s2_2(log_queue):
    logger = configure_logger(log_queue)
    logger.info(f"Starting process name = {current_process().name}")
    time.sleep(0.5)
    logger.info(f"Exiting process name = {current_process().name}")


def task_s2_3(log_queue):
    logger = configure_logger(log_queue)
    logger.info(f"[{current_process().name}] running...")


# -------------------------------------------------------
# SECTION 3 - HELPERS
# -------------------------------------------------------
def task_s3_1(log_queue):
    logger = configure_logger(log_queue)
    logger.info(f"Starting background_process | [Daemon Still alive]")
    for i in range(5, 10):
        logger.info(f" ---> {i + 1} ")
        time.sleep(1)
    logger.info("Exiting background_process")


def task_s3_2(log_queue):
    logger = configure_logger(log_queue)
    logger.info(f"Starting background_process [Daemon Still running]")
    for i in range(5, 10):
        logger.info(f" ---> {i}")
        time.sleep(1)
    logger.info("Exiting background_process")



def task_s3_3(name,use_join,log_queue):
    logger = configure_logger(log_queue)
    if name == "NoJoin":
        logger.info("Starting background_process")
        for i in range(5, 10):
            logger.info(f" ---> {i}")
            time.sleep(0.5)
        logger.info(f"Exiting background_process {name} ")
    else:
        logger.info("Starting NO_background_process")
        for i in range(5):
            logger.info(f" ---> {i}")
            time.sleep(1)
        logger.info(f"Exiting NO_background_process {name} ")


# -------------------------------------------------------
# SECTION 4 - HELPERS
# -------------------------------------------------------
def task_s4_1(log_queue):
    logger = configure_logger(log_queue)
    for _ in range(5):
        logger.info(f"[Child] Still working... PID: {os.getpid()}")
        time.sleep(1)


def task_s4_2(log_queue):
    logger = configure_logger(log_queue)
    for i in range(10):
        if i == 4:
            logger.info("[Child] stopping early")
            break
        logger.info(f"[Child] Working {i + 1}/10")
        time.sleep(1)


def task_s4_3(n,log_queue):
    logger = configure_logger(log_queue)
    logger.info(f"[Process-{n}] Started. PID: {os.getpid()}")
    time.sleep(10)


# -------------------------------------------------------
# SECTION 5 - HELPERS
# -------------------------------------------------------
class MyProcess5_1(Process):
    def __init__(self, log_queue, name=None):
        super().__init__(name=name)
        self.log_queue = log_queue

    def run(self):
        logger = configure_logger(self.log_queue)
        logger.info(f"called run method by {self.name} | PID: {os.getpid()}")


class Worker5_2(Process):
    def __init__(self, id, log_queue):
        super().__init__()
        self.id = id
        self.log_queue = log_queue

    def run(self):
        logger = configure_logger(self.log_queue)
        logger.info(f"called run method by Worker-{self.id} | PID: {os.getpid()}")
        time.sleep(1)
        logger.info(f"Worker-{self.id} finished execution.")


class CounterProcess5_3(Process):
    def __init__(self, start, end, log_queue):
        super().__init__()
        self.start_num = start
        self.end_num = end
        self.log_queue = log_queue

    def run(self):
        logger = configure_logger(self.log_queue)
        logger.info(f"called run method by CounterProcess (counting from {self.start_num} to {self.end_num}) | (PID: {os.getpid()})")
        for i in range(self.start_num, self.end_num + 1):
            logger.info(f" step ---> {i}")
            time.sleep(0.2)
        logger.info("CounterProcess finished counting.")


# -------------------------------------------------------
# SECTION 6 - HELPERS
# -------------------------------------------------------
def queue_worker_s6_1(q,log_queue):
    logger = configure_logger(log_queue)
    msg = "Item A"
    logger.info(f"Process Producer : {msg} appended to queue")
    q.put(msg)


def queue_producer_s6_2(q,log_queue):
    logger = configure_logger(log_queue)
    for i in range(7):
        msg = random.randint(10, 250)
        q.put(msg)
        logger.info(f"Process Producer : item {msg} appended to queue")
        logger.info(f"The size of queue is {q.qsize()}")
        time.sleep(0.2)


def queue_consumer_s6_2(q, producer,log_queue):
    logger = configure_logger(log_queue)
    while not q.empty() or producer.is_alive():
        if not q.empty():
            data = q.get()
            logger.info(f"[Consumer] Got: {data}")
        time.sleep(0.1)


def queue_client_s6_3(input_q, output_q,log_queue):
    while True:
        logger = configure_logger(log_queue)
        msg = input_q.get()
        if msg == "exit":
            logger.info("Process Client : received exit signal, terminating.")
            break
        logger.info(f"Process Client : received -> '{msg}'")
        response = msg.upper()
        logger.info(f"Process Client : responded -> '{response}'")
        output_q.put(response)


def queue_consumer_s6_2_wrapper(q,log_queue):
    logger = configure_logger(log_queue)
    while True:
        if not q.empty():
            data = q.get()
            logger.info(f"Process Consumer : item {data} popped from queue")
            logger.info(f"The size of queue is {q.qsize()}")
        else:
            logger.info("the queue is empty")
            break
        time.sleep(0.1)


# -------------------------------------------------------
# SECTION 7 - HELPERS
# -------------------------------------------------------
def sync_lock_task_s7_1(lock, q ,log_queue):
    logger = configure_logger(log_queue)
    with lock:
        msg = (f"Process {os.getpid()} wrote to file (simulated)")
        q.put(msg)
        time.sleep(0.5)


def sync_event_task_s7_2(event, name, q,log_queue):
    logger = configure_logger(log_queue)
    q.put(f"[{name}] Waiting for event...")
    event.wait()
    q.put(f"[{name}] Event triggered! Continuing...")


def sync_barrier_task_s7_3(barrier, name, q,log_queue):
    logger = configure_logger(log_queue)
    q.put(f"[{name}] Reached barrier at {datetime.now()}")
    barrier.wait(timeout=5)
    q.put(f"[{name}] Passed barrier at {datetime.now()}")


# -------------------------------------------------------
# SECTION 8 - HELPERS
# -------------------------------------------------------
def square_pool_task_s8_1(x,log_queue=None):
    logger = configure_logger(log_queue)
    result = x * x
    logger.info(f"[{current_process().name}] Square of {x} is {result}")
    return result


def worker_pool_task_s8_2(x,log_queue=None):
    logger = configure_logger(log_queue)
    time.sleep(random.uniform(0.5, 1.5))
    logger.info(f"[{current_process().name}] Processed: {x}")
    return x * 10


def delayed_pool_task_s8_3(i,log_queue=None):
    logger = configure_logger(log_queue)
    logger.info(f"[{current_process().name}] Task {i} started (PID: {os.getpid()})")
    time.sleep(1)
    logger.info(f"[{current_process().name}] Task {i} finished")
    return i


# -------------------------------------------------------
# PROCESS SECTION 1: Spawning a Process - MAIN FUNCTION
# -------------------------------------------------------
def process_section_1_spawn_process(scenario_number=1, log_queue=None):
    logger = configure_logger(log_queue)
    logger.info("===== SECTION 1: Spawning a Process =====")

    def scenario_1():
        logger.info("\n--- Scenario 1: Spawn a single process ---")
        p = Process(target=task_s1_1, args=(log_queue,))
        p.start()
        p.join()
        logger.info(f"Main process ID: {os.getpid()}")

    def scenario_2():
        logger.info("\n--- Scenario 2: Spawn multiple processes ---")
        processes = []
        for i in range(5):
            p = Process(target=task_s1_2, args=(i + 1,log_queue))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        logger.info("All processes completed.")

    def scenario_3():
        logger.info("\n--- Scenario 3: Process with custom function ---")
        numbers = [2, 4, 6, 8]
        processes = []
        for n in numbers:
            p = Process(target=task_s1_3, args=(n,log_queue))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        logger.info("Done calculating squares.")

    # اجرای سناریوها
    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        logger.info("Invalid scenario number!")


# -------------------------------------------------------
# PROCESS SECTION 2: Naming a Process - MAIN FUNCTION
# -------------------------------------------------------
def process_section_2_name_process(scenario_number=1, log_queue=None):
    logger = configure_logger(log_queue)
    logger.info("===== SECTION 2: Naming a Process =====")

    def scenario_1():
        logger.info("\n--- Scenario 1: Custom process name ---")
        p = Process(target=task_s2_1, name="MyCustomProcess", args=(log_queue,))
        p.start()
        p.join()

    def scenario_2():
        logger.info("\n--- Scenario 2: Naming multiple processes ---")
        processes = []
        for i in range(3):
            name = f"Worker-{i + 1}"
            p = Process(target=task_s2_2, name=name, args=(log_queue,))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()

    def scenario_3():
        logger.info("\n--- Scenario 3: Accessing name from parent ---")
        p1 = Process(target=task_s2_3, name="NamedProcess-A", args=(log_queue,))
        p2 = Process(target=task_s2_3, name="NamedProcess-B", args=(log_queue,))
        logger.info(f"Created: {p1.name}")
        logger.info(f"Created: {p2.name}")
        p1.start()
        p2.start()
        p1.join()
        p2.join()

    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        logger.info("Invalid scenario number!")


# -----------------------------
# PROCESS SECTION 3: Running processes in the background- MAIN FUNCTION
# -----------------------------
def process_section_3_background_process(scenario_number=1, log_queue=None):
    logger = configure_logger(log_queue)
    logger.info("===== SECTION 3: Background Processes =====")

    def scenario_1():
        logger.info("\n--- Scenario 1: Run process in background (no join) ---")
        p = Process(target=task_s3_1, args=(log_queue,))
        p.start()

        logger.info("Starting NO_background_process ")
        for i in range(5):
            logger.info(f" step ---> {i}")
            time.sleep(1)
        logger.info("Exiting NO_background_process [daemon killed]")
        # p.join()  # حذف شده برای no-join

    def scenario_2():
        logger.info("\n--- Scenario 2: Daemon process dies with main ---")
        p = Process(target=task_s3_2, args=(log_queue,))
        p.daemon = True
        p.start()
        logger.info("Starting NO_background_process...")
        for i in range(5):
            logger.info(f" ---> {i}")
            time.sleep(0.5)
        logger.info("Exiting NO_background_process [daemon killed]")

    def scenario_3():
        logger.info("\n--- Scenario 3: Compare join vs no-join ---")
        p1 = Process(target=task_s3_3, args=("NoJoin", False, log_queue))
        p2 = Process(target=task_s3_3, args=("WithJoin", True, log_queue))
        p1.start()
        p2.start()
        p2.join()
        logger.info("[Main] End of main process (NoJoin may still be running...)")

    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        logger.info("Invalid scenario number!")


# -----------------------------
# PROCESS SECTION 4: Killing a Process - MAIN FUNCTION
# -----------------------------
def process_section_4_kill_process(scenario_number=1, log_queue=None):
    logger = configure_logger(log_queue)
    logger.info("===== SECTION 4: Killing a Process =====")

    def scenario_1():
        logger.info("\n--- Scenario 1: Terminate an infinite process ---")
        p = Process(target=task_s4_1, args=(log_queue,))
        p.start()
        time.sleep(3)
        logger.info("[Main] Terminating child...")
        p.terminate()
        p.join()
        logger.info(f"[Main] Process terminated. Alive? {p.is_alive()} | Exit code: {p.exitcode}")

    def scenario_2():
        logger.info("\n--- Scenario 2: Conditionally terminate a process ---")
        p = Process(target=task_s4_2, args=(log_queue,))
        p.start()
        time.sleep(4)
        if p.is_alive():
            logger.info("[Main] Task taking too long... killing it.")
            p.terminate()
        p.join()
        logger.info(f"[Main] Process done. Exit code: {p.exitcode}")

    def scenario_3():
        logger.info("\n--- Scenario 3: Start, monitor, then kill multiple processes ---")
        processes = []
        for i in range(3):
            p = Process(target=task_s4_3, args=(i + 1, log_queue))
            p.start()
            processes.append(p)
        time.sleep(3)
        logger.info("[Main] Terminating all processes...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()
        for i, p in enumerate(processes, 1):
            logger.info(f"[Main] Process-{i} alive? {p.is_alive()} | Exit: {p.exitcode}")

    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        logger.info("Invalid scenario number!")


# -----------------------------
# PROCESS SECTION 5: Subclassing Process - MAIN FUNCTION
# -----------------------------
def process_section_5_subclass_process(scenario_number=1, log_queue=None):
    logger = configure_logger(log_queue)
    logger.info("===== SECTION 5: Subclassing Process =====")

    def scenario_1():
        logger.info("\n--- Scenario 1: Basic subclassed process ---")
        p = MyProcess5_1(log_queue=log_queue,name="CustomProcess")
        p.start()
        p.join()

    def scenario_2():
        logger.info("\n--- Scenario 2: Subclassed process with custom init ---")
        processes = []
        for i in range(10):
            p = Worker5_2(id=i + 1, log_queue=log_queue)
            processes.append(p)
            p.start()
        for p in processes:
            p.join()

    def scenario_3():
        logger.info("\n--- Scenario 3: Subclass with multiple attributes and logic ---")
        p = CounterProcess5_3(1, 10 ,log_queue=log_queue)
        p.start()
        p.join()

    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        logger.info("Invalid scenario number!")


# -----------------------------
# PROCESS SECTION 6: Queue for Data Exchange - MAIN FUNCTION
# -----------------------------
def process_section_6_queue_exchange(scenario_number=1, log_queue=None):
    logger = configure_logger(log_queue)
    logger.info("===== SECTION 6: Queue for Data Exchange =====")

    def scenario_1():
        logger.info("\n--- Scenario 1: Simple one-way queue communication ---")
        q = mpQueue()
        p = Process(target=queue_worker_s6_1, args=(q,log_queue))
        p.start()
        p.join()
        msg = q.get()
        logger.info(f"Process Consumer : {msg} popped from queue")
        logger.info("the queue is empty")

    def scenario_2():
        logger.info("\n--- Scenario 2: Multiple values through queue ---")
        q = mpQueue()
        p = Process(target=queue_producer_s6_2, args=(q, log_queue))
        c = Process(target=queue_consumer_s6_2_wrapper, args=(q, log_queue))
        p.start()
        c.start()
        p.join()
        c.join()

    def scenario_3():
        logger.info("\n--- Scenario 3: Two-way communication using two queues ---")
        to_client = mpQueue()
        from_client = mpQueue()
        p = Process(target=queue_client_s6_3, args=(to_client, from_client, log_queue))
        p.start()
        to_client.put("hello")
        to_client.put("how are you?")
        to_client.put("exit")
        timeout = 5
        start_time = time.time()

        while time.time() - start_time < timeout:
            if not from_client.empty():
                res = from_client.get()
                logger.info(f"Process Main : got back -> '{res}' from client")
            if not p.is_alive():
                break
            time.sleep(0.1)
        p.join(timeout=2)

    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        logger.info("Invalid scenario number!")


# -----------------------------
# PROCESS SECTION 7: Synchronizing Processes - MAIN FUNCTION
# -----------------------------
def process_section_7_sync_processes(scenario_number=1, log_queue=None):
    logger = configure_logger(log_queue)
    logger.info("===== SECTION 7: Synchronizing Processes =====")

    def scenario_1():
        logger.info("\n--- Scenario 1: Using Lock for process synchronization---")

        lock = Lock()
        q = mpQueue()

        processes = [Process(target=sync_lock_task_s7_1, args=(lock, q, log_queue)) for _ in range(10)]
        for p in processes: p.start()
        for p in processes: p.join()
        while not q.empty():
            logger.info(q.get())

    def scenario_2():
        logger.info("\n--- Scenario 2: Using Event for synchronization ---")

        event = Event()
        q = mpQueue()

        p1 = Process(target=sync_event_task_s7_2, args=(event, "Worker-1", q, log_queue))
        p2 = Process(target=sync_event_task_s7_2, args=(event, "Worker-2", q, log_queue))

        p1.start()
        p2.start()

        time.sleep(2)
        q.put("[Main] Setting event!")
        event.set()

        p1.join()
        p2.join()

        while not q.empty():
            logger.info(q.get())

    def scenario_3():
        logger.info("\n--- Scenario 3: Using Barrier for process synchronization ---")
        num_processes = 5
        barrier = Barrier(num_processes)
        q = mpQueue()

        processes = [
            Process(target=sync_barrier_task_s7_3, args=(barrier, f"Proc-{i + 1}", q, log_queue)) for i in range(num_processes)
        ]

        for p in processes: p.start()
        for p in processes: p.join()
        q.put("All processes synchronized and finished.")

        while not q.empty():
            logger.info(q.get())

    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        logger.info("Invalid scenario number!")


# -----------------------------
# PROCESS SECTION 8: Process Pool - MAIN FUNCTION
# -----------------------------
def process_section_8_process_pool(scenario_number=1, log_queue=None):
    logger = configure_logger(log_queue)
    logger.info("===== SECTION 8: Process Pool =====")

    def scenario_1():
        logger.info("\n--- Scenario 1: Using Pool.map() ---")
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        with Pool(processes=4) as pool:
            task = partial(square_pool_task_s8_1, log_queue=log_queue)
            results = pool.map(task, numbers)
            logger.info(f"[Main] Results: {results}")

    def scenario_2():
        logger.info("\n--- Scenario 2: Using Pool.apply_async() ---")
        numbers = list(range(20))
        with Pool(processes=3) as pool:
            task = partial(worker_pool_task_s8_2, log_queue=log_queue)
            async_results = [pool.apply_async(task, args=(i,)) for i in numbers]
            logger.info("[Main] Waiting for results...")
            results = [res.get() for res in async_results]
        logger.info(f"[Main] Results: {results}")

    def scenario_3():
        logger.info("\n--- Scenario 3: Pool with delayed tasks ---")
        with Pool(processes=2) as pool:
            task = partial(delayed_pool_task_s8_3, log_queue=log_queue)
            results = pool.map(task, range(20))
        logger.info(f"[Main] All tasks complete. Returned: {results}")

    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        logger.info("Invalid scenario number!")

